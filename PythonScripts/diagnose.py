from pathlib import Path
import re

base = Path('/Users/drscottkelly/Dropbox (Personal)/Python/ESG_Procurement/Instructions')

files = {
    'Database_Schema.md': ['Not Started','Shortlisted','Not Selected','Declined','supplier_submissions','DocuSign','docusign','Internal Review','Submission Closed','Award Recommended'],
    'AGENTS.md': ['DocuSign','docusign','@google/generative','lib/gemini','12b','AI_Copilot_Architecture','novel tiptap','gemini/'],
    'Tech_Stack.md': ['DocuSign','docusign','@google/generative','novel tiptap','npm install novel'],
    'Nextjs_Structure.md': ['DocuSign','docusign','@google/generative','lib/gemini','12b','scheduled-publish','novel tiptap'],
    'Product_Spec_V1.md': ['DocuSign','docusign','Internal Review','Submission Closed','Award Recommended','Not Started','Shortlisted','Not Selected','\[1\]','\[web:'],
    'AUTH_FLOWS.md': ['/register ->', 'Routes.*register'],
    'BUILD_LOG.md': [],
}

for fname, patterns in files.items():
    fpath = base / fname
    if not fpath.exists():
        print(f'MISSING: {fname}')
        continue
    text = fpath.read_text()
    print(f'\n=== {fname} ({len(text)} chars) ===')
    if not patterns:
        print(f'  (no patterns to check; first 200 chars: {repr(text[:200])})')
        continue
    for p in patterns:
        matches = [(m.start(), text[max(0,m.start()-30):m.start()+60].replace(chr(10),' ')) for m in re.finditer(p, text)]
        if matches:
            print(f'  FOUND [{p}]: {len(matches)} hit(s)')
            print(f'    first: ...{matches[0][1]}...')
        else:
            print(f'  not found: {p}')
