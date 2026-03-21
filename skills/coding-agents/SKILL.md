---
name: coding-agents
description: Guide for invoking external coding agents (Codex, Claude Code, Gemini) from the CLI to review code, perform tasks, or get second opinions. Use when the user wants to delegate work to another AI agent, run code reviews externally, or needs help choosing between available coding agents.
metadata:
  os:
    - darwin
    - linux
---

# Coding Agents CLI Guide

Use external coding agents to get second opinions, parallel reviews, or delegate tasks that benefit from a fresh context.

## When to Use Which Agent

| Agent                  | Best For                                    | Model              | Key Strength                                 |
| ---------------------- | ------------------------------------------- | ------------------ | -------------------------------------------- |
| **Codex** (`codex`)    | Code review, sandboxed exec                 | OpenAI o3/o4-mini  | Built-in `review` command, strict sandboxing |
| **Claude Code** (`cc`) | Complex multi-file tasks, agentic workflows | Claude Opus/Sonnet | Rich tool ecosystem, worktrees, MCP support  |
| **Gemini** (`gemini`)  | Quick one-shot prompts, codebase Q&A        | Gemini 2.5         | Free tier, fast responses                    |

## Quick Reference

### Code Review

```bash
# Codex — review uncommitted changes (no permissions needed)
codex review --uncommitted

# Codex — review against a base branch
codex review --base main

# Claude Code — review via print mode
cc -p "Review the uncommitted changes in this repo for bugs and improvements"

# Gemini — review via prompt mode
gemini -p "Review the recent changes and suggest improvements"
```

### One-Shot Tasks

```bash
# Codex — non-interactive exec
codex exec "Fix the failing test in src/utils.test.ts"

# Claude Code — non-interactive print
cc -p "Explain what src/index.ts does"

# Gemini — non-interactive prompt
gemini -p "Summarize the architecture of this project"
```

### Interactive Sessions

```bash
# Codex — interactive with full-auto sandbox
codex --full-auto

# Claude Code — interactive (default)
cc

# Gemini — interactive (default)
gemini
```

## Tips

- **Second opinion on code review**: Run `codex review --uncommitted` from within Claude Code via Bash to get an independent review without self-bias.
- **Parallel agents**: Use tmux to run multiple agents simultaneously on different tasks.
- **Piping**: All three support piping stdin — e.g., `git diff | cc -p "Review this diff"`.
- **Model override**: Each agent supports model selection (`codex -m o3`, `cc --model opus`, `gemini -m gemini-2.5-flash`).

## Detailed References

- [Codex CLI](./references/codex.md) — full command reference, review/exec modes, sandbox options
- [Claude Code CLI](./references/claude-code.md) — cc alias, print mode, worktrees, permission modes
- [Gemini CLI](./references/gemini.md) — installation, prompt mode, output formats
