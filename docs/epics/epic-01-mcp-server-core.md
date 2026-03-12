# Epic 01: MCP Server Core Implementation

> Derived from: [01-mcp-server.md](../concept/01-mcp-server.md)
> Status: **closed**

## Description

Implement the core MCP server that exposes specumentation concept documents to Claude Desktop. This includes the Python server with all MCP tools, the project registry, and automatic context loading.

## Tickets

### [E-01.01] Create MCP server with project registry
- **Status:** ✓ RESOLVED — Server created with FastMCP, project registry via projects.json, cwd-based detection, and helpful error messages.
- **Concept ref:** [01-mcp-server.md, Architecture & Data Model](../concept/01-mcp-server.md#architecture)
- **Description:** Create `mcp-server/server.py` using the Anthropic MCP Python SDK. The server must maintain a project registry (`projects.json`) and detect the active project from the working directory. On startup, it should auto-load `docs/concept/00-overview.md` from the active project.
- **Acceptance Criteria:**
  - [x] `mcp-server/server.py` exists and is a valid MCP server using the `mcp` Python SDK
  - [x] Server reads `~/.claude/specumentation-mcp/projects.json` for registered projects
  - [x] Server detects active project from working directory on startup
  - [x] If no active project is detected, server returns a helpful error message
- **Files:** `mcp-server/server.py`

### [E-01.02] Implement `list_projects` and `set_project` tools
- **Status:** ✓ RESOLVED — Both tools implemented in server.py with validation and active project indicator.
- **Concept ref:** [01-mcp-server.md, Interface](../concept/01-mcp-server.md#interface)
- **Description:** Implement the `list_projects()` tool that returns all registered projects from the registry, and the `set_project(path)` tool that validates the path contains `docs/concept/` and switches the active project context.
- **Acceptance Criteria:**
  - [x] `list_projects()` returns all entries from `projects.json` with path and name
  - [x] `set_project(path)` validates the target path has a `docs/concept/` directory
  - [x] `set_project(path)` switches the server's active project context
  - [x] `set_project()` returns an error if path is invalid or not a specumentation project
- **Files:** `mcp-server/server.py`

### [E-01.03] Implement `get_overview` and `list_concepts` tools
- **Status:** ✓ RESOLVED — get_overview reads 00-overview.md; list_concepts parses the Concept Index table.
- **Concept ref:** [01-mcp-server.md, Interface](../concept/01-mcp-server.md#interface)
- **Description:** Implement `get_overview()` to load `00-overview.md` as initial context, and `list_concepts()` to parse and return the Concept Index table from the overview file.
- **Acceptance Criteria:**
  - [x] `get_overview()` returns the full content of `docs/concept/00-overview.md`
  - [x] `list_concepts()` parses the Concept Index table and returns structured data (number, name, status, last updated)
  - [x] Both tools return an error if no active project is set
- **Files:** `mcp-server/server.py`

### [E-01.04] Implement `get_concept` and `update_concept` tools
- **Status:** ✓ RESOLVED — get_concept matches by number or slug; update_concept preserves Change Log via regex.
- **Concept ref:** [01-mcp-server.md, Interface](../concept/01-mcp-server.md#interface)
- **Description:** Implement `get_concept(topic)` to read a specific concept file by topic slug or number, and `update_concept(topic, content)` to write changes back while preserving the Change Log format.
- **Acceptance Criteria:**
  - [x] `get_concept(topic)` finds and returns the matching concept file (by slug or number prefix)
  - [x] `get_concept()` returns an error if the concept is not found
  - [x] `update_concept(topic, content)` writes the full content to the concept file
  - [x] `update_concept()` preserves Change Log entries from the original file
  - [x] Both tools return an error if no active project is set
- **Files:** `mcp-server/server.py`
