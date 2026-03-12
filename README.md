# specumentation

> **spec·u·men·ta·tion** — A portmanteau of *specification* and *documentation*.

A Claude Code skill that enforces a **spec-first development** workflow: write concept documents before code, derive epics with tickets, keep documentation in sync throughout the product lifecycle, and generate various document types as PDF.

## What It Does

- **Init** — Sets up an opinionated `docs/` structure with concept, epics, documents, and inbox directories
- **Concept** — Analyzes the current codebase and creates or updates concept documents that describe the application functionally and technically
- **Epics** — Derives actionable epics with tickets from concept documents
- **Inbox** — Processes external documents (e.g. from ChatGPT) and incorporates them into concepts and epics
- **Update** — Detects divergence between code and concepts, flags it, and synchronizes documentation
- **Work** — Picks the next open ticket from the epics and implements it
- **Whats-Next** — Analyzes the project state and suggests exactly one next step
- **Ticket-Overview** — Displays epic/ticket status as a table and generates a PDF overview
- **Publish** — Generates documents as PDF using predefined document types

## Installation

```bash
git clone https://github.com/McGo/claude-code-specumentation.git
cd specumentation
bash install.sh
```

The installer:
1. Creates a symlink from `~/.claude/skills/specumentation` to the cloned repository
2. Deploys the MCP server to `~/.claude/specumentation-mcp/`
3. Symlinks the `specumentation-mcp` CLI to `/usr/local/bin` (or `~/.local/bin` as fallback)
4. Prints the configuration snippet for Claude Desktop (see [MCP Server](#mcp-server) below)

## Usage

```
/specumentation                              # Full cycle: all phases
/specumentation init                         # Initialize documentation structure
/specumentation concept auth-module          # Write/update concept for a specific topic
/specumentation epics                        # Generate/update epics from concepts
/specumentation inbox                        # Process docs from docs/in/
/specumentation update                       # Sync docs with code changes
/specumentation work                         # Pick next open ticket and implement it
/specumentation work E-02.03                 # Implement a specific ticket
/specumentation whats-next                   # What should I do next?
/specumentation ticket-overview              # Show epic/ticket status overview + PDF
/specumentation publish                      # Generate all document types as PDF
/specumentation publish user-manual          # Generate a specific document type
/specumentation publish architecture lang=de # Combined parameters
```

## Document Types

The skill ships with predefined document types that generate different outputs from your concept documents:

| Type | Description |
|------|------------|
| `user-manual` | End-user documentation: installation, features, configuration, troubleshooting |
| `elevator-pitch` | One-page product summary for quick communication |
| `executive-summary` | Management overview with project status, risks, and roadmap |
| `architecture` | Technical architecture document for developers |
| `ticket-overview` | Tabular status overview of all epics and tickets |

Custom document types can be added by placing a new `.md` file in the skill's `documents/` directory.

## Project Structure

The skill creates and maintains this opinionated structure in your project:

```
docs/
├── concept/                                # Concept documents (specifications)
│   ├── 00-overview.md                      # Project overview, concept index, glossary
│   ├── 01-authentication.md                # Topic concept
│   └── ...
├── epics/                                  # Implementation tasks
│   ├── epic-01-auth-setup.md               # Epic with tickets
│   └── ...
├── documents/                              # Published output
│   ├── document-layout.html                # Shared layout template for PDF generation
│   ├── myproject-user-manual-2026-02-16.pdf
│   ├── myproject-elevator-pitch-2026-02-16.pdf
│   └── ...
├── assets/                                 # Logos, colors, images for documents
│   ├── logo.svg
│   └── brand-colors.json
└── in/                                     # Inbox for external documents (deleted after processing)
    └── new-feature-idea.md                 # Waiting to be processed
```

## Workflow

1. **Spec first** — Before writing code, use `/specumentation concept [topic]` to define what you're building
2. **Plan work** — Use `/specumentation epics` to break concepts into concrete tickets
3. **Build** — Use `/specumentation work` to pick the next ticket and implement it
4. **Stay in sync** — Use `/specumentation update` to detect drift between code and docs
5. **External input** — Drop documents from other sources into `docs/in/`, then run `/specumentation inbox`
6. **Publish** — Use `/specumentation publish [type]` to generate documents at any time

## MCP Server

specumentation includes an **MCP server** that gives [Claude Desktop](https://claude.ai) direct access to your project's concept documents — no manual upload or copy-paste required.

### How It Works

The MCP server runs locally and understands the specumentation directory structure. When Claude Desktop connects, it can automatically read and update your concept documents through structured tools:

| Tool | Description |
|------|-------------|
| `get_overview()` | Load the project overview as initial context |
| `list_concepts()` | List all concepts with status from the index |
| `get_concept(topic)` | Read a specific concept by number or slug |
| `update_concept(topic, content)` | Write changes back, preserving the Change Log |
| `list_projects()` | Show all registered projects |
| `set_project(path)` | Switch to a different project |

### Setup

After running `install.sh`, add the MCP server to your Claude Desktop configuration:

**`~/Library/Application Support/Claude/claude_desktop_config.json`** (macOS):

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

Then register each project:

```bash
cd /path/to/your/project
specumentation-mcp init          # Register this project
specumentation-mcp list          # Show all registered projects
```

Projects are also auto-registered when you run `/specumentation init` (if the CLI is installed).

### Project Detection

The server detects the active project by walking up from the working directory to find a `docs/concept/` folder. As a fallback, it checks the project registry. You can also switch manually using the `set_project` tool.

## Requirements

- [Claude Code](https://claude.ai/code) CLI
- Google Chrome (for PDF generation, auto-detected on macOS/Linux/WSL)
- git, bash
- Python 3 + `mcp` package (for MCP server only — `pip install mcp`)

## License

MIT
