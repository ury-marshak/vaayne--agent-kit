---
name: coding-agents
description: Invoke external coding agents via acpx with preset roles (oracle, reviewer, worker, ui-engineer, librarian, search) for delegation, code review, second opinions, persistent agent sessions, and system utilities (image analysis, generation, handoff, titling).
metadata:
  os:
    - darwin
    - linux
---

# Coding Agents via acpx

## Prerequisites

```bash
bunx acpx

# Get real-time help info
bunx acpx --help
bunx acpx pi --help
```

## Important: Session Auto-Creation

Commands **without `exec`** use a persistent session (conversation state preserved across calls) and require an active session to exist first. Commands **with `exec`** are one-shot and need no session.

**Always prefix persistent commands** with `sessions ensure --name <role>` — use a **named session per purpose** so different tasks stay isolated while the same task can continue across calls:

```bash
# Ensure a named session for the role, then run in that session
bunx acpx pi sessions ensure --name reviewer; bunx acpx --model openai-codex/gpt-5.4 -s reviewer pi "review the auth module"
bunx acpx pi sessions ensure --name worker; bunx acpx --model sonnet -s worker pi "refactor the logger"

# Same name = continues the previous conversation (idempotent)
bunx acpx pi sessions ensure --name reviewer; bunx acpx --model openai-codex/gpt-5.4 -s reviewer pi "now check the tests too"
```

> **`ensure` vs `new`**: `ensure` is idempotent — reuses existing session by name. `new` always creates a fresh session, closing the previous one and losing conversation history. Use `new --name <role>` only when you want a clean slate.

Prefer `exec` when no follow-up is needed — it requires no session.

## Agent Modes

Use `--model` to select the right speed/quality tradeoff. All commands use `bunx acpx --model <model> pi`.

| Mode  | Model              | Command                                          | Use When                              |
| ----- | ------------------ | ------------------------------------------------ | ------------------------------------- |
| Smart | Claude Opus 4.6    | `bunx acpx --model opus pi`                      | Unconstrained, state-of-the-art tasks |
| Rush  | Claude Haiku 4.5   | `bunx acpx --model haiku pi`                     | Fast, cheap, well-defined tasks       |
| Deep  | GPT-5.4 (thinking) | `bunx acpx --model openai-codex/gpt-5.4:high pi` | Deep reasoning with extended thinking |

```bash
# One-shot tasks
bunx acpx --model sonnet pi exec "summarize this repo"
bunx acpx --model haiku pi exec "list all TODO comments"

# Persistent session (named session per purpose)
bunx acpx pi sessions ensure --name refactor; bunx acpx --model opus -s refactor pi "refactor the auth module"

# Code review
bunx acpx --model openai-codex/gpt-5.4 pi exec "review uncommitted changes"
git diff main | bunx acpx --model openai-codex/gpt-5.4 pi exec "review this diff"

# Second opinion (different model)
bunx acpx --model openai-codex/gpt-5.4 pi exec "review uncommitted changes"
bunx acpx --model sonnet pi exec "review uncommitted changes"

# Output formats
bunx acpx --format quiet --model haiku pi exec "summarize repo in 3 lines"
bunx acpx --format json --model sonnet pi exec "list all API endpoints"
```

## Preset Roles

Role prompts live in `references/agents/` relative to this skill. Prepend them to your task prompt for structured delegation.

| Role          | File                                                 | Purpose                                           | Recommended Model             |
| ------------- | ---------------------------------------------------- | ------------------------------------------------- | ----------------------------- |
| `reviewer`    | [reviewer.md](./references/agents/reviewer.md)       | Code review with structured feedback              | `openai-codex/gpt-5.4`        |
| `oracle`      | [oracle.md](./references/agents/oracle.md)           | Architecture advice, critique, planning           | `openai-codex/gpt-5.4:medium` |
| `worker`      | [worker.md](./references/agents/worker.md)           | General-purpose task execution                    | `sonnet`                      |
| `ui-engineer` | [ui-engineer.md](./references/agents/ui-engineer.md) | Visual/UI design and implementation               | `opus`                        |
| `librarian`   | [librarian.md](./references/agents/librarian.md)     | Large-scale retrieval & research on external code | `sonnet`                      |
| `search`      | [search.md](./references/agents/search.md)           | Fast, accurate codebase retrieval                 | `kimi-k2p5-turbo`             |

### Using a preset role

Read the role file and prepend it to the task prompt:

```bash
# Code review with reviewer role (GPT-5.4)
bunx acpx --model openai-codex/gpt-5.4 pi exec "$(cat {skill_dir}/references/agents/reviewer.md)

Review the changes in src/auth/ for security issues"

# Architecture advice with oracle role (GPT-5.4 medium reasoning)
bunx acpx --model openai-codex/gpt-5.4:medium pi exec "$(cat {skill_dir}/references/agents/oracle.md)

Review this architecture and recommend improvements"

# General task with worker role (Sonnet)
bunx acpx --model sonnet pi exec "$(cat {skill_dir}/references/agents/worker.md)

Refactor the logger module to use structured logging"

# Fast codebase search (Kimi K2.5)
bunx acpx --model kimi-k2p5-turbo pi exec "$(cat {skill_dir}/references/agents/search.md)

Find all usages of the AuthService class"

# Pipe role + task via stdin
(cat {skill_dir}/references/agents/reviewer.md; echo; echo "Review uncommitted changes") | bunx acpx --model openai-codex/gpt-5.4 pi exec
```

