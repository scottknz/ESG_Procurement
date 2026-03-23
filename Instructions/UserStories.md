Yes — and the right MVP is not “small” in the sense of being thin; it is **complete around one workflow**: guided RFP drafting, tender management, supplier upload, scoring, and comparison in a single governed flow. Centralized workflows, structured intake, configurable approvals, audit trails, and explainable AI are already standard expectations in procurement software, so those should be in v1 rather than deferred.[1][2][3][4]

## Product goal

The MVP should help a buyer move from vague procurement need to a defendable shortlist decision inside one system. A strong procurement flow usually covers structured intake, RFP creation, vendor response collection, scoring, decision support, and an auditable record of why the final choice was made.[2][5][6]

## Core user stories

### Buyer
- As a buyer, I want to start from standard regulatory templates (e.g., CSRD, Scope 1-3) or save my own custom templates for future use, so I don't start from scratch.
- As a buyer, I want the AI to dynamically adapt my chosen template based on the specific regulatory footprint of my project.
- As a buyer, I want the agent to ask follow-up questions based on my answers so the RFP becomes more complete and specific.
- As a buyer, I want to save the RFP as a draft, edit it later, and only publish it when I am ready.
- As a buyer, I want the RFP to render in a clean on-screen format and export to PDF because formal procurement documents still need structured outputs and reusable content.[5][7]
- As a buyer, I want the system to generate a branded public landing page (my "storefront") where suppliers can view open tenders without needing to log in first.
- As a buyer, I want the system to help me identify regulatory requirements and automatically insert relevant compliance clauses into the RFP so I don't miss legal obligations.
- As a buyer, I want to define my own evaluation criteria with detailed descriptions and weights, so the AI and human evaluators know exactly how to score.
- As a buyer, I want to configure the supplier submission form (toggling budget tables, team profiles, and custom questions) so I get structured data instead of just raw PDFs.
- As a buyer, I want to keep some tenders private and invite selected vendors before making anything public.
- As a buyer, I want a Q&A board where suppliers can ask questions privately, and I can publish the answers anonymously to all suppliers.
- As a buyer, I want the system to lock out submissions exactly at the deadline.
- As a buyer, I want to compare supplier submissions side by side and see which bid scores highest against my criteria.
- As a buyer, I want AI to automatically summarize each submission and flag anomalous "special conditions" or risks before I read the whole document.
- As a buyer, I want AI to explain why a submission scored well or badly, with explicit reasons for any deductions, because explainability is essential in regulated decisions.
- As a buyer, I want the system to automatically generate a full PDF audit report and a ZIP file of all submissions when I award the contract.
- As a buyer, I want an immutable audit trail that tracks exact score changes and document views, and uses AI to generate a plain-English "Defensibility Summary" for the final audit report.
- As a buyer, I want the system to draft acceptance and rejection emails for me to review and send at the end of the process.

### Buyer evaluator / team member
- As an evaluator, I want to review the buyer’s scoring framework before vendor responses are opened.
- As an evaluator, I want to add comments and override scores with reasons so the process reflects human judgment as well as AI support.
- As an evaluator, I want all scoring changes logged so the process is defensible and traceable. Audit trails and evidence traceability are standard best practice for procurement and AI-assisted evaluation.[4][9][2]

### Supplier
- As a supplier, I want to receive a clear RFP package and submit my response through a structured form and file upload flow.
- As a supplier, I want to ask clarification questions and see answers from the buyer.
- As a supplier, I want to build a master profile so I don't have to re-upload standard compliance certificates for every bid.
- As a supplier, I want to know the required deadline, submission format, and evaluation criteria.
- As a supplier, I want confirmation that my response was received and is under review.

### Platform admin
- As an admin, I want to manage organizations, users, and access rights.
- As an admin, I want to see tender status, supplier activity, and scoring completion across the platform.
- As an admin, I want a full history of actions, uploads, and scoring events because centralized oversight and accountability are core procurement requirements.[1][4]

## MVP feature list

### 1. Buyer intake and drafting
- Authentication and organization accounts.
- Template Library (system defaults mapped to regulations + custom saved templates).
- New tender wizard with template selection and AI dynamic adaptation.
- Multi-step questionnaire with AI follow-up questions.
- Structured RFP editor with sections such as scope, timeline, pricing, compliance, implementation, and evaluation.
- Draft autosave.
- PDF export.

A structured intake layer matters because procurement systems increasingly use customizable intake and guided workflows to reduce ambiguity and enforce consistency.[3][1]

### 2. Tender management
- Tender states: Draft, Internal Review, Private Invite, Public, Closed, Awarded.
- Buyer dashboard showing active tenders and deadlines.
- Invite-only supplier option.
- Public listing option.
- Deadline management and submission tracking.

Centralizing the full workflow in one place is a core procurement best practice because fragmented processes reduce visibility and control.[5][1]

### 3. Supplier response handling
- Public branded buyer storefront with open tender list.
- Public tender detail page with multi-document download (individual or ZIP).
- Supplier account creation and master profile compliance data.
- Tender detail page and Q&A clarification board.
- Dynamic form rendering based on buyer config (custom questions, team profiles, budget tables).
- File upload for proposal response and attachments.
- Strict deadline lockout.
- Submission confirmation.

