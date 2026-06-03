# Hero — aurora panel, feature cards, orbit

## Structure

```tsx
<section className="relative isolate overflow-hidden pb-20 sm:pb-28">
  <div className="relative isolate flex min-h-[calc(100svh-4.25rem)] items-center
    overflow-hidden rounded-b-[36px] border-b border-white/24
    px-4 pb-28 pt-28 sm:px-6 lg:px-8 ...">
    <HeroPanelBackdrop />
    <div className="mx-auto w-full max-w-[90rem]">
      {/* centered copy stack */}
      {/* 3-col feature cards, overlapping bottom */}
    </div>
  </div>
</section>
```

Nav offset `4.25rem` matches fixed nav height. Use `100svh` not `100vh`.

## Backdrop variants

Switch via constant (e.g. `HERO_BACKDROP_VARIANT: "blue" | "spectrum"`).

### Blue (default)

Layered absolutely positioned divs inside backdrop wrapper:

1. Base `linear-gradient` navy → electric blue (vertical)
2. `radial-gradient` blooms at top-left / top-right (cyan, low opacity)
3. Optional fine noise or vignette via extra radial at bottom

All `pointer-events-none`, `aria-hidden`, `-z-10`.

### Spectrum (alternate)

SVG/CSS band component with blur filter — keep behind feature flag so teams can A/B without deleting code.

## Copy stack (centered)

Apply `.marketing-rise` + inline `animationDelay` stagger:

| Element | Delay |
|---------|-------|
| Eyebrow pill | 0ms |
| H1 | 80ms |
| Subcopy | 160ms |
| CTA row | 240ms |
| Feature cards row | 320ms+ |

### Eyebrow pill

`rounded-full border border-white/30 bg-white/14 backdrop-blur-md`  
Uppercase `10.5px`, white/80 text, dot indicator `h-1.5 w-1.5 rounded-full bg-white`.

### H1

White text, heavy drop-shadow, optional line breaks for rhythm. One line may use plain white (no gradient) for contrast.

### CTAs

- Primary: white pill → `{{AppUrl}}`, dark ink text, `pressable`
- Secondary: glass outline `border-white/30 bg-white/10 backdrop-blur-md` → docs or video

## Three feature cards (`lg:grid-cols-3`)

Shared class `.hero-feature-card` — see [motion-and-effects.md](motion-and-effects.md).

| Card | Purpose | Visual |
|------|---------|--------|
| Output | Show generated artifact preview | Mock document/list UI inside card |
| Orbit | Integrations | Rotating brand ring (`.joy-card-arc` / icons) |
| Approvals | Trust | Checklist / approval states |

Cards sit in a row that overlaps hero bottom (`-mb-*` or positioned below fold). Equal height via `h-full` flex column.

## Orbit card mechanics

- SVG or div arc path with icons at nodes
- Parent: `.joy-card-arc` rotates 360° / 34s linear infinite
- Each icon child: `.joy-card-icon` counter-rotates -360° / 34s (icons stay upright)
- Brands from `{{Connectors[]}}` subset (7 items typical)

## Hero panel polish

- `rounded-b-[36px]` — large bottom radius merges into page
- `border-b border-white/24`
- `shadow-[0_32px_100px_rgba(20,17,31,0.10)]`

## Don't

- Put Framer Motion on hero entrance (use CSS `.marketing-rise`)
- Use video/WebGL backdrops unless brand explicitly requires it
- Apply glass to entire page — only hero chrome and cards
