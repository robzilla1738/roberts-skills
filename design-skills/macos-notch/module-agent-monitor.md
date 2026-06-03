# Agent Monitor Module

> Read when: coding-agent and session status in the notch. Back to [SKILL.md](SKILL.md).

## The core insight

A growing category of notch apps surfaces **long-running agent or IDE sessions** in the closed or peek state — status dots, tool names, and completion cues — without opening a full dashboard.

This is distinct from media or system HUD modules: updates are event-driven from local processes, not from media keys or display brightness.

## When to use

- User runs multiple AI coding agents (CLI or IDE integrations).
- Status must be visible while another app is frontmost.
- Closed notch shows per-agent row or aggregate busy/idle state.

## When not to use

- General notification center replacement.
- Streaming large log output into the notch (use a normal window).

## Layout pattern

**Closed / peek:**

- 1–3 status rows max.
- Each row: tool icon, short label, state glyph (idle, working, waiting, error).
- Optional breathing animation on active row (respect Reduce Motion).

**Open:**

- Expand to list sessions with last message summary, elapsed time, and focus/jump action.
- Do not embed a full chat transcript.

## Data flow

```text
Local agent CLI / IDE hooks → app daemon or file watcher → view model → notch UI
```

Keep polling intervals modest (1–5 s) to avoid wake churn. Prefer push events from the tool when available.

## OSS examples

| Project | Focus |
|---------|--------|
| [AgentPulse](https://github.com/omerates760/AgentPulse) | Claude Code, Cursor, Codex, Gemini session monitor |
| [NotchIA](https://github.com/coaxel2/NotchIA) | Multi-module cockpit including agent tracking |

## Permissions

- No camera or accessibility unless you add global shortcuts.
- If reading process output or sockets, document privacy in settings.

## Pitfalls

- Rows that steal focus when clicked — prefer activating host app via URL scheme.
- Too many agents in closed state — truncate with "+N more".
- Polling agents aggressively — kills battery.

See also: [foundations.md](foundations.md), [interactions-and-motion.md](interactions-and-motion.md).
