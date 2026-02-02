---
name: handoff
description: Transfer context to a new focused session. Use when starting a new phase of work, handing off to a new session, or when context needs to be summarized for continuation. Triggers on "handoff", "transfer context", "start new session with context", or when the user wants to continue work in a fresh session.
---

# Handoff

Transfer context to a new focused session by generating a summary prompt.

## When to Use This Skill

Use this skill when the user:

- Wants to start a new session but preserve important context
- Says "handoff to new session" or "transfer this context"
- Needs to continue work in a fresh conversation
- Wants a summary of decisions made to hand off to another session
- Says something like "now implement this for X as well" or "execute phase one"

## Usage

```
/handoff <goal for new thread>
```

Examples:

- `/handoff now implement this for teams as well`
- `/handoff execute phase one of the plan`
- `/handoff check other places that need this fix`

## How It Works

When invoked, this skill will:

1. **Analyze the conversation** - Review the current session to identify:
   - Key decisions made
   - Approaches taken
   - Important findings
   - Files modified or discussed

2. **Generate a focused prompt** - Create a self-contained prompt that includes:
   - Relevant context summary
   - List of involved files
   - Clear statement of the next task

3. **Output the prompt** - Present the generated prompt for the user to:
   - Copy and start a new session
   - Edit before using
   - Share with others

## Generating the Handoff Prompt

When this skill is invoked, generate a handoff prompt following this structure:

### Prompt Format

```markdown
## Context

[Brief summary of what was worked on and key decisions/findings]

Key decisions:

- [Decision 1]
- [Decision 2]

Files involved:

- [path/to/file1]
- [path/to/file2]

## Task

[Clear description of what to do next based on the user's goal]
```

### Guidelines for Generating the Prompt

1. **Be concise** - Include only information relevant to the new task
2. **Be self-contained** - The new session should be able to proceed without the old conversation
3. **Focus on decisions** - What was decided, not the full discussion
4. **List concrete files** - Any files that were modified or will need modification
5. **State the task clearly** - Use the user's goal to define exactly what should happen next

## Example Output

If the user says `/handoff now implement the same validation for the settings page`:

```markdown
## Context

We implemented form validation for the user profile page using zod schemas with custom error messages. The validation runs on blur and on submit, showing inline errors.

Key decisions:

- Used zod for schema validation
- Errors shown inline below each field
- Validation triggers on blur + submit

Files involved:

- src/components/profile/ProfileForm.tsx
- src/schemas/profile.ts
- src/hooks/useFormValidation.ts

## Task

Implement the same validation pattern for the settings page. Use the existing `useFormValidation` hook and create a new zod schema for settings fields. The settings form includes email preferences, notification toggles, and timezone selection.
```

## Tips

- If the conversation is short or simple, the handoff prompt can be brief
- Include any gotchas or edge cases discovered during the work
- If there's a plan with multiple phases, reference which phase is being handed off
