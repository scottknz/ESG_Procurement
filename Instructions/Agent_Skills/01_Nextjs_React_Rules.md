# Next.js 16.2 & React 19 Coding Standards

## 1. Core Paradigm
- You are an expert in TypeScript, Node.js, Next.js 16.2 App Router, React 19, and Tailwind CSS. Always install `create-next-app@16.2` — never use `@latest`.
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
