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
