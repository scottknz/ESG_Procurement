# Tech Stack

The ESG Procurement Platform is built entirely using Gemini CLI as the primary code-generation agent. All routes, components, services, and migrations are generated and maintained by Gemini following the instruction files in `/Instructions/`. Lovable may be used later for **visual UI iteration only** (colours, spacing, layout polish) and must never be used to generate schema, business logic, or API routes.

## Core Stack

- **Frontend:** React 19 with Next.js 16.2 (Turbopack stable, 10x faster builds, AI agent improvements) with App Router — standard full-stack React with server components and server actions
- **UI layer:** shadcn/ui + Tailwind CSS — responsive dashboards, forms, multi-step workflows
- **Rich Text Editor:** Novel (built on TipTap) — Notion-style WYSIWYG editor with slash menu, Markdown support, and Supabase image drag-and-drop
- **Security:** Cloudflare Turnstile (CAPTCHA alternative) to prevent bot registration and brute force attacks
- **Backend:** Supabase (March 2026: Storage 14.8x faster, Stripe Sync Engine, Index Advisor) — Postgres, Auth, Storage, Edge Functions
- **AI:** Gemini API (server-side only) via Vercel AI SDK v6.0+ (`ai` package with native agent support) with streaming and function calling for the buyer copilot — RFP drafting, template adaptation, submission evaluation, audit summaries
- **Payments:** Stripe — £200 public listing fee, 5% success fee invoicing, webhook event handling
- **Email:** Resend — transactional emails with HTML templates
- **E-Signature:** Documenso (open-source) — embedded contract signing via Documenso API
- **PDF Generation:** @react-pdf/renderer@4.3+ (with HTML support via react-pdf-html) — audit reports and RFP exports
- **Background Jobs:** Supabase Edge Functions — long-running AI scoring tasks (avoids Vercel timeout)
- **Version control:** GitHub — source of truth
- **Deployment:** Vercel

## What Gemini Owns (Everything)

Gemini generates and maintains ALL of the following:
- Supabase migrations and RLS policies
- TypeScript types (auto-generated + hand-written domain types)
- Authentication and role-based access control
- Tender lifecycle state machine
- Scoring engine and weighted criteria logic
- AI evaluation prompt pipelines
- Stripe payment flows and webhook handlers
- PDF generation service layer
- Email templates and Resend integration
- All Next.js App Router pages, layouts, and API routes
- All shadcn/ui component compositions
- Background job queue for async AI evaluation

## Screen-to-Route Mapping

| Screen | Route | Notes |
|---|---|---|
| Landing / storefront | `(public)/[org_slug]/page.tsx` | Public branded buyer storefront |
| Public tender detail | `(public)/[org_slug]/tenders/[tender_id]/page.tsx` | Document download + reg wall |
| Login | `(auth)/login/page.tsx` | Supabase Auth UI |
| Register | `(auth)/register/page.tsx` | Org type selection + user setup |
| Invite onboarding | `(auth)/register/invite/page.tsx` | Invite token binding flow |
| Buyer dashboard | `(buyer)/buyer/dashboard/page.tsx` | Active tenders, deadlines |
| New tender wizard | `(buyer)/buyer/tenders/new/page.tsx` | AI-assisted multi-step wizard |
| Tender workspace | `(buyer)/buyer/tenders/[tender_id]/page.tsx` | Workspace hub |
| Submissions list | `(buyer)/buyer/tenders/[tender_id]/submissions/page.tsx` | Triage table |
| Submission detail | `(buyer)/buyer/tenders/[tender_id]/submissions/[id]/page.tsx` | Full review + labels |
| Evaluation dashboard | `(buyer)/buyer/tenders/[tender_id]/evaluate/page.tsx` | Side-by-side scoring |
| Award screen | `(buyer)/buyer/tenders/[tender_id]/award/page.tsx` | Final decision + invoice trigger |
| Buyer history | `(buyer)/buyer/history/page.tsx` | Historical archive + audit PDFs |
| Messages | `(buyer)/buyer/tenders/[tender_id]/messages/page.tsx` | Tender message composer |
| Supplier dashboard | `(supplier)/supplier/dashboard/page.tsx` | Invitations + active bids |
| Supplier bid form | `(supplier)/supplier/bids/[tender_id]/page.tsx` | Dynamic submission form |
| Supplier unlock | `(supplier)/supplier/bids/[tender_id]/unlock/page.tsx` | Stripe paywall |
| Supplier final review | `(supplier)/supplier/bids/[tender_id]/review/page.tsx` | Review before submit |
| Admin dashboard | `(admin)/admin/dashboard/page.tsx` | Platform metrics |


## Architecture Constraints & Scaling

- **File Uploads:** Must use direct-to-storage architecture (Signed URLs) directly from the client. Next.js server actions must not buffer file streams due to payload constraints.
- **AI Processing:** Heavy Gemini API calls (like full tender evaluation) must run asynchronously. If deployed on Vercel, long-running processes cannot sit in standard API routes. Use Supabase Edge Functions, Webhooks, or a background queue.
- **Database Engine:** Rely on Postgres Triggers to enforce true immutability on audit tables. RLS alone is not enough, as the service role bypasses RLS.
- **Data Integrity:** Implement optimistic concurrency control (`updated_at` checking) on editable records like `tenders`, `supplier_submissions`, and `evaluations` to prevent silent overwrites.

## Alignment update: messaging and tender workspace requirements

The approved stack already supports the new requirements: Supabase/PostgreSQL for canonical tender messages, recipient groups, attachments metadata, review labels, buyer notes, and per-recipient communication audit; Resend for outbound email delivery; and Next.js server actions or route handlers for draft-save, send, retry, and submission-PDF generation flows.

Message drafting between buyers and suppliers uses the **Novel (Notion-style)** editor. The editor output must be saved to `body_html` (with a generated plain-text fallback in `body_text`) in the `tender_messages` database table, ensuring a seamless rich-text chat experience. The server must sanitize this HTML before storing it and before sending it out via Resend for email notifications.

The implementation should treat email as a delivery channel layered on top of canonical in-app tender messages. That means the database record for a tender conversation remains the source of truth, while the mail provider only handles transport and delivery status.

## Latest Package Versions (March 2026)

This project uses the latest stable versions of all dependencies:

| Package | Version | Key Features |
|---------|---------|--------------|
| Next.js | 16.2 | Agent-ready scaffolding, browser log forwarding, experimental agent DevTools |
| React | 19 | Server Actions, use() hook, improved hydration errors |
| Turbopack | Stable | 76% faster startup, 96% faster refresh, production-ready |
| Supabase | Latest | Storage 14.8x faster, Stripe Sync, PrivateLink access |
| Vercel AI SDK | 6.0+ | Native agent support, configurable call options |
| @react-pdf/renderer | 4.3.2 | Performance boosts, JPEG2000 downscaling |
| TipTap | Latest | Bidirectional Markdown, AI Toolkit |
| shadcn/ui | Latest | Full component library with accessibility |
| Stripe API | Latest | Payment intents, webhooks, customer portal |
| Resend | Latest | React Email templates, delivery tracking |

### Installation Command

```bash
npm install next@16.2 react@19 react-dom@19
npm install @supabase/supabase-js@latest
npm install ai@6 @ai-sdk/google@latest
npm install @react-pdf/renderer@4.3.2 react-pdf-html
npm install novel
npm install stripe@latest
npm install resend@latest
npm install shadcn-ui@latest
```
