# Claude Code CLI Reference

Anthropic's Claude Code agent. Alias: `cc` (configured with Bedrock + dangerously-skip-permissions).

## cc Alias

The `cc` alias is configured as:

```bash
cc() {
  unset ANTHROPIC_API_KEY
  unset ANTHROPIC_AUTH_TOKEN
  CLAUDE_CODE_USE_BEDROCK=1 AWS_PROFILE=dev AWS_REGION=us-west-2 \
    claude --dangerously-skip-permissions "$@"
}
```

This means `cc` runs with full permissions bypassed and uses AWS Bedrock as the provider.

## Non-Interactive Print Mode

```bash
# Basic one-shot prompt
cc -p "Explain what src/index.ts does"

# Pipe input
git diff | cc -p "Review this diff for bugs"
cat error.log | cc -p "Diagnose this error"

# With specific model
cc --model opus -p "Refactor this function for readability"
cc --model sonnet -p "Quick summary of this file"

# JSON output for scripting
cc -p --output-format json "List all exported functions in src/"

# Streaming JSON output
cc -p --output-format stream-json "Analyze this codebase"

# Budget cap
cc -p --max-budget-usd 1.00 "Comprehensive code review of src/"

# With system prompt
cc -p --system-prompt "You are a security auditor" "Review src/auth.ts"

# Append to default system prompt
cc -p --append-system-prompt "Focus on performance" "Review src/api.ts"

# Output to file
cc -p "Summarize changes" > summary.txt
```

## Interactive Mode

```bash
# Default interactive
cc

# Continue last conversation
cc -c

# Resume a specific session
cc -r

# Resume by session ID
cc -r <session-id>

# Named session
cc -n "feature-auth"

# With specific model
cc --model opus

# With effort level
cc --effort high
cc --effort low

# With specific tools only
cc --tools "Bash,Read,Grep"

# With additional directories
cc --add-dir ../shared-lib
```

## Worktree Mode

```bash
# Create isolated git worktree for the session
cc -w

# Named worktree
cc -w feature-branch

# Worktree with tmux
cc -w --tmux
```

## Permission Modes

| Mode                | Description                              |
| ------------------- | ---------------------------------------- |
| `default`           | Ask for approval on risky actions        |
| `plan`              | Read-only, no edits allowed              |
| `acceptEdits`       | Auto-accept file edits, ask for commands |
| `bypassPermissions` | Skip all permission checks               |
| `auto`              | Auto-approve within safety guardrails    |

```bash
cc --permission-mode plan -p "Analyze this codebase"
cc --permission-mode auto
```

## Agents

```bash
# List configured agents
cc agents

# Use a specific agent
cc --agent reviewer
```

## MCP Configuration

```bash
# Manage MCP servers
cc mcp

# Load MCP config from file
cc --mcp-config ./mcp-config.json

# Strict MCP (only use specified config)
cc --strict-mcp-config --mcp-config ./my-servers.json
```

## Session Management

```bash
# Continue most recent conversation
cc -c

# Resume with picker
cc -r

# Resume with search
cc -r "auth feature"

# Fork a session (new ID, same context)
cc -r <id> --fork-session

# Resume from PR
cc --from-pr 123
cc --from-pr https://github.com/org/repo/pull/123
```

## Useful Patterns

```bash
# Quick code review via print mode
git diff main | cc -p "Review this diff"

# Get a second opinion from a different model
cc --model sonnet -p "Review src/auth.ts for security issues"

# Codebase exploration (read-only)
cc --permission-mode plan -p "Explain the architecture of this project"

# Parallel review in worktree
cc -w -p "Run tests and fix any failures"

# Budget-capped analysis
cc -p --max-budget-usd 0.50 "Find all potential memory leaks"

# Structured output
cc -p --json-schema '{"type":"object","properties":{"issues":{"type":"array","items":{"type":"string"}}}}' "List issues in src/"
```
