# Visual System

> Read when: Materials, color, typography density, and closed/open layout rules. Back to [SKILL.md](SKILL.md).

## 10. Visual Design System

### Closed state

Closed state should be minimal:

- Pure black shape.
- Optional tiny album art, visualizer, face, or status icon only if the user enables live activity.
- Keep internal items vertically centered inside the closed notch height.
- No text unless the closed pill is intentionally widened.

### Open state

Open state can expose richer content:

- Top row/header: module tabs, status, close affordance if needed.
- Main content: primary module such as music controls, shelf, calendar, battery, camera.
- Secondary content: tiny status chips, shortcut buttons, contextual info.

Use dense but breathable layout:

- Outer padding: `12–16 pt`.
- Internal control spacing: `8–12 pt`.
- Icon buttons: `28–36 pt`.
- Album art: `72–96 pt`.
- Corner radius: `20–28 pt` for open bottom corners.

### Color

The hardware notch is black. Use color as accent, not background noise.

Good uses:

- Album-art average color for a visualizer or subtle glow.
- Battery color only for warning/charging status.
- Blue accent only for interactive selected controls.
- System colors for accessibility and vibrancy where appropriate.

Avoid saturated neon backgrounds unless the whole product is intentionally playful.

### Materials

For classic notch effects, black is more convincing than glass. For macOS Tahoe/Liquid Glass-inspired versions, use glass inside the expanded content area, not on the closed hardware edge.

Suggested approach:

- Closed shell: black.
- Open shell: black or near-black.
- Internal cards: subtle material or dark elevated panels.
- Do not make the closed notch translucent; it will stop matching the camera housing.

---
