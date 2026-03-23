import re
from pathlib import Path

base = Path('/Users/drscottkelly/Dropbox (Personal)/Python/ESG_Procurement/Instructions')
root = Path('/Users/drscottkelly/Dropbox (Personal)/Python/ESG_Procurement')
fixes = []

def ap(tag, old, new, txt):
    if old in txt:
        fixes.append('  FIXED [' + tag + ']')
        return txt.replace(old, new)
    fixes.append('  SKIP  [' + tag + '] string not found')
    return txt

# ===================== DATABASE_SCHEMA.MD =====================
print('\n=== DATABASE_SCHEMA.MD ===')
f = base / 'Database_Schema.md'
txt = f.read_text()

txt = ap('DB-T1',
    "`'Draft'` | `'Internal Review'` | `'Private Invite'` | `'Published'` | `'Submission Closed'` | `'Evaluation'` | `'Award Recommended'` | `'Awarded'` | `'Withdrawn'` | `'Archived'`",
    "`'draft'` | `'open_for_proposals'` | `'closed'` | `'under_review'` | `'awarded'` | `'withdrawn'` | `'archived'`",
    txt)

txt = ap('DB-S1',
    "`'Draft'` | `'Declined'` | `'Submitted'` | `'Under Review'` | `'Disqualified'` | `'Shortlisted'` | `'Not Selected'` | `'Selected'`",
    "`'draft'` | `'submitted'` | `'withdrawn'` | `'disqualified'` | `'under_review'` | `'awarded'` | `'not_awarded'`",
    txt)

txt = ap('DB-KC1', 'tenders.status must always use the 10-value enum above.', 'tenders.status must always use the 7-value enum above.', txt)

txt = ap('DB-KC2',
    "`'Submission Closed'` is a TENDER-level property set either when `now() > submission_deadline` (enforced by the deadline-lock cron) or when the buyer manually clicks \"Close Submissions\". Supplier submission statuses are entirely separate and unaffected by this. Once status is `'Submission Closed'`, no new `supplier_submissions` rows may be inserted for that tender. The buyer then clicks \"Close and Score\" to move from `'Submission Closed'` to `'Evaluation'` and trigger the AI scoring queue. (Note: 'Submission Closed' is not a tender status; closure is computed dynamically via `submission_deadline`, or status moves directly to 'Evaluation' when scoring begins). Never add new status values without updating this file.",
    "`'closed'` is the TENDER-level status set when `now() > submission_deadline` (enforced by the deadline-lock cron) or when the buyer manually closes the tender. Once a tender is `'closed'`, no new proposals may be submitted. The buyer then moves the tender to `'under_review'` to trigger the AI scoring queue. Never add new status values without updating this file.",
    txt)

txt = ap('DB-KC3', "supplier_submissions.status must always use the 8-value enum above. Includes 'Declined'.", 'supplier_submissions.status must always use the 7-value enum above.', txt)

txt = ap('DB-KC4',
    "Suppliers are free to move their submission between `'Draft'`, `'Declined'`, and `'Submitted'` states at any time BEFORE the `submission_deadline` has passed AND BEFORE the buyer has moved the tender to `'Evaluation'`. Once either condition is true, no further status changes by the supplier are permitted. The only exception is `platform_admin`. There is no enforced ordering of transitions during the open window. Includes 'Withdrawn'. (Note: 'Submission Closed' is not a tender status; closure is computed dynamically via `submission_deadline`, or status moves directly to 'Evaluation' when scoring begins). Never add new status values without updating this file.",
    "Suppliers may move their proposal between `'draft'` and `'submitted'` freely, or set it to `'withdrawn'` to retract, at any time BEFORE the tender `submission_deadline` has passed AND BEFORE the buyer has moved the tender to `'under_review'`. Once either condition is true, no further status changes by the supplier are permitted. The only exception is `platform_admin`. Never add new status values without updating this file.",
    txt)

txt = ap('DB-AUD', "'SUBMISSION_DECLINED'", "'SUBMISSION_WITHDRAWN'", txt)

f.write_text(txt)

# ===================== PRODUCT_SPEC_V1.MD =====================
print('\n=== PRODUCT_SPEC_V1.MD ===')
f = base / 'Product_Spec_V1.md'
txt = f.read_text()

if not txt.startswith('# ESG Procurement Platform'):
    txt = '# ESG Procurement Platform - Product Specification V1\n> **Status:** Active | **Last updated:** March 2026\n> All citations and external links have been removed from this file.\n\n' + txt
    fixes.append('  FIXED [SPEC-VER] version header added')
else:
    fixes.append('  SKIP  [SPEC-VER] already present')

before = len(re.findall(r'\[\d+\]', txt))
txt = re.sub(r'\[\d+\]', '', txt)
fixes.append('  FIXED [SPEC-CIT1] stripped ' + str(before) + ' numbered citations')

