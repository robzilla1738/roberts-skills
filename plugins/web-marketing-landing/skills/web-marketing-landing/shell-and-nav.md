# Shell, navigation, footer

## MarketingShell

```tsx
<div className="marketing-shell min-h-screen overflow-x-clip bg-[var(--color-bg)]">
  <PublicNav active={active} solid={solidNav} />
  {children}
  <PublicFooter backdrop={footerBackdrop} />
</div>
```

Props:

| Prop | Purpose |
|------|---------|
| `active` | Highlights current nav item |
| `solidNav` | Force solid nav from scroll 0 (pricing, legal pages) |
| `footerBackdrop` | Optional decorative node behind footer; default giant wordmark |

Export constants: support email, last-updated string for legal footers.

## PublicNav (client component)

Fixed top bar; listens to `scroll` and `resize`.

### Scroll interpolation

Between `scrollY` 0 and ~120–160px, interpolate:

- Nav container `max-width` (e.g. full → `72rem`)
- Horizontal padding
- `borderRadius` (0 → pill)
- `backgroundColor` / `borderColor` (transparent → elevated surface)
- Toggle `data-glass` attribute when over hero (dark) zone

`data-glass` drives CSS in unlayered `.public-nav[data-glass]` rules — white links, white CTA pill, glass dropdown viewport. See [motion-and-effects.md](motion-and-effects.md).

### Structure

- Logo: dual assets — `.public-nav-logo--glass` (white) and `--solid` (default); cross-fade via opacity
- Desktop: Radix `NavigationMenu` with Product / Company dropdowns
- Mobile: menu button + sheet or stacked panel
- CTAs: Sign in (ghost) + Open app (filled) → `{{AppUrl}}`

### Mega-menu items

Link to in-page hashes (`/#product`) and standalone routes (`/integrations`). Descriptions one line each; lucide icon per item.

## PublicFooter

Three-column grid `md:grid-cols-[1.1fr_1fr_1fr]`:

1. Brand blurb + logo
2. Product links
3. Company / legal links

Optional `backdrop` slot: absolute `inset-0 -z-10` decorative wordmark (low contrast, huge type).

## FooterWordmark (home CTA band)

Final section before footer:

- Large display headline or outlined wordmark
- Short subcopy
- Primary CTA → `{{AppUrl}}`
- Contained card with gradient border or wash

Distinct from footer link grid — this is the **conversion** band.

## Nav height contract

Document nav height in one constant shared with hero `calc(100svh - <nav>)` if nav size changes.

## External app links

Marketing site does not host auth. All “Open app” / “Get started” hrefs point to `{{AppUrl}}` (e.g. `https://app.example.com`).

## Accessibility

- `suppressHydrationWarning` on `<html>` if theme toggle exists
- Mobile menu: focus trap, `aria-expanded` on toggle
- Skip link optional for keyboard users
