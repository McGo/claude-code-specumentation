---
name: specumentation
description: "Spec-first development workflow: create concept documents, derive epics with tickets, maintain living documentation, generate documents (manuals, pitches, architecture docs) as PDF"
disable-model-invocation: true
---

You are executing the **specumentation** skill — a combined specification and documentation workflow for Claude Code projects.

## Parameter Parsing

Parse `$ARGUMENTS` for:
- **Mode**: `init`, `concept`, `epics`, `inbox`, `update`, `publish`, `work` (default if none given: `full` = all phases sequentially, excluding `work`)
- **Topic name**: After `concept`, e.g. `concept auth-module`
- **Ticket ID**: After `work`, e.g. `work E-02.03` (default if none given: next open ticket by priority)
- **Document type**: After `publish`, e.g. `publish user-manual` (default if none given: all available document types)
- **Language**: `lang=XX` (e.g. `lang=de`, `lang=fr`; default: `en`)

All output (Markdown files, console messages, PDF content) MUST use the detected language.

---

## Opinionated Directory Structure

This skill expects and enforces the following structure in every project:

```
docs/
├── concept/          # Concept documents (functional & technical specifications)
├── epics/            # Epics with tickets, derived from concepts
├── documents/        # Generated documents (PDFs, HTML) + layout template
│   └── document-layout.html
├── assets/           # Logos, color definitions, images for documentation
└── in/               # Inbox: external concepts & change requests to be processed
```

Each directory has a distinct role. Files are NEVER deleted — only updated or superseded.

---

## Document Types

The skill ships with predefined document types in its `documents/` directory. Each document type is a Markdown file with frontmatter metadata and a generation prompt.

To list available document types, read all `.md` files from the skill's `documents/` directory. Each file defines:
- `name` — identifier used in `publish [name]`
- `title` — human-readable title for the generated document
- `output` — filename pattern (`[project]` and `[date]` are replaced)
- `description` — what this document type produces
- Generation instructions — the body of the file

When publishing, read the document type definition and follow its instructions to compose the document from the project's concept documents and epics.

---

## Phase 1 — Init (mode: `init` or `full`)

**Goal:** Set up the `docs/` directory structure in the target project.

### Steps:

1. Create directories if they don't exist: `docs/concept/`, `docs/epics/`, `docs/documents/`, `docs/assets/`, `docs/in/`.
2. Check if `docs/concept/00-overview.md` exists. If not, create it:

```markdown
# [Project Name] — Project Overview

> This document is the entry point for all project documentation.
> Managed by [specumentation](https://github.com/McGo/specumentation).

## Project Description

[Brief description — read from README.md or package manager config if available]

## Concept Index

| # | Concept | Status | Last Updated |
|---|---------|--------|--------------|
| — | — | — | — |

## Architecture Decisions

[High-level architecture notes, key technology choices, constraints]

## Glossary

| Term | Definition |
|------|-----------|
| — | — |
```

3. Check if `docs/documents/document-layout.html` exists. If not, create it with a professional HTML/CSS layout for A4 PDF printing (title page, table of contents, chapter styling, code blocks, tables, print-optimized CSS with proper page breaks and margins).
4. If `README.md` exists, extract project name and description to populate the overview.
5. If a package manager config exists (`package.json`, `composer.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`), extract project metadata.

**Output:** Confirm what was created and what already existed.

---

## Phase 2 — Concept (mode: `concept [topic]` or `full`)

**Goal:** Create or update concept documents that describe the application functionally and technically.

### When mode is `concept [topic]`:

Analyze the codebase for the named topic and create/update its concept document.

### When mode is `full`:

1. Analyze the entire codebase structure.
2. Identify logical components/features that should be documented.
3. Read existing concepts in `docs/concept/` to avoid duplication.
4. Create or update concept documents for components that are missing or outdated.

### Concept Document Format:

Each concept is saved as `docs/concept/[NN]-[topic-slug].md` where NN is a zero-padded sequence number.

```markdown
# [Topic Name]

> Concept document — Status: **draft** | **approved** | **implemented**

## Purpose

[What this component/feature does and why it exists]

## Functional Description

[Business logic, user stories, workflows, use cases]

## Technical Description

### Architecture

[How this fits into the overall system]

### Interface

[API surface, CLI commands, UI elements — whatever applies]

### Data Model

[Relevant data structures, schemas, database tables]

### Behavior

[State machines, algorithms, edge cases, error handling]

## Dependencies

[Internal and external dependencies]

## Open Questions

- [ ] [Unresolved questions that need answers before implementation]

## Change Log

| Date | Change | Author |
|------|--------|--------|
| [today] | Initial concept | specumentation |
```

