# Stack and scaffold — greenfield repo

## Recommended stack

| Package | Version | Role |
|---------|---------|------|
| `next` | 16.x | App Router, `next/font`, metadata |
| `react` / `react-dom` | 19.x | UI |
| `tailwindcss` | 4.x | Utilities |
| `@tailwindcss/postcss` | 4.x | PostCSS plugin |
| `typescript` | 5.9+ | Types |
| `lucide-react` | latest | Section icons |
| `@radix-ui/react-navigation-menu` | 1.2+ | Nav mega-menu |
| `react-icons` | optional | Brand / connector glyphs |
| `clsx` + `tailwind-merge` | latest | `cn()` helper |
| `geist` | optional | Mono font |

**Not required:** `framer-motion`, Clerk (marketing-only site links out to app).

## File tree (marketing-only)

```
app/
  layout.tsx          # fonts, metadata, globals.css
  page.tsx            # home sections + data arrays
  globals.css         # tokens + marketing utilities + .public-nav
  fonts/              # display OTF files
components/
  marketing/
    MarketingShell.tsx
    PublicNav.tsx
    HeroAurora.tsx
    ConnectorHub.tsx
    FooterWordmark.tsx
    ProductPreview.tsx   # flow + security exports
  ui/
    features-8.tsx       # or Features.tsx
    BrandIcon.tsx
    BrandLogoMark.tsx
    Card.tsx
    navigation-menu.tsx
    menu-toggle-icon.tsx
    cosmos-spectrum.tsx  # optional hero variant
lib/
  cn.ts
  seo.ts
  site-url.ts
public/
  brand/
  icons/connectors/
postcss.config.mjs
tsconfig.json           # paths: "@/*": ["./*"]
```

## `layout.tsx` essentials

- Import `./globals.css`
- `Poppins` + local display font variables on `<html>`
- No auth provider on marketing-only deploy
- `metadata` / `metadataBase` for OG images in `public/`

## `globals.css` load order

1. `@import "tailwindcss"`
2. `@theme { ... }`
3. `:root` tokens + `[data-theme="dark"]`
4. Base `html, body`
5. `.marketing-shell`
6. `@layer components` — buttons if used
7. `@layer utilities` — `.marketing-rise`, washes, cards, orbit
8. **Unlayered** `.public-nav[...]` rules last

## Environment

```env
NEXT_PUBLIC_SITE_URL=https://www.example.com
NEXT_PUBLIC_APP_URL=https://app.example.com
```

Use `NEXT_PUBLIC_APP_URL` for all “Open app” CTAs.

## Port checklist from reference

When cloning from a reference implementation:

1. Copy marketing components + UI dependencies (trace imports).
2. Copy marketing slice of `globals.css` (tokens + utilities + nav).
3. Copy `page.tsx` structure; replace copy with `{{Brand}}`.
4. Copy `public/brand` and connector SVGs.
5. Simplify `lib/seo.ts` if billing/catalog deps exist in reference.
6. Remove unused product/chat CSS from globals (~50% reduction possible).
7. Run `pnpm build` and fix missing imports.

## Scripts

```json
{
  "scripts": {
    "dev": "next dev --turbopack",
    "build": "next build",
    "start": "next start",
    "lint": "eslint ."
  }
}
```

## Stub routes

Nav/footer may link to `/pricing`, `/integrations`, `/docs`. For v1 marketing-only:

- Return minimal `MarketingShell` + “Coming soon”, or
- `redirect()` to canonical site, or
- `href` to external docs

Document choice in project README.

## Fonts fallback

If display OTF is unavailable, fallback stack in `.marketing-shell` headings:

```css
font-family: var(--font-display), var(--font-sans);
```

Use a licensed display face or Georgia as interim.