before2 = len(re.findall(r'\[web:\d+\]', txt))
txt = re.sub(r'\[web:\d+\]', '', txt)
fixes.append('  FIXED [SPEC-CIT2] stripped ' + str(before2) + ' web citation artefacts')

txt = re.sub(r'\nSources\n\[1\].*?(?=\n## |\Z)', '', txt, flags=re.DOTALL)
fixes.append('  FIXED [SPEC-SRC] Sources section removed')

txt = ap('SPEC-TS',
    '**Draft**, **Internal Review**, **Private Invite**, **Published**, **Submission Closed**, **Evaluation**, **Award Recommended**, **Awarded**, and **Archived**.',
    '**draft**, **open_for_proposals**, **closed**, **under_review**, **awarded**, **withdrawn**, and **archived**.',
    txt)

txt = ap('SPEC-TS2',
    '**Draft** means the buyer is still defining the problem and editing the RFP, **Internal Review** means internal stakeholders can check requirements and scoring setup, and **Private Invite** means only selected suppliers can access the tender.  **Published** opens the tender to the intended supplier audience, **Submission Closed** stops uploads, **Evaluation** runs scoring and comparison, and the final states lock the decision trail for governance and future review.',
    '**draft**: buyer is preparing the RFP. **open_for_proposals**: tender is live and suppliers may submit. **closed**: no further proposals accepted. **under_review**: buyer is scoring and comparing proposals. **awarded**: decision is final. **withdrawn**: tender cancelled before award. **archived**: post-award archival.',
    txt)

txt = ap('SPEC-SS',
    '**Not Started**, **In Progress**, **Submitted**, **Under Review**, **Disqualified**, **Shortlisted**, **Not Selected**, and **Selected**.',
    '**draft**, **submitted**, **withdrawn**, **disqualified**, **under_review**, **awarded**, and **not_awarded**.',
    txt)

txt = ap('SPEC-SS2',
    'This mirrors the recruitment-style process you want and makes it easier to track comparisons, bidder drop-off, and review progress.',
    'A proposal moves from **draft** to **submitted** when the supplier confirms. It can be **withdrawn** by the supplier before the tender closes. The buyer may **disqualify** proposals failing mandatory criteria. During scoring proposals are **under_review**. After award they become either **awarded** (winner) or **not_awarded** (unsuccessful).',
    txt)

txt = ap('SPEC-DOC', 'DocuSign API or Documenso', 'Documenso', txt)

f.write_text(txt)

# ===================== NEXTJS_STRUCTURE.MD =====================
print('\n=== NEXTJS_STRUCTURE.MD ===')
f = base / 'Nextjs_Structure.md'
txt = f.read_text()

txt = ap('NX-PKG1', '`@google/generative-ai`, ', '', txt)
txt = ap('NX-PKG2', '`ai`.', '`ai`, `@ai-sdk/google`.', txt)
txt = ap('NX-GEM1',
    '├── gemini/\n│   ├── client.ts                  # Gemini API wrapper (server only)',
    '├── ai/\n│   ├── client.ts                  # ABSOLUTE: Vercel AI SDK wrapper (server only). Use @ai-sdk/google. Never import @google/generative-ai directly.',
    txt)
txt = ap('NX-SCHED',
    'scheduled-publish/route.ts # Cron: when now() > publish_at, sets status to Published, sets tenders.status to Submission Closed (tender-level). Does NOT touch supplier_submissions statuses.',
    "scheduled-publish/route.ts # Cron: moves tenders from 'draft' to 'open_for_proposals' when publish_at is reached. Does NOT close proposals - that is the deadline-lock cron.",
    txt)
txt = ap('NX-STEP', '12b. `src/middleware.ts`', '12.5. `src/middleware.ts`', txt)
txt = ap('NX-DOC',
    '├── docusign.ts                # E-signature integration for final contract execution',
    '├── documenso.ts               # E-signature integration via Documenso (open-source)',
    txt)
txt = ap('NX-DL',
    "Cron: sets tenders.status to 'Submission Closed' when deadline passes",
    "Cron: moves tenders.status from 'open_for_proposals' to 'closed' when submission_deadline passes",
    txt)
txt = ap('NX-SP2',
    "Cron: checks `publish_at` and moves Drafts to Published.",
    "Cron: checks `publish_at` and moves tenders from 'draft' to 'open_for_proposals'.",
    txt)
f.write_text(txt)

# ===================== TECH_STACK.MD =====================
print('\n=== TECH_STACK.MD ===')
f = base / 'Tech_Stack.md'
txt = f.read_text()
txt = ap('TS-NPM', 'npm install novel tiptap', 'npm install novel', txt)
txt = ap('TS-DOC',
    '**E-Signature:** DocuSign API (or equivalent) — embedded contract signing — transactional emails with HTML templates',
    '**E-Signature:** Documenso (open-source) — embedded contract signing via Documenso API',
    txt)
