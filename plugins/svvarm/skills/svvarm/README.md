# svvarm (skill)

Opinionated design director for frontend interfaces. Hub-and-spoke with a two-tier
reference library: full builds read one compiled digest (~5K tokens); focused tasks read
one deep file.

| File | Role |
| --- | --- |
| `SKILL.md` | Hub — identity, routing table, 5 modes (init/setup/audit/CDO/action), full-build workflow |
| `references/core.md` | The digest — 38 anti-slop patterns, all domain rules, font shortlist, self-audit gate. Full builds read only this |
| `references/color.md` | OKLCH palettes, tinted neutrals, contrast, dark mode architecture |
| `references/typography.md` | Type systems, fluid scales, weight discipline, dark mode type |
| `references/font-pairings.md` | 19 curated pairings with sources and imports |
| `references/layout.md` | Composition, spacing scale, layout primitives, semantic HTML, component recipes |
| `references/content.md` | Landing copy, UX writing, the humanizer |
| `references/slop.md` | The Anti-Slop Bible — 38 patterns with detection, fixes, 0-100 scoring |
| `references/polish.md` | 6-pass refinement and distill mode |
| `references/interaction.md` | Production hardening: a11y, responsive, 8-state components, forms |
| `references/motion.md` | Easing, duration rules, scroll choreography, reduced motion |
| `references/icons.md` | Icon library selection, sizing, accessibility |
| `references/inspiration.md` | Case studies, design gallery anatomy, advanced pattern catalog |
| `scripts/ui.py` | Optional terminal banner/progress UI (plain `python3`, never required) |

Copy or symlink this whole folder into your assistant's skills directory
(`~/.claude/skills/svvarm`, `~/.codex/skills/svvarm`, `~/.cursor/skills/svvarm`,
`~/.config/opencode/skills/svvarm`). All paths inside SKILL.md resolve relative to the
folder containing it, so it works identically everywhere.
