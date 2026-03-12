#!/usr/bin/env python3
"""Specumentation MCP Server — exposes concept documents to Claude Desktop."""

import json
import os
import re
from pathlib import Path

from mcp.server.fastmcp import FastMCP

REGISTRY_DIR = Path.home() / ".claude" / "specumentation-mcp"
REGISTRY_FILE = REGISTRY_DIR / "projects.json"

mcp = FastMCP(
    "specumentation",
    instructions=(
        "Specumentation MCP server. Provides access to concept documents "
        "for the active project. Use get_overview() first to see the project context."
    ),
)

# --- Project Registry ---


def load_registry() -> list[dict]:
    """Load the project registry from disk."""
    if not REGISTRY_FILE.exists():
        return []
    with open(REGISTRY_FILE) as f:
        return json.load(f)


def save_registry(projects: list[dict]) -> None:
    """Save the project registry to disk."""
    REGISTRY_DIR.mkdir(parents=True, exist_ok=True)
    with open(REGISTRY_FILE, "w") as f:
        json.dump(projects, f, indent=2)


# --- Active Project Detection ---

_active_project: Path | None = None


def _detect_project_from_cwd() -> Path | None:
    """Walk up from cwd to find a directory containing docs/concept/."""
    current = Path.cwd()
    for directory in [current, *current.parents]:
        if (directory / "docs" / "concept").is_dir():
            return directory
        if directory == directory.parent:
            break
    return None


def _detect_project_from_registry() -> Path | None:
    """Check if cwd is inside any registered project."""
    cwd = str(Path.cwd())
    for project in load_registry():
        if cwd.startswith(project["path"]):
            return Path(project["path"])
    return None


def get_active_project() -> Path | None:
    """Return the active project path, or None."""
    return _active_project


def set_active_project(path: Path | None) -> None:
    """Set the active project path."""
    global _active_project
    _active_project = path


def require_active_project() -> Path:
    """Return active project or raise an error with a helpful message."""
    project = get_active_project()
    if project is None:
        raise ValueError(
            "No active project. Either:\n"
            "  1. Run 'specumentation-mcp init' in your project directory to register it\n"
            "  2. Use the set_project tool to switch to a registered project\n"
            "  3. Start the server from within a project that has a docs/concept/ directory"
        )
    return project


# --- MCP Tools ---


@mcp.tool()
def list_projects() -> str:
    """List all registered specumentation projects."""
    projects = load_registry()
    if not projects:
        return "No projects registered. Run 'specumentation-mcp init' in a project directory."
    lines = []
    for p in projects:
        active = " (active)" if _active_project and str(_active_project) == p["path"] else ""
        lines.append(f"- {p['name']}: {p['path']}{active}")
    return "\n".join(lines)


@mcp.tool()
def set_project(path: str) -> str:
    """Switch the active project to a different registered project.

    Args:
        path: Absolute path to the project directory
    """
    target = Path(path).expanduser().resolve()
    if not (target / "docs" / "concept").is_dir():
        return f"Error: {target} is not a specumentation project (no docs/concept/ directory)"
    set_active_project(target)
    overview = target / "docs" / "concept" / "00-overview.md"
    if overview.exists():
        return f"Switched to project at {target}\n\n{overview.read_text()}"
    return f"Switched to project at {target} (no 00-overview.md found)"


@mcp.tool()
def get_overview() -> str:
    """Get the project overview (00-overview.md) for the active project.

    This is the best starting point — it contains the project description,
    concept index, architecture decisions, and glossary.
    """
    project = require_active_project()
    overview = project / "docs" / "concept" / "00-overview.md"
    if not overview.exists():
        return "No 00-overview.md found. Run '/specumentation init' to create it."
    return overview.read_text()


@mcp.tool()
def list_concepts() -> str:
    """List all concept documents with their status from the Concept Index.

    Parses the Concept Index table in 00-overview.md and returns structured info.
    """
    project = require_active_project()
    overview = project / "docs" / "concept" / "00-overview.md"
    if not overview.exists():
        return "No 00-overview.md found."

    content = overview.read_text()
    # Parse the Concept Index table
    lines = content.split("\n")
    in_table = False
    concepts = []
    for line in lines:
        if "| # |" in line and "Concept" in line:
            in_table = True
            continue
        if in_table and line.startswith("|---"):
            continue
        if in_table and line.startswith("|"):
            cols = [c.strip() for c in line.split("|")[1:-1]]
            if len(cols) >= 4 and cols[0] != "—":
                concepts.append(
                    {"number": cols[0], "name": cols[1], "status": cols[2], "updated": cols[3]}
                )
        elif in_table and not line.startswith("|"):
            break

    if not concepts:
        return "No concepts found in the index."

    lines_out = []
    for c in concepts:
        lines_out.append(f"- [{c['number']}] {c['name']} — {c['status']} (updated: {c['updated']})")
    return "\n".join(lines_out)


@mcp.tool()
def get_concept(topic: str) -> str:
    """Read a specific concept document by topic slug or number.

    Args:
        topic: Concept number (e.g. "01") or topic slug (e.g. "mcp-server")
    """
    project = require_active_project()
    concept_dir = project / "docs" / "concept"

    # Try exact match by number prefix or slug
    for f in sorted(concept_dir.glob("*.md")):
        if f.name == "00-overview.md":
            continue
        name = f.stem  # e.g. "01-mcp-server"
        if name.startswith(topic) or topic in name:
            return f.read_text()

    return f"Concept '{topic}' not found. Use list_concepts() to see available concepts."


@mcp.tool()
def update_concept(topic: str, content: str) -> str:
    """Update a concept document's content.

    Args:
        topic: Concept number (e.g. "01") or topic slug (e.g. "mcp-server")
        content: The full new content for the concept file
    """
    project = require_active_project()
    concept_dir = project / "docs" / "concept"

    target_file = None
    for f in sorted(concept_dir.glob("*.md")):
        if f.name == "00-overview.md":
            continue
        name = f.stem
        if name.startswith(topic) or topic in name:
            target_file = f
            break

    if target_file is None:
        return f"Concept '{topic}' not found. Use list_concepts() to see available concepts."

    # Read existing Change Log to preserve it
    existing = target_file.read_text()
    changelog_match = re.search(r"## Change Log\s*\n(.*)", existing, re.DOTALL)
    new_changelog_match = re.search(r"## Change Log\s*\n(.*)", content, re.DOTALL)

    # If the new content has a Change Log, use it as-is; otherwise append the old one
    if not new_changelog_match and changelog_match:
        content = content.rstrip() + "\n\n## Change Log\n" + changelog_match.group(1)

    target_file.write_text(content)
    return f"Updated {target_file.name}"


# --- Startup ---


def _initialize():
    """Detect active project on startup."""
    project = _detect_project_from_cwd()
    if project is None:
        project = _detect_project_from_registry()
    if project is not None:
        set_active_project(project)


_initialize()

if __name__ == "__main__":
    mcp.run()
