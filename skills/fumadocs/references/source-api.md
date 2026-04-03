# Fumadocs Source & Loader API

## Overview

The source/loader system builds a page tree and page lookup from virtual files. This project uses it with `import.meta.glob` for auto-discovery (see `web/src/lib/source.ts`).

## source()

Creates a Source object from virtual pages and metas:

```typescript
import { source } from "fumadocs-core/source"

const s = source({
  pages: [
    {
      type: "page",
      path: "docs/getting-started.md",
      data: { title: "Getting Started", description: "..." },
    },
  ],
  metas: [
    {
      type: "meta",
      path: "docs/meta.json",
      data: { title: "Docs", pages: ["getting-started", "api"] },
    },
  ],
})
```

### VirtualPage

```typescript
{
  type: "page"
  path: string           // Virtual path (e.g., "docs/page.md")
  slugs?: string[]       // Override URL slugs (auto-generated if omitted)
  data: {
    title?: string
    description?: string
    icon?: string
  }
}
```

### VirtualMeta

```typescript
{
  type: "meta"
  path: string           // Virtual path (e.g., "docs/meta.json")
  data: {
    title?: string
    pages?: string[]     // Ordered page/folder names
    root?: boolean
    defaultOpen?: boolean
    collapsible?: boolean
    icon?: string
  }
}
```

## loader()

Builds a complete documentation source with tree, pages, and lookup functions:

```typescript
import { loader } from "fumadocs-core/source"

const docs = loader(s, {
  baseUrl: "/docs",           // URL prefix
  // Optional:
  url?: (slugs, locale) => string,  // Custom URL builder
  i18n?: { ... },                    // i18n config
  icon?: (icon) => ReactNode,       // Icon resolver
  plugins?: [...],                   // Loader plugins
})
```

### Returned API

```typescript
docs.pageTree                          // Root tree for DocsLayout
docs.getPage(slugs: string[])         // Get page by slug array
docs.getPages(locale?: string)        // All pages
docs.getPageByHref(href, opts?)       // Lookup by URL
docs.getNodeMeta(folder, locale?)     // Folder metadata
docs.getNodePage(item, locale?)       // Page from tree item
docs.resolveHref(href, parentPage)    // Resolve relative links

// SSG helpers
docs.generateParams(slugParam?, langParam?)  // For static generation
docs.serializePageTree(tree)                 // Serialize for client
```

### Page Object

```typescript
{
  path: string          // Virtual path
  absolutePath?: string
  slugs: string[]       // URL segments
  url: string           // Full URL (baseUrl + slugs)
  data: PageData        // Frontmatter
  locale?: string
}
```

## multiple()

Merge multiple sources (e.g., docs + blog):

```typescript
import { multiple } from "fumadocs-core/source"

const combined = multiple({
  docs: docsSource,
  blog: blogSource,
})

const all = loader(combined, { baseUrl: "/" })
// Pages have `type` field: "docs" | "blog"
```

## update()

Mutate source in-place (e.g., for access control):

```typescript
import { update } from "fumadocs-core/source"

const filtered = update(s)
  .page((page) => {
    if (page.data.private) return null // Remove page
    return page
  })
  .build()
```

## Loader Plugins

```typescript
const myPlugin: LoaderPlugin = {
  name: "my-plugin",
  enforce: "pre",  // or "post"
  transformStorage({ storage }) {
    // Modify virtual filesystem
  },
  transformPageTree: {
    file(node, filePath) { return node },
    folder(node, folderPath) { return node },
    root(node) { return node },
  },
}

loader(s, { baseUrl: "/docs", plugins: [myPlugin] })
```

## Page Tree Structure

```typescript
interface Root {
  name: ReactNode
  children: Node[]
}

type Node = Item | Separator | Folder

interface Item {
  type: "page"
  name: ReactNode
  url: string
  icon?: ReactNode
  external?: boolean
}

interface Folder {
  type: "folder"
  name: ReactNode
  children: Node[]
  index?: Item
  defaultOpen?: boolean
  collapsible?: boolean
}

interface Separator {
  type: "separator"
  name?: ReactNode
}
```

### Tree Utilities

```typescript
import { flattenTree, visit, findPath, findNeighbour } from "fumadocs-core/page-tree"

flattenTree(root)              // All pages as flat array
visit(root, fn)                // Traverse tree
findPath(root, url)            // Breadcrumb path to URL
findNeighbour(root, node)      // { prev?, next? } for pagination
```

## This Project's Source Setup

`web/src/lib/source.ts`:
- Uses `import.meta.glob("/src/content/docs/**/*.md", { query: "?raw", eager: true })` to discover all .md files
- Parses frontmatter to extract title/description
- Loads `meta.json` files for ordering
- Exports `docs` (loader output) and `getDocContent(slugs)` for raw markdown access