### Rules:

- NEVER delete existing concepts — update them.
- When updating, add an entry to the Change Log.
- Set status to `draft` for new concepts, keep existing status unless the user explicitly changes it.
- Cross-reference between concepts using relative Markdown links.
- Update `docs/concept/00-overview.md` Concept Index after creating/updating any concept.
- If code exists but no concept exists, reverse-engineer the concept from the code and mark status as `implemented`.
- If a concept exists but code has diverged, note the divergence and add entries to Open Questions.

---

## Phase 3 — Epics (mode: `epics` or `full`)

**Goal:** Derive actionable epics with tickets from the concept documents.

### Steps:

1. Read all concept documents in `docs/concept/`.
2. Read all existing epics in `docs/epics/` to avoid duplication.
3. For each concept (or changed concept), derive implementation tasks:
   - Break down functional and technical requirements into concrete, implementable tickets.
   - Group related tickets into epics.
4. Create or update epic files.

### Epic File Format:

Each epic is saved as `docs/epics/epic-[NN]-[slug].md`.

```markdown
# Epic [NN]: [Epic Title]

> Derived from: [link to concept document(s)]
> Status: **open** | **in progress** | **closed**

## Description

[What this epic achieves as a whole]

## Tickets

### [E-NN.01] [Ticket Title]
- **Status:** open | in progress | resolved
- **Concept ref:** [link to concept, section]
- **Description:** [What needs to be done]
- **Acceptance Criteria:**
  - [ ] [Testable criterion]
  - [ ] [Testable criterion]
- **Files:** [Expected files/modules to be touched]

### [E-NN.02] [Ticket Title]
...
```

### Rules:

- NEVER delete resolved tickets — they form an audit trail.
- Resolved tickets get a `✓ RESOLVED` marker and a brief resolution description.
- When concepts change, update affected epics: add new tickets, mark obsolete ones as superseded.
- Ticket IDs are stable — never renumber existing tickets.
- Each ticket must have concrete acceptance criteria that can be tested.
- Reference the originating concept section for traceability.

---

## Phase 4 — Inbox (mode: `inbox` or `full`)

**Goal:** Process external documents from `docs/in/` and incorporate them into concepts and epics.

### Steps:

1. Read all files in `docs/in/` (Markdown, text, or any readable format). Ignore the `processed/` subdirectory.
2. For each document:
   a. Analyze its content — is it a new concept, a change to an existing concept, a feature request, a bug description, or a specification from an external source (e.g. ChatGPT)?
   b. Determine which existing concept(s) it relates to, or if a new concept is needed.
3. Incorporate the content:
   - **New concept**: Create a new concept document in `docs/concept/` with status `draft`, referencing the inbox document as source.
   - **Change to existing concept**: Update the affected concept(s), add Change Log entries noting the inbox document as source.
   - **New requirements**: Add to the relevant concept's Functional/Technical Description and create corresponding epic tickets.
4. After processing, move the inbox document to `docs/in/processed/` with a date prefix: `[YYYY-MM-DD]-[original-filename]`.
5. Update the Concept Index and affected epics.

### Rules:

- NEVER delete inbox documents — move them to `docs/in/processed/` after incorporation.
- Always note the source in Change Log entries: `Source: docs/in/[filename]`.
- If an inbox document is ambiguous or contradicts existing concepts, flag it in the Open Questions section of the affected concept.

---

## Phase 5 — Update (mode: `update` or `full`)

**Goal:** Synchronize documentation with the current state of the codebase.

### Steps:

1. Read all existing concepts in `docs/concept/`.
2. Analyze the codebase for changes since the last concept update (use Change Log dates and git history if available).
3. For each concept:
   a. Verify that described interfaces still match the code.
   b. Verify that data models are current.
   c. Check if new features have been implemented that aren't documented.
   d. Check if documented features have been removed or changed.
4. Update concepts where divergence is found.
5. Add Change Log entries for all updates.
6. Update the Concept Index in `00-overview.md`.
7. Update affected epics — mark implemented tickets as resolved, flag new divergences.

### Divergence Handling:

When code and concept diverge, add a notice block at the top of the affected section:

```markdown
> **⚠ Divergence detected** ([date]): [brief description of what changed in code vs. concept]
```

---

## Phase 6 — Work (mode: `work [ticket-id]`)

**Goal:** Pick the next open ticket from the epics and implement it.

**Important:** This phase is NOT part of `full` mode — it must be invoked explicitly.

### Ticket Selection:

