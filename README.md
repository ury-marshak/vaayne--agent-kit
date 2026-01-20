# agent-kit

Reusable components for AI coding agents: skills, subagents, MCP servers, and extensions.

## What's Inside

| Directory                              | Description                             | For             |
| -------------------------------------- | --------------------------------------- | --------------- |
| [`skills/`](./skills/)                 | Task-specific instructions (15+ skills) | Pi, Claude Code |
| [`agents/`](./agents/)                 | Subagent definitions                    | Pi              |
| [`pi/`](./pi/)                         | Extensions for Pi agent                 | Pi              |
| [`claude-plugins/`](./claude-plugins/) | Slash command plugins                   | Claude Code     |
| [`mcps/`](./mcps/)                     | MCP servers                             | Any MCP client  |

## Quick Start

```bash
git clone https://github.com/vaayne/agent-kit.git
cd agent-kit
```

### Claude Code Plugin Marketplace

```bash
/plugin marketplace add vaayne/agent-kit
```

### Sync to Your Agent

```bash
mise run sync:pi           # Sync skills, agents, extensions to ~/.pi/agent
mise run sync:claude:skills # Sync skills to ~/.claude/skills
mise run sync:codex:skills  # Sync skills to ~/.codex/skills
```

## Highlights

**Skills** — codex-analyze, gemini-analyze, web-search, frontend-design, specs-dev, and more

**Subagents** — librarian (code research), oracle (architecture advisor), ui-engineer, worker

**MCP Servers** — mcp-fs (unified filesystem: S3, WebDAV, FTP, local)

**Pi Extensions** — notify, handoff, permission-gate, status-line

## Development

Requires [mise](https://mise.jdx.dev/) and [uv](https://github.com/astral-sh/uv).

```bash
mise install        # Setup tools
mise run format     # Format code
```

## License

[MIT](./LICENSE)
