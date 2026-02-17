---
name: ticket-overview
title: "Ticket Overview"
output: "[project]-ticket-overview-[date]"
description: "Tabular overview of all epics and tickets with status and summary"
---

Generate a compact ticket overview from the epic files. This document provides a **status dashboard** — a quick reference of all work items across all epics.

## Structure

1. **Title Page** — Project name, "Ticket Overview", date
2. **Summary** — Total epics, total tickets, breakdown by status (open / in progress / resolved)
3. **Overview Table** — One table per epic:

   **Epic [NN]: [Title]** — Status: [epic status]

   | ID | Status | Ticket Title | Summary |
   |----|--------|-------------|---------|
   | E-NN.01 | ✓ | [Title] | [1-2 sentence summary from description] |
   | E-NN.02 | → | [Title] | [1-2 sentence summary from description] |
   | E-NN.03 | ○ | [Title] | [1-2 sentence summary from description] |

4. **Legend**
   - `✓` — Resolved
   - `→` — In Progress
   - `○` — Open

## Status Indicators

Extract ticket status from the epic files:
- **resolved** → `✓`
- **in progress** → `→`
- **open** → `○`

## Tone & Style

- Compact and scannable — maximize information density
- Use tables exclusively — no prose paragraphs
- Sort epics by filename (natural order)
- Within each epic, list tickets in ID order
- Summaries are derived from the ticket description (first 1-2 meaningful sentences)
- 1-3 pages maximum when rendered as PDF
