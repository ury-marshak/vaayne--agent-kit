---
name: mcp-grep-code
description: Search real-world code examples from over a million public GitHub repositories. Use when finding code patterns, implementation examples, or how libraries are used in practice. Triggers on "find code examples", "how is [library] used", "search GitHub code", "grep.app search", "code pattern".
---

# Grep.app Code Search

MCP service at `https://mcp.grep.app` (http) with 1 tool.

## Requirements

- `mh` CLI must be installed. If not available, install with:
  ```bash
  curl -fsSL https://raw.githubusercontent.com/vaayne/mcphub/main/scripts/install.sh | sh
  ```

## Usage

```
List tools: `mh list -u https://mcp.grep.app -t http`
Get tool details: `mh inspect -u https://mcp.grep.app -t http searchGitHub`
Invoke tool: `mh invoke -u https://mcp.grep.app -t http searchGitHub '{"query": "pattern"}'`
```

## Notes

- Run `inspect` before invoking unfamiliar tools to get full parameter schema
- Timeout: 30s default, use `--timeout <seconds>` to adjust
- **Important**: This searches for literal code patterns (like grep), NOT keywords
- Use actual code that would appear in files, not descriptions
- Use `useRegexp=true` with `(?s)` prefix for multi-line patterns

## Tools

| Tool | Description |
| ---- | ----------- |
| `searchGitHub` | Find real-world code examples from public GitHub repositories. Searches for literal code patterns across millions of repos. |

## Tool Parameters

### `searchGitHub`

```
Required:
  query (string)             — literal code pattern, e.g. "useState(" or "import React from"

Optional:
  language (array)           — filter by language, e.g. ["TypeScript", "TSX"], ["Python"]
  repo (string)              — filter by repo, e.g. "facebook/react" or "vercel/"
  path (string)              — filter by file path, e.g. "src/components" or "/route.ts"
  useRegexp (boolean)        — treat query as regex (default: false)
  matchCase (boolean)        — case-sensitive search (default: false)
  matchWholeWords (boolean)  — match whole words only (default: false)
```

## Search Tips

**Good queries** (literal code patterns):
- `useState(`
- `import React from`
- `async function`
- `(?s)try {.*await`

**Bad queries** (keywords — won't work well):
- `react state management`
- `how to use hooks`

## Examples

```bash
# Find useState usage patterns
mh invoke -u https://mcp.grep.app -t http searchGitHub '{"query": "useState("}'

# Find async/await patterns in TypeScript
mh invoke -u https://mcp.grep.app -t http searchGitHub '{"query": "async function fetch", "language": ["TypeScript"]}'

# Find multi-line patterns with regex
mh invoke -u https://mcp.grep.app -t http searchGitHub '{"query": "(?s)useEffect\\(\\(\\) => {.*removeEventListener", "useRegexp": true}'

# Search within a specific repo
mh invoke -u https://mcp.grep.app -t http searchGitHub '{"query": "from \"openai\"", "repo": "vercel/ai"}'
```
