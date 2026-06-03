# Integration and Shipping

> Read when: Menu bar fallback, preferences, accessibility, edge cases, checklists, and build order. Back to [SKILL.md](SKILL.md).

## 12. Menu Bar Integration

A notch app should usually include a menu bar extra because the notch itself may be hidden, closed, or unavailable on external displays.

Menu bar menu should include:

- Open/close notch.
- Current module selection.
- Preferences.
- Display selection.
- Enable/disable hover open.
- Enable/disable HUD replacement.
- Launch at login.
- Quit.

Do not put every feature only in the notch UI. The menu bar is the fallback control surface.

---

## 13. Preferences

Expose power-user settings without making the default experience complicated.

Good settings:

- Preferred display.
- Show on all displays.
- Automatically follow active display.
- Open on hover.
- Minimum hover duration.
- Enable gestures.
- Enable haptics.
- Show live activity when closed.
- Simulated notch size on non-notch displays.
- Match real notch height / match menu bar height / custom height.
- Hide from screen recording.
- HUD replacement.
- Launch at login.

Use safe defaults:

- Open on hover: on.
- Hover delay: `0.35s`.
- Haptics: on if available.
- HUD replacement: off until permission granted.
- Show on all displays: off.
- Closed live activity: conservative.

---

## 14. Accessibility and Permissions

A beautiful notch app should not be hostile to accessibility.

Requirements:

- Respect Reduce Motion: shorten or remove spring animations.
- Respect Increase Contrast: ensure controls remain visible in black UI.
- Provide keyboard shortcuts for open/close and module navigation.
- Ensure controls have accessibility labels.
- Do not trap focus.
- Do not steal app focus unless opening a real settings window.
- Make hover behavior optional.
- Avoid tiny-only targets for essential actions.

Permission rules:

- Camera/microphone: ask only when the user opens those modules.
- Calendar/reminders: ask only when enabling those modules.
- Accessibility/input monitoring: ask only for HUD/media-key replacement or global shortcuts that require it.
- Screen recording privacy: provide setting and explain tradeoff.

---

## 15. Display and Safe-Area Edge Cases

Handle:

- MacBook with notch.
- MacBook without notch.
- External monitor.
- Multiple monitors with different menu bar positions.
- Full-screen apps.
- Mission Control / Spaces.
- Menu bar auto-hide.
- Screen resolution changes.
- Display sleep/wake.
- Clamshell mode.

Rules:

- Never assume one screen.
- Never assume the notch exists.
- Never assume the menu bar height equals notch height.
- Recompute geometry on screen changes.
- Store preferred screen by UUID.
- Hide or simulate gracefully when the physical notch is absent.

---

## 16. Quality Checklist

Before calling a notch app polished, verify:

- Closed state aligns exactly with the physical notch or simulated center pill.
- No white/transparent seam appears at the top edge.
- The panel does not steal focus from the active app.
- Hover open does not trigger accidentally during normal menu-bar use.
- Open and close animations keep the top edge anchored.
- Text and controls do not clip during animation.
- The app works on external displays.
- The app works in full-screen spaces.
- The app survives display connect/disconnect.
- The app has a menu bar fallback.
- The user can disable hover, haptics, HUD replacement, and closed live activity.
- Permissions are requested just-in-time.
- The UI remains readable in light and dark macOS appearances.
- Reduce Motion is respected.
- The app does not depend on private frameworks for core behavior.

---

## 17. Common Anti-Patterns

Avoid these:

- Making the notch a normal floating rounded rectangle with no hardware alignment.
- Using translucent glass for the closed notch, causing it not to match the camera housing.
- Opening instantly on hover with no delay.
- Stealing focus whenever the notch opens.
- Making every module large and busy.
- Ignoring external displays.
- Hardcoding one notch size for all MacBooks.
- Requiring accessibility permission before the user enables a feature that needs it.
- Treating the notch as a full app launcher or notification center clone.
- Hiding critical controls inside hover-only UI with no menu bar fallback.

---

## 18. LLM Implementation Prompt Template

When asked to create a notch app, follow this prompt internally:

```text
Create a native macOS SwiftUI + AppKit notch-style app.

Architecture:
- Use an AppKit NSPanel subclass for the floating notch window.
- Make it borderless, transparent, nonactivating, above menu bar level, and joined to all spaces only if configured.
- Host SwiftUI with NSHostingView.
- Position the panel at the top center of the selected NSScreen.
- Recompute geometry on screen changes.

Geometry:
- Detect notch displays using safeAreaInsets.top and auxiliary top areas when available.
- Use fallback simulated notch dimensions for non-notch displays.
- Keep closed notch compact and open state around 560–640 pt wide by 160–200 pt tall.

UI:
- Implement a custom animatable NotchShape with separate top and bottom radii.
- Use a black shell that visually fuses with the hardware notch.
- Add subtle shadow only when open or hovered.
- Keep content aligned to the top so the notch appears to grow downward.

State:
- Implement a state machine: closed, peeking, open, expanded, dragging.
- Use cancellable Swift concurrency tasks for hover delay and auto-dismiss.
- Use spring animations and matchedGeometryEffect for polished transitions.

Interactions:
- Hover opens after a short delay.
- Tap opens immediately.
- Optional pan down opens and pan up closes.
- Optional file drag opens shelf mode.
- Provide a menu bar extra for preferences and fallback controls.

Accessibility:
- Respect Reduce Motion.
- Do not steal focus.
- Use accessibility labels and keyboard shortcuts.
- Ask for permissions only when needed.
```

---

## 19. Minimal Build Order

Build in this order:

1. `NotchPanel`: transparent nonactivating top-center panel.
2. `NotchGeometry`: closed/open sizes, screen positioning, safe-area fallback.
3. `NotchShape`: animatable shape with top/bottom radii.
4. `NotchViewModel`: closed/open/peek state machine.
5. `NotchRootView`: black shell with hover/tap open/close.
6. `StatusItemController`: menu bar fallback.
7. `Music` or `HUD` module: one high-quality module first.
8. Preferences: hover delay, display selection, simulated notch size.
9. Multi-display and full-screen QA.
10. Accessibility and Reduce Motion polish.

Do not start with every module. Start with one perfect notch shell and one perfect interaction.

---

## 20. Design Direction Summary

The best notch apps feel like hardware that learned a few useful tricks. They are calm when idle, responsive when approached, and useful only when they have something contextual to show. Keep the closed notch nearly invisible, make the expansion buttery, and make every module glanceable.

The visual formula is:

```text
hardware-aligned black shell
+ top-pinned expansion
+ spring motion
+ tiny live activity
+ transient peeks
+ one strong utility module
+ menu bar fallback
= beautiful macOS notch app
```

---


---

## Related topics

- [../macos-design/layout-and-windowing.md](../macos-design/layout-and-windowing.md) — safe areas vs notch apps; when not to fake a notch in standard windows
- [../macos-design/appkit-patterns.md](../macos-design/appkit-patterns.md) — `NSPanel`, screen geometry, safe-area helpers
- [../macos-design/toolbars-and-menus.md](../macos-design/toolbars-and-menus.md) — menu bar extra fallback controls
- [../macos-design/accessibility.md](../macos-design/accessibility.md) — Reduce Motion, permissions, keyboard access
- [../macos-design/swiftui-patterns.md](../macos-design/swiftui-patterns.md) — SwiftUI hosting and composition patterns
- [../macos-design/critique-checklists.md](../macos-design/critique-checklists.md) — launch checklist and anti-patterns
