# MCP Server

> Concept document — Status: **draft**

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

The server detects the active project via the working directory of Claude Desktop (analogous to Claude Code). A manual `set_project(path)` tool allows switching if needed.

## Technical Description

### Architecture

A single global MCP server instance running locally, serving all registered specumentation projects.

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
      "command": "python",
      "args": ["~/.claude/specumentation-mcp/server.py"]
    }
  }
}
```

### Interface

| Tool | Description |
|------|-------------|
| `list_concepts()` | Returns the concept index from `docs/concept/00-overview.md` |
| `get_concept(topic)` | Reads the matching concept file, e.g. `01-authentication.md` |
| `update_concept(topic, content)` | Writes changes back to the concept file |
| `get_overview()` | Loads `00-overview.md` as initial context |
| `set_project(path)` | Manually switch the active project |
| `list_projects()` | Shows all registered projects |

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

- On server start: Detect active project from working directory, auto-load `00-overview.md`.
- On `set_project(path)`: Validate path contains `docs/concept/`, switch context.
- On `update_concept()`: Write changes, preserve Change Log format.
- If no active project detected: Return helpful error suggesting `specumentation-mcp init`.

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
  - `install.sh` — Extended to copy `server.py` and create CLI symlink
  - `/specumentation init` — Extended to call `specumentation-mcp init` for project registration

## Repository Structure Changes

```
specumentation/
├── SKILL.md
├── CLAUDE.md
├── install.sh              ← Extended
├── documents/
└── mcp-server/             ← New
    ├── server.py           ← MCP server (~100 lines Python)
    ├── specumentation-mcp  ← CLI for init/list
    └── README.md           ← Setup instructions
```

## Implementation Estimate

- `server.py`: ~100 lines Python (MCP SDK + file access)
- `specumentation-mcp` CLI: ~30 lines Bash
- `install.sh` extension: ~10 lines
- `/specumentation init` extension: 1 additional call

## Open Questions

- [ ] Should the server support watching for file changes and notifying Claude Desktop of updates?
- [ ] Should `install.sh` automatically update `claude_desktop_config.json` or always require manual setup?
- [ ] How to handle multiple Claude Desktop windows pointing to different projects simultaneously?
- [ ] Should epic files also be exposed via MCP tools, or only concepts?

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-03-12 | Initial concept — Source: docs/in/specumentation-mcp-concept.md | specumentation |
