from pathlib import Path

base = Path('/Users/drscottkelly/Dropbox (Personal)/Python/ESG_Procurement/Instructions')

# =============================================================================
# DATABASE_SCHEMA.MD
# =============================================================================
db_file = base / 'Database_Schema.md'
db_text = db_file.read_text()

# --- FIX 1: Add supplier_tender_unlocks table ---
if 'supplier_tender_unlocks' not in db_text:
    unlock_table = """
### `supplier_tender_unlocks` (Pay-to-access public tender tracking)
*Tracks which supplier organisations have paid to unlock a public tender's documents and submission flow.
RLS on `tender_documents` storage bucket must check for a matching row here before serving files to uninvited suppliers.*
- `id` (uuid, primary key, default: gen_random_uuid())
- `tender_id` (uuid, not null, references tenders, on delete cascade)
- `supplier_org_id` (uuid, not null, references organizations)
- `stripe_payment_intent_id` (text, not null) — Stripe PaymentIntent ID for idempotency checks
- `amount_paid` (numeric, not null) — should always equal the platform unlock fee at time of payment
- `currency` (text, default: 'GBP')
- `unlocked_at` (timestamptz, default: now())
- Unique constraint: (`tender_id`, `supplier_org_id`) — a supplier can only unlock a tender once
"""
    db_text = db_text.replace(
        "---\n\n## 4. Files & Attachments",
        unlock_table + "\n---\n\n## 4. Files & Attachments"
    )

# --- FIX 2 & 8: Update organizations table with lead_profile_id, terms fields ---
org_old = "- `stripe_customer_id` (text)\n- `terms_accepted_at` (timestamptz) \u2014 records when the organization agreed to platform T&Cs"
org_new = """- `stripe_customer_id` (text)
- `lead_profile_id` (uuid, nullable, references profiles) \u2014 the designated organisational lead. Only this person can agree to T&Cs and submit tenders. If the lead changes, terms must be re-accepted.
- `terms_accepted_at` (timestamptz) \u2014 when the current lead accepted the platform T&Cs
- `terms_accepted_by` (uuid, nullable, references profiles) \u2014 the profile_id of the lead who accepted"""
db_text = db_text.replace(org_old, org_new)

# --- FIX 2 & 8: Update profiles table to include is_org_lead ---
if '`is_org_lead`' not in db_text:
    profile_old = "- `created_at` (timestamptz, default: now())\n\n**Role permissions matrix:**"
    profile_new = """- `is_org_lead` (boolean, default: false) \u2014 true for the designated lead of the supplier organisation. Only one lead per organisation is allowed.
- `created_at` (timestamptz, default: now())

**Role permissions matrix:**"""
    db_text = db_text.replace(profile_old, profile_new)

# --- FIX 3: Add public_listing_stripe_payment_id to tenders ---
if 'public_listing_stripe_payment_id' not in db_text:
    fee_old = "- `public_listing_fee_paid` (boolean, default: false) \u2014 true if buyer paid \u00a3200 to open to marketplace"
    fee_new = """- `public_listing_fee_paid` (boolean, default: false) \u2014 true if buyer paid \u00a3200 to open to marketplace
- `public_listing_stripe_payment_id` (text) \u2014 Stripe PaymentIntent ID for the \u00a3200 listing fee; used for idempotency and dispute resolution"""
    db_text = db_text.replace(fee_old, fee_new)

# --- FIX 2: Add free invite cap note to tenders ---
if 'free_invite_cap' not in db_text:
    cap_old = "- `qa_deadline` (timestamptz) \u2014 deadline for suppliers to ask questions"
    cap_new = """- `qa_deadline` (timestamptz) \u2014 deadline for suppliers to ask questions
- `private_invite_count` (integer, default: 0) \u2014 server-managed count of invitations sent. Free tier is capped at 3. Incremented on each `tender_invitations` insert."""
    db_text = db_text.replace(cap_old, cap_new)

# --- FIX 4: Add missing audit log action values ---
audit_old = "  `'TENDER_AWARDED'` | `'EMAIL_SENT'` | `'USER_ADDED'`"
audit_new = """  `'TENDER_AWARDED'` | `'TENDER_WITHDRAWN'` | `'EMAIL_SENT'` | `'USER_ADDED'`
  `'SUBMISSION_DECLINED'` | `'SUBMISSION_RETRACTED'` | `'INTENT_TO_BID'`
  `'FEE_INVOICED'` | `'FEE_PAID'` | `'TENDER_UNLOCKED'`"""
db_text = db_text.replace(audit_old, audit_new)

# --- FIX 5: Add submission status transition rules to constraints ---
if 'Submission Status Transitions' not in db_text:
    constraints_old = "1. `tenders.status` must always use the 9-value enum above."
    constraints_new = """1. `tenders.status` must always use the 9-value enum above. Includes 'Withdrawn'. (Note: 'Submission Closed' is not a tender status; closure is computed dynamically via `submission_deadline`, or status moves directly to 'Evaluation' when scoring begins). Never add new status values without updating this file.

**Submission Status Transitions:** Suppliers are free to move their submission between `'Draft'`, `'Declined'`, and `'Submitted'` states at any time BEFORE the `submission_deadline` has passed AND BEFORE the buyer has moved the tender to `'Evaluation'`. Once either condition is true, no further status changes by the supplier are permitted. The only exception is `platform_admin`. There is no enforced ordering of transitions during the open window."""
    db_text = db_text.replace(constraints_old, constraints_new)

