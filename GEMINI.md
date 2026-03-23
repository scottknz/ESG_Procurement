# GEMINI.md — Project Context for Gemini CLI

This is the root context file for the ESG Procurement Platform project.
Gemini must read ONLY the explicitly listed canonical instruction files below before making any change. Ignore any other files in the directory.

## Context Exclusions

🔴 ABSOLUTE: Do not read, scan, or ingest the following files unless explicitly requested by the user for a specific task:
- Any Python scripts (these are located in `/PythonScripts/`)
- Environment files (`.env.local`, `.env`)
- System files (`.DS_Store`)
- Backup files (`*.bak*`)
- Non-canonical AI assistant directories (`.goose`, `.roo`, `.windsurf`, `.agents`, `.cursor`, etc.). The only canonical paths for Gemini are `.gemini/` and `Instructions/`.

## Instruction Files (read in this order)

🔴 ABSOLUTE: You MUST read every file listed below before writing a single line of code.

### Core Rules
1. `/Instructions/GEMINI.md` — Agent operating rules, product principles, coding standards, guardrails
2. `/Instructions/AGENTS.md` — 🔴 ABSOLUTE: Your agent persona, responsibilities, quality checklist, and validation commands
3. `/Instructions/AUTH_FLOWS.md` — Authentication and onboarding flow specifications

### Data & Architecture
4. `/Instructions/Database_Schema.md` — Single source of truth for all schema, RLS, and migration decisions
5. `/Instructions/Nextjs_Structure.md` — Canonical folder structure, route map, build order
6. `/Instructions/Tech_Stack.md` — Approved technology stack and architecture constraints

### Product
7. `/Instructions/Product_Spec_V1.md` — Full product specification and feature descriptions
8. `/Instructions/UserStories.md` — All user stories, grouped by role and feature

### Agent Skills (read the relevant file for your active task)
9. `/Instructions/Agent_Skills/01_Nextjs_React_Rules.md` — Next.js 16.2 & React 19 coding standards
10. `/Instructions/Agent_Skills/02_Supabase_DB_Rules.md` — Supabase & PostgreSQL standards
11. `/Instructions/Agent_Skills/03_Testing_and_AI_Rules.md` — Testing and AI SDK standards
12. `/Instructions/Agent_Skills/04_UI_Shadcn_Rules.md` — UI, Shadcn, and Tailwind standards

### Handoff
13. `/Instructions/Handoffs/handoff_template.md` — 🔴 ABSOLUTE: Mandatory context handoff template between phases
14. `/Instructions/Handoffs/phase-[XX]-context.md` — Read the latest phase handoff file if one exists

## Source of Truth Priority (when files conflict)

🔴 ABSOLUTE: When any two files contradict each other, resolve using this order. Lower number wins.

1. `Database_Schema.md` — Schema is always the ground truth
2. `AUTH_FLOWS.md` — Security and auth rules override everything except schema
3. `AGENTS.md` — Agent behaviour, personas, and quality checklists
4. `Nextjs_Structure.md` — Folder structure and build order
5. `Product_Spec_V1.md` — Feature requirements
6. `UserStories.md` — User intent
7. `Tech_Stack.md` — Technology constraints
8. `GEMINI.md` (`/Instructions/` version) — Workflow and coding behaviour
9. `Agent_Skills/*.md` — Syntax standards for the active task

If a conflict cannot be resolved using this list, STOP and ask the human.

## One-line project summary

A buyer-first ESG/sustainability procurement and RFP platform with AI-assisted drafting, scoring, and audit trail generation, built with Next.js 16.2 App Router, Supabase (Postgres + Auth + Storage), Gemini AI, Stripe, and Resend.

## Before doing ANYTHING

- Read all instruction files listed above (14 total).
- Produce a short execution plan.
- Wait for approval before writing code.
- Never invent tables, fields, routes, or libraries not listed in the instruction files.