### 4. Scoring and comparison
- Buyer-defined criteria with descriptions and weighting.
- Optional pass/fail rules, floors, ceilings, and automatic disqualification logic.
- AI generation of 150-word summary and "special conditions" flag per submission.
- Split-screen scorecard per supplier showing AI raw score, AI justification, AI deductions, and Human raw score.
- Side-by-side comparison table with mathematically rolled-up weighted scores.

### 5. Governance and Post-Award Automation
- Immutable audit log of exact state changes, document views, score changes (`previous_value` and `new_value`), emails sent, and decisions.
- Evidence links from AI reasoning back to source documents where possible.
- Visibility controls by organization and tender.
- Automated ZIP and PDF audit report generation on award, including an AI "Defensibility Summary".
- Automated drafting of award/rejection emails.

Explainability, evidence traceability, and auditability are especially important when AI is influencing procurement decisions.[9][2][8]

## Not in MVP

These should stay out of the first pilot:
- Full contract management.
- Payment workflows.
- API integrations into ERP or procurement suites.
- Supplier marketplace billing.

Keeping those out protects the build while preserving a complete pilot workflow.

## Success criteria

Your MVP is working if a buyer can:
1. define a procurement need,
2. generate a clean RFP,
3. publish or privately share it,
4. receive supplier uploads,
5. score responses using custom rules,
6. produce a shortlist with explainable reasoning.[6][2][8]

That is enough for a paid pilot because it mirrors the real decision path buyers already follow in enterprise software selection and tender management.[6][5]

## Priority order

Build in this order:
1. Auth + organization model.
2. Buyer RFP wizard.
3. RFP editor + PDF export.
4. Tender state management.
5. Supplier upload flow.
6. Scoring engine.
7. AI reasoning + comparison dashboard.
8. Audit trail.

That sequence follows the logic of procurement software: structured intake first, workflow second, evaluation third.[4][1][6]

Next, I can turn this into either:
- a **v1 product spec with screens and states**, or
- a **database schema and table plan**.

Sources
[1] 8 Procurement Software Best Practices For 2026 | Ivalua https://www.ivalua.com/blog/procurement-software-best-practices/
[2] AI procurement top tops: Critical risk assessment - CITMA https://www.citma.org.uk/resources/ai-procurement-top-tops-critical-risk-assessment-mb26.html
[3] Procurement Management Software: The Best Solutions in 2026 https://monday.com/blog/service/procurement-management-software/
[4] AI-led procurement fraud detection in 2026 | Infosys BPM https://www.infosysbpm.com/blogs/sourcing-procurement/procurement-fraud-detection-in-2026.html
[5] Tender Management: Process, Software, Best Practices (2026) https://www.inventive.ai/blog-posts/tender-management-a-complete-guide
[6] Enterprise Software Selection Playbook - 2026 https://www.viewpointanalysis.com/post/enterprise-software-selection-playbook-2026
[7] Free IDP RFP Template: How to Write a Request for Proposal https://www.klippa.com/en/blog/information/rfp-template/
[8] AI in Procurement: The Complete 2026 Guide | SpecLens https://www.speclens.ai/blog/ai-in-procurement-complete-guide
[9] Best RFP Software for Tech Companies in 2026 https://www.steerlab.ai/blog/best-rfp-software-for-tech-companies-in-2026-a-practical-buyers-guide
[10] How Can I Use AI to Streamline Our Tendering Process? https://info.mercell.com/en/blog/ai-in-tendering
[11] Improving Decision-Making with AI-Powered RFP Scoring Systems https://www.zycus.com/blog/appxtend/ai-powered-rfp-scoring-systems
[12] Best procurement software 2026: Top solutions and buying guide https://www.spendesk.com/blog/best-procurement-software/
[13] The 9 Best Procurement Software Platforms 2026 | Vertice Blog https://www.vertice.one/blog/best-procurement-software-platforms-2026
[14] Top 10 Procurement Management Software in 2026 https://procurement360.io/blog/top-10-procurement-management-software-2026/
[15] Top 10 Procurement Management Software 2026 https://www.freqens.com/blog/top-10-procurement-management-software-2026
[16] RFPs for Insurance Software: A Checklist That Filters Out ... https://www.linkedin.com/pulse/rfps-insurance-software-checklist-filters-out-rework-vendors-tp5nc
[17] Top 10 Best Procurement Software: Comparison & Guide 2026 https://origami-marketplace.com/en-gb/best-procurement-software-comparison/
[18] Marketing automation RFP questions: Complete checklist ... https://www.sifthub.io/blog/marketing-automation-rfp-questions


## Additional user stories: tender workspace and messaging

### Buyer tender workspace
- As a buyer, I want each tender to open into a workspace that shows the title, summary, status, deadline, and countdown so I can manage the tender from one place.
- As a buyer, I want to see a submissions table on the tender workspace so I can quickly monitor response volume and status.
- As a buyer, I want to add short internal notes to the tender so my team can retain important context that is not visible to suppliers.

