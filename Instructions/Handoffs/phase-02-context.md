# 🔴 ABSOLUTE — Phase 02 - API Architect - Handoff Context

**Completed By:** Agent 2: API Architect
**Target Next Agent:** Agent 3: Component Builder
**Phase Summary:** Implemented the full database schema, deployed Row-Level Security, and scaffolded the core API actions.

## Notes for Agent 3
- Next.js Route Groups `(auth)`, `(buyer)`, `(supplier)`, and `(public)` exist conceptually but lack `layout.tsx` and `page.tsx` files. You are responsible for building these with `shadcn/ui`.
- Import `shadcn` components into `src/components/ui/`.
- Always use `"use client"` ONLY when absolutely necessary for hooks and interactivity.
- Avoid fetching data in `useEffect` — rely on Server Components natively.
