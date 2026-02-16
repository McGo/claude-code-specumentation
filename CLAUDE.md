# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**specumentation** is a Claude Code skill (invoked via `/specumentation`) that combines specification and documentation into a single workflow. It enforces a "spec first" development approach and maintains living documentation throughout the product lifecycle, with the ability to generate various document types as PDF.

## Skill Architecture

This is a **declarative skill** — no runtime code, just structured prompts and templates:

- `SKILL.md` — Core skill definition with frontmatter metadata and phased execution instructions. This is what Claude Code reads and executes.
- `documents/` — Document type definitions shipped with the skill. Each `.md` file defines a document type (frontmatter + generation prompt) that the publish phase uses.
- `install.sh` — Symlink-based installer to `~/.claude/skills/specumentation`.

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

Built-in types: `user-manual`, `elevator-pitch`, `executive-summary`, `architecture`.
New types can be added by creating a new `.md` file in `documents/`.

## Key Conventions (from sibling skill `security-audit`)

- Skills are installed as symlinks in `~/.claude/skills/`
- `SKILL.md` frontmatter uses `name`, `description`, `disable-model-invocation`
- PDF generation uses headless Chrome (`--headless --disable-gpu --print-to-pdf`)
- Documents are never deleted — they form an audit trail
- Language support via `lang=XX` parameter parsing

## Commands

```bash
# Install skill globally
bash install.sh

# Invoke in any project
/specumentation                          # Full cycle: all phases
/specumentation init                     # Set up docs/ directory structure
/specumentation concept [topic]          # Create/update a concept document
/specumentation epics                    # Derive epics with tickets from concepts
/specumentation inbox                    # Process external docs from docs/in/
/specumentation update                   # Sync documentation with code changes
/specumentation publish                  # Generate all document types as PDF
/specumentation publish user-manual      # Generate a specific document type
/specumentation publish elevator-pitch lang=de  # Combined parameters
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
└── in/               # Inbox for external docs (e.g. from ChatGPT)
    └── processed/    # Inbox items after incorporation
```
