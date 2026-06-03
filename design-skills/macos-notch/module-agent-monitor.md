# Agent Monitor Module

> Read when: coding-agent and session status in the notch. Back to [SKILL.md](SKILL.md).

## The core insight

A growing category of notch apps surfaces **long-running agent or IDE sessions** in the closed or peek state — status dots, tool names, and completion cues — without opening a full dashboard.

This is distinct from media or system HUD modules: updates are event-driven from local processes, not from media keys or display brightness.

---

## When to use

- User runs multiple AI coding agents (CLI or IDE integrations).
- Status must be visible while another app is frontmost.
- Closed notch shows per-agent row or aggregate busy/idle state.
- User must approve tool permissions or answer agent questions without hunting terminal tabs.

## When not to use

- General notification center replacement.
- Streaming large log output into the notch (use a normal window).

---

## Layout pattern

### Closed / peek

- 1–3 status rows max.
- Each row: tool icon, short label, state glyph (idle, working, waiting, error).
- Optional breathing animation on active row (respect Reduce Motion).
- **AgentPulse pattern:** dynamic pill width; border glow by state (e.g. active, permission pending, question pending).

### Open

- Expand to list sessions with last message summary, elapsed time, and focus/jump action.
- **Approvals:** Allow Once / Always Allow / Deny for tool requests; show bash preview when relevant.
- **Questions:** single-select and multi-select; batch submit when multiple questions queued.
- Do not embed a full chat transcript.

---

## Data flow

```text
Local agent CLI / IDE hooks → app daemon or file watcher → view model → notch UI
```

**AgentPulse (MIT)** installs hooks automatically for Claude Code, Cursor, Codex, and Gemini CLI; supports terminal jump via AppleScript (iTerm2, Terminal, VS Code, Cursor, Warp, Ghostty, Kitty).

**NotchIA (GPL-3.0)** embeds agent tracking inside a multi-module cockpit — study UX, do not copy source without compliance.

Keep polling intervals modest (1–5 s) when push events are unavailable. Prefer hook/file events from the tool.

---

## Permissions

- No camera or accessibility unless you add global shortcuts or HUD interception.
- If reading process output or sockets, document privacy in settings.
- Hook installation should be explicit in onboarding (“we will configure agent hooks”).

---

## Pitfalls

- Rows that steal focus when clicked — prefer activating host app via URL scheme or terminal jump.
- Too many agents in closed state — truncate with “+N more”.
- Polling agents aggressively — kills battery.
- Playing notification sounds when the target terminal is already focused (AgentPulse “smart suppression” is a good pattern).

See also: [foundations.md](foundations.md), [interactions-and-motion.md](interactions-and-motion.md), [ecosystem-landscape.md](ecosystem-landscape.md).
