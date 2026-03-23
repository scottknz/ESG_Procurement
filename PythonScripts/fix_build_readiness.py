import os
import shutil
from pathlib import Path

root = Path('/Users/drscottkelly/Dropbox (Personal)/Python/ESG_Procurement')
instructions = root / 'Instructions'

print('Starting build readiness fixes...')

# =============================================================================
# ISSUE 1: Rename AGENTS.MD -> GEMINI.md, create root GEMINI.md
# =============================================================================
agents_path = instructions / 'AGENTS.MD'
gemini_instructions_path = instructions / 'GEMINI.md'

if agents_path.exists() and not gemini_instructions_path.exists():
    agents_path.rename(gemini_instructions_path)
    print('  [1] Renamed Instructions/AGENTS.MD -> Instructions/GEMINI.md')
elif gemini_instructions_path.exists():
    print('  [1] Instructions/GEMINI.md already exists, skipping rename')

# Update all other instruction files that reference AGENTS.MD
for f in instructions.glob('*.md'):
    text = f.read_text()
    if 'AGENTS.MD' in text or 'AGENTS.md' in text:
        text = text.replace('AGENTS.MD', 'GEMINI.md').replace('AGENTS.md', 'GEMINI.md')
        f.write_text(text)
print('  [1] Updated all AGENTS.MD references -> GEMINI.md in Instructions/')

# Create root-level GEMINI.md
root_gemini = root / 'GEMINI.md'
root_gemini_content = """# GEMINI.md — Project Context for Gemini CLI

This is the root context file for the ESG Procurement Platform project.
Gemini must read ALL files in the `/Instructions/` directory before making any change.

## Instruction Files (read in this order)

1. `/Instructions/GEMINI.md` — Agent operating rules, source-of-truth priority, product principles, guardrails
2. `/Instructions/Database_Schema.md` — The single source of truth for all schema, RLS, and migration decisions
3. `/Instructions/Nextjs_Structure.md` — Canonical folder structure, route map, build order
4. `/Instructions/Product_Spec_V1.md` — Full product specification and feature descriptions
5. `/Instructions/UserStories.md` — All user stories, grouped by role and feature
6. `/Instructions/Tech_Stack.md` — Approved technology stack and architecture constraints

## Source of Truth Priority (when files conflict)

1. `Database_Schema.md`
2. `Nextjs_Structure.md`
3. `Product_Spec_V1.md`
4. `UserStories.md`
5. `Tech_Stack.md`
6. `GEMINI.md` (this file) for workflow and coding behaviour

## One-line project summary

A buyer-first ESG/sustainability procurement and RFP platform with AI-assisted drafting, scoring, and audit trail generation, built with Next.js 15 App Router, Supabase (Postgres + Auth + Storage), Gemini AI, Stripe, and Resend.

## Before doing ANYTHING

- Read all six instruction files above.
- Produce a short execution plan.
- Wait for approval before writing code.
- Never invent tables, fields, routes, or libraries not listed in the instruction files.
"""
root_gemini.write_text(root_gemini_content)
print('  [1] Created root-level GEMINI.md')


# =============================================================================
# ISSUE 2: Fix folder casing in all instruction files (instructions/ -> Instructions/)
# =============================================================================
for f in instructions.glob('*.md'):
    text = f.read_text()
    updated = text.replace('`instructions/`', '`Instructions/`').replace(
        'instructions/', 'Instructions/'
    ).replace('`/instructions`', '`/Instructions`')
    if updated != text:
        f.write_text(updated)
print('  [2] Fixed Instructions/ folder casing in all markdown files')


# =============================================================================
# ISSUE 3: Fix deadline-lock logic and Submission Closed as tender-level status
# =============================================================================
db_file = instructions / 'Database_Schema.md'
db_text = db_file.read_text()

# Add 'Submission Closed' back to tender status as a TENDER-level state
old_enum = "`'Draft'` | `'Internal Review'` | `'Private Invite'` | `'Published'` | `'Evaluation'` | `'Award Recommended'` | `'Awarded'` | `'Withdrawn'` | `'Archived'`"
new_enum = "`'Draft'` | `'Internal Review'` | `'Private Invite'` | `'Published'` | `'Submission Closed'` | `'Evaluation'` | `'Award Recommended'` | `'Awarded'` | `'Withdrawn'` | `'Archived'`"
db_text = db_text.replace(old_enum, new_enum)

