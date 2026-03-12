# specumentation — Project Overview

> This document is the entry point for all project documentation.
> Managed by [specumentation](https://github.com/McGo/claude-code-specumentation).

## Project Description

**specumentation** is a Claude Code skill that combines specification and documentation into a single workflow. It enforces a "spec first" development approach: write concept documents before code, derive epics with tickets, keep documentation in sync throughout the product lifecycle, and generate various document types as PDF.

The core skill is **declarative** — structured prompts and templates (`SKILL.md`, document type definitions, and an installer script). The project also includes an **MCP server** (Python) that exposes concept documents to Claude Desktop.

## Concept Index

| # | Concept | Status | Last Updated |
|---|---------|--------|--------------|
| 01 | [MCP Server](01-mcp-server.md) | implemented | 2026-03-12 |

## Architecture Decisions

- **Declarative skill architecture**: The skill itself is purely structured prompts and templates executed by Claude Code.
- **Symlink-based installation**: `install.sh` creates a symlink from `~/.claude/skills/specumentation` to the cloned repository.
- **Document types as Markdown files**: Each document type is a `.md` file with frontmatter metadata and a generation prompt in `documents/`.
- **PDF generation via headless Chrome**: Uses `--headless --print-to-pdf` for reliable A4 output.
- **Files are never deleted**: Documents and resolved tickets form an audit trail.
- **MCP server via FastMCP**: A Python-based MCP server provides Claude Desktop with structured access to concept documents, using stdio transport and a global project registry.

## Glossary

| Term | Definition |
|------|-----------|
| Concept | A functional and technical specification document describing a component or feature |
| Epic | A group of related implementation tickets derived from one or more concepts |
| Ticket | A concrete, implementable task within an epic, with acceptance criteria |
| Document type | A template definition that controls how concepts/epics are transformed into a published document |
| Inbox | The `docs/in/` directory where external documents are placed for processing |
| MCP | Model Context Protocol — Anthropic's protocol for connecting AI models to external data sources |
| MCP Server | A local server that exposes specumentation concepts to Claude Desktop via MCP |
| FastMCP | The high-level Python framework from the MCP SDK used to build MCP servers |
