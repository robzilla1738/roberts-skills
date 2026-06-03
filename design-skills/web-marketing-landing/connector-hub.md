# Connector hub — 5×3 grid

## Purpose

Visual proof of integrations without a scrolling logo strip. Center cell is the product mark; 14 surrounding cells are connector brands.

## Grid geometry

- **Layout:** CSS grid `grid-cols-5` × 3 rows = 15 cells
- **Center index:** 7 (0-based) or “middle of 15” — leave empty for brand mark
- **Tile count:** 14 connectors

Example slot order (clockwise from top-left):

```
[0][1][2][3][4]
[5][6][X][8][9]   X = center brand
[10][11][12][13][14]
```

Implement as flat array with `null` or sentinel at index 7, or explicit 5×3 matrix.

## Container

```tsx
<div className="relative isolate overflow-hidden py-1">
  {/* horizontal glow band */}
  <div className="relative mx-auto max-w-[24rem] sm:max-w-3xl">
    <div className="grid grid-cols-5 gap-2 sm:gap-3">
      {/* tiles */}
    </div>
  </div>
</div>
```

## Horizontal glow

Absolutely positioned behind grid:

```css
background: linear-gradient(90deg, transparent, cyan-12%, blue-10%, transparent);
mask-image: linear-gradient(to bottom, transparent, black 24%, black 76%, transparent);
```

Low opacity (`~0.65`), centered vertically on grid.

## Center cell

Wrap brand mark in `.hub-center-ring`:

- `conic-gradient` cyan → navy → cyan
- 2px padding ring via mask-composite exclude
- Soft shadow + white hairline

Mark size ~`h-12 w-12` inside padded circle on elevated white/dark circle.

## Connector tiles

Each tile:

- Rounded square `aspect-square`
- Border `hairline`, bg `elevated`
- Centered brand icon (SVG or react-icons)
- Hover: slight scale or border strengthen

Use `brandIsSelfContained` (or equivalent) to skip extra padding on marks that include their own background.

## Data

```ts
const HUB_TILES: (BrandKey | "center")[] = [ ... ];
```

`BrandKey` union type for allowed icons. Source SVGs from `public/icons/connectors/*.svg` or icon library.

## Section wrapper

Parent section `#connectors`:

- Centered `max-w-2xl` headline block
- Eyebrow + H2 with one `.accent-gradient-text` span
- Secondary CTA → integrations page
- `mt-12 sm:mt-14` before hub

## Don't

- Animate entire grid on scroll (static + optional hover only)
- Use more than 14 outer tiles without redesigning grid
- Mix unrelated icon sizes — normalize to `h-6 w-6` or `h-7 w-7`