### Submission triage
- As a buyer, I want a quick dropdown label such as `Consider`, `Reject`, or `Follow Up` on each submission so I can triage responses before full evaluation.
- As a buyer, I want those triage labels to be editable per tender so each procurement process can use its own workflow language.
- As a buyer, I want to open a submission and download both uploaded files and a generated PDF of structured answers so I can review complete submissions offline.

### Tender messaging
- As a buyer or supplier, I want to exchange in-app messages tied to a specific tender so all relevant communication stays attached to that procurement record.
- As a buyer, I want to draft an outbound email with To, CC, subject, attachments, and rich formatting so I can send polished communications from inside the platform.
- As a buyer, I want the platform to send that email to all registered users in the selected buyer and supplier organizations so nobody misses important tender communications.
- As a buyer or supplier, I want every outbound email to appear in the in-app tender communication history so the platform preserves one complete trace of communication.
- As an administrator, I want delivery outcomes recorded per recipient so I can audit who was contacted and whether the email was sent successfully.

### Evaluation and Scoring trigger
- As a buyer, I want to manually click "Close and Score Tenders" after the deadline passes, so that I can evaluate all submissions fairly at the same time without seeing early scores.
- As a buyer, I want the tender status to move to "Evaluation" when I trigger scoring, so suppliers know no further edits are permitted.

### Supplier Access and Registration
- As an invited supplier, I want my invite link to seamlessly add me to my company's existing organization profile during sign-up, so I don't accidentally create a duplicate company.
- As an uninvited supplier registering on the platform, I want to be able to enter a unique tender code during sign-up, so I can gain access to a private tender I was told about offline.


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


### Supplier Experience & Anti-Fraud
- As a supplier viewing a public tender, I must register an account to download the RFP documents, so the buyer knows my company is reviewing it.
- As a supplier, I want to click "Decline" so the buyer knows I am passing, or "Intend to Bid" to start a collaborative draft with my team.
- As a supplier, I want to pull my company's standard ESG and ISO policies directly from my profile into the submission, so I save time on repetitive uploads.
- As a supplier, I want to be able to retract my submission before the deadline, so I can fix a pricing error and resubmit.
- As a supplier, I must explicitly check a box agreeing to the 5% success fee during the final submission review, so the platform has a binding legal record.
- As an administrator, I want the system to block buyers from entering a final contract value that is less than 90% of the bid amount, so users cannot collude to evade the platform fee.

### Supplier Lead Role & T&Cs
- As the org lead of a supplier, I must accept the Terms and Conditions before my organisation can interact with any tender on the platform.
- As the org lead, I am the only person who can click the final Submit button on a tender submission.
- As a supplier org admin, I can reassign the lead role to another team member, at which point the new lead will be required to re-accept T&Cs.
- As a supplier, I can freely switch my submission between Draft, Intent to Bid, and Declined at any point before the deadline or before the buyer closes scoring.

### Free Tier and Unlock Flow
- As a buyer on the free tier, I can invite up to 3 suppliers privately before being prompted to pay the £200 public listing fee.
- As an uninvited supplier, when I try to download tender documents I am prompted to pay the platform unlock fee via Stripe before the documents are served.


### Advanced Procurement Features
- As a buyer, I want the system to automatically draft rejection emails for unsuccessful suppliers using the AI evaluation notes, so I can close out the process professionally and quickly.
- As a regulated buyer, I want to enforce a 10-day standstill period after announcing the award, so my procurement process complies with public sector regulations.
- As a buyer and supplier, I want to digitally sign the final contract directly within the platform, so the process is legally binding and kept entirely on-system.
- As a buyer, I want to leave a performance rating and review for the winning supplier after the project is finished, so the platform can build a reliable quality metric over time.


### AI Wizard & Document Editing
- As a buyer, I want to have a conversational chat with an AI agent that asks me relevant regulatory and scope questions, so I don't have to start from a blank page.
- As a buyer, I want the AI to automatically generate both the supplier submission form and a separate, detailed RFP document based on our conversation.
- As a buyer, I want to edit the AI-generated RFP document in a Notion-style rich-text editor (Novel), where I can import my own Markdown (.md) notes and drag-and-drop inline images, so I have full creative control over the final PDF.
- As a buyer, I want my supplier submission form to be automatically branded with my organisation's logo, colours, and banner image.
- As a buyer, I want to set a 'Go Live' date for my tender, so it automatically publishes at a specific time in the future.

### Supplier AI Assistant
- As a supplier, I want an AI agent to explain the tender requirements in plain English, so I understand what's expected.
- As a supplier, I want the AI to draft answers to complex questions based on my company's existing compliance data, so I don't start from a blank page.
- As a supplier, I want to ask the AI "Am I ready to submit?" and get a checklist of missing items.
- As a supplier, I want the AI to proactively warn me when the deadline is approaching and my submission is incomplete.
- As a supplier, I want to tell the AI "Add John Smith as a team member with a day rate of £800" instead of manually filling in forms.
- As a supplier, I want the AI to review my executive summary and suggest improvements before I submit.
