# Layout — sections, grids, spacing

## Page wireframe

```
┌─────────────────────────────────────────┐
│ PublicNav (fixed)                        │
├─────────────────────────────────────────┤
│ HERO (full viewport panel)               │
│   eyebrow / h1 / sub / CTAs              │
│   [ card ] [ card ] [ card ]  (3-col)   │
├─────────────────────────────────────────┤
│ #what-is-*     │  copy + 3 pills        │
├─────────────────────────────────────────┤
│ #connectors    │  hub grid              │
├─────────────────────────────────────────┤
│ #product       │  bento Features        │
├─────────────────────────────────────────┤
│ deliverables   │  4-col cards           │
├─────────────────────────────────────────┤
│ #flow (+ wash) │  preview component     │
├─────────────────────────────────────────┤
│ comparison     │  stacked 2-col rows    │
├─────────────────────────────────────────┤
│ #secure        │  security matrix       │
├─────────────────────────────────────────┤
│ use cases      │  4-col cards           │
├─────────────────────────────────────────┤
│ FAQ            │  2-col cards           │
├─────────────────────────────────────────┤
│ FooterWordmark CTA                       │
├─────────────────────────────────────────┤
│ PublicFooter (3-col links)               │
└─────────────────────────────────────────┘
```

## Horizontal rhythm

Standard section padding:

```
px-5 sm:px-6 lg:px-8
```

Content containers:

| Width | Sections |
|-------|----------|
| `max-w-7xl` | Most body sections |
| `max-w-5xl` | Connector band |
| `max-w-4xl` | Hero text column |
| `max-w-[90rem]` | Hero outer panel |

Center with `mx-auto`.

## Vertical rhythm

| Band | Classes |
|------|---------|
| Compact intro | `py-14 sm:py-18` |
| Standard | `py-20 sm:py-28` |
| Hero bottom | `pb-20 sm:pb-28` inside hero section |

Inner stacks: `mt-12 sm:mt-14` below section headers.

## Grid recipes

### 55 / 45 intro (`#what-is-*`)

```
md:grid-cols-[0.55fr_1fr] md:items-start gap-8
```

Left: eyebrow + H2. Right: 2 paragraphs + `sm:grid-cols-3` fact pills.

### 72 / 90 split (flow, use cases header)

```
md:grid-cols-[0.72fr_0.9fr] md:items-start
```

Right column copy uses negative margin pull on desktop: `md:-ml-16 md:pt-10 lg:-ml-20` for optical alignment.

### 80 / 120 split (comparison, secure)

```
lg:grid-cols-[0.8fr_1.2fr] lg:gap-14
```

### Card grids

| Layout | Classes |
|--------|---------|
| Deliverables / use cases | `gap-4 md:grid-cols-4` or `lg:grid-cols-4` |
| FAQ | `gap-3 md:grid-cols-2` |
| Hero features | `lg:grid-cols-3 gap-4` overlapping hero bottom |

## Section IDs and anchors

Provide hash IDs for nav deep links: `#product`, `#connectors`, `#flow`, `#secure`. Nav mega-menu items point to these paths.

## Background treatments

- **Default:** inherit `--surface-page` from body.
- **Flow section:** `relative isolate` + absolutely positioned `.marketing-wash` (`inset-0 -z-10`).
- **Hero:** self-contained gradients inside hero panel (see [hero-aurora.md](hero-aurora.md)).

## Data-driven sections

Keep copy arrays in `page.tsx` (or co-located `content/home.ts`):

- `deliverables[]` — icon, title, copy
- `comparisonRows[]` — task, old, product
- `useCases[]` — title, copy
- `homepageFaqs[]` — question, answer

Map to card components; do not hard-code eleven separate static sections without data structures.

## Responsive rules

1. Stack all multi-column grids to single column below `md` unless noted (`sm:grid-cols-2` for FAQ).
2. Hero H1 scales at `sm` / `md` / `lg` breakpoints — never below `40px` on mobile.
3. Connector hub: `max-w-[24rem]` mobile → `sm:max-w-3xl` desktop.
4. Use `overflow-x-clip` on shell and hero to prevent orbit/grid bleed.
