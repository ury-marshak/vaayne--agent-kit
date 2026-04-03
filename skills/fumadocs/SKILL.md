---
name: fumadocs
description: >
  Work with Fumadocs documentation framework — add pages, customize themes,
  configure search, use UI components, and manage content sources.
  Use when modifying docs under web/src/content/docs/, working with fumadocs-ui
  components, customizing fd-* CSS tokens, setting up search, or adding new
  documentation pages to the web app.
  Triggers on: "add a doc page", "fumadocs", "docs layout", "docs theme",
  "DocsLayout", "DocsPage", "fd-* tokens", "meta.json", "page tree",
  "docs search", "content source", "fumadocs component".
---

# Fumadocs

Documentation framework powering the `/docs` section of the web app.

## Project Setup

This project uses fumadocs with **TanStack Start** (not Next.js):

- **Content**: `web/src/content/docs/*.md` — auto-discovered via `import.meta.glob`
- **Source/Loader**: `web/src/lib/source.ts` — `source()` + `loader()` from `fumadocs-core/source`
- **Markdown Renderer**: `web/src/lib/markdown.ts` — sync `createMarkdownRenderer` with remark-gfm + rehype-highlight
- **Routes**: `web/src/routes/docs/` — layout (`route.tsx`), index, `$slug` catch-all
- **Theme**: `web/src/styles.css` — fd-* token overrides for warm editorial palette

## Adding a Doc Page

1. Create `web/src/content/docs/<name>.md`:
   ```markdown
   ---
   title: Page Title
   description: Short description.
   ---

   Content here...
   ```
2. Add `"<name>"` to `web/src/content/docs/meta.json` `pages` array.
3. Done — auto-discovered, no route changes needed.

## meta.json

Controls page ordering per directory:

```json
{
  "title": "Section Name",
  "pages": ["index", "page-a", "page-b"]
}
```

Special syntax: `"---"` (separator), `"[Name](url)"` (external link), `"...folder"` (expand).

## Key UI Components

| Component         | Import                          | Purpose                 |
| ----------------- | ------------------------------- | ----------------------- |
| `DocsLayout`      | `fumadocs-ui/layouts/docs`      | Sidebar + nav wrapper   |
| `DocsPage`        | `fumadocs-ui/page`              | Page container with TOC |
| `DocsTitle`       | `fumadocs-ui/page`              | Page heading            |
| `DocsDescription` | `fumadocs-ui/page`              | Page subtitle           |
| `DocsBody`        | `fumadocs-ui/page`              | Prose content area      |
| `RootProvider`    | `fumadocs-ui/provider/tanstack` | Root wrapper (TanStack) |

For more components (Tabs, Accordion, Steps, CodeBlock, Cards, Banner, etc.), read `references/components.md`.

## Theming

Override `--color-fd-*` tokens in `@theme` block after importing `fumadocs-ui/css/preset.css`:

```css
@theme {
  --color-fd-background: oklch(...);
  --color-fd-primary: oklch(...);
  /* ... */
}
```

11 preset themes available: neutral, black, vitepress, dusk, catppuccin, ocean, purple, solar, emerald, ruby, aspen.

For full token reference, read `references/theming.md`.

## Source API

```typescript
import { source, loader } from "fumadocs-core/source"

const s = source({ pages: [...], metas: [...] })
const docs = loader(s, { baseUrl: "/docs" })

docs.pageTree    // Root tree for DocsLayout
docs.getPage([]) // Get page by slug array
docs.getPages()  // All pages
```

For full source/loader API, read `references/source-api.md`.
