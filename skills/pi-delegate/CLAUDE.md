# Adding a New Agent

Place a new `.md` file in the `agents/` directory next to this file.

## File format

```markdown
You are a [role description].

## What You Do

- capability 1
- capability 2

## Output Format

How to structure the response.
```

## Requirements

- **File name**: `kebab-case.md` (e.g. `data-analyst.md`)
- **Content**: A system prompt — write it as direct instructions to the agent
- **Keep it concise**: Under 200 lines. The prompt is injected via `--append-system-prompt` so token cost matters.
- **No frontmatter needed**: Unlike top-level `agents/*.md`, these don't need YAML frontmatter. They're plain system prompts.

## After adding

1. Update `SKILL.md` — add the new agent to the "Preset agents" table
2. Include: name, purpose, recommended model tier, and tool scope
