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
