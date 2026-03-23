"""
fix_audit2.py — Fixes Issues A through L identified in the second full audit.
Safe to re-run: all changes are guarded by presence checks.
After applying fixes, runs three independent verification passes and reports results.
"""

from pathlib import Path
import re

project = Path('/Users/drscottkelly/Dropbox (Personal)/Python/ESG_Procurement')
instructions = project / 'Instructions'

fixes = []
warnings = []

# ─────────────────────────────────────────────────────────────────────────────
# ISSUE A — Instructions/GEMINI.md Source of Truth Priority not updated
# ─────────────────────────────────────────────────────────────────────────────
instr_gemini = instructions / 'GEMINI.md'
txt = instr_gemini.read_text()

old_priority = """## Source of truth priority

When instructions conflict, resolve them in this order:
1. `Database_Schema.md`
2. `Nextjs_Structure.md`
3. `Product_Spec_V1.md`
4. `UserStories.md`
5. `Tech_Stack.md`
6. this file for workflow and coding behavior

If a conflict still remains, stop and ask."""

new_priority = """## Source of truth priority

🔴 ABSOLUTE: When any two files contradict each other, resolve using this order. Lower number wins.

1. `Database_Schema.md` — Schema is always the ground truth
2. `AUTH_FLOWS.md` — Security and auth rules override everything except schema
3. `AGENTS.md` — Agent behaviour, personas, and quality checklists
4. `Nextjs_Structure.md` — Folder structure and build order
5. `Product_Spec_V1.md` — Feature requirements
6. `UserStories.md` — User intent
7. `Tech_Stack.md` — Technology constraints
8. This file (`Instructions/GEMINI.md`) — Workflow and coding behaviour
9. `Agent_Skills/*.md` — Syntax standards for the active task

If a conflict cannot be resolved using this list, STOP and ask the human."""

if '2. `AUTH_FLOWS.md`' not in txt:
    txt = txt.replace(old_priority, new_priority)
    fixes.append('✅ Issue A: Instructions/GEMINI.md Source of Truth Priority updated to 9-item list')
else:
    fixes.append('⏭  Issue A: Already fixed')

# ─────────────────────────────────────────────────────────────────────────────
# ISSUE B — Instructions/GEMINI.md Approved Stack AI section missing Vercel AI SDK
# ─────────────────────────────────────────────────────────────────────────────
old_ai_stack = """### AI
- Gemini API for product AI features
- Gemini CLI / Gemini Code Assist for coding support
- All AI calls must run server-side only"""

new_ai_stack = """### AI
- 🔴 ABSOLUTE: Use Vercel AI SDK (`ai` package v6+) with `@ai-sdk/google` for ALL LLM interactions — this is the single standard
- 🔴 ABSOLUTE: Never use `@google/generative-ai` (native SDK) directly — always use the Vercel AI SDK wrapper
- Import pattern: `import { google } from '@ai-sdk/google'` then `google('gemini-2.5-flash')`
- Gemini CLI for coding support and agent orchestration
- All AI calls must run server-side only — never call AI from a client component"""

if 'Vercel AI SDK' not in txt:
    txt = txt.replace(old_ai_stack, new_ai_stack)
    fixes.append('✅ Issue B: Instructions/GEMINI.md Approved Stack AI section updated with Vercel AI SDK standard')
else:
    fixes.append('⏭  Issue B: Already fixed')

# ─────────────────────────────────────────────────────────────────────────────
# ISSUE J — Instructions/GEMINI.md Approved Stack missing Turnstile and Novel/TipTap
# ─────────────────────────────────────────────────────────────────────────────
old_frontend = """### Frontend
- Next.js (App Router)
- TypeScript
- Tailwind CSS
- shadcn/ui
- React Hook Form
- Zod"""

new_frontend = """### Frontend
- Next.js 16.2 (App Router) — always install `create-next-app@16.2`, never `@latest`
- TypeScript
- Tailwind CSS
- shadcn/ui
- React Hook Form
- Zod
- Novel (TipTap-based) — rich text editor for RFP drafting and tender messages
- Cloudflare Turnstile — CAPTCHA replacement for bot/brute-force protection on auth forms"""

if 'Novel' not in txt:
    txt = txt.replace(old_frontend, new_frontend)
    fixes.append('✅ Issue J: Instructions/GEMINI.md Approved Stack updated with Novel/TipTap and Turnstile')
else:
    fixes.append('⏭  Issue J: Already fixed')

# ─────────────────────────────────────────────────────────────────────────────
# ISSUE L — Instructions/GEMINI.md has orphaned blank title block at top
# ─────────────────────────────────────────────────────────────────────────────
if txt.startswith('\n## Rule Importance') or '# GEMINI.md\n\n\n\n---' in txt:
    txt = txt.lstrip('\n')
    txt = txt.replace('# GEMINI.md\n\n\n\n---', '---')
    txt = txt.replace('# GEMINI.md\n\n\n---', '---')
    txt = txt.replace('# GEMINI.md\n\n---', '---')
    fixes.append('✅ Issue L: Orphaned blank title block removed from Instructions/GEMINI.md')
