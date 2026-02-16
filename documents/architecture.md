---
name: architecture
title: "Architecture Document"
output: "[project]-architecture-[date]"
description: "Technical architecture overview for developers and technical stakeholders"
---

Generate a technical architecture document from the concept documents. This document is written for **developers and technical stakeholders** who need to understand how the system is built.

## Structure

1. **Title Page** — Project name, version, date
2. **Table of Contents**
3. **System Overview** — High-level description of what the system does and its boundaries
4. **Architecture Principles** — Key design decisions and their rationale
5. **System Context** — External systems, APIs, services the application interacts with
6. **Component Overview** — Major components/modules and their responsibilities:
   - Component name and purpose
   - Key interfaces (inputs/outputs)
   - Dependencies between components
7. **Data Architecture**
   - Data models and their relationships
   - Data flow between components
   - Storage systems (databases, caches, file systems)
8. **Infrastructure & Deployment**
   - Runtime environment
   - Deployment architecture (containers, servers, cloud services)
   - Configuration management
9. **Cross-Cutting Concerns**
   - Authentication & authorization
   - Error handling & logging
   - Performance & scalability considerations
   - Security measures
10. **Technology Stack** — Languages, frameworks, libraries with version info where available
11. **Architecture Decision Records** — From `00-overview.md` Architecture Decisions section
12. **Glossary** — From `00-overview.md`

## Tone & Style

- Technical but accessible — a new developer should understand the system after reading this
- Use diagrams described in text (Mermaid syntax in code blocks where helpful)
- Reference specific files and directories from the codebase
- Explain the "why" behind architectural choices, not just the "what"
- 5-15 pages when rendered as PDF, depending on project complexity
