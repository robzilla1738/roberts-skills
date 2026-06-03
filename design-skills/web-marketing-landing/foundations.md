# Foundations — tokens, typography, utilities

## Color system

### Monochrome surfaces (light default)

| Token | Typical value | Use |
|-------|---------------|-----|
| `--color-bg` | warm off-white | Page background under gradient wash |
| `--color-bg-elevated` | white | Cards, inputs |
| `--color-fg` | near-black | Primary text |
| `--color-fg-muted` | mid gray | Body secondary |
| `--color-fg-subtle` | light gray | Eyebrows, labels |
| `--color-hairline` | rgba black ~12% | Borders |
| `--color-hairline-strong` | rgba black ~22% | Hover borders, card top shine |
| `--surface-panel` | translucent white | Soft panels |
| `--surface-panel-strong` | white | Marketing cards |
| `--surface-page` | layered gradients | `html`/`body` backdrop |

Dark mode: mirror via `[data-theme="dark"]` on `:root` with inverted fg/bg and stronger shadows.

### Accent gradient (brand punctuation)

Four stops — cyan → electric blue → royal blue → navy:

```
--accent-grad-1: #5fe3ff
--accent-grad-2: #1ab2ff
--accent-grad-3: #0a7df5
--accent-grad-4: #062aa6
```

Compose:

```css
--accent-gradient: linear-gradient(
  115deg,
  var(--accent-grad-1) 0%,
  var(--accent-grad-2) 35%,
  var(--accent-grad-3) 68%,
  var(--accent-grad-4) 100%
);
```

Hero panel vertical wash (separate from sweep):

```css
--hero-panel-gradient: linear-gradient(
  180deg,
  #061a55 0%,
  #0a2576 28%,
  #0a64ef 62%,
  #04113a 100%
);
```

**Usage budget:** one `.accent-gradient-text` span per section headline, one decorative wash per band, footer wordmark outline. Not for every card background.

### Ink on hero CTAs

`--accent-ink: #14111f` for text on white hero buttons.

## Typography

| Role | Font | Application |
|------|------|-------------|
| Body | Geometric sans (e.g. Poppins) | `font-family: var(--font-sans)` on `body` |
| Display | Distinct display OTF | `.marketing-shell :where(h1, h2, h3, .marketing-title)` |
| Mono | Optional mono variable | Code snippets only |

Load display via `next/font/local`; body via `next/font/google`. Set CSS variables on `<html className={...}>`.

Scale (hero):

- Eyebrow pill: `10.5px`, uppercase, `tracking-[0.14em]`
- H1: `40px` → `88px` across breakpoints, `leading-[0.97]`, `tracking-[-0.035em]`
- Hero subcopy: `16–18px`, `leading-7/8`

Scale (sections):

- H2: `28–56px`, `leading-[1.05]`, `tracking-[-0.02em]`
- Body: `14.5–18px` with `text-pretty`

Utilities: `.text-balance`, `.text-pretty` (`text-wrap`).

## Marketing shell

```css
.marketing-shell {
  max-width: 100%;
  overflow-x: clip;
  font-family: var(--font-sans);
}
```

Apply on the outer wrapper that contains nav + main + footer.

## Reusable utilities

### Eyebrow

`.eyebrow-marketing` — inline-flex, uppercase, subtle color, `::before` 1.6rem bar filled with accent gradient. Add `justify-center` when centered.

### Buttons

- `.button-primary` — filled accent/ink, hover lift
- `.button-secondary` — hairline border, elevated bg
- `.pressable` — `scale(0.96)` on `:active`, 180ms easing

Hero primary CTA: white pill, `rounded-full`, strong shadow (not necessarily `.button-primary`).

### Marketing card (Tailwind string pattern)

```
group relative overflow-hidden rounded-[18px]
border border-[var(--color-hairline)]
bg-[var(--surface-panel-strong)]
shadow-[0_14px_42px_rgba(20,17,31,0.06)]
transition-[transform,box-shadow,border-color] duration-200
hover:-translate-y-0.5 hover:shadow-[0_22px_58px_rgba(20,17,31,0.1)]
```

Top hairline shine: `absolute inset-x-0 top-0 h-px` gradient line inside card.

### Icon tile (in cards)

`h-10 w-10 rounded-[var(--radius-sm)]` border + bg; on group hover invert fg/bg.

## Tailwind theme block

```css
@theme {
  --font-sans: var(--font-poppins), ui-sans-serif, system-ui, sans-serif;
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 14px;
}
```

## Shape tokens

Prefer CSS variables for radii on marketing cards (`18px` outer, `var(--radius-sm)` inner cells) so light/dark stay consistent.
