# SEO and metadata

## Page metadata

Use Next.js `Metadata` export on `app/page.tsx`:

```ts
export const metadata: Metadata = publicPageMetadata({
  title: "{{Brand}} | …",
  description: "…",
  path: "/",
});
```

Helper should set:

- `title`, `description`
- `alternates.canonical`
- `openGraph` (title, description, url, siteName, images)
- `twitter` card `summary_large_image`

`metadataBase` in root layout from `getPublicSiteUrl()`.

## JSON-LD on home

Inject in page:

```tsx
<script
  type="application/ld+json"
  dangerouslySetInnerHTML={jsonLd([...schemas])}
/>
```

Recommended types:

| Schema | Purpose |
|--------|---------|
| `SoftwareApplication` | Product name, category, feature list |
| `WebPage` | Page name, description, `isPartOf` website |
| `BreadcrumbList` | `[{ name: "Home", path: "/" }]` |
| `FAQPage` | Map from `homepageFaqs[]` |

Optional sitewide (layout or home):

- `Organization` — name, url, logo, email
- `WebSite` — publisher link

## `jsonLd` helper

```ts
export function jsonLd(data: unknown) {
  return {
    __html: JSON.stringify(data).replace(/</g, "\\u003c"),
  };
}
```

## `siteUrl` helper

```ts
export function siteUrl(path = "/"): string {
  const base = process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000";
  return new URL(path, base).toString();
}
```

Use in schema `@id` and `url` fields.

## Offers / pricing in schema

If marketing site has no pricing page, simplify `SoftwareApplication.offers` to a single free-tier `Offer` or omit `AggregateOffer` rather than importing billing catalogs.

## OG image

- Place `linkprev*.jpg` or PNG in `public/`
- Reference in metadata `images: [{ url: "/…", width, height, alt }]`
- Match twitter `images` array

## Icons

```ts
icons: {
  icon: [
    { url: "/favicon.ico", sizes: "any" },
    { url: "/icon.png", type: "image/png", sizes: "256x256" },
  ],
  apple: [{ url: "/apple-icon.png", sizes: "180x180" }],
}
```

## Content rules

- Description ≤ ~160 chars for SERP
- Title includes brand + primary value prop
- FAQ answers plain text (no markdown in schema strings)
