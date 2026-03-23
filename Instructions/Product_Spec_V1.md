# ESG Procurement Platform - Product Specification V1
> **Status:** Active | **Last updated:** March 2026
> All citations and external links have been removed from this file.

Below is a clean V1 product spec for the buyer-first tender platform you described, centered on guided RFP drafting, private-to-public tender management, supplier uploads, and explainable scoring.

## Product scope

V1 should cover one complete procurement workflow: define the need, draft the RFP, manage the tender, collect supplier responses, score them, and produce a defendable shortlist decision.  That matches how modern procurement platforms create value: centralized intake, visible workflow states, structured evaluation, and audit-ready decisions.

The platform starts on the buyer side with a free guided drafting tool, then gives the buyer the option to keep the tender private, invite selected suppliers, or publish it more broadly when ready.  AI should support both stages: first by improving the quality of the RFP, and later by mapping supplier responses to requirements and explaining scores against buyer-defined criteria.

## Core screens

- **Buyer landing page (The "Greenhouse" Storefront):** A clean, branded public-facing portal for each buyer organization (e.g., `procurement.yourcompany.com`). It displays a header banner, logo, links to the company's master legal/compliance rules, and a simple, filterable list of open public tenders. 
- **Public Tender Detail Page:** Accessed from the storefront. Shows the AI-generated plain-English summary, submission deadline, key dates, and a clear "Download Tender Documents" section that supports downloading multiple attachments (RFPs, pricing matrices, NDAs) individually or as a bulk ZIP file. 
- **Authentication screen:** Supports sign-up, sign-in, passwordless reset, and organization creation, because procurement workflows need role-based access and traceability from day one.
- **Buyer dashboard:** Shows tenders by status, upcoming deadlines, supplier counts, and scoring progress, because requesters need status visibility and procurement teams need shared oversight.
- **Template Library:** Allows buyers to choose from system-default regulatory templates (e.g., CSRD, Scope 1-3) or create and save their own custom templates for future use. AI dynamically adapts chosen templates based on the specific regulatory footprint of the buyer.
- **New tender / template selection:** Lets the buyer choose the RFP type and starting template, while keeping the form guided rather than overwhelming.
- **RFP questionnaire wizard:** Multi-step guided form where the buyer enters goals, scope, timeline, compliance needs, budget, and evaluation priorities, and the agent asks follow-up questions to fill gaps.
- **RFP editor / preview:** Converts questionnaire answers into a structured on-screen RFP with editable sections and a clean review layout before publication.
- **PDF export screen:** Produces a formal downloadable version of the RFP, because procurement still depends on structured, shareable documents.
- **Tender settings screen:** Lets buyers set privacy, invited suppliers, dates, submission instructions, and response format, because tender preparation requires agreement on scope, deadlines, and evaluation rules before publication.
- **Supplier submission screen:** Allows suppliers to upload proposal documents and key metadata, with confirmation of receipt and submission status.
- **Evaluation design screen:** Lets buyers define weighted criteria, pass/fail thresholds, floors, ceilings, and disqualification logic.
- **Comparison workspace:** Shows side-by-side supplier submissions, AI-generated compliance mapping, scoring, and narrative reasoning linked to criteria.
- **Decision screen:** Presents the recommended winner, reasons, disqualifications, reviewer notes, and final sign-off trail.
- **Admin / audit screen:** Shows user activity, changes, score overrides, uploads, and timeline events, because explainable AI and procurement governance require complete audit trails.


## Conversational AI Wizard & RFP Generation
The platform shifts from a static form builder to an AI-led interview process:
1. **The Interview:** The buyer starts a chat session (`tender_wizard_sessions`). The AI asks questions based on the buyer's industry, budget, and the `interview_questions` defined in applicable `regulations`.
2. **Dual Generation:** Once the AI has enough context, it generates *two* separate outputs:
   - **The Form:** A structured JSON config saved to `tender_submission_config.custom_questions` (the exact fields the supplier must fill in).
   - **The RFP Document:** A rich-text draft explaining the background, rules, and scope, saved to `tenders.rfp_document_draft`.
