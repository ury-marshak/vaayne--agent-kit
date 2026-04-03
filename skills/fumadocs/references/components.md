# Fumadocs UI Components

## Layout Components

### DocsLayout

```tsx
import { DocsLayout } from "fumadocs-ui/layouts/docs";

<DocsLayout
  tree={pageTree} // Root from loader
  nav={{ title: "Docs", url: "/docs" }}
  links={[{ text: "Home", url: "/" }]}
  sidebar={{ defaultOpenLevel: 1, collapsible: true }}
>
  {children}
</DocsLayout>;
```

Props: `tree`, `nav`, `links`, `sidebar`, `tabMode`, `tabs`, `containerProps`, `slots`.

### DocsPage

```tsx
import {
  DocsPage,
  DocsTitle,
  DocsDescription,
  DocsBody,
} from "fumadocs-ui/page";

<DocsPage>
  <DocsTitle>Page Title</DocsTitle>
  <DocsDescription>Subtitle text.</DocsDescription>
  <DocsBody>{content}</DocsBody>
</DocsPage>;
```

Props: `editOnGithub`, `lastUpdate`, `children`.

### RootProvider

Framework-specific wrapper. For TanStack Start:

```tsx
import { RootProvider } from "fumadocs-ui/provider/tanstack";
```

Other frameworks: `fumadocs-ui/provider` (Next.js), `fumadocs-ui/provider/react-router`.

### HomeLayout

Minimal navbar + search for non-docs pages:

```tsx
import { HomeLayout } from "fumadocs-ui/layouts/home";
```

## Content Components

### Tabs

```tsx
import { Tab, Tabs } from "fumadocs-ui/components/tabs";

<Tabs items={["npm", "pnpm", "yarn"]} groupId="pkg" persist>
  <Tab value="npm">npm install pkg</Tab>
  <Tab value="pnpm">pnpm add pkg</Tab>
  <Tab value="yarn">yarn add pkg</Tab>
</Tabs>;
```

Props: `items`, `groupId` (sync across instances), `persist` (localStorage), `updateAnchor`.

### Accordion

```tsx
import { Accordion, Accordions } from "fumadocs-ui/components/accordion";

<Accordions type="single">
  <Accordion title="Question?" id="q1">
    Answer here.
  </Accordion>
</Accordions>;
```

Supports hash navigation via `id` prop.

### Steps

```tsx
import { Step, Steps } from "fumadocs-ui/components/steps";

<Steps>
  <Step>First step content</Step>
  <Step>Second step content</Step>
</Steps>;
```

Or use Tailwind utilities directly: `fd-steps` on wrapper, `fd-step` on children.

### CodeBlock

```tsx
import { CodeBlock, Pre } from "fumadocs-ui/components/codeblock";

<CodeBlock title="example.ts" lang="typescript">
  <Pre>{code}</Pre>
</CodeBlock>;
```

Features: copy button, title bar, icon, `keepBackground` for Shiki colors.

### DynamicCodeBlock

Client-side highlighting for runtime content:

```tsx
import { DynamicCodeBlock } from "fumadocs-ui/components/dynamic-codeblock";

<DynamicCodeBlock lang="json" code={jsonString} />;
```

### Banner

```tsx
import { Banner } from "fumadocs-ui/components/banner";

<Banner id="v2-release" variant="rainbow">
  Version 2.0 is out!
</Banner>;
```

Dismissible when `id` is set (persists to localStorage).

### InlineTOC

```tsx
import { InlineTOC } from "fumadocs-ui/components/inline-toc";

<InlineTOC items={tocItems} />;
```

### ImageZoom

```tsx
import { ImageZoom } from "fumadocs-ui/components/image-zoom";

<ImageZoom src="/screenshot.png" alt="Screenshot" />;
```

### Files

```tsx
import { Files, File, Folder } from "fumadocs-ui/components/files";

<Files>
  <Folder name="src" defaultOpen>
    <File name="index.ts" />
    <File name="utils.ts" />
  </Folder>
</Files>;
```

### TypeTable

```tsx
import { TypeTable } from "fumadocs-ui/components/type-table";

<TypeTable
  type={{
    name: { type: "string", description: "The name", default: "'default'" },
    count: { type: "number", description: "Item count" },
  }}
/>;
```

### Cards

```tsx
import { Card, Cards } from "fumadocs-ui/components/card";

<Cards>
  <Card title="Getting Started" href="/docs" />
  <Card title="API Reference" href="/docs/api" />
</Cards>;
```

### Callout

```tsx
import { Callout } from "fumadocs-ui/components/callout"

<Callout type="info" title="Note">Important information.</Callout>
<Callout type="warn">Warning message.</Callout>
<Callout type="error">Error details.</Callout>
```

Types: `info`, `warn`, `error`.