txt = ap('TS-PKG', '`@google/generative-ai`', '', txt)
f.write_text(txt)

# ===================== AGENTS.MD =====================
print('\n=== AGENTS.MD ===')
f = base / 'AGENTS.md'
txt = f.read_text()
txt = ap('AG-DOC', 'DocuSign', 'Documenso', txt)
txt = ap('AG-GEM', 'src/lib/gemini/**/*.ts', 'src/lib/ai/**/*.ts', txt)
txt = ap('AG-EX',
    '- `Instructions/AI_Copilot_Architecture.md`\n- `Instructions/Agent_Skills/03_Testing_and_AI_Rules.md`',
    '- `Instructions/Nextjs_Structure.md`\n- `Instructions/AUTH_FLOWS.md`\n- `Instructions/Agent_Skills/01_Nextjs_React_Rules.md`',
    txt)
f.write_text(txt)

# ===================== AUTH_FLOWS.MD =====================
print('\n=== AUTH_FLOWS.MD ===')
f = base / 'AUTH_FLOWS.md'
txt = f.read_text()
txt = ap('AF-RT',
    '**Routes:** `/register` -> `/register/[type]`',
    '**Routes:** `(auth)/register/page.tsx` -> `(auth)/register/[type]/page.tsx`',
    txt)
f.write_text(txt)

# ===================== INSTRUCTIONS/GEMINI.MD =====================
print('\n=== INSTRUCTIONS/GEMINI.MD ===')
f = base / 'GEMINI.md'
txt = f.read_text()
txt = ap('IG-TS',
    'Use only the exact tender states defined in `Database_Schema.md`.\nDo not invent extra ones.',
    'Use only the exact tender states defined in `Database_Schema.md`.\n7 valid tender states: `draft` | `open_for_proposals` | `closed` | `under_review` | `awarded` | `withdrawn` | `archived`.\n7 valid proposal states: `draft` | `submitted` | `withdrawn` | `disqualified` | `under_review` | `awarded` | `not_awarded`.\nDo not invent extra ones.',
    txt)
txt = ap('IG-DOC', 'DocuSign', 'Documenso', txt)
f.write_text(txt)

# ===================== AI_COPILOT_ARCHITECTURE.MD =====================
print('\n=== AI_COPILOT_ARCHITECTURE.MD ===')
f = base / 'AI_Copilot_Architecture.md'
txt = f.read_text()
txt = ap('CP-S2', "status='Selected'", "status='awarded'", txt)
txt = ap('CP-S3', "status='Not Selected'", "status='not_awarded'", txt)
txt = ap('CP-DOC', 'DocuSign', 'Documenso', txt)
f.write_text(txt)

# ===================== BUILD_LOG.MD =====================
print('\n=== BUILD_LOG.MD ===')
f = base / 'BUILD_LOG.md'
txt = f.read_text()
if 'DEVIATION LOG TEMPLATE' not in txt:
    template = '\n---\n\n## Deviation Log Template\n\nEvery time a REQUIRED rule is deviated from, add an entry below BEFORE continuing.\nEntries are permanent. Do not edit or remove them.\n\n```\n### Deviation Entry\n- Date/Time: [ISO timestamp]\n- Agent: [e.g. Agent 2: API Architect]\n- Rule broken: [exact rule text]\n- File affected: [path]\n- Justification: [specific technical reason]\n- Risk: [potential impact]\n- Approved by: [Human / Platform Admin]\n```\n\n---\n\n## Phase Progress\n\n| Phase | Agent | Status | Started | Completed |\n|-------|-------|--------|---------|-----------|\n| 1 | Database Architect | Pending | - | - |\n| 2 | API Architect | Pending | - | - |\n| 3 | Component Builder | Pending | - | - |\n| 4 | Integration Specialist | Pending | - | - |\n| 5 | AI Features Engineer | Pending | - | - |\n| 6 | Test Engineer | Pending | - | - |\n| 7 | Security Auditor | Pending | - | - |\n'
    f.write_text(txt.rstrip() + template)
    fixes.append('  FIXED [BL-SEED] BUILD_LOG.md seeded with deviation template + phase tracker')
else:
    fixes.append('  SKIP  [BL-SEED] already seeded')

print('\n' + '='*65)
print('ALL FIX RESULTS')
print('='*65)
for fx in fixes:
    print(fx)

