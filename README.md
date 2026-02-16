# specumentation

> **spec·u·men·ta·tion** — A portmanteau of *specification* and *documentation*.

A Claude Code skill that enforces a **spec-first development** workflow: write concept documents before code, derive epics with tickets, keep documentation in sync throughout the product lifecycle, and generate various document types as PDF.

## What It Does

- **Init** — Sets up an opinionated `docs/` structure with concept, epics, documents, and inbox directories
- **Concept** — Creates or updates concept documents that describe the application functionally and technically
- **Epics** — Derives actionable epics with tickets from concept documents
- **Inbox** — Processes external documents (e.g. from ChatGPT) and incorporates them into concepts and epics
- **Update** — Detects divergence between code and concepts, flags it, and synchronizes documentation
- **Publish** — Generates documents as PDF using predefined document types

## Installation

```bash
git clone https://github.com/McGo/specumentation.git
cd specumentation
bash install.sh
```

The installer creates a symlink from `~/.claude/skills/specumentation` to the cloned repository. No packages installed, no environment modified, no privileges required.

## Usage

```
/specumentation                              # Full cycle: all phases
/specumentation init                         # Initialize documentation structure
/specumentation concept auth-module          # Write/update concept for a specific topic
/specumentation epics                        # Generate/update epics from concepts
/specumentation inbox                        # Process docs from docs/in/
/specumentation update                       # Sync docs with code changes
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
└── in/                                     # Inbox for external documents
    ├── new-feature-idea.md                 # Waiting to be processed
    └── processed/                          # Already incorporated
        └── 2026-02-15-api-changes.md
```

## Workflow

1. **Spec first** — Before writing code, use `/specumentation concept [topic]` to define what you're building
2. **Plan work** — Use `/specumentation epics` to break concepts into concrete tickets
3. **Build** — Implement the code based on the specs
4. **Stay in sync** — Use `/specumentation update` to detect drift between code and docs
5. **External input** — Drop documents from other sources into `docs/in/`, then run `/specumentation inbox`
6. **Publish** — Use `/specumentation publish [type]` to generate documents at any time

## Requirements

- [Claude Code](https://claude.ai/code) CLI
- Google Chrome (for PDF generation, auto-detected on macOS/Linux/WSL)
- git, bash

## License

MIT
