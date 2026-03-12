# MCP Server

> Concept document — Status: **implemented**

## Purpose

Enable Claude Desktop to automatically access specumentation concept documents without manual upload or copy-paste. A dedicated MCP (Model Context Protocol) server understands the specumentation directory structure and provides context-aware tools for reading and updating concepts.

## Functional Description

### Problem Statement

When using Claude Desktop (e.g. with Opus), users currently have to manually upload or paste concept documents. This breaks the seamless workflow that Claude Code enjoys via `CLAUDE.md` and skill invocation.

### Core Workflow

1. **One-time setup**: Install the MCP server via `install.sh`, add the server entry to `claude_desktop_config.json`.
2. **Per-project registration**: Running `/specumentation init` (or `specumentation-mcp init`) registers the current project directory in a global project list.
3. **Automatic context**: When Claude Desktop connects, the server automatically loads `docs/concept/00-overview.md` from the active project — no user action required.
4. **Concept access**: Claude Desktop can list, read, and update concept documents through MCP tools.

### Project Detection

The server detects the active project by walking up from the working directory to find a `docs/concept/` directory. As a fallback, it checks if the working directory is inside any registered project. A manual `set_project(path)` tool allows switching if needed.

## Technical Description

### Architecture

A single global MCP server instance running locally via FastMCP (stdio transport), serving all registered specumentation projects.

```
~/.claude/specumentation-mcp/
├── server.py          ← Single instance, serves all projects
└── projects.json      ← Registry of known project paths

claude_desktop_config.json  ← One-time entry, never touched again

Project A/docs/concept/     ← Read/written by MCP server
Project B/docs/concept/     ← Same server, different directory
```

#### Configuration (`claude_desktop_config.json`)

```json
{
  "mcpServers": {
    "specumentation": {
      "command": "python3",
      "args": ["~/.claude/specumentation-mcp/server.py"]
    }
  }
}
```

### Interface

| Tool | Description |
|------|-------------|
| `list_projects()` | Shows all registered projects, marks active one |
| `set_project(path)` | Validates target has `docs/concept/`, switches context, returns overview |
| `get_overview()` | Loads `00-overview.md` as initial context |
| `list_concepts()` | Parses the Concept Index table and returns structured data |
| `get_concept(topic)` | Reads matching concept file by number prefix or slug |
| `update_concept(topic, content)` | Writes content to concept file, preserves Change Log via regex |

No generic filesystem access — only specumentation-aware operations.

### Data Model

**Project registry** (`~/.claude/specumentation-mcp/projects.json`):
```json
[
  {"path": "/Users/user/project-a", "name": "Project A"},
  {"path": "/Users/user/project-b", "name": "Project B"}
]
```

### Behavior

- On server start: Walk up from cwd to find `docs/concept/`; fallback to registry lookup.
- On `set_project(path)`: Validate path contains `docs/concept/`, switch context, return overview.
- On `update_concept()`: Write full content; if new content lacks Change Log but original has one, append the original's Change Log.
- If no active project detected: Raise ValueError with 3 suggested remedies.
- `list_projects()` marks the active project with "(active)".

### Comparison to Generic Filesystem MCP

| Capability | GitLab/GitHub MCP | Specumentation MCP |
|---|---|---|
| File access | Yes | Yes |
| Understands concept structure | No | Yes |
| Auto-loads context | No | Yes |
| Understands 00-overview as index | No | Yes |
| Focused tool set | No (generic) | Yes (specific) |

## Dependencies

- **External**: Python 3, `mcp` package (Anthropic MCP Python SDK — `pip install mcp`)
- **Internal**: Specumentation directory structure (`docs/concept/`)
- **Integration points**:
  - `install.sh` — Copies `server.py`, symlinks CLI, prints config snippet
  - `SKILL.md` init phase — Calls `specumentation-mcp init` (non-blocking)

## Repository Structure

```
specumentation/
├── SKILL.md
├── CLAUDE.md
├── install.sh              ← Deploys skill + MCP server
├── documents/
└── mcp-server/
    ├── server.py           ← MCP server (~250 lines Python, FastMCP)
    └── specumentation-mcp  ← CLI for init/list (~100 lines Bash)
```

## Open Questions

- [ ] Should the server support watching for file changes and notifying Claude Desktop of updates?
- [ ] Should `install.sh` automatically update `claude_desktop_config.json` or always require manual setup?
- [ ] How to handle multiple Claude Desktop windows pointing to different projects simultaneously?
- [ ] Should epic files also be exposed via MCP tools, or only concepts?

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-03-12 | Initial concept — Source: docs/in/specumentation-mcp-concept.md | specumentation |
| 2026-03-12 | Update: status → implemented, sync with actual code (python3, FastMCP, file sizes, CLI fallback, project detection behavior) | specumentation |