# ===================== BROAD DIRECTORY SCAN =====================
print('\n' + '='*65)
print('BROAD SCAN - ALL .md FILES')
print('='*65)
all_md = list(base.rglob('*.md')) + [root / 'GEMINI.md']
dangers = [
    ('stale:InternalReview',   r'Internal Review'),
    ('stale:SubmissionClosed', r'Submission Closed'),
    ('stale:AwardRecommended', r'Award Recommended'),
    ('stale:PrivateInvite',    r'Private Invite'),
    ('stale:NotSelected',      r'Not Selected'),
    ('stale:Shortlisted',      r'Shortlisted'),
    ('stale:NotStarted',       r'Not Started'),
    ('stale:@google/gen',      r'@google/generative'),
    ('stale:ai@4',             r'ai@4\.'),
    ('DocuSign',               r'DocuSign'),
    ('citation:[web]',         r'\[web:\d+\]'),
    ('citation:[N]',           r'\[\d{1,2}\]'),
    ('stale:lib/gemini/',      r'lib/gemini/'),
    ('stale:hardcoded-model',  r"gemini\('gemini-2"),
    ('stale:toAIStream',       r'toAIStreamResponse'),
    ('stale:Declined-state',   r"'Declined'"),
    ('stale:novel-tiptap',     r'novel tiptap'),
    ('stale:docusign.ts',      r'docusign\.ts'),
]
broad = []
for md in sorted(all_md):
    try:
        c = md.read_text()
    except:
        continue
    nm = str(md).replace(str(base)+'/', '').replace(str(root)+'/', '')
    for (label, pat) in dangers:
        hits = re.findall(pat, c)
        if hits:
            broad.append((nm, label, len(hits)))
if broad:
    print('\nWARNINGS:')
    for (nm, label, n) in broad:
        print('  ' + nm + ' [' + label + '] ' + str(n) + ' hit(s)')
else:
    print('\nNo stale patterns found')

# ===================== VERIFICATION x2 =====================
def verify():
    errs = []
    db = (base / 'Database_Schema.md').read_text()
    for old in ['Internal Review','Submission Closed','Award Recommended','Private Invite','Not Started','Shortlisted','Not Selected']:
        if old in db: errs.append('FAIL DB: stale "' + old + '"')
    for new in ['open_for_proposals','under_review','not_awarded','SUBMISSION_WITHDRAWN']:
        if new not in db: errs.append('FAIL DB: missing "' + new + '"')
    if '7-value enum' not in db: errs.append('FAIL DB: key constraints not updated')
    spec = (base / 'Product_Spec_V1.md').read_text()
    if re.search(r'\[\d+\]', spec): errs.append('FAIL SPEC: numbered citations remain')
    if re.search(r'\[web:\d+\]', spec): errs.append('FAIL SPEC: web citations remain')
    for old in ['Internal Review','Submission Closed','Award Recommended','Not Started','Shortlisted','Not Selected']:
        if old in spec: errs.append('FAIL SPEC: stale "' + old + '"')
    nx = (base / 'Nextjs_Structure.md').read_text()
    if '@google/generative-ai' in nx: errs.append('FAIL NX: @google/generative-ai in build order')
    if '@ai-sdk/google' not in nx: errs.append('FAIL NX: @ai-sdk/google missing')
    if 'lib/gemini/' in nx: errs.append('FAIL NX: lib/gemini/ still present')
    if 'docusign.ts' in nx: errs.append('FAIL NX: docusign.ts still present')
    if '12b.' in nx: errs.append('FAIL NX: ambiguous 12b still present')
    if 'sets status to Published, sets tenders.status to Submission Closed' in nx: errs.append('FAIL NX: contradictory comment')
    ts = (base / 'Tech_Stack.md').read_text()
    if 'novel tiptap' in ts: errs.append('FAIL TS: novel tiptap remains')
    if 'DocuSign' in ts: errs.append('FAIL TS: DocuSign remains')
    ag = (base / 'AGENTS.md').read_text()
    if 'DocuSign' in ag: errs.append('FAIL AG: DocuSign remains')
    if 'lib/gemini/' in ag: errs.append('FAIL AG: lib/gemini/ in output files')
    af = (base / 'AUTH_FLOWS.md').read_text()
    if '`/register` -> `/register/[type]`' in af: errs.append('FAIL AF: old route notation')
    ig = (base / 'GEMINI.md').read_text()
    if 'open_for_proposals' not in ig: errs.append('FAIL IG: new states not in GEMINI.md')
    bl = (base / 'BUILD_LOG.md').read_text()
    if 'DEVIATION LOG TEMPLATE' not in bl: errs.append('FAIL BL: deviation template missing')
    return errs

for i in [1,2]:
    errs = verify()
    print('\n' + '='*65)
    print('VERIFICATION PASS ' + str(i))
    print('='*65)
    if not errs:
        print('ALL CHECKS PASSED')
    else:
        for e in errs: print('  ' + e)

print('\n' + '='*65 + '\nDONE\n' + '='*65)
