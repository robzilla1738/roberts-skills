# Peek and Transient UI

> Read when: short-lived HUD and live-activity surfaces. Back to [SKILL.md](SKILL.md).

## The core insight

Transient notch UI is not the same as the open panel. **Peek** states show a sliver of information (volume level, download progress, now-playing tick) and auto-dismiss without stealing focus. **Live activity** in the closed notch is optional and must stay minimal.

Rules (from state machine):

- `peeking` auto-dismisses after **1.2–3.0 s**.
- Only one peek at a time; cancel prior dismiss tasks before showing a new peek.
- Do not stack peeks with an open panel unless the product explicitly supports it.

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

## Timing table

| Surface | Duration | Interaction |
|---------|----------|-------------|
| Volume / brightness HUD | 1.2–2.0 s | Non-interactive; may replace system HUD only with consent |
| Download / progress | 1.5–3.0 s | Show bar or percent only |
| Music tick | Until track changes or user opens | Keep closed footprint tiny |
| Weather / Bluetooth / charging | Peek only | Never dominate open layout |

## OSS examples

- **boring.notch** — rich peek/live-activity patterns (GPL; study behavior, do not copy code without compliance).
- **NotchIA** — combines peeks with multi-module cockpit.

## Pitfalls

- Peeks that require click to dismiss (feels like a notification).
- Peeks longer than 3 s without user action.
- Animated peeks when Reduce Motion is on — shorten or disable.

See also: [module-system-hud.md](module-system-hud.md), [module-media-now-playing.md](module-media-now-playing.md).


## Compact status chips


These should usually be peek or compact modules, not dominant panels.

---