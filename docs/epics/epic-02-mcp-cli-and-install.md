# Epic 02: CLI Tool and Installation Integration

> Derived from: [01-mcp-server.md](../concept/01-mcp-server.md)
> Status: **in progress**

## Description

Create the `specumentation-mcp` CLI tool for project registration and extend `install.sh` to deploy the MCP server alongside the skill. Also update the specumentation `init` phase to auto-register projects.

## Tickets

### [E-02.01] Create `specumentation-mcp` CLI tool
- **Status:** ✓ RESOLVED — Bash script with init (duplicate-safe registration) and list subcommands, usage help on no args.
- **Concept ref:** [01-mcp-server.md, Repository Structure Changes](../concept/01-mcp-server.md#repository-structure-changes)
- **Description:** Create `mcp-server/specumentation-mcp` as a Bash script that supports `init` (register current directory in `projects.json`) and `list` (show registered projects) subcommands.
- **Acceptance Criteria:**
  - [x] `mcp-server/specumentation-mcp` is an executable Bash script
  - [x] `specumentation-mcp init` adds the current directory to `~/.claude/specumentation-mcp/projects.json`
  - [x] `specumentation-mcp init` does not add duplicates if the project is already registered
  - [x] `specumentation-mcp init` creates `projects.json` if it does not exist
  - [x] `specumentation-mcp list` prints all registered projects
  - [x] Running without arguments prints usage help
- **Files:** `mcp-server/specumentation-mcp`

### [E-02.02] Extend `install.sh` for MCP server deployment
- **Status:** open
- **Concept ref:** [01-mcp-server.md, Integration in den Skill](../concept/01-mcp-server.md#repository-structure-changes)
- **Description:** Extend `install.sh` to copy `server.py` to `~/.claude/specumentation-mcp/`, symlink the CLI tool to `/usr/local/bin/specumentation-mcp`, and print the `claude_desktop_config.json` snippet the user needs to add manually.
- **Acceptance Criteria:**
  - [ ] `install.sh` creates `~/.claude/specumentation-mcp/` directory
  - [ ] `install.sh` copies `mcp-server/server.py` to `~/.claude/specumentation-mcp/server.py`
  - [ ] `install.sh` creates a symlink for `specumentation-mcp` CLI in a PATH-accessible location
  - [ ] `install.sh` prints the JSON snippet for `claude_desktop_config.json` with clear instructions
  - [ ] Existing skill symlink creation is preserved (no regression)
- **Files:** `install.sh`

### [E-02.03] Extend SKILL.md init phase for MCP project registration
- **Status:** open
- **Concept ref:** [01-mcp-server.md, Integration in den Skill](../concept/01-mcp-server.md#repository-structure-changes)
- **Description:** Update `SKILL.md` Phase 1 (Init) to call `specumentation-mcp init` after creating the `docs/` structure, so that each initialized project is automatically registered with the MCP server.
- **Acceptance Criteria:**
  - [ ] `SKILL.md` init phase includes a step to run `specumentation-mcp init`
  - [ ] The step only runs if the `specumentation-mcp` command is available in PATH
  - [ ] The step's success or failure does not block the rest of init
  - [ ] The summary output notes whether MCP registration succeeded
- **Files:** `SKILL.md`