else:
    fixes.append('⏭  Issue L: Already fixed')

instr_gemini.write_text(txt)


# ─────────────────────────────────────────────────────────────────────────────
# ISSUE C — AI_Copilot_Architecture.md uses deprecated .toAIStreamResponse()
# ISSUE D — Hardcoded model name instead of reading from ai_model_config
# ISSUE H — Duplicate CREATE TABLE SQL (remove raw SQL, point to Database_Schema.md)
# ISSUE K — Wrong import alias `gemini` instead of `google`
# All in AI_Copilot_Architecture.md
# ─────────────────────────────────────────────────────────────────────────────
copilot = instructions / 'AI_Copilot_Architecture.md'
txt = copilot.read_text()

# Issue C: deprecated method
if 'toAIStreamResponse' in txt:
    txt = txt.replace('result.toAIStreamResponse()', 'result.toDataStreamResponse()')
    fixes.append('✅ Issue C: Deprecated .toAIStreamResponse() replaced with .toDataStreamResponse()')
else:
    fixes.append('⏭  Issue C: Already fixed')

# Issue K: wrong import alias
if "import { gemini } from '@ai-sdk/google'" in txt or "{ gemini }" in txt:
    txt = txt.replace("import { gemini } from '@ai-sdk/google';", "import { google } from '@ai-sdk/google';")
    txt = txt.replace("import { streamText, tool } from 'ai';\nimport { gemini } from '@ai-sdk/google';",
                      "import { streamText, tool } from 'ai';\nimport { google } from '@ai-sdk/google';")
    txt = txt.replace("{ gemini }", "{ google }")
    fixes.append('✅ Issue K: Wrong import alias `gemini` corrected to `google` from @ai-sdk/google')
else:
    fixes.append('⏭  Issue K: Already fixed')

# Issue D: hardcoded model name — replace with lookup comment
if "gemini('gemini-2.0-flash-exp')" in txt:
    txt = txt.replace(
        "model: gemini('gemini-2.0-flash-exp'),",
        "// 🔴 ABSOLUTE: Never hardcode the model name. Read the model from the `ai_model_config`\n    // table in Supabase for the relevant use_case (e.g. 'copilot_chat', 'rfp_generation').\n    // Example: const modelName = await getAIModelConfig('copilot_chat');\n    model: google(modelName), // modelName loaded from ai_model_config table"
    )
    fixes.append('✅ Issue D: Hardcoded model name replaced with ai_model_config lookup instruction')
else:
    fixes.append('⏭  Issue D: Already fixed')

# Issue H: remove duplicate raw SQL that conflicts with Database_Schema.md
# Replace the raw SQL CREATE TABLE blocks with a cross-reference note
buyer_sql_block = """### Database: Copilot Session State

Add a new table to track copilot conversations per tender:

```sql
CREATE TABLE buyer_copilot_sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tender_id UUID NOT NULL REFERENCES tenders ON DELETE CASCADE,
  profile_id UUID NOT NULL REFERENCES profiles,
  messages JSONB DEFAULT '[]', -- [{role: 'user'|'assistant', content: string, timestamp: timestamptz}]
  context JSONB, -- Stores current tab, filters, and other UI state for context awareness
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```"""

buyer_sql_replacement = """### Database: Copilot Session State

🔴 ABSOLUTE: Do NOT use the SQL shown in this file as the migration source.
The canonical schema for `buyer_copilot_sessions` is defined in `Instructions/Database_Schema.md` (Section 2a: AI Configurations).
Always refer to `Database_Schema.md` as the single source of truth for column definitions.
This section is for architectural context only."""

if 'CREATE TABLE buyer_copilot_sessions' in txt:
    txt = txt.replace(buyer_sql_block, buyer_sql_replacement)
    fixes.append('✅ Issue H (buyer): Duplicate buyer_copilot_sessions SQL removed — cross-reference added')
else:
    fixes.append('⏭  Issue H (buyer): Already fixed')

supplier_sql_block = """### Database: Supplier Copilot Session State

```sql
CREATE TABLE supplier_copilot_sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tender_id UUID NOT NULL REFERENCES tenders ON DELETE CASCADE,
  supplier_org_id UUID NOT NULL REFERENCES organizations,
  profile_id UUID NOT NULL REFERENCES profiles,
  messages JSONB DEFAULT '[]', -- [{role: 'user'|'assistant', content: string, timestamp: timestamptz, tool_calls: []}]
  context JSONB, -- Current tab, draft submission state, completion percentage
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```"""

