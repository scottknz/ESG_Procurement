from pathlib import Path

base = Path('/Users/drscottkelly/Dropbox (Personal)/Python/ESG_Procurement/Instructions')

# --- 1. Database_Schema.md ---
db_file = base / 'Database_Schema.md'
db_text = db_file.read_text()

# Update Organizations
org_old = """- `master_compliance_data` (jsonb) — supplier-only: reusable certs, ISO docs, standard policy uploads
- `created_at` (timestamptz, default: now())"""
org_new = """- `master_compliance_data` (jsonb) — supplier-only: reusable certs, ISO docs, standard policy uploads
- `stripe_customer_id` (text)
- `terms_accepted_at` (timestamptz) — records when the organization agreed to platform T&Cs
- `created_at` (timestamptz, default: now())"""
db_text = db_text.replace(org_old, org_new)

# Update Tenders - Status & Visiblity & QA
tender_old = """- `status` (text, not null) — use ONLY these exact values:
  `'Draft'` | `'Internal Review'` | `'Private Invite'` | `'Published'` | `'Evaluation'` | `'Award Recommended'` | `'Awarded'` | `'Archived'`
- `submission_deadline` (timestamptz, not null before publication)"""
tender_new = """- `status` (text, not null) — use ONLY these exact values:
  `'Draft'` | `'Internal Review'` | `'Private Invite'` | `'Published'` | `'Evaluation'` | `'Award Recommended'` | `'Awarded'` | `'Withdrawn'` | `'Archived'`
- `visibility` (text, default: `'Private'`) — `'Private'` | `'Public'`
- `public_listing_fee_paid` (boolean, default: false) — true if buyer paid £200 to open to marketplace
- `submission_deadline` (timestamptz, not null before publication)
- `qa_deadline` (timestamptz) — deadline for suppliers to ask questions"""
db_text = db_text.replace(tender_old, tender_new)

# Update Tenders - Award fees
award_old = """- `awarded_at` (timestamptz)"""
award_new = """- `awarded_at` (timestamptz)
- `final_contract_value` (numeric) — confirmed by buyer upon award
- `success_fee_status` (text) — `'Pending'` | `'Invoiced'` | `'Paid'`
- `success_fee_invoice_url` (text) — link to 5% supplier invoice via Stripe"""
db_text = db_text.replace(award_old, award_new)

# Update Rule 1
rule_old = "1. `tenders.status` must always use the 8-value enum above."
rule_new = "1. `tenders.status` must always use the 9-value enum above. Includes 'Withdrawn'."
db_text = db_text.replace(rule_old, rule_new)

db_file.write_text(db_text)

# --- 2. Product_Spec_V1.md ---
spec_file = base / 'Product_Spec_V1.md'
spec_text = spec_file.read_text()

business_logic = """
## Monetization & Marketplace Model
The platform uses a freemium SaaS + marketplace model:
- **Private Free Tier:** Buyers can draft a tender and invite up to 3 suppliers privately for free.
- **Public Marketplace (£200 Fee):** If a buyer wants to reach the entire supplier network, they pay a flat £200 fee via Stripe. The tender `visibility` becomes `'Public'` and appears on the storefront.
- **Supplier Access:** Any supplier can view, download, and bid on public tenders for free.
- **Success Fee (5%):** When a contract is awarded, the winning supplier is invoiced a 5% success fee based on the final contract value.
- **Anti-Disintermediation (The Audit Moat):** To prevent parties from taking the deal offline to avoid the 5% fee, the platform's core value—the cryptographically verifiable Audit Report PDF—is strictly locked. It is ONLY generated and made accessible to the buyer's compliance team *after* the buyer formally confirms the `final_contract_value` and clicks "Award", triggering the Stripe invoice to the supplier.

## Q&A, Withdrawals, and Archiving
- **Q&A vs Direct Messages:** Tenders have a `qa_deadline`. Clarifications asked by suppliers can be broadcast anonymously to all bidders. This is distinct from private 1:1 `tender_messages`.
- **Withdrawals:** A buyer can click "Withdraw Tender" if a project is cancelled. This sets the status to `'Withdrawn'` and automatically emails active suppliers. Public listing fees are non-refundable.
- **Historical Archive:** The buyer dashboard includes a Historical Archive view showing all past tenders, their final statuses, the winning supplier, final contract value, and a download link to the Audit PDF.
"""
if '## Monetization & Marketplace Model' not in spec_text:
    spec_text += "\n" + business_logic
    spec_file.write_text(spec_text)

# --- 3. UserStories.md ---
stories_file = base / 'UserStories.md'
stories_text = stories_file.read_text()

new_stories = """
### Monetization and T&Cs
- As a newly registered user, I must accept the Terms and Conditions so the platform can legally enforce the 5% success fee.
- As a buyer, I want to invite up to 3 suppliers to my private tender for free.
- As a buyer, I want to pay a £200 flat fee via Stripe to publish my tender to the public marketplace to maximize my supplier responses.
- As a supplier, I want to view and bid on public tenders for free, so there is no friction in submitting my proposal.
- As a buyer awarding a contract, I want to confirm the final negotiated contract value so the system records the accurate amount.
- As a supplier who just won a tender, I want to receive an automated Stripe invoice for the 5% success fee.

### Q&A and Withdrawals
- As a buyer, I want to set a Q&A deadline separate from the submission deadline.
- As a buyer, I want to broadcast a clarification answer to all suppliers anonymously, so everyone gets the same information.
- As a buyer, I want to withdraw a tender if my project is cancelled, and automatically notify all suppliers who were working on it.
- As a buyer, I want a Historical Archive on my dashboard so my compliance team can audit all past awards, withdrawals, and PDF reports.
"""
if '### Monetization and T&Cs' not in stories_text:
    stories_text += "\n" + new_stories
    stories_file.write_text(stories_text)

# --- 4. Tech_Stack.md ---
tech_file = base / 'Tech_Stack.md'
tech_text = tech_file.read_text()
if '- Stripe (for £200' not in tech_text:
    tech_text = tech_text.replace("- Supabase\n- PostgreSQL", "- Supabase\n- PostgreSQL\n- Stripe (for £200 buyer public listing fees and 5% supplier success fee invoicing)")
    tech_file.write_text(tech_text)

# --- 5. AGENTS.MD ---
agents_file = base / 'AGENTS.MD'
agents_text = agents_file.read_text()

env_old = """- `NEXT_PUBLIC_APP_URL`
- `SUPABASE_PROJECT_ID`"""
env_new = """- `NEXT_PUBLIC_APP_URL`
- `SUPABASE_PROJECT_ID`
- `STRIPE_SECRET_KEY`
- `STRIPE_WEBHOOK_SECRET`
- `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`"""
agents_text = agents_text.replace(env_old, env_new)

guardrail_old = "- Invitation tokens must be preserved through the auth flow to bind users to the correct organization."
guardrail_new = """- Invitation tokens must be preserved through the auth flow to bind users to the correct organization.
- **Audit Report Moat:** To prevent disintermediation, the final cryptographic Audit Report PDF MUST NOT be generated or accessible until the buyer formally confirms the `final_contract_value` and clicks "Award", which triggers the 5% Stripe invoice to the supplier."""
agents_text = agents_text.replace(guardrail_old, guardrail_new)

agents_file.write_text(agents_text)

print('UPDATED: Applied Monetization, Stripe, Free Tier, and Withdrawn logic.')
