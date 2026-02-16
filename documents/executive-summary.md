---
name: executive-summary
title: "Executive Summary"
output: "[project]-executive-summary-[date]"
description: "Management-oriented overview of the project: goals, status, risks, and roadmap"
---

Generate an executive summary from the concept documents and epics. This document is written for **decision makers** — management, stakeholders, investors.

## Structure

1. **Title Page** — Project name, version, date, confidentiality notice
2. **Executive Overview** — 3-5 sentences summarizing the project
3. **Goals & Objectives** — What the project aims to achieve
4. **Current Status**
   - What has been implemented (from concepts with status `implemented`)
   - What is in progress (from open epics)
   - What is planned (from concepts with status `draft` or `approved`)
5. **Key Metrics** — Quantifiable facts:
   - Number of concepts / features
   - Epic completion rate (resolved vs. open tickets)
   - Documentation coverage
6. **Risks & Open Questions** — Aggregated from all concept Open Questions sections
7. **Roadmap** — Derived from epic priorities and concept statuses
8. **Resource Requirements** — If derivable from the epics

## Tone & Style

- Professional, concise, fact-based
- Use tables and bullet points over prose
- Lead with conclusions, then provide supporting detail
- Avoid technical implementation details — focus on business impact
- 2-4 pages maximum when rendered as PDF
