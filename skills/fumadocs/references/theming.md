# Fumadocs Theming

## CSS Setup (Tailwind v4)

```css
@import 'tailwindcss';
@import 'fumadocs-ui/css/<theme>.css';  /* color preset */
@import 'fumadocs-ui/css/preset.css';   /* base styles + animations */
```

For shadcn compatibility: `@import 'fumadocs-ui/css/shadcn.css'` instead of a theme preset.

## Preset Themes

| Theme | Style |
|---|---|
| `neutral` | Gray scale (default) |
| `black` | Pure black/white |
| `vitepress` | VitePress-inspired green |
| `dusk` | Warm dark purple |
| `catppuccin` | Catppuccin palette |
| `ocean` | Blue ocean tones |
| `purple` | Purple accent |
| `solar` | Warm golden |
| `emerald` | Green earth tones |
| `ruby` | Red accent |
| `aspen` | Warm green (nature) |

## fd-* Color Tokens

Override these in a `@theme` block after the imports:

```css
@theme {
  --color-fd-background: hsl(0, 0%, 96%);
  --color-fd-foreground: hsl(0, 0%, 3.9%);
  --color-fd-primary: hsl(0, 0%, 9%);
  --color-fd-primary-foreground: hsl(0, 0%, 98%);
  --color-fd-border: hsla(0, 0%, 80%, 50%);
  --color-fd-ring: hsl(0, 0%, 63.9%);
  --color-fd-accent: hsla(0, 0%, 82%, 50%);
  --color-fd-accent-foreground: hsl(0, 0%, 9%);
  --color-fd-muted: hsl(0, 0%, 96.1%);
  --color-fd-muted-foreground: hsl(0, 0%, 45.1%);
  --color-fd-secondary: hsl(0, 0%, 93.1%);
  --color-fd-secondary-foreground: hsl(0, 0%, 9%);
  --color-fd-card: hsl(0, 0%, 94.7%);
  --color-fd-card-foreground: hsl(0, 0%, 3.9%);
  --color-fd-popover: hsl(0, 0%, 98%);
  --color-fd-popover-foreground: hsl(0, 0%, 15.1%);
  --color-fd-overlay: hsla(0, 0%, 0%, 0.2);
}
```

Dark mode: override inside `.dark { }` selector.

## Static Color Tokens (non-themeable)

These are constant across light/dark:

```css
@theme static {
  --color-fd-info: oklch(62.3% 0.214 259.815);
  --color-fd-warning: oklch(76.9% 0.188 70.08);
  --color-fd-error: oklch(63.7% 0.237 25.331);
  --color-fd-success: oklch(72.3% 0.219 149.579);
  --color-fd-idea: oklch(70.5% 0.209 60.849);
  --color-fd-diff-remove: rgba(200, 10, 100, 0.12);
  --color-fd-diff-remove-symbol: rgb(230, 10, 100);
  --color-fd-diff-add: rgba(14, 180, 100, 0.1);
  --color-fd-diff-add-symbol: rgb(10, 200, 100);
}
```

## Layout Variables

```css
:root {
  --fd-layout-width: 1400px;  /* Max layout width */
  --fd-nav-height: 56px;      /* Navigation bar height */
}
```

## Typography

Fumadocs includes a forked Tailwind typography plugin (loaded via `preset.css`). It applies prose styles inside `DocsBody`. Conflicts with `@tailwindcss/typography` — don't use both.

## RTL Support

Set `dir="rtl"` on `<body>` and pass `dir="rtl"` to `RootProvider`.

## This Project's Overrides

In `web/src/styles.css`, the fd-* tokens are mapped to the warm editorial palette:

| Token | Maps to | Value |
|---|---|---|
| `fd-background` | ivory | `oklch(0.97 0.01 80)` |
| `fd-foreground` | ink | `oklch(0.15 0.01 60)` |
| `fd-primary` | terracotta | `oklch(0.55 0.12 45)` |
| `fd-border` | rule | `oklch(0.85 0.01 75 / 60%)` |
| `fd-muted` | cream | `oklch(0.94 0.015 75)` |
| `fd-muted-foreground` | graphite | `oklch(0.40 0.01 60)` |
