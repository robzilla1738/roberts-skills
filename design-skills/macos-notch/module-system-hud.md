# System HUD Replacement

> Read when: volume, brightness, battery, and transient HUD peeks. Back to [SKILL.md](SKILL.md).

### System HUD replacement

Closed/peek:

- Volume, brightness, keyboard backlight, mic, battery, or download progress.
- Auto-dismiss after `1.2–2s`.

Important:

- Only intercept media keys or suppress system HUDs with user consent and required accessibility permissions.
- Provide a setting to disable HUD replacement.
- Fall back gracefully if permission is denied.