1. If a ticket ID is given (e.g. `work E-02.03`), use that ticket.
2. If no ticket ID is given, select the next open ticket by priority:
   a. Read all epics in `docs/epics/` sorted by filename.
   b. Within each epic, find tickets by status priority: `in progress` first (resume), then `open`.
   c. Pick the first match.
3. If no open tickets exist, inform the user and suggest running `epics` to generate new tickets.

### Steps:

1. Read the selected ticket's full details (description, acceptance criteria, files, concept ref).
2. Read the referenced concept section(s) for context.
3. Display the ticket to the user:

```
── specumentation work ─────────────────────────────
Ticket:  [E-NN.XX] [Title]
Epic:    [Epic title]
Concept: [Concept reference]
─────────────────────────────────────────────────────
[Description]

Acceptance Criteria:
  - [ ] [Criterion 1]
  - [ ] [Criterion 2]
─────────────────────────────────────────────────────
```

4. Mark the ticket as `in progress` in the epic file.
5. Implement the ticket:
   - Follow the description and acceptance criteria.
   - Touch only the files listed in the ticket, unless additional files are clearly necessary.
   - Write code that satisfies all acceptance criteria.
6. After implementation, verify each acceptance criterion.
7. Mark the ticket as `✓ RESOLVED` in the epic file with a brief resolution description.
8. Update the related concept if the implementation revealed new information or divergence.
9. Git commit the code changes and the updated epic file separately:
   - Code: `feat|fix|refactor(...): [description]` (conventional commit based on change type)
   - Docs: `docs(specumentation): resolve [E-NN.XX] [title]`

### Rules:

- Only work on ONE ticket at a time.
- If the ticket is blocked or cannot be completed, keep it as `in progress` and add a note to the ticket explaining the blocker.
- Do NOT mark a ticket as resolved if acceptance criteria are not met.
- If implementation requires changes not covered by the ticket, create a new ticket in the appropriate epic for the additional work.

---

## Phase 7 — Publish (mode: `publish [document-type]` or `full`)

**Goal:** Generate a document as PDF from the project's concepts and epics.

### Document Type Resolution:

1. If a document type is specified (e.g. `publish user-manual`), read the matching definition from the skill's `documents/` directory.
2. If no document type is specified, generate **all** available document types.
3. If the requested document type does not exist, list available types and abort.

### Steps (per document type):

1. Read the document type definition from the skill's `documents/[type].md` file.
2. Read all concepts from `docs/concept/` in order (sorted by filename).
3. Read all epics from `docs/epics/` if the document type requires them.
4. Read `docs/documents/document-layout.html` as the layout template.
   - If the file does not exist, create it first (same as init phase).
5. Check `docs/assets/` for branding resources (logos, color definitions, images). If present, incorporate them into the generated document (e.g. logo on title page, brand colors in styling).
6. Follow the document type's generation instructions to compose the content.
7. Insert the composed content into the layout template.
7. Write the filled HTML to `docs/documents/`.
8. Auto-detect Chrome binary:
   - macOS: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`
   - Linux: `google-chrome` or `chromium-browser`
   - Windows/WSL: `/mnt/c/Program Files/Google*/Application/chrome.exe`
9. Generate PDF:
   ```
   "[chrome-path]" --headless --disable-gpu --no-sandbox --print-to-pdf="docs/documents/[output-pattern].pdf" --print-to-pdf-no-header "docs/documents/[output-pattern].html"
   ```
   Where `[output-pattern]` comes from the document type's `output` frontmatter field with `[project]` and `[date]` replaced.
10. Keep the HTML file alongside the PDF for reference.

### Filename Strategy:

- Pattern from document type: e.g. `[project]-user-manual-[date].pdf`
- If a PDF with today's date exists, append time: `[project]-user-manual-YYYY-MM-DD-HHmmSS.pdf`

### Available Document Types:

List them by reading the skill's `documents/` directory. Built-in types include:
- `user-manual` — End-user documentation
- `elevator-pitch` — One-page product summary
- `executive-summary` — Management overview with status and roadmap
- `architecture` — Technical architecture document for developers

---

## Git Integration

After each phase, if the project is a git repository:

1. Stage all new and modified files in `docs/` (except `docs/documents/*.pdf`).
2. Commit with message: `docs(specumentation): [brief description of what changed]`
3. Do NOT stage or commit PDF files.
4. Do NOT push — leave that to the user.

---

## Summary Output

After completing all requested phases, print a summary:

```
── specumentation complete ─────────────────────────
Mode:             [mode]
Concepts created:  [count]
Concepts updated:  [count]
Epics created:     [count]
Epics updated:     [count]
Inbox processed:   [count]
Documents generated:
  - [document-type]: [path]
  - ...
────────────────────────────────────────────────────
```
