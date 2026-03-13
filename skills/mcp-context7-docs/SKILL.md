---
name: mcp-context7-docs
description: Query up-to-date documentation and code examples for any programming library or framework. Use when looking up API docs, finding code examples, or checking library usage. Triggers on "how to use [library]", "docs for [package]", "show me examples of [framework]", "Context7 lookup".
---

# Context7 Documentation

MCP service at `https://mcp.context7.com/mcp` (http) with 2 tools.

## Requirements

- `mh` CLI must be installed. If not available, install with:
  ```bash
  curl -fsSL https://raw.githubusercontent.com/vaayne/mcphub/main/scripts/install.sh | sh
  ```

## Usage

```
List tools: `mh list -u https://mcp.context7.com/mcp -t http`
Get tool details: `mh inspect -u https://mcp.context7.com/mcp -t http <tool-name>`
Invoke tool: `mh invoke -u https://mcp.context7.com/mcp -t http <tool-name> '{"param": "value"}'`
```

## Notes

- Run `inspect` before invoking unfamiliar tools to get full parameter schema
- Timeout: 30s default, use `--timeout <seconds>` to adjust
- **Important**: Always call `resolveLibraryId` first to get the Context7-compatible library ID before calling `queryDocs`, unless user provides ID in `/org/project` format
- Do not call either tool more than 3 times per question

## Tools

| Tool               | Description                                                                                                                                                         |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `resolveLibraryId` | Resolves a package/product name to a Context7-compatible library ID. Must be called before `queryDocs` to get a valid library ID.                                   |
| `queryDocs`        | Retrieves and queries up-to-date documentation and code examples from Context7 for any programming library or framework. Requires a Context7-compatible library ID. |

## Tool Parameters

### `resolveLibraryId`

```
Required:
  libraryName (string)  — library name to search for, e.g. "react", "nextjs"
  query (string)        — the question or task you need help with (used for ranking)
```

### `queryDocs`

```
Required:
  libraryId (string)    — exact Context7 ID, e.g. "/vercel/next.js" or "/vercel/next.js/v14"
  query (string)        — specific question, e.g. "How to set up JWT authentication in Express.js"
```

## Workflow

1. **Resolve library ID** — get the Context7-compatible ID for the library:
   ```bash
   mh invoke -u https://mcp.context7.com/mcp -t http resolveLibraryId '{"libraryName": "react", "query": "useState hook examples"}'
   ```

2. **Query documentation** — use the resolved ID to fetch docs:
   ```bash
   mh invoke -u https://mcp.context7.com/mcp -t http queryDocs '{"libraryId": "/facebook/react", "query": "how to use useState hook"}'
   ```