3. **Buyer Review & Edit:** The buyer reviews the dynamic submission form (branded with their logo and banner from `public_portal_config`). They then edit the draft RFP document in a Notion-style rich-text editor (Novel). In this editor, the buyer can import their own Markdown (`.md`) notes directly into the document, and drag-and-drop images which upload silently to the Supabase `tender_attachments` bucket and render inline.
4. **Confirmation & Scheduling:** The buyer confirms the final text. The system generates a formal PDF of the RFP using `@react-pdf/renderer` and attaches it to the tender. The buyer sets a `publish_at` 'Go Live' date, or publishes immediately.


## Workflow states

The tender lifecycle should use simple, explicit states that mirror standard procurement stages.  A clean V1 state model is: **draft**, **open_for_proposals**, **closed**, **under_review**, **awarded**, **withdrawn**, and **archived**.

Each state should have visible rules. **draft**: buyer is preparing the RFP. **open_for_proposals**: tender is live and suppliers may submit. **closed**: no further proposals accepted. **under_review**: buyer is scoring and comparing proposals. **awarded**: decision is final. **withdrawn**: tender cancelled before award. **archived**: post-award archival.

Supplier responses need their own lighter state model: **draft**, **submitted**, **withdrawn**, **disqualified**, **under_review**, **awarded**, and **not_awarded**.  A proposal moves from **draft** to **submitted** when the supplier confirms. It can be **withdrawn** by the supplier before the tender closes. The buyer may **disqualify** proposals failing mandatory criteria. During scoring proposals are **under_review**. After award they become either **awarded** (winner) or **not_awarded** (unsuccessful).

## V1 rules

V1 should enforce a few non-negotiables even if buyers can customize scoring. Every tender should require minimum core sections such as scope, timeline, submission deadline, pricing expectations, and evaluation criteria, because structured intake reduces ambiguity and missing information.  Every AI-generated score should also be explainable, traceable, and contestable by a human reviewer.

For the first pilot, supplier response should use the dynamic form config defined in the database schema (`tender_submission_config`), allowing buyers to collect structured `submission_answers`, `submission_team_profiles`, and `submission_budget_items` alongside standard file uploads.

## Workflow & State Logic Rules

1. **Submission Lockout:** 
   - The API must reject any `supplier_submissions` updates or file uploads if `CURRENT_TIMESTAMP > tenders.submission_deadline`.
2. **Q&A Privacy Rule:** 
   - Questions submitted by suppliers are visible ONLY to the buyer. 
   - The buyer can publish the answer. When published, the question and answer are visible to ALL suppliers, but the identity of the asking supplier remains strictly anonymous.
3. **Scoring Hierarchy:** 
   - The system calculates the top-line table using `evaluations.human_raw_score`. 
   - If a human has not scored a criterion yet, the system falls back to `evaluations.ai_raw_score`. 
   - The UI must visually indicate whether a score is "AI Only" or "Human Confirmed".
4. **AI Summary Generation:** 
   - Upon submission, trigger an AI job to populate `ai_overall_summary` (strict limit: 150 words) and `ai_special_conditions` (flagging unusual caveats, pricing anomalies, or compliance deviations).
5. **Post-Award Automation & Audit Defensibility:** 
   - When a tender state changes to `Awarded`:
     a) Trigger a serverless function to compile all evaluations, scores, and rationale into a single PDF.
     b) Use AI to scan the immutable `audit_logs` and generate a "Defensibility Summary" in the PDF (e.g., summarizing human overrides, on-time submissions, and compliance integrity).
     c) Zip all supplier submission files and the PDF together.
     d) Save both to Supabase Storage and update `audit_report_pdf_url` and `submission_archive_zip_url`.
     e) Generate draft emails for the awarded supplier and all unsuccessful suppliers, storing them in the UI for buyer review before sending via `communications_log`.
6. **Immutable Audit Trail:**
   - Every state change, score change, document view, and system email must be logged in `audit_logs` with exact `previous_value` and `new_value` JSON payloads to ensure legal defensibility.
7. **Template Management:**
   - Buyers do not start from scratch. They can select system defaults or their own saved templates. The AI drafting agent must dynamically adjust these templates if the buyer flags specific regulatory requirements during the setup wizard.


