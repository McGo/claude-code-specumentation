# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**specumentation** is a Claude Code skill (invoked via `/specumentation`) that combines specification and documentation into a single workflow. It enforces a "spec first" development approach and maintains living documentation throughout the product lifecycle, with the ability to generate various document types as PDF.

## Skill Architecture

The skill has two parts:

### Declarative Skill (no runtime code)
- `SKILL.md` — Core skill definition with frontmatter metadata and phased execution instructions. This is what Claude Code reads and executes.
- `documents/` — Document type definitions shipped with the skill. Each `.md` file defines a document type (frontmatter + generation prompt) that the publish phase uses.
- `install.sh` — Installer that symlinks the skill and deploys the MCP server.

### MCP Server (Python)
- `mcp-server/server.py` — FastMCP-based server (~250 lines) that exposes concept documents to Claude Desktop via 6 tools: `list_projects`, `set_project`, `get_overview`, `list_concepts`, `get_concept`, `update_concept`.
- `mcp-server/specumentation-mcp` — Bash CLI (~100 lines) for project registration (`init`) and listing (`list`).

Deployed to `~/.claude/specumentation-mcp/` by `install.sh`.

## Document Type System

Document types live in `documents/` and follow this pattern:

```yaml
---
name: user-manual          # Identifier for publish command
title: "User Manual"       # Human-readable title
output: "[project]-user-manual-[date]"  # Filename pattern
description: "..."         # What this type produces
---
[Generation prompt with structure and style instructions]
```

Built-in types: `user-manual`, `elevator-pitch`, `executive-summary`, `architecture`, `ticket-overview`.
New types can be added by creating a new `.md` file in `documents/`.

## Key Conventions

- Skills are installed as symlinks in `~/.claude/skills/`
- `SKILL.md` frontmatter uses `name`, `description`, `disable-model-invocation`
- PDF generation uses headless Chrome (`--headless --disable-gpu --print-to-pdf`)
- Documents are never deleted — they form an audit trail
- Language support via `lang=XX` parameter parsing
- MCP server uses FastMCP with stdio transport
- Project registry at `~/.claude/specumentation-mcp/projects.json`

## Commands

```bash
# Install skill globally (also deploys MCP server)
bash install.sh

# Invoke in any project (Claude Code)
/specumentation                          # Full cycle: all phases
/specumentation init                     # Set up docs/ directory structure
/specumentation concept [topic]          # Create/update a concept document
/specumentation epics                    # Derive epics with tickets from concepts
/specumentation inbox                    # Process external docs from docs/in/
/specumentation update                   # Sync documentation with code changes
/specumentation work                     # Pick next open ticket and implement it
/specumentation work E-02.03             # Implement a specific ticket
/specumentation whats-next               # Suggest the next step to take
/specumentation ticket-overview          # Show epic/ticket status overview + PDF
/specumentation publish                  # Generate all document types as PDF
/specumentation publish user-manual      # Generate a specific document type
/specumentation publish elevator-pitch lang=de  # Combined parameters

# MCP project management
specumentation-mcp init                  # Register current project
specumentation-mcp list                  # List registered projects
```

## Opinionated Target Project Structure

The skill enforces this structure in every project where it is used:

```
docs/
├── concept/          # Concept documents (functional & technical specs)
│   └── 00-overview.md
├── epics/            # Epics with tickets, derived from concepts
├── documents/        # Generated documents (PDF, HTML) + layout template
│   └── document-layout.html
├── assets/           # Logos, color definitions, images for documentation
└── in/               # Inbox for external docs (e.g. from ChatGPT), deleted after processing
```

## Specumentation

This project uses [specumentation](https://github.com/McGo/claude-code-specumentation) for spec-first development.

### Assumptions

- **Document language**: English (en) — derived from README language
- **Concept language**: English (en)
- **Project name**: specumentation
- **Project version source**: manual — no package manager config found

### Directory Structure

- `docs/concept/` — Concept documents (specifications)
- `docs/epics/` — Epics with tickets
- `docs/documents/` — Generated documents (PDF, HTML)
- `docs/assets/` — Branding resources (logos, colors)
- `docs/in/` — Inbox for external documents
