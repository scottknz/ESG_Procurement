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
