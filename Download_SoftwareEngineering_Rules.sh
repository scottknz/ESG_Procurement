#!/bin/bash

# Define the target directory
TARGET_DIR="/Users/drscottkelly/Dropbox (Personal)/Python/ESG_Procurement/Instructions/Agent_Skills"

# Create the directory if it doesn't exist
mkdir -p "$TARGET_DIR"
cd "$TARGET_DIR"

echo "Creating Agent Skills directory and downloading best practices..."

# 1. Next.js 16 & React 19 Best Practices
cat << 'EOF' > 01_Nextjs_React_Rules.md
# Next.js 16 & React 19 Coding Standards

## 1. Core Paradigm
- You are an expert in TypeScript, Node.js, Next.js App Router, React 19, and Tailwind CSS.
- Use Server Components by default. Use `"use client"` ONLY when necessary (hooks, event listeners, state).
- Favor standard React 19 features over legacy hooks: Use `use()` instead of `useEffect` for data fetching where applicable.
- Avoid Next.js legacy features. Never use `getServerSideProps`, `getStaticProps`, or the `pages/` directory.

## 2. Server Actions & Data Fetching
- All data mutations must use Server Actions (`"use server"`).
- Place Server Actions in dedicated files (e.g., `src/lib/actions/`) or colocated with the feature.
- Always use `zod` for input validation on both client forms and server actions.
- Use Next.js caching (`unstable_cache`, `revalidatePath`, `revalidateTag`) aggressively but correctly.

## 3. TypeScript & Safety
- Use strict TypeScript. Avoid `any`. Use `unknown` if absolutely necessary.
- Prefer interfaces over types for object definitions.
- Implement early returns to avoid deep nesting (Guard Clauses).
EOF

# 2. Supabase & PostgreSQL Best Practices
cat << 'EOF' > 02_Supabase_DB_Rules.md
# Supabase & PostgreSQL Standards

## 1. Database Architecture
- All database modifications MUST be written as incremental SQL migrations in `supabase/migrations/`.
- Use `JSONB` for flexible, non-relational configurations to prevent schema bloat.
- Enforce data integrity using PostgreSQL Triggers, especially for audit logs (prevent updates/deletes).

## 2. Row Level Security (RLS)
- EVERY table must have RLS enabled (`ALTER TABLE table_name ENABLE ROW LEVEL SECURITY;`).
- Write explicit policies for `SELECT`, `INSERT`, `UPDATE`, and `DELETE`.
- Do not bypass RLS in the client. Only bypass RLS in server environments using the Supabase Service Role Key when explicitly required (e.g., automated webhooks).

## 3. Client Interaction
- Use the generated `Database` types from `src/types/database.types.ts` in all Supabase queries.
- Never write raw SQL in application code. Use the `@supabase/supabase-js` query builder.
EOF

# 3. AI & Testing Standards
cat << 'EOF' > 03_Testing_and_AI_Rules.md
# AI Features & Testing Standards

## 1. Vercel AI SDK Integration
- Use the Vercel AI SDK (`ai` and `@ai-sdk/google`) for all LLM interactions.
- Utilize `streamText` for UI responsiveness during long generations.
- For function calling, explicitly define `tools` with strict `zod` schemas.

## 2. Test-Driven Development (TDD)
- Write deterministic unit tests using `vitest`.
- Test the business logic, not just syntax.
- Mock Supabase clients and Stripe integrations to prevent network dependency in tests.
- Agents MUST run tests via terminal (`npx vitest run`) and self-correct if a test fails before handing off code.

## 3. Semantic Commenting
- Leave AI-to-AI declarative comments above every complex function explaining:
  1) Intent (What it does)
  2) Business Logic (Why it does it)
  3) State changes (Expected inputs/outputs)
EOF

# 4. Shadcn & Tailwind Best Practices
cat << 'EOF' > 04_UI_Shadcn_Rules.md
# UI, Shadcn, & Tailwind Standards

## 1. Mobile-First & Responsive
- Default to mobile-first utility classes in Tailwind.
- Ensure all interactive elements have sufficient touch targets (min 44x44px).

## 2. Shadcn/UI Component Usage
- Use unmodified Shadcn components from `src/components/ui/` where possible to maintain consistency.
- Forms must use Shadcn `Form`, `FormField`, and `react-hook-form` paired with `zod` resolvers.
- Always implement loading states (Skeleton components or Spinners) for async operations.

## 3. Accessibility (a11y)
- Ensure proper `aria-labels` on icons and icon-only buttons.
- Preserve keyboard navigation (tab indexing) and focus management.
EOF

echo "Successfully downloaded all Agent Skills"
1