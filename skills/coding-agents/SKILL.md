---
name: coding-agents
description: Guide for invoking external coding agents (Codex, Claude Code, Gemini) from the CLI to review code, perform tasks, or get second opinions. Use when the user wants to delegate work to another AI agent, run code reviews externally, or needs help choosing between available coding agents.
metadata:
  os:
    - darwin
    - linux
---

# Coding Agents CLI Guide

## Agent Overview

| Agent       | Command  | Default Model | Best For                            |
| ----------- | -------- | ------------- | ----------------------------------- |
| Codex       | `codex`  | gpt-5.4       | Code review, sandboxed exec         |
| Claude Code | `claude` | Opus 4.6      | Multi-file tasks, agentic workflows |
| Gemini      | `gemini` | Gemini 2.5    | One-shot prompts (not installed)    |

> `cc` is a local shell alias for `claude` with Bedrock + bypass permissions. Use `claude` when `cc` is unavailable.

## Claude Code Models (`claude --model`)

| Alias    | Use When                                    |
| -------- | ------------------------------------------- |
| `opus`   | Complex refactors, architecture, multi-file |
| `sonnet` | Default — 80% of tasks, good speed/quality  |
| `haiku`  | Simple lookups, boilerplate, bulk queries   |

## Quick Reference

```bash
# Code review
codex review --uncommitted            # Independent review
codex review --base main              # Review against branch
claude -p "Review uncommitted changes"

# One-shot tasks
codex exec "Fix the failing test"
claude -p "Explain what src/index.ts does"
claude --model haiku -p "Summarize this file"

# Interactive
codex --full-auto                     # Sandboxed, approval on-request
claude
claude --model sonnet

# Resume / continue sessions
codex resume --last                   # Resume last Codex session
claude -c                             # Continue last Claude session
claude -r                             # Pick a Claude session to resume

# Piping
git diff | claude -p "Review this diff"
git diff | codex review -
```

## Tips

- **Second opinion**: `codex review --uncommitted` — different model family eliminates self-bias
- **Model override**: `codex -m gpt-5.4`, `claude --model opus/sonnet/haiku`. Codex models depend on account type.
- **Cost control**: `claude -p --max-budget-usd 1.00` caps spending
- **Turn limit**: `claude -p --max-turns 3` limits agentic loops in print mode

## Detailed References

- [Codex CLI](./references/codex.md)
- [Claude Code CLI](./references/claude-code.md)
- [Gemini CLI](./references/gemini.md)
