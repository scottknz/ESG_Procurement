from pathlib import Path

base = Path('/Users/drscottkelly/Dropbox (Personal)/Python/ESG_Procurement/Instructions')

# --- AGENTS.MD ---
agents = base / 'AGENTS.MD'
text = agents.read_text()
core_old = "- Clarification / Q&A\n- Invitation\n- Communication log\n- Audit log\n- AI analysis result"
core_new = "- Clarification / Q&A\n- Invitation\n- Tender message\n- Tender message recipient group\n- Tender message attachment\n- Communication log\n- Submission review label\n- Buyer internal tender note\n- Audit log\n- AI analysis result"
if core_old in text:
    text = text.replace(core_old, core_new)
if '## Tender workspace and communications' not in text:
    insert_after = "---\n\n## Definition of Done\n"
    section = "---\n\n## Tender workspace and communications\n\n- Every tender must have a dedicated workspace page for the buyer organization and the supplier organization.\n- The tender workspace must show, at minimum: tender title, tender summary, submission deadline, countdown to close, communication history, and files relevant to that tender.\n- The buyer tender workspace must also show a submissions table, buyer internal notes, and quick submission triage labels.\n- Submission triage labels are tender-specific and buyer-editable; default examples are `Consider`, `Reject`, and `Follow Up`.\n- Buyers must be able to click a submission, inspect the structured response, download uploaded proposal files, and download a generated PDF of form-based answers.\n- Internal tender communication between buyer and supplier organizations must be stored as canonical in-app `tender_messages`.\n- When the platform sends an email about a tender, it must also create one canonical in-app `tender_messages` record so the tender workspace shows the full communication history in one place.\n- Outbound tender emails may be drafted with To/CC fields, HTML formatting, and attachments, but actual delivery audit must be stored per recipient in `communications_log`.\n- Email fan-out must send to all registered users in the addressed buyer or supplier organization groups when `include_all_registered_users` is enabled.\n- Draft messages must be savable before send; sending, failure, and delivery state must be traceable.\n\n"
    if insert_after in text:
        text = text.replace(insert_after, section + insert_after)
    else:
        text += "\n\n" + section
agents.write_text(text)

# --- Product_Spec_V1.md ---
product = base / 'Product_Spec_V1.md'
text = product.read_text()
if '## Tender workspace and communications alignment' not in text:
    text += "\n\n## Tender workspace and communications alignment\n\nThe tender detail experience should become a persistent tender workspace for each participating organization, not just a static detail screen. For buyers, this workspace should show the tender title, summary, current status, submission deadline, countdown timer, attachments, clarifications, buyer-only internal notes, a communication timeline, and a submissions table with quick triage labels such as `Consider`, `Reject`, and `Follow Up`.\n\nSuppliers should see the same tender context that is relevant to them, including title, summary, deadline, clarifications, downloadable files, submission status, and the shared communication timeline. If a message concerns one specific submission, the platform should be able to associate that message with the related submission while still keeping it visible in the tender-level history.\n\nThe communication model must support both simple in-app tender messaging and formal email composition. Internal messages can be lightweight, but outbound email drafting should support To, CC, subject, attachments, rich HTML body content, and a plain-text fallback. When an email is sent from the platform, the system should fan delivery out to all registered users in the addressed buyer and supplier organizations, while preserving one canonical in-app message record and separate delivery-audit records per recipient.\n\nSubmission review in V1 should include a fast buyer workflow for screening responses before and during evaluation. Buyers should be able to open a submission, review the structured answer set, download the uploaded proposal package, download a generated PDF of form-based responses, apply a tender-specific review label, and record short buyer notes at the tender level.\n"
product.write_text(text)

# --- UserStories.md ---
stories = base / 'UserStories.md'
text = stories.read_text()
if '## Additional user stories: tender workspace and messaging' not in text:
    text += "\n\n## Additional user stories: tender workspace and messaging\n\n### Buyer tender workspace\n- As a buyer, I want each tender to open into a workspace that shows the title, summary, status, deadline, and countdown so I can manage the tender from one place.\n- As a buyer, I want to see a submissions table on the tender workspace so I can quickly monitor response volume and status.\n- As a buyer, I want to add short internal notes to the tender so my team can retain important context that is not visible to suppliers.\n\n### Submission triage\n- As a buyer, I want a quick dropdown label such as `Consider`, `Reject`, or `Follow Up` on each submission so I can triage responses before full evaluation.\n- As a buyer, I want those triage labels to be editable per tender so each procurement process can use its own workflow language.\n- As a buyer, I want to open a submission and download both uploaded files and a generated PDF of structured answers so I can review complete submissions offline.\n\n### Tender messaging\n- As a buyer or supplier, I want to exchange in-app messages tied to a specific tender so all relevant communication stays attached to that procurement record.\n- As a buyer, I want to draft an outbound email with To, CC, subject, attachments, and rich formatting so I can send polished communications from inside the platform.\n- As a buyer, I want the platform to send that email to all registered users in the selected buyer and supplier organizations so nobody misses important tender communications.\n- As a buyer or supplier, I want every outbound email to appear in the in-app tender communication history so the platform preserves one complete trace of communication.\n- As an administrator, I want delivery outcomes recorded per recipient so I can audit who was contacted and whether the email was sent successfully.\n"
stories.write_text(text)

# --- Nextjs_Structure.md ---
structure = base / 'Nextjs_Structure.md'
text = structure.read_text()
if '## Alignment update: tender workspace, review labels, and messaging' not in text:
    text += "\n\n## Alignment update: tender workspace, review labels, and messaging\n\nThe application structure must include a dedicated tender workspace route for both buyer and supplier contexts. The buyer route should support a tender overview, submissions table, submission detail drawer or page, internal notes panel, communications timeline, and message-composer UI.\n\nMinimum route coverage should include buyer tender workspace pages, supplier tender workspace pages, and submission detail pages nested under the tender context. The buyer workspace should expose actions for updating tender notes, applying submission review labels, opening a message draft, attaching files, and sending or saving a draft.\n\nServer-side modules should include one service for canonical tender message creation, one service for email fan-out and per-recipient `communications_log` writes, one helper for generating submission PDFs from structured answers, and one helper for tender countdown/status derivation. Keep message composition UI separate from message delivery logic so draft, preview, send, and retry paths remain easy to test.\n"
structure.write_text(text)

# --- Tech_Stack.md ---
tech = base / 'Tech_Stack.md'
text = tech.read_text()
if '## Alignment update: messaging and tender workspace requirements' not in text:
    text += "\n\n## Alignment update: messaging and tender workspace requirements\n\nThe approved stack already supports the new requirements: Supabase/PostgreSQL for canonical tender messages, recipient groups, attachments metadata, review labels, buyer notes, and per-recipient communication audit; Resend for outbound email delivery; and Next.js server actions or route handlers for draft-save, send, retry, and submission-PDF generation flows.\n\nMessage drafting must support both `body_text` and `body_html`. If a richer editor is introduced later, it must remain compatible with server-side sanitization, safe HTML storage, and plain-text fallback generation. Do not add a rich-text dependency unless it is justified, secure, and documented in this file first.\n\nThe implementation should treat email as a delivery channel layered on top of canonical in-app tender messages. That means the database record for a tender conversation remains the source of truth, while the mail provider only handles transport and delivery status.\n"
tech.write_text(text)

print('UPDATED: AGENTS.MD, Product_Spec_V1.md, UserStories.md, Nextjs_Structure.md, Tech_Stack.md')