## System Utilities

These tasks use dedicated skills or lightweight agent calls rather than preset roles.

| Utility     | Purpose                                    | Model            | How                                                    |
| ----------- | ------------------------------------------ | ---------------- | ------------------------------------------------------ |
| **Look At** | Image, PDF, and media file analysis        | Gemini Flash     | Use `vertex-ai-image` skill `read` command             |
| **Painter** | Image generation and editing               | Gemini Pro Image | Use `vertex-ai-image` skill `generate`/`edit` commands |
| **Handoff** | Fallback context analysis for continuation | —                | Use `handoff` skill                                    |
| **Titling** | Fast title generation for threads          | Claude Haiku 4.5 | `bunx acpx --model haiku pi exec "..."`                |

### Look At — image & media analysis

```bash
# Describe an image
uv run --script scripts/vertex_ai_image.py read \
  --image screenshot.png \
  --prompt "What's in this image?"

# Analyze a PDF page
uv run --script scripts/vertex_ai_image.py read \
  --image document.pdf \
  --prompt "Summarize the key points"
```

> See the `vertex-ai-image` skill for full options.

### Painter — image generation & editing

```bash
# Generate an image
uv run --script scripts/vertex_ai_image.py generate \
  --prompt "A diagram showing microservice architecture" \
  --output output/architecture.png

# Edit an existing image
uv run --script scripts/vertex_ai_image.py edit \
  --prompt "Add labels to each component" \
  --image output/architecture.png \
  --output output/architecture-labeled.png
```

> See the `vertex-ai-image` skill for models, aspect ratios, and resolution options.

### Handoff — context continuation

Use the `handoff` skill to generate a `handoff.md` summary for the next session. No agent delegation needed — invoke the skill directly.

### Titling — fast title generation

```bash
bunx acpx --model haiku pi exec "Generate a concise title for this thread: <context>"
```

## acpx Reference

### Sessions

```bash
# Create / use named sessions
bunx acpx pi sessions new
bunx acpx pi -s backend "fix API pagination bug"
bunx acpx pi -s docs "draft changelog entry"

# Queue a follow-up without waiting
bunx acpx pi --no-wait "after tests, summarize failures"

# List / inspect / close sessions
bunx acpx pi sessions list
bunx acpx pi sessions show
bunx acpx pi sessions history --limit 20
bunx acpx pi sessions close

# Cross-repo work
bunx acpx --cwd ~/repos/other-project pi "fix lint errors"
```

### Permissions

| Flag              | Behavior                                        |
| ----------------- | ----------------------------------------------- |
| `--approve-all`   | Auto-approve all permission requests            |
| `--approve-reads` | Auto-approve reads, prompt for writes (default) |
| `--deny-all`      | Deny all permission requests                    |

```bash
bunx acpx --approve-all pi "fix all lint errors and commit"
bunx acpx --deny-all pi exec "explain the architecture"
```

### Output formats

| Format  | Use Case                        |
| ------- | ------------------------------- |
| `text`  | Human-readable stream (default) |
| `json`  | NDJSON event stream for scripts |
| `quiet` | Final assistant text only       |

```bash
bunx acpx --format json --model sonnet pi exec "review changes" | jq -r 'select(.type=="tool_call")'
result=$(bunx acpx --format quiet --model haiku pi exec "summarize this repo")
```

### Session control

```bash
bunx acpx pi cancel                    # Cancel in-flight prompt
bunx acpx pi set-mode plan             # Read-only mode
bunx acpx pi set-mode auto             # Auto-approve mode
```

### Other agents

While `pi` is the primary agent, other agents are available via acpx for second opinions or specific use cases:

| Agent   | Command             | Best For                            |
| ------- | ------------------- | ----------------------------------- |
| Codex   | `bunx acpx codex`   | Sandboxed exec (acpx default)       |
| Claude  | `bunx acpx claude`  | Multi-file tasks, agentic workflows |
| Gemini  | `bunx acpx gemini`  | Fast one-shot prompts, free tier    |
| Kimi    | `bunx acpx kimi`    | Kimi agent                          |
| Cursor  | `bunx acpx cursor`  | IDE-integrated agent                |
| Copilot | `bunx acpx copilot` | GitHub Copilot agent                |

## Tips

- **Second opinion**: Use a different model for the same review to eliminate self-bias
- **Queue follow-ups**: Use `--no-wait` to fire-and-forget while a session is busy
- **Named sessions**: Use `-s <name>` for parallel workstreams in the same repo
- **Cost control**: Use `--max-turns` to limit agentic loops
- **Raw adapter**: `bunx acpx --agent ./custom-acp-server "run checks"` for custom agents
- **Preset roles**: Combine any role with its recommended model — e.g., oracle + `gpt-5.4:medium` for architecture, reviewer + `gpt-5.4` for reviews, search + `kimi-k2p5-turbo` for fast retrieval
- **Thinking levels**: Append `:<level>` to model ID — levels: off, minimal, low, medium, high, xhigh