# --- FIX 6: Add qa_deadline enforcement rule ---
if 'qa_deadline enforcement' not in db_text:
    db_text = db_text.replace(
        "9. `submission_answers.question_id` maps to",
        "9. **qa_deadline enforcement:** The server action for creating a `tender_clarifications` row must check `now() < tenders.qa_deadline` before inserting. If the Q&A deadline has passed, return a 400 error and do not insert.\n\n9. `submission_answers.question_id` maps to"
    )

# --- FIX 7: Add Q&A broadcast comms rule ---
if 'Q&A broadcast' not in db_text:
    db_text = db_text.replace(
        "11. Email composition supports rich HTML",
        "11. **Q&A broadcast:** When a buyer sets `tender_clarifications.is_public = true` (publishing an answer to all bidders), the server action MUST also create one canonical `tender_messages` record (channel: 'Email') and fan out a `communications_log` email to all organisations with active submissions on that tender, consistent with Rule 10.\n\n11. Email composition supports rich HTML"
    )

# --- FIX 9: Update constraints rule count and add unlock rule ---
if '15. **Free Tier Invite Cap:**' not in db_text:
    db_text += """
15. **Free Tier Invite Cap:** `tenders.private_invite_count` must be checked server-side before inserting into `tender_invitations`. If `private_invite_count >= 3` and `tenders.public_listing_fee_paid = false`, return a 403 error explaining the free tier cap.
16. **Org Lead Constraint:** Only one `profiles` row per `organization_id` may have `is_org_lead = true`. Enforce via a partial unique index: `CREATE UNIQUE INDEX one_lead_per_org ON profiles (organization_id) WHERE is_org_lead = true`.
17. **Lead T&C Re-acceptance:** When `organizations.lead_profile_id` is updated to a new profile, the server action must reset `terms_accepted_at = null` and `terms_accepted_by = null`. The new lead will be prompted to re-accept T&Cs on their next login before any further platform actions.
18. **Submission Auth:** Only the supplier org lead (`is_org_lead = true`) can click the final Submit button for a tender and agree to the 5% success fee checkbox. Other `supplier_editor` roles can edit the draft but not submit.
"""

# --- FIX 9: Update ERD to include supplier_tender_unlocks ---
erd_old = "    organizations ||--o{ audit_logs : belongs_to"
erd_new = """    organizations ||--o{ audit_logs : belongs_to
    organizations ||--o{ supplier_tender_unlocks : purchases
    tenders ||--o{ supplier_tender_unlocks : unlocked_by"""
db_text = db_text.replace(erd_old, erd_new)

db_file.write_text(db_text)


# =============================================================================
# PRODUCT_SPEC_V1.MD
# =============================================================================
spec_file = base / 'Product_Spec_V1.md'
spec_text = spec_file.read_text()

lead_spec = """
## Supplier Organisation Lead Role
Every supplier organisation has one designated Lead. The Lead is the only person who can:
1. Accept the platform Terms and Conditions on behalf of the organisation.
2. Click the final Submit button on a tender submission (agreeing to the 5% success fee).
3. Any registered user in the organisation can download documents and edit the draft submission.
4. If the Lead changes (updated in org settings), the new Lead must re-accept T&Cs before any further platform actions are permitted.

For a buyer-side organisation, the equivalent constraint is `buyer_admin` — only a `buyer_admin` can Publish a tender, Award a contract, or Withdraw a tender.
"""
if '## Supplier Organisation Lead Role' not in spec_text:
    spec_text += lead_spec
    spec_file.write_text(spec_text)


# =============================================================================
# USERSTORIES.MD
# =============================================================================
stories_file = base / 'UserStories.md'
stories_text = stories_file.read_text()

lead_stories = """
### Supplier Lead Role & T&Cs
- As the org lead of a supplier, I must accept the Terms and Conditions before my organisation can interact with any tender on the platform.
- As the org lead, I am the only person who can click the final Submit button on a tender submission.
- As a supplier org admin, I can reassign the lead role to another team member, at which point the new lead will be required to re-accept T&Cs.
- As a supplier, I can freely switch my submission between Draft, Intent to Bid, and Declined at any point before the deadline or before the buyer closes scoring.

### Free Tier and Unlock Flow
- As a buyer on the free tier, I can invite up to 3 suppliers privately before being prompted to pay the £200 public listing fee.
- As an uninvited supplier, when I try to download tender documents I am prompted to pay the platform unlock fee via Stripe before the documents are served.
"""
if '### Supplier Lead Role & T&Cs' not in stories_text:
    stories_text += lead_stories
    stories_file.write_text(stories_text)


# =============================================================================
# AGENTS.MD
# =============================================================================
agents_file = base / 'AGENTS.MD'
agents_text = agents_file.read_text()

agents_notes = """
## Supplier Lead & T&C Rules
- Only one `profiles` row per organisation may have `is_org_lead = true`. Enforce via partial unique index.
- Only the org lead can submit tenders and agree to the 5% fee checkbox. Do not allow `supplier_editor` or `supplier_viewer` to hit the final submit action.
- If `lead_profile_id` changes on an `organizations` row, always reset `terms_accepted_at` and `terms_accepted_by` to null in the same transaction.
- The `supplier_tender_unlocks` table is the RLS gate for uninvited suppliers accessing `tender_documents` storage bucket. Check for a matching row before serving files.
- Never cap supplier submission status transitions server-side unless `now() > submission_deadline` OR `tenders.status = 'Evaluation'`.
"""
if '## Supplier Lead & T&C Rules' not in agents_text:
    agents_text += agents_notes
    agents_file.write_text(agents_text)

print('FIXED: All 9 issues applied across Database_Schema.md, Product_Spec_V1.md, UserStories.md, AGENTS.MD')
