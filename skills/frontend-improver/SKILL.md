---
name: frontend-improver
description: Improve frontend interfaces using 17 targeted steering commands covering design intensity, responsiveness, animation, accessibility, UX copy, color, critique, delight, simplification, extraction, hardening, normalization, onboarding, optimization, and polish. Use when the user wants to enhance, refine, or review an existing UI.
user-invokable: true
args:
  - name: target
    description: The feature, component, or area to improve (optional)
    required: false
  - name: action
    description: Specific action — adapt, animate, audit, bolder, clarify, colorize, critique, delight, distill, extract, harden, normalize, onboard, optimize, polish, quieter, teach-impeccable (optional, runs full review if omitted)
    required: false
---

# Frontend Improver

A unified entry point for all frontend improvement steering commands. Each command targets a specific dimension of interface quality.

## Available Commands

Use `action` to run a specific command, or omit it to run a full review across all dimensions.

| Command              | Purpose                                                                |
| -------------------- | ---------------------------------------------------------------------- |
| **adapt**            | Adapt designs across screen sizes, devices, and platforms              |
| **animate**          | Add purposeful animations and micro-interactions                       |
| **audit**            | Comprehensive audit of accessibility, performance, and responsiveness  |
| **bolder**           | Amplify safe or boring designs to be more visually interesting         |
| **clarify**          | Improve UX copy, error messages, labels, and microcopy                 |
| **colorize**         | Add strategic color to monochromatic interfaces                        |
| **critique**         | Evaluate design effectiveness with actionable feedback                 |
| **delight**          | Add moments of joy, personality, and unexpected touches                |
| **distill**          | Strip designs to their essence, remove unnecessary complexity          |
| **extract**          | Extract reusable components, tokens, and patterns into a design system |
| **harden**           | Improve resilience with error handling, i18n, and edge cases           |
| **normalize**        | Normalize design to match your design system for consistency           |
| **onboard**          | Design or improve onboarding flows and first-time user experiences     |
| **optimize**         | Improve loading speed, rendering, animations, and bundle size          |
| **polish**           | Final quality pass for alignment, spacing, and consistency             |
| **quieter**          | Tone down overly bold or visually aggressive designs                   |
| **teach-impeccable** | One-time setup to gather and save project design context               |

## Workflow

1. **Assess** — Read the target code and understand the current state
2. **Diagnose** — Identify which dimensions need improvement
3. **Apply** — Use the appropriate steering command(s) below
4. **Verify** — Confirm improvements and check for regressions

## Steering Command References

Apply these skills as needed based on the diagnosed issues:

- [Adapt](references/adapt.md) — responsive design, cross-platform adaptation
- [Animate](references/animate.md) — motion, transitions, micro-interactions
- [Audit](references/audit.md) — accessibility, performance, theming audit
- [Bolder](references/bolder.md) — amplify visual impact and intensity
- [Clarify](references/clarify.md) — UX writing, labels, error messages
- [Colorize](references/colorize.md) — color strategy, visual engagement
- [Critique](references/critique.md) — design evaluation, visual hierarchy
- [Delight](references/delight.md) — personality, joy, memorable touches
- [Distill](references/distill.md) — simplify, remove unnecessary complexity
- [Extract](references/extract.md) — reusable components and design tokens
- [Harden](references/harden.md) — error handling, i18n, edge cases
- [Normalize](references/normalize.md) — design system consistency
- [Onboard](references/onboard.md) — onboarding flows, empty states
- [Optimize](references/optimize.md) — performance, speed, efficiency
- [Polish](references/polish.md) — final pass, pixel-perfect details
- [Quieter](references/quieter.md) — reduce visual intensity
- [Teach Impeccable](references/teach-impeccable.md) — project design context setup

## Full Review Mode

When no specific `action` is given, run a full review:

1. **Critique** the overall design quality first
2. **Audit** for accessibility and performance issues
3. **Normalize** to match design system
4. **Clarify** any confusing copy or labels
5. **Colorize** if the interface lacks visual interest
6. **Bolder** if the design feels too safe
7. **Animate** where motion would improve usability
8. **Adapt** for responsive/cross-platform needs
9. **Harden** for error handling and edge cases
10. **Onboard** if first-time experience needs work
11. **Extract** reusable patterns into design system
12. **Distill** to remove unnecessary complexity
13. **Optimize** for performance
14. **Polish** as the final pass
15. **Delight** to add memorable finishing touches

Report findings as a prioritized list of improvements, then implement the highest-impact changes.
