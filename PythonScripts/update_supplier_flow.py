from pathlib import Path

base = Path('/Users/drscottkelly/Dropbox (Personal)/Python/ESG_Procurement/Instructions')

# --- 1. Database_Schema.md ---
db_file = base / 'Database_Schema.md'
db_text = db_file.read_text()

sub_old = """- `status` (text, not null) — use ONLY these exact values:
  `'Draft'` | `'Submitted'` | `'Under Review'` | `'Disqualified'` | `'Shortlisted'` | `'Not Selected'` | `'Selected'`"""
sub_new = """- `status` (text, not null) — use ONLY these exact values:
  `'Draft'` | `'Declined'` | `'Submitted'` | `'Under Review'` | `'Disqualified'` | `'Shortlisted'` | `'Not Selected'` | `'Selected'`"""
db_text = db_text.replace(sub_old, sub_new)

sub_fields_old = "- `submission_pdf_url` (text) — generated PDF of structured form answers for download and audit"
sub_fields_new = """- `submission_pdf_url` (text) — generated PDF of structured form answers for download and audit
- `agreed_to_success_fee` (boolean, default: false) — supplier checked the mandatory 5% fee box at submission
- `success_fee_agreed_at` (timestamptz) — timestamp of when the fee was agreed"""
db_text = db_text.replace(sub_fields_old, sub_fields_new)

rule_old = "2. `supplier_submissions.status` must always use the 7-value enum above."
rule_new = "2. `supplier_submissions.status` must always use the 8-value enum above. Includes 'Declined'."
db_text = db_text.replace(rule_old, rule_new)

if 'Anti-Fraud Rule:' not in db_text:
    db_text += "\n14. **Anti-Fraud Rule:** When a buyer awards a tender, the `final_contract_value` cannot be set lower than 90% of the winning submission's `total_bid_amount` without platform admin intervention, to prevent fee evasion.\n"

db_file.write_text(db_text)

# --- 2. Product_Spec_V1.md ---
spec_file = base / 'Product_Spec_V1.md'
spec_text = spec_file.read_text()

supplier_refinements = """
## Supplier Journey & Workflow Refinements
- **The Registration Wall:** Public tenders show a rich summary, but downloading the RFP documents requires a supplier to register or log in. This tracks exactly which organizations download the documents for the buyer.
- **Intent to Bid vs. Decline:** After reviewing documents, suppliers must click "Intend to Bid" (creates a `Draft` submission) or "Decline" (updates status to `Declined`). This gives buyers early visibility into pipeline health.
- **Collaboration & ESG Reuse:** Submissions are shared organization drafts. Any user in the supplier org can edit the draft. During the guided workflow, suppliers can pull existing ISO certificates and ESG policies from their `master_compliance_data` profile instead of re-uploading them.
- **Retract & Edit:** Before the `submission_deadline`, suppliers can click "Retract" on a submitted proposal. This reverts the status to `'Draft'` so they can fix errors and resubmit.
- **Binding the 5% Fee:** At the final review step before clicking Submit, the supplier MUST check a box explicitly agreeing to the 5% success fee on the final contract value.
- **Anti-Fraud Deviation Guardrail:** To prevent a buyer and supplier from colluding to log a fake low contract value (e.g., £10k instead of £100k to avoid fees), the system enforces that the `final_contract_value` inputted at Award cannot be less than 90% of the supplier's original `total_bid_amount`. (A >10% deviation requires a platform admin to manually override).
"""
if '## Supplier Journey & Workflow Refinements' not in spec_text:
    spec_text += "\n" + supplier_refinements
    spec_file.write_text(spec_text)

# --- 3. UserStories.md ---
stories_file = base / 'UserStories.md'
stories_text = stories_file.read_text()

supplier_stories = """
### Supplier Experience & Anti-Fraud
- As a supplier viewing a public tender, I must register an account to download the RFP documents, so the buyer knows my company is reviewing it.
- As a supplier, I want to click "Decline" so the buyer knows I am passing, or "Intend to Bid" to start a collaborative draft with my team.
- As a supplier, I want to pull my company's standard ESG and ISO policies directly from my profile into the submission, so I save time on repetitive uploads.
- As a supplier, I want to be able to retract my submission before the deadline, so I can fix a pricing error and resubmit.
- As a supplier, I must explicitly check a box agreeing to the 5% success fee during the final submission review, so the platform has a binding legal record.
- As an administrator, I want the system to block buyers from entering a final contract value that is less than 90% of the bid amount, so users cannot collude to evade the platform fee.
"""
if '### Supplier Experience & Anti-Fraud' not in stories_text:
    stories_text += "\n" + supplier_stories
    stories_file.write_text(stories_text)

print('UPDATED: Applied Supplier Reg-Wall, Intent to Bid, Retract, and 10% Anti-Fraud rule.')