old_rule1 = "1. `tenders.status` must always use the 9-value enum above. Includes 'Withdrawn'."
new_rule1 = """1. `tenders.status` must always use the 10-value enum above. `'Submission Closed'` is a TENDER-level property set either when `now() > submission_deadline` (enforced by the deadline-lock cron) or when the buyer manually clicks \"Close Submissions\". Supplier submission statuses are entirely separate and unaffected by this. Once status is `'Submission Closed'`, no new `supplier_submissions` rows may be inserted for that tender. The buyer then clicks \"Close and Score\" to move from `'Submission Closed'` to `'Evaluation'` and trigger the AI scoring queue."""
db_text = db_text.replace(old_rule1, new_rule1)
db_file.write_text(db_text)
print('  [3] Fixed Submission Closed as tender-level status in Database_Schema.md')

# Fix the deadline-lock route comment in Nextjs_Structure.md
nx_file = instructions / 'Nextjs_Structure.md'
nx_text = nx_file.read_text()
nx_text = nx_text.replace(
    '├── deadline-lock/route.ts     # Cron: closes submissions at deadline',
    '├── deadline-lock/route.ts     # Cron: when now() > submission_deadline, sets tenders.status to Submission Closed (tender-level). Does NOT touch supplier_submissions statuses.'
)
nx_file.write_text(nx_text)
print('  [3] Fixed deadline-lock route comment in Nextjs_Structure.md')


# =============================================================================
# ISSUE 4: Rewrite Tech_Stack.md as Gemini-first, remove Lovable references
# =============================================================================
tech_file = instructions / 'Tech_Stack.md'
tech_text = tech_file.read_text()

# Write a new Gemini-first header and replace the Lovable split sections
gemini_first_header = """# Tech Stack

The ESG Procurement Platform is built entirely using Gemini CLI as the primary code-generation agent. All routes, components, services, and migrations are generated and maintained by Gemini following the instruction files in `/Instructions/`. Lovable may be used later for **visual UI iteration only** (colours, spacing, layout polish) and must never be used to generate schema, business logic, or API routes.

## Core Stack

- **Frontend:** Next.js 15 with App Router — standard full-stack React with server components and server actions
- **UI layer:** shadcn/ui + Tailwind CSS — responsive dashboards, forms, multi-step workflows
- **Backend:** Supabase — Postgres, Auth, Storage, Edge Functions
- **AI:** Gemini API (server-side only) — RFP drafting, template adaptation, submission evaluation, audit summaries
- **Payments:** Stripe — £200 public listing fee, 5% success fee invoicing, webhook event handling
- **Email:** Resend — transactional emails with HTML templates
- **PDF Generation:** @react-pdf/renderer — audit reports and RFP exports
- **Background Jobs:** Supabase Edge Functions — long-running AI scoring tasks (avoids Vercel timeout)
- **Version control:** GitHub — source of truth
- **Deployment:** Vercel

## What Gemini Owns (Everything)

Gemini generates and maintains ALL of the following:
- Supabase migrations and RLS policies
- TypeScript types (auto-generated + hand-written domain types)
- Authentication and role-based access control
- Tender lifecycle state machine
- Scoring engine and weighted criteria logic
- AI evaluation prompt pipelines
- Stripe payment flows and webhook handlers
- PDF generation service layer
- Email templates and Resend integration
- All Next.js App Router pages, layouts, and API routes
- All shadcn/ui component compositions
- Background job queue for async AI evaluation

## Screen-to-Route Mapping

| Screen | Route | Notes |
|---|---|---|
| Landing / storefront | `(public)/[org_slug]/page.tsx` | Public branded buyer storefront |
| Public tender detail | `(public)/[org_slug]/tenders/[tender_id]/page.tsx` | Document download + reg wall |
| Login | `(auth)/login/page.tsx` | Supabase Auth UI |
| Register | `(auth)/register/page.tsx` | Org type selection + user setup |
| Invite onboarding | `(auth)/register/invite/page.tsx` | Invite token binding flow |
| Buyer dashboard | `(buyer)/buyer/dashboard/page.tsx` | Active tenders, deadlines |
| New tender wizard | `(buyer)/buyer/tenders/new/page.tsx` | AI-assisted multi-step wizard |
| Tender workspace | `(buyer)/buyer/tenders/[tender_id]/page.tsx` | Workspace hub |
| Submissions list | `(buyer)/buyer/tenders/[tender_id]/submissions/page.tsx` | Triage table |
| Submission detail | `(buyer)/buyer/tenders/[tender_id]/submissions/[id]/page.tsx` | Full review + labels |
| Evaluation dashboard | `(buyer)/buyer/tenders/[tender_id]/evaluate/page.tsx` | Side-by-side scoring |
| Award screen | `(buyer)/buyer/tenders/[tender_id]/award/page.tsx` | Final decision + invoice trigger |
| Buyer history | `(buyer)/buyer/history/page.tsx` | Historical archive + audit PDFs |
| Messages | `(buyer)/buyer/tenders/[tender_id]/messages/page.tsx` | Tender message composer |
| Supplier dashboard | `(supplier)/supplier/dashboard/page.tsx` | Invitations + active bids |
| Supplier bid form | `(supplier)/supplier/bids/[tender_id]/page.tsx` | Dynamic submission form |
| Supplier unlock | `(supplier)/supplier/bids/[tender_id]/unlock/page.tsx` | Stripe paywall |
| Supplier final review | `(supplier)/supplier/bids/[tender_id]/review/page.tsx` | Review before submit |
| Admin dashboard | `(admin)/admin/dashboard/page.tsx` | Platform metrics |

"""

