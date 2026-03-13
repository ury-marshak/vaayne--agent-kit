---
name: pi-delegate
description: Delegate tasks to Pi subagents with preset roles (oracle, worker, reviewer, ui-engineer, librarian) or ad-hoc prompts. Use for fresh context, model specialization, second opinions, code review, isolated execution, or parallel task delegation.
---

# Pi Delegate

Use Pi as a separate non-interactive subagent when you want fresh context, a different model, or isolated task execution.

## Use this skill when

- you want to delegate a bounded task to Pi
- you want a different model for the task
- you want an independent second pass or critique
- you want to isolate noisy work from the current conversation

## Preset agents

Preset agent profiles live in `agents/` relative to this skill. Read the agent file and pass its content via `--append-system-prompt`.

| Agent | Purpose | Model tier |
|-------|---------|------------|
| `oracle` | Architecture advice, critique, second opinion | Best (opus/pro/codex) |
| `reviewer` | Code review with structured feedback | Best (opus/pro/codex) |
| `worker` | General-purpose subtask execution | Balanced (sonnet/codex) |
| `ui-engineer` | Visual/UI design and implementation | Best (pro/opus) |
| `librarian` | Code search, docs lookup, examples | Fast (flash) |

### Using a preset agent

1. Read the agent file (e.g. `agents/oracle.md`) to get the system prompt.
2. Pass it via `--append-system-prompt "$(cat agents/oracle.md)"`.
3. Set `--model` per the table above.

```bash
cd "/path/to/project" && pi --offline --no-prompt-templates --no-themes --append-system-prompt "$(cat {skill_dir}/agents/oracle.md)" --model {model} -p "Your task"
```

Ad-hoc delegation (no preset) still works — just omit `--append-system-prompt`.

## Command rules

- Change to the target working directory first (quote paths with spaces).
- Default to `--offline --no-prompt-templates --no-themes` for reproducible, low-noise runs.
- Choose a model with: `--model {model}` when model choice matters.
- Use `pi --help` if exact flags are unclear.

### Fresh run vs continuation

- **Fresh run (default):** Start a new isolated session. Use this for independent delegation.
- **Continuation (`-c`):** Resume the most recent delegated session. Only use when intentionally continuing the same thread — e.g., refining a previous result or adding follow-up instructions to the same task.

Pattern (ad-hoc):

```bash
cd "/path/to/project" && pi --offline --no-prompt-templates --no-themes [--model {model}] [-c] -p "Your task"
```

## Model selection

Discover available models dynamically — do not rely on memorized model IDs:

```bash
pi --list-models [search]
```

Without `[search]`, lists all available models. With a search term, filters by keyword.

Examples: `pi --list-models`, `pi --list-models gpt`, `pi --list-models claude`, `pi --list-models gemini`.

### Selection guide

Pick a model by matching the task to the right family and tier.

| Family | Best | Balanced / Fast | Notes |
|---------|------|-----------------|-------|
| **GPT** | Highest version with `codex` (e.g. gpt-5.4-codex) | Highest version without `codex` | `codex` variants are optimized for coding. Non-codex are general purpose. Higher version number = better (5.4 > 5.3). |
| **Claude** | `opus` | `sonnet` (balanced), `haiku` (fastest) | Opus is most capable, sonnet is strong all-rounder, haiku is cheapest and fastest. |
| **Gemini** | `pro` | `flash` | Pro is most capable. Flash is fast and cheap. |

### When to pick what

- **Complex reasoning, planning, critique** — pick the best tier (opus, pro, or highest codex).
- **Coding tasks** — prefer GPT codex variants or Claude opus/sonnet.
- **General purpose / balanced** — Claude sonnet or GPT without codex.
- **Fast, cheap, high-volume** — Claude haiku or Gemini flash.
- **Vision / image understanding** — Gemini flash is good enough and cost-effective; prefer it over heavier models.

## Execution workflow

1. Run Pi via `bash` and capture stdout.
2. Read the output — treat it as input for your judgment, not automatic truth.
3. Summarize findings back into the main task context.
4. Decide whether to act on, discard, or refine the delegated result.

## Error handling

If Pi fails or returns unexpected results:

1. Verify the working directory exists and is correct.
2. Run `pi --list-models` to confirm the model ID is valid.
3. Retry without `--model` to use the default model.
4. Run `pi --help` to check for flag changes.

## Examples

```bash
# Oracle: architecture review (preset agent)
cd "/path/to/project" && pi --offline --no-prompt-templates --no-themes --append-system-prompt "$(cat {skill_dir}/agents/oracle.md)" --model {opus-model} -p "Review this architecture and recommend improvements"

# Reviewer: code review (preset agent)
cd "/path/to/project" && pi --offline --no-prompt-templates --no-themes --append-system-prompt "$(cat {skill_dir}/agents/reviewer.md)" --model {opus-model} -p "Review the changes in src/auth/ for security issues"

# Worker: general task (preset agent, full tools)
cd "/path/to/project" && pi --offline --no-prompt-templates --no-themes --append-system-prompt "$(cat {skill_dir}/agents/worker.md)" --model {sonnet-model} -p "Refactor the logger module to use structured logging"

# Ad-hoc delegation (no preset)
cd "/path/to/project" && pi --offline --no-prompt-templates --no-themes --model {sonnet-model} -p "Think through this decision and recommend the best option"

# Continue a previous delegated session
cd "/path/to/project" && pi --offline --no-prompt-templates --no-themes -c -p "Refine the recommendation from the previous run"
```

## Prompt guidance

Keep prompts direct. Ask Pi for the output you want back, such as:

- findings
- risks
- options
- recommendation
- next actions
