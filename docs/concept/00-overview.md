# specumentation — Project Overview

> This document is the entry point for all project documentation.
> Managed by [specumentation](https://github.com/McGo/claude-code-specumentation).

## Project Description

**specumentation** is a Claude Code skill that combines specification and documentation into a single workflow. It enforces a "spec first" development approach: write concept documents before code, derive epics with tickets, keep documentation in sync throughout the product lifecycle, and generate various document types as PDF.

This is a **declarative skill** — no runtime code, just structured prompts and templates (`SKILL.md`, document type definitions, and an installer script).

## Concept Index

| # | Concept | Status | Last Updated |
|---|---------|--------|--------------|
| 01 | [MCP Server](01-mcp-server.md) | draft | 2026-03-12 |

## Architecture Decisions

- **Declarative skill architecture**: No runtime code — the skill is purely structured prompts and templates executed by Claude Code.
- **Symlink-based installation**: `install.sh` creates a symlink from `~/.claude/skills/specumentation` to the cloned repository.
- **Document types as Markdown files**: Each document type is a `.md` file with frontmatter metadata and a generation prompt in `documents/`.
- **PDF generation via headless Chrome**: Uses `--headless --print-to-pdf` for reliable A4 output.
- **Files are never deleted**: Documents and resolved tickets form an audit trail.

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