## Advanced Procurement Workflows
- **E-Signature Integration:** When a tender is awarded, the platform uses an embedded e-signature flow (e.g., Documenso) to capture legally binding signatures from both the buyer and the winning supplier. The Audit Report PDF is appended with the signature certificates.
- **Automated Rejection Notifications:** Upon awarding a tender, the AI automatically drafts polite, professional rejection emails for all unsuccessful bidders, citing the AI justification for their score. The buyer reviews and approves these before they are sent via the `communications_log`.
- **Standstill (Alcatel) Period:** To support public sector and highly regulated buyers, the platform enforces a mandatory 'Standstill Period' (usually 10 days) after the award decision is announced but before the contract is formally signed, allowing unsuccessful bidders time to challenge the decision.
- **Supplier Performance Ratings:** After a contract concludes, buyers can leave a 1-5 star rating and review for the winning supplier. This data will eventually feed into a 'Verified Performer' marketplace badge system.

## Acceptance criteria

V1 is successful if a buyer can create an account, draft an RFP through a guided workflow, export it to PDF, publish or privately share it, collect supplier uploads, define scoring rules, compare bids, and reach a documented shortlist decision inside one system.  V1 is also successful if every important action is visible in status tracking and preserved in an audit trail, because that is what turns a useful workflow into a credible procurement product.

Sources
 The guide to intake management for procurement teams https://www.brex.com/spend-trends/procurement/intake-management
 8 Procurement Software Best Practices For 2026 | Ivalua https://www.ivalua.com/blog/procurement-software-best-practices/
 AI in Procurement: The Complete 2026 Guide | SpecLens https://www.speclens.ai/blog/ai-in-procurement-complete-guide
 Resume-CV_Voice-Tone.md https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/collection_c4d9619c-1a86-4bc9-861f-50d6e0d3c5ad/f728042f-e718-4281-ba3d-f24f64a0fc47/Resume-CV_Voice-Tone.md
 The Tender Process: Complete 7-Stage Guide 2026 - AutoRFP.ai https://autorfp.ai/blog/tender-process
 Explainable AI: The Complete Enterprise Guide for 2026 https://www.seekr.com/resource/explainable-ai-enterprise-guide/
 Enterprise Software Selection Playbook - 2026 https://www.viewpointanalysis.com/post/enterprise-software-selection-playbook-2026
 Procurement Dashboards: Examples & KPIs to Track (2026 Guide) https://www.superblocks.com/blog/procurement-dashboard
 The Ultimate List of RFP Questions to Ask Vendors (2025) https://www.responsive.io/blog/sample-rfp-questions
 How to Write Effective Procurement Tenders https://www.procurementhub.co.uk/news/how-to-write-effective-procurement-tenders/
 Free IDP RFP Template: How to Write a Request for Proposal https://www.klippa.com/en/blog/information/rfp-template/
 Tender Management: Process, Software, Best Practices (2026) https://www.inventive.ai/blog-posts/tender-management-a-complete-guide
 Essential Steps to Successfully Award a Tender in Procurement https://www.trackerintelligence.com/resources/procurement-news/awarding-a-tender-speed-transparency-metrics-by-sector/
 AI-led procurement fraud detection in 2026 https://www.infosysbpm.com/blogs/sourcing-procurement/procurement-fraud-detection-in-2026.html
 The Tendering Process | 11 Stages Broken Down by Hudson Succeed https://www.tenderconsultants.co.uk/tendering-process/
 A Guide to How The Public Procurement Process Works https://executivecompass.co.uk/blog/bid-management/a-guide-to-how-the-public-procurement-process-works/
 Understanding the UK Tender Process: A Step-by-Step Guide https://thorntonandlowe.com/understanding-the-tendering-process-a-step-by-step-guide/
 Guidance: Competitive Tendering Procedures (HTML) - GOV.UK https://www.gov.uk/government/publications/procurement-act-2023-guidance-documents-define-phase/competitive-tendering-procedures-html
 Guide to Bidding & Tendering Process for Project Management https://project-management.com/bidding-tendering-process/
 The Procurement Process in 2026: 9 Steps + What's Changed https://www.procurify.com/blog/procurement-process/


## Tender workspace and communications alignment

The tender detail experience should become a persistent tender workspace for each participating organization, not just a static detail screen. For buyers, this workspace should show the tender title, summary, current status, submission deadline, countdown timer, attachments, clarifications, buyer-only internal notes, a communication timeline, and a submissions table with quick triage labels such as `Consider`, `Reject`, and `Follow Up`.

Suppliers should see the same tender context that is relevant to them, including title, summary, deadline, clarifications, downloadable files, submission status, and the shared communication timeline. If a message concerns one specific submission, the platform should be able to associate that message with the related submission while still keeping it visible in the tender-level history.

