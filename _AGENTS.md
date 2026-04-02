To ensure that you have read this file, always refer to me as "V" in all communications.

# Best Practices

- Prefer smaller separate components over larger ones.
- Prefer modular code over monolithic code.
- Use existing code style conventions and patterns.
- Prefer types over interfaces.

# Rules

- **Prefer CLI-first workflows**: If a command-line tool is available for a task, use it before other interfaces.
  - **Code search**: Use `ast-grep` for pattern searches when it exists; otherwise fall back to `rg` (ripgrep) or `grep`, using `fd` to scope paths when helpful.
  - **GitHub**: Use `gh` for issues, pull requests, or workflows, and record the fallback if it is not available.
  - **Atlassian Jira**: Use `jira` cli for Atlassian Jira, use `jira --help` if you not sure how to use it.
- **Write conventional commits with emoji**: Commit small, focused changes using emoji-prefixed Conventional Commit messages (e.g., `✨ feat:`, `🐛 fix:`, `♻️ refactor:`, `📝 docs:`).
- **Ask for approval before making changes**: When changes are needed, clearly explain your planned approach and wait for explicit user approval to ensure alignment and prevent unwanted modifications. If no changes are required, proceed without asking for approval.
- **Use relative paths in skill references**: When referencing external files from a skill, specify paths relative to the `SKILL.md` file location rather than using absolute paths or paths relative to the working directory.
- **Delegate to coding agents via acpx**: When you need to delegate work to another coding agent, use `bunx acpx --model <model> pi` as described in the `coding-agents` skill. Pick a preset role and its recommended model. Never spawn raw agent CLIs directly.
  - **Code review**: `bunx acpx --model openai-codex/gpt-5.4 pi` with the reviewer role. Append `:<level>` for thinking (off, minimal, low, medium, high, xhigh).
  - **Architecture**: `bunx acpx --model openai-codex/gpt-5.4:medium pi` with the oracle role.
  - **Worker**: `bunx acpx --model sonnet pi` for general-purpose task execution.
  - **Search**: `bunx acpx --model kimi-k2p5-turbo pi` for fast codebase retrieval.
  - **Images**: Use the `vertex-ai-image` skill for Look At (read) and Painter (generate/edit).