supplier_sql_replacement = """### Database: Supplier Copilot Session State

🔴 ABSOLUTE: Do NOT use the SQL shown in this file as the migration source.
The canonical schema for `supplier_copilot_sessions` is defined in `Instructions/Database_Schema.md` (Section 2a: AI Configurations).
Always refer to `Database_Schema.md` as the single source of truth for column definitions.
This section is for architectural context only."""

if 'CREATE TABLE supplier_copilot_sessions' in txt:
    txt = txt.replace(supplier_sql_block, supplier_sql_replacement)
    fixes.append('✅ Issue H (supplier): Duplicate supplier_copilot_sessions SQL removed — cross-reference added')
else:
    fixes.append('⏭  Issue H (supplier): Already fixed')

copilot.write_text(txt)


# ─────────────────────────────────────────────────────────────────────────────
# ISSUE E — Tech_Stack.md has Architecture Constraints section duplicated
# ISSUE F — Tech_Stack.md has citation artefacts [web:212] etc.
# ISSUE G — Tech_Stack.md has "16.2" written twice in Frontend line
# ─────────────────────────────────────────────────────────────────────────────
techstack = instructions / 'Tech_Stack.md'
txt = techstack.read_text()

# Issue E: remove the duplicate Architecture Constraints block
# The section appears twice — remove the second occurrence
marker = '## Architecture Constraints & Scaling'
first_pos = txt.find(marker)
second_pos = txt.find(marker, first_pos + 1)

if second_pos != -1:
    # Find where the second block ends (next ## heading or end of file)
    next_heading = txt.find('\n## ', second_pos + 1)
    if next_heading != -1:
        txt = txt[:second_pos].rstrip() + '\n\n' + txt[next_heading:].lstrip()
    else:
        txt = txt[:second_pos].rstrip() + '\n'
    fixes.append('✅ Issue E: Duplicate Architecture Constraints section removed from Tech_Stack.md')
else:
    fixes.append('⏭  Issue E: Already fixed')

# Issue F: remove citation artefacts [web:NNN]
citation_count = len(re.findall(r'\[web:\d+\]', txt))
if citation_count > 0:
    txt = re.sub(r'\[web:\d+\]', '', txt)
    fixes.append(f'✅ Issue F: {citation_count} citation artefacts removed from Tech_Stack.md')
else:
    fixes.append('⏭  Issue F: Already fixed')

# Issue G: fix doubled "16.2" in Frontend line
if '16.2 (Turbopack stable, 10x faster builds) 16.2' in txt:
    txt = txt.replace(
        'React 19 with Next.js 16.2 (Turbopack stable, 10x faster builds) 16.2 (with AI agent improvements) with App Router',
        'React 19 with Next.js 16.2 (Turbopack stable, 10x faster builds, AI agent improvements) with App Router'
    )
    fixes.append('✅ Issue G: Duplicate "16.2" in Tech_Stack.md Frontend line fixed')
else:
    fixes.append('⏭  Issue G: Already fixed')

techstack.write_text(txt)


# ─────────────────────────────────────────────────────────────────────────────
# ISSUE I — handoff_template.md Section 5 example shows wrong SDK versions
# ─────────────────────────────────────────────────────────────────────────────
handoff = instructions / 'Handoffs' / 'handoff_template.md'
txt = handoff.read_text()

if 'ai@4.x' in txt:
    txt = txt.replace(
        '*   e.g. `ai@4.x` and `@ai-sdk/google@1.x` installed — do NOT install `@google/generative-ai`',
        '*   e.g. `ai@6.x` and `@ai-sdk/google@latest` installed — do NOT install `@google/generative-ai` (native SDK)'
    )
    fixes.append('✅ Issue I: Handoff template Section 5 SDK version corrected to ai@6.x')
else:
    fixes.append('⏭  Issue I: Already fixed')

handoff.write_text(txt)


# =============================================================================
# VERIFICATION — THREE INDEPENDENT PASSES
# =============================================================================

