---
name: specs-dev
description: Plan-first development workflow with review gates. Use when implementing features, refactoring, or any task requiring structured planning, iterative implementation with reviews, and clean commits. Triggers on requests like "implement feature X", "plan and build", "spec-driven development", or when user wants disciplined, reviewed code changes.
---

# Specs-Dev Workflow

A disciplined, review-gated development workflow: plan first, implement in phases, review between phases.

## Workflow

| Phase             | Purpose                 | Gate                  |
| ----------------- | ----------------------- | --------------------- |
| 1. Discovery      | Understand requirements | User approves summary |
| 2. Planning       | Create reviewed plan    | User approves plan    |
| 3. Implementation | Phase-by-phase coding   | Each phase reviewed   |

## Phase 1: Discovery

**Goal:** Shared understanding before planning.

1. State your understanding of the request
2. Ask clarifying questions (goals, constraints, success criteria, out-of-scope)
3. Iterate until clear
4. Present final requirements summary

**Gate:** "Do I understand correctly? Should I proceed to planning?" — Wait for approval.

## Phase 2: Planning

**Goal:** Create a comprehensive, reviewed implementation plan.

1. Draft plan using `references/templates/plan.md`
2. Review with reviewer subagent (see `references/agents/reviewer.md`) — max 3 rounds
3. Integrate feedback, iterate until approved
4. If still not approved after 3 rounds — summarize unresolved concerns and ask user whether to revise scope, continue anyway, or stop
5. Resolve all Open Questions — convert remaining unknowns into explicit assumptions before proceeding
6. Present plan to user — wait for approval
7. Create session folder: `.agents/sessions/{YYYY-MM-DD}-{feature-name}/`
8. Save `plan.md`, `tasks.md`, and `handoff.md` (initialized from `references/templates/handoff.md`) to session folder

**Plan quality check:**

- Every requirement from Phase 1 addressed
- Tasks are actionable and logically ordered
- Testing strategy specified
- Risks captured
- No unresolved Open Questions (converted to assumptions or removed)

## Phase 3: Implementation

**Goal:** Implement the plan phase-by-phase with reviews between phases.

> Read `references/loop.md` before starting. It defines the phase loop.

**Summary of the loop:**

```
For each phase in the plan:
  1. Spawn worker subagent → implements all tasks, commits each one
  2. Worker writes phase summary to handoff.md
  3. Spawn reviewer subagent → reads handoff.md, reviews the phase
  4. If changes needed → fix in main agent context
  5. Continue to next phase
```

After the last phase: run full test suite, update session docs, confirm with user.

**Subagents:**

- Worker: `references/agents/worker.md`
- Reviewer: `references/agents/reviewer.md`
- Handoff protocol: `references/handoff.md`

## Session Structure

```
.agents/sessions/{YYYY-MM-DD}-{feature-name}/
├── plan.md       # Strategic plan
├── tasks.md      # Task checklist
└── handoff.md    # Phase handoff log (appended each phase)
```

## References

| File                            | When to Read            |
| ------------------------------- | ----------------------- |
| `references/loop.md`            | Start of Phase 3        |
| `references/handoff.md`         | Start of Phase 3        |
| `references/agents/reviewer.md` | Plan/phase reviews      |
| `references/agents/worker.md`   | Phase implementation    |
| `references/templates/`         | Phase 2 (plan creation) |