# Preserve alignment/architecture constraint sections appended previously
alignment_start = '## Architecture Constraints & Scaling'
if alignment_start in tech_text:
    constraints_section = tech_text[tech_text.index(alignment_start):]
else:
    constraints_section = ""

# Write the clean new file
new_tech = gemini_first_header
if constraints_section:
    new_tech += "\n" + constraints_section

# Re-add messaging and alignment sections if present
for section_marker in ['## Alignment update: messaging', 'alignment update']:
    if section_marker.lower() in tech_text.lower() and section_marker not in new_tech:
        idx = tech_text.lower().index(section_marker.lower())
        section = tech_text[idx:]
        # Only add up to the next ## heading if there is one after
        new_tech += "\n" + section
        break

tech_file.write_text(new_tech)
print('  [4] Rewrote Tech_Stack.md as Gemini-first')


# =============================================================================
# ISSUE 5 + 8: Fix build order — add Step 0 and 6 missing steps
# =============================================================================
nx_text = nx_file.read_text()

new_build_order = """## Build Order for Gemini

Build in this strict sequence. Do not skip ahead. Each step must pass its checks before the next begins.

0. **Initialise project:** Run `npx create-next-app@latest` with App Router + TypeScript + Tailwind. Run `npx supabase init`. Install core dependencies: `@supabase/supabase-js`, `@supabase/ssr`, `stripe`, `@stripe/stripe-js`, `resend`, `@google/generative-ai`, `@react-pdf/renderer`, `zod`, `shadcn/ui`.
1. `supabase/migrations/` — Write all migration SQL from `Database_Schema.md`. Include all triggers for audit immutability, the partial unique index for org lead, and the `updated_at` triggers.
2. `src/types/database.ts` — Regenerate after migrations with `npx supabase gen types typescript`
3. `src/lib/supabase/` — Server + browser + admin clients
4. `src/lib/stripe/client.ts` — Stripe server-side client, £200 listing fee checkout, 5% invoice creation
5. `src/lib/validation/schemas.ts` — Zod schemas for all key types and form inputs
6. `src/lib/audit/log.ts` — Central audit helper (used everywhere)
7. `src/lib/tender/state-machine.ts` — All tender status transitions with validation
8. `src/lib/tender/deadline.ts` — Deadline lockout checker
9. `src/lib/messages/service.ts` — Canonical tender message creation + email fan-out + communications_log writes
10. `src/lib/storage/unlock-check.ts` — Checks `supplier_tender_unlocks` before serving documents to uninvited suppliers
11. `src/lib/scoring/calculate.ts` — Weighted score formula and disqualification logic
12. `src/lib/background/scoring-queue.ts` — Async AI evaluation job dispatcher (Supabase Edge Function trigger)
13. `(auth)` routes — Login, register, callback, invite token onboarding
14. `(buyer)` routes — Dashboard, wizard, evaluation, award, history, messages
15. `(supplier)` routes — Dashboard, profile, bid form, unlock paywall, final review
16. `(public)` routes — Storefront and public tender detail with reg-wall
17. `(admin)` routes — Platform metrics, org management, audit log
18. `api/ai/` routes — All Gemini AI integrations (server-side only)
19. `api/webhooks/stripe/route.ts` — Handle £200 listing fee + 5% invoice Stripe webhook events
20. `api/webhooks/deadline-lock/route.ts` — Cron: sets tenders.status to 'Submission Closed' when deadline passes
21. `api/webhooks/award-tender/route.ts` — Post-award: generate audit PDF, ZIP archive, send emails
22. `src/lib/pdf/` — Audit report + RFP export PDF generation
23. `src/lib/email/` — Resend client + all email templates
"""