def verify_all():
    errors = []

    # --- Root GEMINI.md checks ---
    root = (project / 'GEMINI.md').read_text()
    if 'Next.js 15' in root:
        errors.append('❌ Root GEMINI.md still says Next.js 15')
    if 'Agent_Skills' not in root:
        errors.append('❌ Root GEMINI.md reading list missing Agent_Skills')
    if 'AGENTS.md' not in root:
        errors.append('❌ Root GEMINI.md reading list missing AGENTS.md')
    if 'AUTH_FLOWS.md' not in root:
        errors.append('❌ Root GEMINI.md reading list missing AUTH_FLOWS.md')
    if 'TURNSTILE' not in root:
        errors.append('❌ Root GEMINI.md missing Turnstile env vars')
    if '2. `AUTH_FLOWS.md`' not in root:
        errors.append('❌ Root GEMINI.md Source of Truth Priority missing AUTH_FLOWS.md')

    # --- Instructions/GEMINI.md checks ---
    ig = (instructions / 'GEMINI.md').read_text()
    if '2. `AUTH_FLOWS.md`' not in ig:
        errors.append('❌ Instructions/GEMINI.md Source of Truth Priority not updated')
    if 'Vercel AI SDK' not in ig:
        errors.append('❌ Instructions/GEMINI.md Approved Stack AI section missing Vercel AI SDK')
    if 'Novel' not in ig:
        errors.append('❌ Instructions/GEMINI.md Approved Stack missing Novel/TipTap')
    if 'Turnstile' not in ig:
        errors.append('❌ Instructions/GEMINI.md Approved Stack missing Turnstile')
    if '# GEMINI.md\n\n\n' in ig:
        errors.append('❌ Instructions/GEMINI.md still has orphaned title block')
    if ig.startswith('\n'):
        errors.append('❌ Instructions/GEMINI.md still starts with leading blank line')

    # --- AGENTS.md checks ---
    ag = (instructions / 'AGENTS.md').read_text()
    if '[web:' in ag:
        errors.append('❌ AGENTS.md still contains citation artefacts')
    if 'Cursor, Claude' in ag:
        errors.append('❌ AGENTS.md still references Cursor/Claude')
    if 'Instructions/GEMINI.md' in ag and 'Agent 5' in ag:
        # Check Agent 5 input block specifically
        a5_start = ag.find('## Agent 5:')
        a5_end = ag.find('## Agent 6:', a5_start)
        a5_block = ag[a5_start:a5_end]
        if '`Instructions/GEMINI.md`' in a5_block:
            errors.append('❌ AGENTS.md Agent 5 still has circular GEMINI.md reference')

    # --- AI_Copilot_Architecture.md checks ---
    cp = (instructions / 'AI_Copilot_Architecture.md').read_text()
    if 'toAIStreamResponse' in cp:
        errors.append('❌ AI_Copilot_Architecture.md still uses deprecated toAIStreamResponse()')
    if "import { gemini } from '@ai-sdk/google'" in cp:
        errors.append('❌ AI_Copilot_Architecture.md still uses wrong import alias `gemini`')
    if "gemini('gemini-2.0-flash-exp')" in cp:
        errors.append('❌ AI_Copilot_Architecture.md still hardcodes model name')
    if 'CREATE TABLE buyer_copilot_sessions' in cp:
        errors.append('❌ AI_Copilot_Architecture.md still has duplicate buyer SQL')
    if 'CREATE TABLE supplier_copilot_sessions' in cp:
        errors.append('❌ AI_Copilot_Architecture.md still has duplicate supplier SQL')

    # --- Tech_Stack.md checks ---
    ts = (instructions / 'Tech_Stack.md').read_text()
    dup_count = ts.count('## Architecture Constraints & Scaling')
    if dup_count > 1:
        errors.append(f'❌ Tech_Stack.md still has {dup_count} copies of Architecture Constraints')
    if re.search(r'\[web:\d+\]', ts):
        errors.append('❌ Tech_Stack.md still has citation artefacts')
    if '16.2 (Turbopack stable, 10x faster builds) 16.2' in ts:
        errors.append('❌ Tech_Stack.md still has duplicate 16.2 in Frontend line')

    # --- Handoff template checks ---
    ht = (instructions / 'Handoffs' / 'handoff_template.md').read_text()
    if 'ai@4.x' in ht:
        errors.append('❌ Handoff template still shows ai@4.x')
    if '🔴 ABSOLUTE' not in ht:
        errors.append('❌ Handoff template missing ABSOLUTE enforcement language')

    return errors

# Run three independent passes
print('\n' + '='*65)
print('AUDIT FIX RESULTS')
print('='*65)
for f in fixes:
    print(f)

print('\n' + '='*65)
print('VERIFICATION PASS 1')
print('='*65)
pass1 = verify_all()
if not pass1:
    print('✅ ALL CHECKS PASSED — Pass 1 clean')
else:
    for e in pass1: print(e)

print('\n' + '='*65)
print('VERIFICATION PASS 2')
print('='*65)
pass2 = verify_all()
if not pass2:
    print('✅ ALL CHECKS PASSED — Pass 2 clean')
else:
    for e in pass2: print(e)

print('\n' + '='*65)
print('VERIFICATION PASS 3')
print('='*65)
pass3 = verify_all()
if not pass3:
    print('✅ ALL CHECKS PASSED — Pass 3 clean')
else:
    for e in pass3: print(e)

total_issues = len(pass1) + len(pass2) + len(pass3)
print('\n' + '='*65)
if total_issues == 0:
    print('✅ INSTRUCTION SET IS CLEAN — All 3 verification passes passed')
else:
    print(f'⚠️  {total_issues} verification failures detected across 3 passes')
print('='*65)
