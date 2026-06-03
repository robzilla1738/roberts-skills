# Motion and effects — CSS only

## Entrance: `.marketing-rise`

```css
@keyframes marketing-rise {
  from {
    opacity: 0;
    transform: translateY(14px);
    filter: blur(6px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
    filter: blur(0);
  }
}

.marketing-rise {
  animation: marketing-rise 560ms cubic-bezier(0.2, 0, 0, 1) both;
}
```

Stagger via inline `style={{ animationDelay: "80ms" }}` on children.

## Accent gradient text: `.accent-gradient-text`

(Map from reference `.joy-gradient-text`)

- `background-clip: text`, transparent color
- `background-size: 200% 100%`
- `animation: accent-gradient-shift 12s ease-in-out infinite`

```css
@keyframes accent-gradient-shift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}
```

## Section washes

### `.marketing-wash`

Multi-layer cyan/blue linear gradients + vertical **mask** fading top/bottom so band blends into page (symmetric bell curve in mask stops).

### `.marketing-wash-top`

Stronger top anchor — mask keeps top opaque, fades to transparent at bottom. Use when wash should anchor below a heading.

Apply on `absolute inset-0 -z-10` inside `relative isolate` section.

## Hero feature card: `.hero-feature-card`

- `border-radius: 30px`, white/translucent border
- Layered `radial-gradient` + `linear-gradient` fill
- `backdrop-filter: blur(36px) saturate(1.18)`
- `::before` highlight gradient, `::after` screen blend sheen
- Dark theme variant: deeper gray fill + subtle accent tint

## Connector orbit

```css
.joy-card-arc {
  animation: joy-card-arc-spin 34s linear infinite;
  transform-origin: center;
}
.joy-card-icon {
  animation: joy-card-icon-counter 34s linear infinite;
}
```

Rename to neutral `.orbit-arc` / `.orbit-icon` in new projects if desired.

## Hub ring: `.hub-center-ring`

`conic-gradient` stroke via padding + mask-composite exclude (see [connector-hub.md](connector-hub.md)).

## Pressable

```css
.pressable:active { transform: scale(0.96); }
```

180ms transitions on buttons/links.

## Smooth scroll

```css
html { scroll-behavior: smooth; }
```

Disable in reduced-motion block.

## Public nav glass (unlayered CSS)

Place **after** `@layer utilities` so rules beat Tailwind hover utilities.

Key selectors:

- `.public-nav[data-glass] .public-nav-link` — white text
- `.public-nav[data-glass] .public-nav-cta` — white pill, ink text
- `.public-nav:not([data-glass]) .public-nav-cta` — ink fill
- Logo cross-fade `.public-nav-logo--glass` / `--solid`

Nav component sets `data-glass` when `scrollY < threshold` and page has dark hero.

## Reduced motion

```css
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  .marketing-rise { animation: none; }
  .accent-gradient-text { animation: none; }
  .joy-card-arc, .joy-card-icon { animation: none; }
  .pressable { transition-duration: 1ms; }
}
```

## Explicitly avoid on landing

- Framer Motion layout animations
- Scroll-jacking parallax
- Canvas/WebGL particles (unless new creative direction)
- `animation` on `width`/`height` of nav (use `transform`/`opacity` or interpolated inline styles sparingly)
