---
name: mcp-exa-search
description: Search the web and find code examples using Exa AI. Use when performing web searches, finding current information, or looking up code examples and documentation. Triggers on "search the web", "find online", "web search", "search for", "find code examples", "Exa search".
---

# Exa AI Search

MCP service at `https://mcp.exa.ai/mcp` (http) with 2 tools.

## Requirements

- `mh` CLI must be installed. If not available, install with:
  ```bash
  curl -fsSL https://raw.githubusercontent.com/vaayne/mcphub/main/scripts/install.sh | sh
  ```

## Usage

```
List tools: `mh list -u https://mcp.exa.ai/mcp -t http`
Get tool details: `mh inspect -u https://mcp.exa.ai/mcp -t http <tool-name>`
Invoke tool: `mh invoke -u https://mcp.exa.ai/mcp -t http <tool-name> '{"param": "value"}'`
```

## Notes

- Run `inspect` before invoking unfamiliar tools to get full parameter schema
- Timeout: 30s default, use `--timeout <seconds>` to adjust
- `getCodeContextExa` is best for programming-related queries (libraries, SDKs, APIs)
- `webSearchExa` returns clean text content ready for LLM use

## Tools

| Tool                | Description                                                                                                                                                                        |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `webSearchExa`      | Search the web for any topic and get clean, ready-to-use content. Best for: current information, news, facts, or answering questions about any topic.                              |
| `getCodeContextExa` | Find code examples, documentation, and programming solutions. Searches GitHub, Stack Overflow, and official docs. Best for: API usage, library examples, code snippets, debugging. |

## Tool Parameters

### `webSearchExa`

```
Required:
  query (string)                — web search query

Optional:
  numResults (number)           — number of results to return (default: 8)
  category (string)             — filter: "company" | "research paper" | "people"
  livecrawl (string)            — "fallback" (default) | "preferred"
  type (string)                 — "auto" (default) | "fast"
  contextMaxCharacters (number) — max chars in response (default: 10000)
```

### `getCodeContextExa`

```
Required:
  query (string)         — search query, e.g. "React useState hook examples"

Optional:
  tokensNum (number)     — tokens to return, 1000–50000 (default: 5000)
```

## Examples

```bash
# Web search
mh invoke -u https://mcp.exa.ai/mcp -t http webSearchExa '{"query": "openclaw plugins"}'

# Web search with options
mh invoke -u https://mcp.exa.ai/mcp -t http webSearchExa '{"query": "Go 1.23 release notes", "numResults": 5}'

# Code context
mh invoke -u https://mcp.exa.ai/mcp -t http getCodeContextExa '{"query": "Go chi router middleware examples"}'
```