# Replace the old build order section
build_start = '## Build Order for Gemini'
build_end = '\n\n\n## Alignment update:'
if build_start in nx_text:
    before_build = nx_text[:nx_text.index(build_start)]
    after_build_idx = nx_text.index(build_start) + len(build_start)
    remaining = nx_text[after_build_idx:]
    # Find where next major section starts after build order
    if '\n## ' in remaining:
        after_section = remaining[remaining.index('\n## '):]
    elif '\n---' in remaining:
        after_section = remaining[remaining.index('\n---'):]
    else:
        after_section = ''
    nx_text = before_build + new_build_order + after_section
nx_file.write_text(nx_text)
print('  [5+8] Updated build order with Step 0 and all missing steps')


# =============================================================================
# ISSUE 6: Add missing routes to Nextjs_Structure.md
# =============================================================================
nx_text = nx_file.read_text()

# Add Stripe webhook route
if 'webhooks/stripe' not in nx_text:
    nx_text = nx_text.replace(
        '│   ├── webhooks/',
        '│   ├── webhooks/\n│   │   ├── stripe/route.ts             # Stripe webhook: £200 listing fee + 5% success fee invoice events'
    )

# Add submission detail route under submissions
if 'submissions/[submission_id]' not in nx_text and 'submissions/[id]' not in nx_text:
    nx_text = nx_text.replace(
        '│   │   │       ├── submissions/\n│   │   │       │   ├── page.tsx       # All submissions list + topline table',
        '│   │   │       ├── submissions/\n│   │   │       │   ├── page.tsx       # All submissions list + topline table\n│   │   │       │   ├── [submission_id]/\n│   │   │       │       ├── page.tsx   # Full submission detail: answers, files, PDF download, review label'
    )

# Add messages route to buyer tender
if 'messages/page.tsx' not in nx_text:
    nx_text = nx_text.replace(
        '│   │   │       ├── award/page.tsx     # Final decision + email drafting',
        '│   │   │       ├── award/page.tsx     # Final decision + email drafting\n│   │   │       ├── messages/page.tsx  # Tender message composer: To/CC/subject/HTML/attachments'
    )

# Add buyer history route
if 'history/page.tsx' not in nx_text:
    nx_text = nx_text.replace(
        '│   │   ├── portal/page.tsx',
        '│   │   ├── history/page.tsx           # Historical archive: all past tenders, statuses, audit PDFs\n│   │   ├── portal/page.tsx'
    )

# Add invite onboarding route
if 'register/invite' not in nx_text:
    nx_text = nx_text.replace(
        '│   ├── register/page.tsx              # Organization type selection + user setup',
        '│   ├── register/page.tsx              # Organization type selection + user setup\n│   ├── register/invite/page.tsx       # Invite token onboarding: binds new user to org + tender'
    )

# Add supplier unlock + review routes
if 'unlock/page.tsx' not in nx_text:
    nx_text = nx_text.replace(
        '│           ├── page.tsx           # Dynamic submission form + file upload\n│           ├── qa/page.tsx        # Private Q&A thread for this tender',
        '│           ├── page.tsx           # Dynamic submission form + file upload\n│           ├── unlock/page.tsx    # Stripe paywall for uninvited supplier document access\n│           ├── review/page.tsx    # Final submission review + 5% fee checkbox before submit\n│           ├── qa/page.tsx        # Private Q&A thread for this tender'
    )

