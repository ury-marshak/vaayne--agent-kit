# Handoff Protocol

The handoff file (`handoff.md` in the session folder) is the communication channel between phase subagents. It's a single file, appended after each phase.

## Purpose

- **Worker subagent writes** a phase summary after finishing implementation
- **Reviewer subagent reads** it to understand what was done before reviewing
- **Next worker subagent reads** it to get full context of prior phases

## When to Write

The worker subagent appends to `handoff.md` after completing all tasks in a phase, before returning to the main agent.

If the main agent makes fixes after review, it also appends fix notes.

## What to Write

Each phase section should include:

1. **Status** — `complete`, `partial`, or `blocked`
2. **What was done** — tasks completed, approach taken
3. **What changed** — files modified, key decisions made
4. **Commits** — list of commit hashes with short descriptions
5. **Context for next phase** — anything the next subagent needs to know (gotchas, patterns established, dependencies)
6. **Blockers** (if partial/blocked) — what's blocking and why

Keep it concise. This is a summary, not a code dump.

## Template

Use `references/templates/handoff.md` for the format.

## Rules

- **Always append, never overwrite** — each phase adds a new section
- **Write before returning** — the worker must write the handoff before finishing
- **Read before starting** — the next worker must read the full handoff before implementing
- **Fix notes go inline** — if the main agent fixes issues after review, append a short "Fixes" subsection under the relevant phase
