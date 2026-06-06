# Section components — bento, cards, previews

## Features bento (`Features`)

Internal grid: `grid-cols-6` with cells spanning `col-span-*` / `row-span-*`.

Typical cells:

| Cell | Span | Content |
|------|------|---------|
| Policy / trust | 3×2 | Icon + headline + short copy |
| Connectors | 2×1 | Brand icon row |
| Skills / workflows | 2×1 | List or chips |
| Handoffs | 2×1 | Diagram or mini UI |

Use shared `Card` / `CardContent` primitives. Decorative SVG waves optional in cell backgrounds (`aria-hidden`).

Keep copy specific to product capabilities; layout is the portable pattern.

## Deliverable cards

4-column grid (`lg:grid-cols-4`). Each article uses marketing card class +:

- `iconTile` square at top
- H3 `15px` semibold
- Muted body `12.5px`

Data: `{ icon: LucideIcon, title, copy }[]`.

## Comparison band (“The shift”)

`lg:grid-cols-[0.8fr_1.2fr]` — left column static pitch, right column stacked rows.

Each row article (marketing card):

- Task label top
- `sm:grid-cols-2` — **Typical** cell: hairline border, elevated bg, muted label “Typical …”
- **Product** cell: vertical blue gradient `linear-gradient(0deg, #128cff, #0d3aa6 48%, #061a55)`, white text, subtle shadow

Data: `{ task, old, product }[]`.

## Product flow preview

Client or server component showing 4-step pipeline as mini cards in `md:grid-cols-4`:

1. Request
2. Context gather
3. Prepare output
4. Approval gate

Use monospace labels, hairline connectors, or numbered badges. Wrapped by `#flow` section with `.marketing-wash` backdrop.

## Security matrix

`md:grid-cols-3` grid of trust pillars (access control, audit log, approvals). Icon + title + one paragraph each. Sits in right column of `#secure` split layout.

## FAQ

`md:grid-cols-2` gap-3. Each item: question as H3, answer body `13px leading-7`. Same marketing card shell.

Feed `homepageFaqs[]` to `faqSchema()` JSON-LD on the page.

## Footer wordmark CTA

Large typographic CTA — “Launch {{Brand}}” pattern:

- Full-width contained card
- Primary button → `{{AppUrl}}`
- Optional gradient outline on container

## Icon tile helper

```ts
const iconTile =
  "flex h-10 w-10 items-center justify-center rounded-[var(--radius-sm)] border ... group-hover:bg-[var(--color-fg)] group-hover:text-[var(--color-bg-elevated)]";
```

## Product preview / avatar dependencies

If flow preview uses agent avatar component, port minimal avatar (static image or initials) — do not pull entire chat UI.

## Composition tip

Define shared `marketingCard` string constant in `page.tsx` and reuse across sections for consistent hover lift.
