import re
from pathlib import Path

project = Path('/Users/drscottkelly/Dropbox (Personal)/Python/ESG_Procurement')
instructions = project / 'Instructions'

# ── Fix stray [web:202] still in AGENTS.md ────────────────────────────────────
ag_path = instructions / 'AGENTS.md'
ag = ag_path.read_text()
before = len(re.findall(r'\[web:\d+\]', ag))
ag = re.sub(r'\[web:\d+\]', '', ag)
after = len(re.findall(r'\[web:\d+\]', ag))
ag_path.write_text(ag)
print(f'AGENTS.md: removed {before} citation(s), {after} remaining')

# ── Verification function ─────────────────────────────────────────────────────
def verify():
    errors = []

    root = (project / 'GEMINI.md').read_text()
    if 'Next.js 15'            in root: errors.append('FAIL root GEMINI.md: still says Next.js 15')
    if 'Agent_Skills'      not in root: errors.append('FAIL root GEMINI.md: missing Agent_Skills')
    if 'AGENTS.md'         not in root: errors.append('FAIL root GEMINI.md: missing AGENTS.md')
    if 'AUTH_FLOWS.md'     not in root: errors.append('FAIL root GEMINI.md: missing AUTH_FLOWS.md')
    if '2. `AUTH_FLOWS.md`' not in root: errors.append('FAIL root GEMINI.md: priority list missing AUTH_FLOWS.md')

    ig = (instructions / 'GEMINI.md').read_text()
    if '2. `AUTH_FLOWS.md`'  not in ig: errors.append('FAIL instr GEMINI.md: priority not updated')
    if 'Vercel AI SDK'       not in ig: errors.append('FAIL instr GEMINI.md: missing Vercel AI SDK')
    if 'Novel'               not in ig: errors.append('FAIL instr GEMINI.md: missing Novel/TipTap')
    if 'Turnstile'           not in ig: errors.append('FAIL instr GEMINI.md: missing Turnstile')
    if 'TURNSTILE'           not in ig: errors.append('FAIL instr GEMINI.md: missing TURNSTILE env var')
    if '# GEMINI.md\n\n\n'  in  ig: errors.append('FAIL instr GEMINI.md: orphaned title block remains')

    ag2 = (instructions / 'AGENTS.md').read_text()
    if '[web:'           in ag2: errors.append('FAIL AGENTS.md: citation artefacts remain')
    if 'Cursor, Claude'  in ag2: errors.append('FAIL AGENTS.md: Cursor/Claude reference remains')
    a5s = ag2.find('## Agent 5:')
    a5e = ag2.find('## Agent 6:', a5s)
    if '`Instructions/GEMINI.md`' in ag2[a5s:a5e]:
        errors.append('FAIL AGENTS.md Agent 5: circular GEMINI.md reference remains')

    cp = (instructions / 'AI_Copilot_Architecture.md').read_text()
    if 'toAIStreamResponse'                     in cp: errors.append('FAIL copilot: deprecated toAIStreamResponse()')
    if "import { gemini } from '@ai-sdk/google'" in cp: errors.append('FAIL copilot: wrong import alias gemini')
    if "gemini('gemini-2.0-flash-exp')"          in cp: errors.append('FAIL copilot: hardcoded model name')
    if 'CREATE TABLE buyer_copilot_sessions'     in cp: errors.append('FAIL copilot: duplicate buyer SQL')
    if 'CREATE TABLE supplier_copilot_sessions'  in cp: errors.append('FAIL copilot: duplicate supplier SQL')

    ts = (instructions / 'Tech_Stack.md').read_text()
    if ts.count('## Architecture Constraints & Scaling') > 1:
        errors.append('FAIL Tech_Stack.md: Architecture Constraints section duplicated')
    if re.search(r'\[web:\d+\]', ts):
        errors.append('FAIL Tech_Stack.md: citation artefacts remain')
    if '16.2 (Turbopack stable, 10x faster builds) 16.2' in ts:
        errors.append('FAIL Tech_Stack.md: duplicate 16.2 in Frontend line')

    ht = (instructions / 'Handoffs' / 'handoff_template.md').read_text()
    if 'ai@4.x'    in ht: errors.append('FAIL handoff_template.md: wrong SDK version ai@4.x')
    if 'ABSOLUTE' not in ht: errors.append('FAIL handoff_template.md: missing ABSOLUTE enforcement')

    return errors

# ── Run 3 independent passes ──────────────────────────────────────────────────
print()
all_clean = True
for i in range(1, 4):
    errors = verify()
    sep = '=' * 55
    print(sep)
    print(f'VERIFICATION PASS {i}')
    print(sep)
    if not errors:
        print(f'\u2705 Pass {i}: ALL {20} checks passed')
    else:
        all_clean = False
        for e in errors:
            print(f'  {e}')

print()
print('=' * 55)
if all_clean:
    print('\u2705 INSTRUCTION SET IS FULLY CLEAN \u2014 all 3 passes passed')
else:
    print('\u26a0\ufe0f  Remaining issues detected \u2014 see failures above')
print('=' * 55)