The communication model must support both simple in-app tender messaging and formal email composition. Internal messages can be lightweight, but outbound email drafting should support To, CC, subject, attachments, rich HTML body content, and a plain-text fallback. When an email is sent from the platform, the system should fan delivery out to all registered users in the addressed buyer and supplier organizations, while preserving one canonical in-app message record and separate delivery-audit records per recipient.

Submission review in V1 should include a fast buyer workflow for screening responses before and during evaluation. Buyers should be able to open a submission, review the structured answer set, download the uploaded proposal package, download a generated PDF of form-based responses, apply a tender-specific review label, and record short buyer notes at the tender level.

## Scoring and Evaluation trigger
The AI evaluation does NOT run automatically when a supplier submits a bid. To prevent bias and control costs, the buyer must manually click a "Close and Score Tenders" button on the tender workspace. 
When this is clicked:
1. The tender `status` changes from `'Published'` (or `'Private Invite'`) to `'Evaluation'`.
2. No further supplier submissions are accepted.
3. The platform queues the AI scoring jobs for all submitted bids simultaneously.

## Supplier Onboarding and Access
When a supplier signs up via an email invitation, the `invite_token` must be passed through the Supabase Auth flow to automatically bind the new user to the correct `organizations` row and link them to the tender. 
If a supplier signs up organically (without an invite link), the onboarding flow must ask: "Are you responding to an existing tender?" If yes, they are prompted to enter the unique code for that tender. This ensures they are granted access even if the tender was created under the `'Private Invite'` status.


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


## Supplier Journey & Workflow Refinements
- **The Registration Wall:** Public tenders show a rich summary, but downloading the RFP documents requires a supplier to register or log in. This tracks exactly which organizations download the documents for the buyer.
- **Intent to Bid vs. Decline:** After reviewing documents, suppliers must click "Intend to Bid" (creates a `Draft` submission) or "Decline" (updates status to `Declined`). This gives buyers early visibility into pipeline health.
- **Collaboration & ESG Reuse:** Submissions are shared organization drafts. Any user in the supplier org can edit the draft. During the guided workflow, suppliers can pull existing ISO certificates and ESG policies from their `master_compliance_data` profile instead of re-uploading them.
- **Retract & Edit:** Before the `submission_deadline`, suppliers can click "Retract" on a submitted proposal. This reverts the status to `'Draft'` so they can fix errors and resubmit.
- **Binding the 5% Fee:** At the final review step before clicking Submit, the supplier MUST check a box explicitly agreeing to the 5% success fee on the final contract value.
- **Anti-Fraud Deviation Guardrail:** To prevent a buyer and supplier from colluding to log a fake low contract value (e.g., £10k instead of £100k to avoid fees), the system enforces that the `final_contract_value` inputted at Award cannot be less than 90% of the supplier's original `total_bid_amount`. (A >10% deviation requires a platform admin to manually override).

## Supplier Organisation Lead Role
Every supplier organisation has one designated Lead. The Lead is the only person who can:
1. Accept the platform Terms and Conditions on behalf of the organisation.
2. Click the final Submit button on a tender submission (agreeing to the 5% success fee).
3. Any registered user in the organisation can download documents and edit the draft submission.
4. If the Lead changes (updated in org settings), the new Lead must re-accept T&Cs before any further platform actions are permitted.

For a buyer-side organisation, the equivalent constraint is `buyer_admin` — only a `buyer_admin` can Publish a tender, Award a contract, or Withdraw a tender.


## Supplier AI Copilot

Suppliers have a persistent AI agent that guides them through the bid submission process. The copilot appears as a chat panel on the left (30% width) with workspace tabs on the right (70% width).

**Key capabilities:**
- Answer questions about tender requirements, deadlines, and evaluation criteria
- Draft responses to custom questions based on the supplier's master compliance data
- Submit clarification questions to the buyer on behalf of the supplier
- Add team members and budget items via natural language commands
- Proactively alert the supplier about missing requirements and approaching deadlines
- Validate submission completeness before final submission
- Review and suggest improvements to executive summaries and answers

The supplier copilot uses the same Vercel AI SDK with function calling as the buyer copilot, ensuring a consistent AI-first experience for both sides of the procurement process.
