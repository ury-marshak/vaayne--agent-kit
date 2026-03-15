# Phase Loop

The implementation loop for Phase 3. One subagent per phase, review between phases.

## Flow

```
For each phase in plan.md:

  1. IMPLEMENT (worker subagent)
     - Read plan.md, tasks.md, and handoff.md for prior context
     - Implement all tasks in the phase
     - Commit after each task (emoji + conventional format)
     - Append phase summary to handoff.md
     - Return to main agent

  2. REVIEW (reviewer subagent)
     - Read handoff.md (focus on latest phase section)
     - Review all commits in the phase
     - Return verdict: APPROVED or CHANGES NEEDED with feedback

  3. FIX (main agent, only if changes needed)
     - Apply fixes directly
     - Commit fixes
     - Append fix notes to handoff.md
     - If fixes are substantial, re-run reviewer on this phase

  4. NEXT PHASE
     - Update tasks.md (check off completed tasks)
     - Continue to next phase
```

## After Last Phase

1. Run full test suite
2. Update plan.md with final status
3. Verify all tasks checked off in tasks.md
4. Summarize completed work to user
5. Confirm session is ready for merge/release

## Escalation

If a phase review requires major rework (not just fixes):

- Pause and ask the user for guidance
- Do not start the next phase until resolved

## Commit Format

- `✨ feat:` — New features
- `🐛 fix:` — Bug fixes
- `♻️ refactor:` — Code restructuring
- `📝 docs:` — Documentation
- `✅ test:` — Tests
- `⚡️ perf:` — Performance