nx_file.write_text(nx_text)
print('  [6] Added 7 missing routes to Nextjs_Structure.md')


# =============================================================================
# ISSUE 7: Add missing service modules to src/lib/ tree
# =============================================================================
nx_text = nx_file.read_text()

if 'stripe/' not in nx_text:
    nx_text = nx_text.replace(
        '├── gemini/',
        '├── stripe/\n│   ├── client.ts                  # Stripe server-side client\n│   ├── listing-fee.ts             # £200 public listing fee checkout session creation\n│   ├── success-invoice.ts         # 5% success fee invoice generation and send to supplier\n├── gemini/'
    )

if 'messages/service' not in nx_text:
    nx_text = nx_text.replace(
        '├── scoring/',
        '├── messages/\n│   ├── service.ts                 # Create canonical tender_messages + fan out to communications_log\n│   ├── composer.ts                # Helpers for email draft formatting, HTML sanitisation, plain-text fallback\n├── scoring/'
    )

if 'background/' not in nx_text:
    nx_text = nx_text.replace(
        '├── audit/',
        '├── background/\n│   ├── scoring-queue.ts           # Dispatch async Gemini AI evaluation jobs via Supabase Edge Function\n├── audit/'
    )

if 'unlock-check' not in nx_text:
    nx_text = nx_text.replace(
        '├── signed-url.ts',
        '├── signed-url.ts              # Generate secure signed download URLs\n│   ├── unlock-check.ts            # Checks supplier_tender_unlocks table before serving files to uninvited suppliers'
    )

nx_file.write_text(nx_text)
print('  [7] Added 4 missing service modules to src/lib/ tree')


# =============================================================================
# ISSUE 9: Remove floating alignment appendix, integrate into canonical tree
# =============================================================================
nx_text = nx_file.read_text()
if '## Alignment update: tender workspace, review labels, and messaging' in nx_text:
    # Remove the appended prose section since it is now baked into the tree and build order
    idx = nx_text.index('## Alignment update: tender workspace, review labels, and messaging')
    nx_text = nx_text[:idx].rstrip() + '\n'
    nx_file.write_text(nx_text)
print('  [9] Removed floating alignment appendix from Nextjs_Structure.md (now in tree and build order)')


# =============================================================================
# ISSUE 10: Remove hardcoded Supabase key from .gemini/settings.json
# =============================================================================
import json
settings_path = root / '.gemini' / 'settings.json'
settings = json.loads(settings_path.read_text())
if 'supabase' in settings.get('mcpServers', {}):
    args = settings['mcpServers']['supabase'].get('args', [])
    new_args = []
    skip_next = False
    for i, arg in enumerate(args):
        if skip_next:
            skip_next = False
            continue
        if arg == '--supabase-key':
            new_args.append(arg)
            new_args.append('${SUPABASE_MCP_KEY}')  # Use env var reference
            skip_next = True
        else:
            new_args.append(arg)
    settings['mcpServers']['supabase']['args'] = new_args
    settings_path.write_text(json.dumps(settings, indent=2))
print('  [10] Replaced hardcoded Supabase key in .gemini/settings.json with ${SUPABASE_MCP_KEY}')

# Add SUPABASE_MCP_KEY to .env.example
env_example = root / '.env.example'
env_text = env_example.read_text()
if 'SUPABASE_MCP_KEY' not in env_text:
    env_text += '\n# Supabase MCP Server (for Gemini CLI direct DB access)\nSUPABASE_MCP_KEY="your-supabase-service-role-key-here"\n'
    env_example.write_text(env_text)
print('  [10] Added SUPABASE_MCP_KEY to .env.example')


# =============================================================================
# ISSUE 11: Remove duplicate agent skill folders
# =============================================================================
duplicate_dirs = [
    root / '.adal',
    root / '.agent',
    root / '.augment',
    root / '.claude',
    root / '.codebuddy',
    root / '.commandcode',
    root / '.cortex',
    root / '.crush',
    root / '.continue',
    root / '.factory',
]
for d in duplicate_dirs:
    if d.exists():
        shutil.rmtree(d)
        print(f'  [11] Removed duplicate folder: {d.name}/')

print('')
print('All 11 issues resolved.')
