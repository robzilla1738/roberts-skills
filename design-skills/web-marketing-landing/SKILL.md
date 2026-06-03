---
name: web-marketing-landing
description: >
  Design and scaffold a premium SaaS marketing home page: aurora hero,
  glass nav, connector hub, bento product grid, comparison bands, FAQ,
  CSS-driven motion (no Framer required). Use for /web-marketing-landing
  or when recreating a long-form product landing in Next.js + Tailwind v4.
disable-model-invocation: true
version: 2026-06-02.1
platforms: [Web, Next.js, Tailwind CSS, React]
primary_use_cases:
  - Scaffold a new marketing site from the section blueprint
  - Port a reference landing to a new brand/repo
  - Review an existing landing for visual/UX parity with this pattern
---

# Web Marketing Landing

Hub skill for a **long-form product landing page**: editorial typography, monochrome surfaces with a single cyan–navy accent gradient, glass on hero/chrome only, CSS-first motion, and eleven ordered sections inside a marketing shell.

Read this file first, then open only the spoke files needed for the task.

## Mission

Build a landing that feels **premium and product-specific**, not a generic SaaS template. The page should read as one continuous story: hero promise → plain explanation → integrations → product depth → outputs → flow → differentiation → trust → personas → FAQ → final CTA.

Use placeholders in specs and copy decks: `{{Brand}}`, `{{Accent}}`, `{{AppUrl}}`, `{{Connectors[]}}`. Do not hard-code a customer name in skill prose.

## Non-negotiables

1. **CSS-first motion** — entrance stagger, gradient shift, connector orbit, and nav glass use keyframes/utilities. Do not require Framer Motion for the landing.
2. **Token-driven color** — monochrome UI (`--color-bg`, `--surface-panel*`, hairlines) plus one accent gradient (`--accent-grad-*` or project-prefixed vars). Accent is punctuation, not wallpaper.
3. **Glass discipline** — `backdrop-blur` on hero eyebrow, CTAs, hero feature cards, and scroll-phase nav only. Body sections use solid panels and hairline borders.
4. **Viewport-aware hero** — `min-h-[calc(100svh-<nav-offset>)]` on the hero panel; respect mobile safe areas.
5. **Reduced motion** — disable rise, gradient shift, and orbit animations under `prefers-reduced-motion: reduce`; set `scroll-behavior: auto` on `html`.
6. **Scroll nav** — fixed nav interpolates width/padding/background; `data-glass` over dark hero, solid pill after scroll threshold. Support `solidNav` for pages without a dark hero.
7. **Accessible structure** — semantic sections, `aria-hidden` on decorative layers, focus-visible outlines on interactive elements.

## Section blueprint (implement in order)

| # | Section ID | Component pattern | Spoke |
|---|------------|-------------------|-------|
| 1 | (hero) | Full-viewport aurora hero + 3 feature cards | [hero-aurora.md](hero-aurora.md) |
| 2 | `#what-is-{{slug}}` | 55/45 intro grid + 3 fact pills | [layout-sections.md](layout-sections.md) |
| 3 | `#connectors` | Centered copy + connector hub | [connector-hub.md](connector-hub.md) |
| 4 | `#product` | Headline + bento features grid | [section-components.md](section-components.md) |
| 5 | (deliverables) | 4-column icon cards | [section-components.md](section-components.md) |
| 6 | `#flow` | Split header + flow preview + `marketing-wash` | [section-components.md](section-components.md) |
| 7 | (comparison) | “Typical vs {{Brand}}” gradient panel rows | [section-components.md](section-components.md) |
| 8 | `#secure` | Split header + security matrix | [section-components.md](section-components.md) |
| 9 | (use-cases) | 4-column persona cards | [layout-sections.md](layout-sections.md) |
| 10 | (faq) | 2-column FAQ cards | [section-components.md](section-components.md) |
| 11 | (footer CTA) | Large wordmark CTA band | [shell-and-nav.md](shell-and-nav.md) |

Wrap all sections in **MarketingShell** → `main` → sections. See [shell-and-nav.md](shell-and-nav.md).

## Spoke routing

| Task | Read |
|------|------|
| Tokens, type, buttons, cards | [foundations.md](foundations.md) |
| Section grids, spacing, max-widths | [layout-sections.md](layout-sections.md) |
| Hero backdrop, cards, orbit | [hero-aurora.md](hero-aurora.md) |
| Shell, nav scroll, footer | [shell-and-nav.md](shell-and-nav.md) |
| Connector grid | [connector-hub.md](connector-hub.md) |
| CSS animations, washes, glass | [motion-and-effects.md](motion-and-effects.md) |
| Bento, comparison, FAQ, previews | [section-components.md](section-components.md) |
| New repo, deps, file tree | [stack-and-scaffold.md](stack-and-scaffold.md) |
| JSON-LD, metadata | [seo-metadata.md](seo-metadata.md) |

## Greenfield checklist

1. Next.js 16+ App Router, React 19, Tailwind CSS v4 — see [stack-and-scaffold.md](stack-and-scaffold.md).
2. Add `globals.css` tokens + marketing utilities + `.public-nav` rules (unlayered, after `@layer utilities`).
3. Implement shell + nav + footer, then hero, then remaining sections top to bottom.
4. Wire CTAs to `{{AppUrl}}` (external app) — marketing site does not embed auth.
5. Add JSON-LD on home per [seo-metadata.md](seo-metadata.md).
6. Verify: hero stagger, nav glass→solid, hub ring, bento breakpoints, reduced-motion, production build.

## Do / don't

| Do | Don't |
|----|-------|
| One gradient accent word per major headline | Gradient-fill every heading |
| Hairline borders + soft shadows on cards | Heavy neumorphism everywhere |
| `text-balance` / `text-pretty` on headlines and body | Fixed pixel widths that break mobile |
| Stagger `animationDelay` 0–320ms on hero children | Identical delay on all elements |
| Keep connector hub to 14 tiles + center mark | Crowd the hub with 20+ icons |

## Reference implementation

If the user has an existing marketing home built with this stack, use it for parity checks only; the skill itself stays brand-agnostic.
