# System HUD Replacement

> Read when: volume, brightness, battery, and transient HUD peeks. Back to [SKILL.md](SKILL.md).

## The core insight

System HUD modules replace or supplement macOS volume/brightness overlays with notch-native peeks. They are **transient by default** — the user should never feel trapped in a HUD panel.

---

## Behavior

### Closed / peek

- Volume, brightness, keyboard backlight, mic, battery, or download progress.
- Auto-dismiss after **1.2–2.0 s** (see [module-peek-transient.md](module-peek-transient.md)).

### Display modes (OSS pattern)

NotchMac documents three HUD presentations worth considering when designing open/peek layouts:

| Mode | UX |
|------|-----|
| **Minimal** | Icon + percentage, no expansion |
| **Progress bar** | Classic bar under icon |
| **Notched** | Segmented bar aligned to shell width (iOS-like) |

boring.notch replaces volume, brightness, and keyboard backlight HUDs (GPL — patterns only).

---

## Permissions and consent

Important:

- Only intercept media keys or suppress system HUDs with **user consent** and required accessibility permissions.
- Provide a setting to **disable HUD replacement** (default off until permission granted).
- Fall back gracefully if permission is denied — show in-notch peek only, or defer to system HUD.

See [integration-shipping.md](integration-shipping.md) §14 for just-in-time permission prompts.

---

## Battery

Treat battery as HUD/peek, not a full dashboard:

- Charging indicator and percentage in closed or peek (boring.notch, NotchMac).
- Unplug notification as brief peek + optional sound (NotchMac) — respect user mute settings.

---

## Pitfalls

- Requesting accessibility permission on first launch before the user enables HUD replacement.
- HUD peeks that steal focus or block menu bar interaction.
- Replacing system HUD without a visible “off” switch in menu bar extra.

See also: [foundations.md](foundations.md) (state machine `PeekKind`), [ecosystem-landscape.md](ecosystem-landscape.md).
