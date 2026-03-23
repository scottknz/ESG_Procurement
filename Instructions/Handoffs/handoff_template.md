# 🔴 ABSOLUTE — Phase [XX] - [Phase Name] - Handoff Context

> **This document is MANDATORY and must be completed before closing this chat session.**
> Failure to complete this file means the next agent will start blind, will hallucinate
> architectural decisions, and will break the build. This is a non-negotiable step.
>
> Save this file to: `Instructions/Handoffs/phase-[XX]-context.md`

**Completed By:** [Agent Name — e.g. Agent 1: Database Architect]
**Target Next Agent:** [Next Agent Name — e.g. Agent 2: API Architect]
**Phase Summary:** [One sentence describing what was built]


## 1. Work Completed
*   [List of major features built and files created]

## 2. Key Architectural Decisions & Context
*   [Why a specific approach was taken]
*   [Any deviations from the original spec and why]

## 3. Exposed Interfaces & Data Contracts
*   [Database types generated, API route URLs, exported function signatures]
*   *This is critical for the next agent so they know exactly how to consume your work without reading every file.*

## 4. Pending Items & Warnings for Next Agent
*   [Edge cases not handled, RLS policies that need corresponding UI, etc.]

## 5. Dependency & SDK Contract
*   [List any packages installed, versions pinned, and why — so the next agent doesn't reinstall conflicting versions]
*   e.g. `ai@6.x` and `@ai-sdk/google@latest` installed — do NOT install `@google/generative-ai` (native SDK)

## 6. Environment Variables Required
*   [List any new env vars this phase introduced that must be present in `.env.local` before the next agent starts]

> 🔴 ABSOLUTE: Do not hand off without completing every section above.
> The next agent will read ONLY this file plus the core instruction files.
> If context is missing here, it will be lost forever.
