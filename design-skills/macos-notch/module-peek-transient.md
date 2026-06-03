# Peek and Transient UI

> Read when: short-lived HUD and live-activity surfaces. Back to [SKILL.md](SKILL.md).

## The core insight

Transient notch UI is not the same as the open panel. **Peek** states show a sliver of information (volume level, download progress, now-playing tick) and auto-dismiss without stealing focus. **Live activity** in the closed notch is optional and must stay minimal.

Rules (from state machine in [foundations.md](foundations.md)):

- `peeking` auto-dismisses after **1.2–3.0 s**.
- Only one peek at a time; cancel prior dismiss tasks before showing a new peek.
- Do not stack peeks with an open panel unless the product explicitly supports it.

---

## Peek kinds

```swift
enum PeekKind: Equatable {
    case music
    case volume(Double)
    case brightness(Double)
    case battery(Double)
    case microphone(Bool)
    case download(Double)
    case custom(String)
}
```

---

## Timing table

| Surface | Duration | Interaction |
|---------|----------|-------------|
| Volume / brightness HUD | 1.2–2.0 s | Non-interactive; may replace system HUD only with consent |
| Download / progress | 1.5–3.0 s | Show bar or percent only |
| Music tick / sneak peek | Until track changes or user opens | Keep closed footprint tiny |
| Weather / Bluetooth / charging | Peek only | Never dominate open layout |

---

## Live activity vs peek

| | Live activity (closed) | Peek |
|--|------------------------|------|
| Purpose | Optional ambient hint (art, visualizer, charging glyph) | React to a system event |
| Duration | Until state changes or user disables | Auto-dismiss |
| User setting | “Show live activity when closed” — default conservative | Usually always on for HUD events |

**OSS:** boring.notch ships playback live activity, charging indicator, and roadmap Bluetooth/weather peeks (GPL — patterns only). NotchMac uses animated charging and unplug notifications as transient surfaces.

---

## Weather / Bluetooth / charging

These should usually be **peek or compact modules**, not dominant panels.

- **Charging:** percent or bolt glyph in closed state; brief peek on plug/unplug (NotchMac adds sound + haptic — use sparingly).
- **Bluetooth:** connect/disconnect icon peek; do not mirror full Bluetooth UI.
- **Weather:** icon + temperature peek only; full forecast belongs in a normal window or menu bar menu.

---

## OSS examples

- **boring.notch** — playback live activity, charging %, HUD peeks (GPL; study behavior, do not copy code without compliance).
- **NotchMac** — battery plug/unplug notifications; lock-screen indicator (note SkyLight dependency in that repo).
- **NotchIA** — “Sneak Peek” on track change for media.

---

## Pitfalls

- Peeks that require click to dismiss (feels like a notification).
- Peeks longer than 3 s without user action.
- Animated peeks when Reduce Motion is on — shorten or disable.
- Closed live activity enabled by default with busy animations — feels like adware.

See also: [module-system-hud.md](module-system-hud.md), [module-media-now-playing.md](module-media-now-playing.md), [interactions-and-motion.md](interactions-and-motion.md).
