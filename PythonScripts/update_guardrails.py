from pathlib import Path

base = Path('/Users/drscottkelly/Dropbox (Personal)/Python/ESG_Procurement/Instructions')

# --- 1. Database_Schema.md ---
schema_file = base / 'Database_Schema.md'
text = schema_file.read_text()

old_status = "`'Draft'` | `'Internal Review'` | `'Private Invite'` | `'Published'` | `'Submission Closed'` | `'Evaluation'` | `'Award Recommended'` | `'Awarded'` | `'Archived'`"
new_status = "`'Draft'` | `'Internal Review'` | `'Private Invite'` | `'Published'` | `'Evaluation'` | `'Award Recommended'` | `'Awarded'` | `'Archived'`"
text = text.replace(old_status, new_status)

old_rule = "1. `tenders.status` must always use the 9-value enum above."
new_rule = "1. `tenders.status` must always use the 8-value enum above. (Note: 'Submission Closed' is not a tender status; closure is computed dynamically via `submission_deadline`, or status moves directly to 'Evaluation' when scoring begins)."
text = text.replace(old_rule, new_rule)

storage_rules = """
12. **Storage Buckets:** Gemini must create two distinct private Supabase Storage buckets: `tender_documents` and `submission_documents`.
13. **Bucket RLS:** `tender_documents` are readable by anyone if the tender is public, or invited users if private. `submission_documents` are strictly locked via RLS so only the submitting supplier organization and the buyer organization can read them. Never mix these files in the same bucket.
"""
if "12. **Storage Buckets:**" not in text:
    text += storage_rules
schema_file.write_text(text)


# --- 2. Product_Spec_V1.md ---
spec_file = base / 'Product_Spec_V1.md'
text = spec_file.read_text()

trigger_rule = """
## Scoring and Evaluation trigger
The AI evaluation does NOT run automatically when a supplier submits a bid. To prevent bias and control costs, the buyer must manually click a "Close and Score Tenders" button on the tender workspace. 
When this is clicked:
1. The tender `status` changes from `'Published'` (or `'Private Invite'`) to `'Evaluation'`.
2. No further supplier submissions are accepted.
3. The platform queues the AI scoring jobs for all submitted bids simultaneously.
"""
if '## Scoring and Evaluation trigger' not in text:
    text += trigger_rule

onboarding_rule = """
## Supplier Onboarding and Access
When a supplier signs up via an email invitation, the `invite_token` must be passed through the Supabase Auth flow to automatically bind the new user to the correct `organizations` row and link them to the tender. 
If a supplier signs up organically (without an invite link), the onboarding flow must ask: "Are you responding to an existing tender?" If yes, they are prompted to enter the unique code for that tender. This ensures they are granted access even if the tender was created under the `'Private Invite'` status.
"""
if '## Supplier Onboarding and Access' not in text:
    text += onboarding_rule

spec_file.write_text(text)


# --- 3. UserStories.md ---
stories_file = base / 'UserStories.md'
text = stories_file.read_text()

trigger_story = """
### Evaluation and Scoring trigger
- As a buyer, I want to manually click "Close and Score Tenders" after the deadline passes, so that I can evaluate all submissions fairly at the same time without seeing early scores.
- As a buyer, I want the tender status to move to "Evaluation" when I trigger scoring, so suppliers know no further edits are permitted.

### Supplier Access and Registration
- As an invited supplier, I want my invite link to seamlessly add me to my company's existing organization profile during sign-up, so I don't accidentally create a duplicate company.
- As an uninvited supplier registering on the platform, I want to be able to enter a unique tender code during sign-up, so I can gain access to a private tender I was told about offline.
"""
if '### Evaluation and Scoring trigger' not in text:
    text += trigger_story
    stories_file.write_text(text)


# --- 4. AGENTS.MD ---
agents_file = base / 'AGENTS.MD'
text = agents_file.read_text()

agents_storage = """
## Storage and Security Guardrails
- **Two distinct Supabase Storage buckets are mandatory:** `tender_documents` (buyer files) and `submission_documents` (supplier files). 
- `submission_documents` must have strict RLS preventing lateral access between competing suppliers.
- Do not automate the AI evaluation upon submission; it must only fire when the buyer clicks "Close and Score Tenders".
- Invitation tokens must be preserved through the auth flow to bind users to the correct organization.
"""
if '- **Two distinct Supabase Storage buckets are mandatory:**' not in text:
    insert_point = "---\n\n## Definition of Done"
    if insert_point in text:
        text = text.replace(insert_point, agents_storage + "\n" + insert_point)
    agents_file.write_text(text)

print('UPDATED: Resolved Storage, Scoring Trigger, Status, and Onboarding constraints.')
