# Design System — ESG Procurement Platform

> 🔴 ABSOLUTE: Agent 3 must read this file in full before writing a single component.
> All design decisions defined here override personal judgement or default shadcn themes.

## 1. Design Philosophy
- Vercel-inspired, minimal, high data density, no noise/glows/gradients.
- Clean layout architecture: Collapsible left sidebar (56px to 220px), main content area, and a 30% slide-in AI Chat Panel.

## 2. Typography
- Primary: Inter (variable font) — all UI text
- Code/Data: Geist Mono
- Numbers in tables must use **tabular figures** (`font-variant-numeric: tabular-nums`).

## 3. Color Palette
- Backgrounds: `#FFFFFF` (background), `#F8F9FA` (surface), `#F3F4F6` (surface-hover)
- Brand Green: `#16A34A` (brand-green), `#F0FDF4` (brand-green-light)

## 4. UI Components
- Status badges are `rounded-full`, small text (`text-xs font-medium`), with a light fill and matching border.
- Header row: `--surface` background, `text-xs font-medium text-secondary uppercase tracking-wide`
- Shadcn `Form` + `FormField` + `react-hook-form` + `zod` resolver on every form

## 5. Advanced B2B Patterns
- **Source Citations:** AI rationale must include clickable inline pill badges referencing the source document and page number.
- **Workflow Stepper:** Use a horizontal pipeline visualization for the Tender lifecycle.
- **Comparison Matrix:** Use dense, horizontal scrolling tables with sticky first columns.
- **Expert Personas:** Criteria builders should use dropdowns to assign specific AI personas.
- **Modular Document Builder:** Shift from a monolithic editor to a vertical stack of Sections/Assets.
