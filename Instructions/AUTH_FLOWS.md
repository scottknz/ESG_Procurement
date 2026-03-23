
## Rule Importance Levels

Every rule in this instruction set is tagged with one of three levels:

| Level | Tag | Meaning |
|-------|-----|---------|
| **ABSOLUTE** | 🔴 ABSOLUTE | This rule is non-negotiable. Breaking it will cause data loss, a security breach, or a broken application. You must STOP and ask the human before proceeding if you cannot satisfy it. |
| **REQUIRED** | 🟠 REQUIRED | This rule must be followed in all normal circumstances. If a rare edge case forces a deviation, you must log the exception in BUILD_LOG.md with a justification before continuing. |
| **STANDARD** | 🟡 STANDARD | This is best practice. Follow it unless a stronger architectural reason overrides it. Deviations are acceptable but must be noted in a code comment. |

# Authentication & Onboarding Flows

This document defines the 5 critical authentication and onboarding flows that must be implemented by the API Architect and Component Builder agents.

## Required Environment Variables
The following environment variables must be present in `.env.local` for the auth system to function:
```env
NEXT_PUBLIC_SUPABASE_URL=your-project-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-key
NEXT_PUBLIC_TURNSTILE_SITE_KEY=your-cloudflare-turnstile-site-key
TURNSTILE_SECRET_KEY=your-cloudflare-turnstile-secret-key
```

## 1. Registration Flow (Multi-Step)
**Routes:** `(auth)/register/page.tsx` -> `(auth)/register/[type]/page.tsx`
- **Step 1: Type Selection.** User selects if they are joining as a "Buyer" or "Supplier".
- **Step 2: Organization Info.** User fills out the comprehensive B2B organization data (Trading Name, Legal Name, Registration Number, Address, etc.).
- 🔴 ABSOLUTE — **Step 3: Admin Profile Setup.** Cloudflare Turnstile must be validated server-side before creating any user. User sets their own name, email, and password. Cloudflare Turnstile CAPTCHA is validated.
- **Result:** A backend transaction creates the `organizations` row, registers the auth user, and creates the `profiles` row with `is_org_lead = true` and role `[type]_admin`.

## 2. Invite Token System (Adding users to existing Orgs)
**Route:** `/register/invite`
- **Context:** Buyers inviting suppliers to private tenders, or admins inviting colleagues to their organization.
- **Flow:** User receives an email with a secure token. They click the link and arrive at the invite page.
- 🔴 ABSOLUTE — **Action:** Validate invite token server-side before creating profile or granting any role. (or logs in via OAuth). The backend validates the token, creates their `profiles` row, links them to the existing `organization_id`, and grants the appropriate role.

## 3. OAuth & Email Callback Handlers
**Routes:** `/api/auth/callback/route.ts` and `/api/auth/confirm/route.ts`
- **Purpose:** Handles the PKCE code exchange required by Supabase SSR (Server-Side Rendering) for magic links, password resets, and social logins (Google/Microsoft).
- **Flow:** The URL contains a `?code=...` parameter. The route handler exchanges this code for a secure HTTP-only session cookie.
- **Routing:** After successfully setting the cookie, the handler queries the user's `profiles.role` and redirects them to their appropriate dashboard (`/buyer/dashboard` or `/supplier/dashboard`).

## 4. T&Cs Acceptance Interstitial
**Trigger:** Post-login check on `organizations.terms_accepted_at`.
- **Context:** B2B platforms require formal acceptance of Terms & Conditions by the authorized organizational lead.
- **Flow:** If a user with `is_org_lead = true` logs in, and their organization's `terms_accepted_at` is null, they are intercepted by a mandatory interstitial screen to view and accept the T&Cs. 
- 🔴 ABSOLUTE — **Enforcement:** RLS policies and API routes should actively reject tender publication (for buyers) or tender submission (for suppliers) if the organization hasn't accepted the latest T&Cs.

## 5. Session Management & Auth Guards
**Implementation:** Next.js `middleware.ts` + Server Components
- 🔴 ABSOLUTE — **Middleware:** Must protect the `(buyer)`, `(supplier)`, and `(admin)` route groups using `@supabase/ssr`. Unauthenticated users are immediately redirected to `/login`.
- 🔴 ABSOLUTE — **Role Guards:** If a user with a `supplier_admin` role tries to access a `/buyer/*` route, the middleware or layout component must detect the role mismatch and redirect them back to `/supplier/dashboard` (and vice versa).
- **Context Passing:** The session must be correctly passed to all Server Actions to ensure database interactions use the authenticated user's context, preserving Row-Level Security (RLS) integrity.
