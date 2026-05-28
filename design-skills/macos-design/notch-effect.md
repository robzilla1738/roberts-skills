# Notch Effect

> Read when: designing or implementing a notch-style macOS app — top-center panel, hardware-aligned black shell, peek/HUD/shelf modules, Dynamic Island behavior. Back to [SKILL.md](SKILL.md).

Use this spoke when designing or implementing a beautiful macOS notch-style app: a small, top-center, always-available surface that visually merges with the MacBook camera housing or simulates one on non-notch displays. The goal is to create a polished, native-feeling dynamic island for macOS, not a gimmick that fights the menu bar.

This spoke is inspired by public architectural patterns visible in TheBoredTeam's `boring.notch` project, but it should not copy that GPL-licensed code unless the resulting project complies with the GPL. Prefer original implementation using the patterns below.

For standard windowed apps that should avoid the camera housing, see [layout-and-windowing.md](layout-and-windowing.md) §3 instead.

---

## 1. Core Mental Model

A notch app is not a normal app window. It is a tiny, borderless, transparent, top-center panel whose visible SwiftUI content is shaped to look like the physical black notch. The app then animates that closed shape into a larger capsule/card when the user hovers, taps, drags, or when a transient system event appears.

Think in layers:

1. **Window layer**: an AppKit `NSPanel`/`NSWindow` that is transparent, borderless, nonactivating, above normal windows, and pinned to the top center of a screen.
2. **Shape layer**: a SwiftUI black notch silhouette with separately animated top and bottom radii.
3. **State layer**: a small state machine: hidden, closed, peek, open, expanded, dragging, transient HUD.
4. **Content layer**: compact modules such as Now Playing, volume, brightness, battery, calendar, file shelf, camera mirror, shortcuts, or live activity cards.
5. **Interaction layer**: hover delay, click-to-open, drag-to-open, drop target, keyboard shortcut, menu bar extra, and timed auto-dismiss.
6. **Adaptation layer**: per-display positioning, notch/no-notch fallback, safe-area handling, full-screen spaces, screen recording privacy, and accessibility.

The trick is making the panel feel like it belongs to the display hardware. The closed state should be visually indistinguishable from the notch or a centered menu-bar pill. The open state should feel like the notch is stretching downward.

---

## 2. Recommended File Structure

For a serious SwiftUI + AppKit app, use a structure like this:

```text
NotchApp/
  App/
    NotchApp.swift
    AppDelegate.swift
    StatusItemController.swift
  Window/
    NotchPanel.swift
    NotchWindowController.swift
    DisplayManager.swift
    NotchGeometry.swift
  Model/
    NotchState.swift
    NotchViewModel.swift
    Preferences.swift
  UI/
    NotchRootView.swift
    NotchShape.swift
    NotchBackground.swift
    NotchHeader.swift
    PeekView.swift
    OpenNotchView.swift
    LiveActivityView.swift
  Modules/
    Music/
    HUD/
    Battery/
    Shelf/
    Calendar/
    Camera/
  Input/
    HoverController.swift
    GestureModifiers.swift
    DragDetector.swift
  Utilities/
    Haptics.swift
    AccessibilityPermissions.swift
    ColorSampling.swift
```

Keep AppKit window management separate from SwiftUI view composition. The SwiftUI layer should not know too much about screen coordinates.

---

## 3. Window Layer

### Use a transparent nonactivating panel

The notch surface should usually be an `NSPanel`, not a normal titled window.

Desired traits:

- Borderless.
- Nonactivating, so opening it does not steal focus from the current app.
- Transparent background.
- Not movable by the user.
- No titlebar.
- Above the menu bar or near menu-bar level.
- Joins all spaces if the app is intended to be omnipresent.
- Full-screen auxiliary behavior so it can appear over full-screen apps.
- Not part of Cmd-Tab or normal window cycling.

Implementation pattern:

```swift
final class NotchPanel: NSPanel {
    init(contentRect: NSRect) {
        super.init(
            contentRect: contentRect,
            styleMask: [.borderless, .nonactivatingPanel, .utilityWindow, .hudWindow],
            backing: .buffered,
            defer: false
        )

        isFloatingPanel = true
        isOpaque = false
        backgroundColor = .clear
        titleVisibility = .hidden
        titlebarAppearsTransparent = true
        isMovable = false
        hasShadow = false
        isReleasedWhenClosed = false
        level = .mainMenu + 3
        collectionBehavior = [
            .fullScreenAuxiliary,
            .stationary,
            .canJoinAllSpaces,
            .ignoresCycle
        ]
    }

    override var canBecomeKey: Bool { false }
    override var canBecomeMain: Bool { false }
}
```

Use `NSHostingView(rootView:)` to host SwiftUI content.

### Position the window at the top center

A notch panel is usually larger than the closed notch because the open state needs room to grow downward. Position the panel itself at the top-center of the target screen; keep the SwiftUI content aligned to the top inside it.

```swift
func position(_ window: NSWindow, on screen: NSScreen) {
    let frame = screen.frame
    let x = frame.origin.x + frame.width / 2 - window.frame.width / 2
    let y = frame.origin.y + frame.height - window.frame.height
    window.setFrameOrigin(NSPoint(x: x, y: y))
}
```

Do not use `visibleFrame` for final y-positioning if you want the panel to touch the top hardware edge. Use the full `screen.frame` and then account for safe areas in your geometry calculations.

### Handle multiple displays

Provide a setting for:

- Show only on preferred display.
- Automatically follow main display.
- Show on all displays.

Use stable display UUIDs, not display names, because names can collide or change. Observe `NSApplication.didChangeScreenParametersNotification` and reposition/recreate panels when screens change.

### Avoid private framework dependency unless absolutely necessary

Some notch apps use private SkyLight behavior for special cases such as lock-screen or space behavior. Do not depend on private frameworks for normal App Store-ready behavior. Private frameworks can break across macOS versions and may block App Store distribution.

For a shippable app, start with public AppKit APIs: `NSPanel`, collection behaviors, window levels, and accessibility permissions only when necessary.

---

## 4. Geometry and Notch Detection

### Closed size

A convincing closed notch needs to match the hardware notch when one exists and degrade gracefully when one does not.

Use this logic:

1. Start with a fallback width around `180–210 pt` and a fallback height around the menu bar height.
2. If the screen has a top safe area, treat it as a notch display.
3. Derive notch height from `screen.safeAreaInsets.top` or the menu-bar height depending on user preference.
4. Derive notch width from `auxiliaryTopLeftArea` and `auxiliaryTopRightArea` if available.
5. For non-notch screens, render a smaller centered pill, or let users set a custom simulated notch height.

Conceptual geometry:

```swift
struct NotchGeometry {
    var closedWidth: CGFloat
    var closedHeight: CGFloat
    var openWidth: CGFloat
    var openHeight: CGFloat
    var shadowPadding: CGFloat
}
```

Suggested defaults:

```swift
let closedFallbackWidth: CGFloat = 185
let closedFallbackHeight: CGFloat = 32
let openSize = CGSize(width: 640, height: 190)
let shadowPadding: CGFloat = 20
```

### Open size

A beautiful notch app expands downward and sideways, but not too far. Good starting values:

- Compact open: `420 × 140`.
- Media open: `560 × 180`.
- Shelf/dashboard open: `640 × 190`.
- Large utility mode: `720 × 260`, only when needed.

Never let the open view feel like a normal window glued to the top. It should still feel anchored to the notch.

---

## 5. Shape Layer

### Use a custom SwiftUI Shape

A notch shape is not just a rounded rectangle. It is flatter at the top and more rounded at the lower corners, creating the illusion that the panel is attached to the display edge.

Create a shape with independently animatable top and bottom corner radii:

```swift
struct NotchShape: Shape {
    var topRadius: CGFloat = 6
    var bottomRadius: CGFloat = 14

    var animatableData: AnimatablePair<CGFloat, CGFloat> {
        get { AnimatablePair(topRadius, bottomRadius) }
        set {
            topRadius = newValue.first
            bottomRadius = newValue.second
        }
    }

    func path(in rect: CGRect) -> Path {
        var path = Path()
        path.move(to: CGPoint(x: rect.minX, y: rect.minY))
        path.addQuadCurve(
            to: CGPoint(x: rect.minX + topRadius, y: rect.minY + topRadius),
            control: CGPoint(x: rect.minX + topRadius, y: rect.minY)
        )
        path.addLine(to: CGPoint(x: rect.minX + topRadius, y: rect.maxY - bottomRadius))
        path.addQuadCurve(
            to: CGPoint(x: rect.minX + topRadius + bottomRadius, y: rect.maxY),
            control: CGPoint(x: rect.minX + topRadius, y: rect.maxY)
        )
        path.addLine(to: CGPoint(x: rect.maxX - topRadius - bottomRadius, y: rect.maxY))
        path.addQuadCurve(
            to: CGPoint(x: rect.maxX - topRadius, y: rect.maxY - bottomRadius),
            control: CGPoint(x: rect.maxX - topRadius, y: rect.maxY)
        )
        path.addLine(to: CGPoint(x: rect.maxX - topRadius, y: rect.minY + topRadius))
        path.addQuadCurve(
            to: CGPoint(x: rect.maxX, y: rect.minY),
            control: CGPoint(x: rect.maxX - topRadius, y: rect.minY)
        )
        path.closeSubpath()
        return path
    }
}
```

Suggested radii:

```swift
let closedTopRadius: CGFloat = 6
let closedBottomRadius: CGFloat = 14
let openTopRadius: CGFloat = 19
let openBottomRadius: CGFloat = 24
```

### Draw a black hardware-matched background

The closed state should usually be pure black or near-black. This visually fuses with the physical notch.

Use:

```swift
.background(Color.black)
.clipShape(NotchShape(topRadius: top, bottomRadius: bottom))
```

Add a tiny top black strip to prevent anti-aliased light seams at the display edge:

```swift
.overlay(alignment: .top) {
    Rectangle()
        .fill(.black)
        .frame(height: 1)
        .padding(.horizontal, topRadius)
}
```

### Shadow rules

Use shadows only when the notch is open or hovered. In closed state, shadows often make the hardware merge worse.

Good default:

```swift
.shadow(color: isOpenOrHovering ? .black.opacity(0.55) : .clear, radius: 6, y: 2)
```

---

## 6. State Machine

Use a clear state machine. Avoid scattering boolean flags everywhere.

Recommended states:

```swift
enum NotchState: Equatable {
    case hidden
    case closed
    case peeking(PeekKind)
    case open(OpenPanel)
    case expanded(ExpandedKind)
    case dragging
}

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

Rules:

- `closed` is the idle state.
- `peeking` is transient and auto-dismisses after `1.2–3.0s`.
- `open` is interactive and remains while hovered, tapped, or focused by an active popover.
- `expanded` is for richer content such as shelf, calendar, or camera.
- `dragging` opens the shelf/drop zone immediately.

Use cancellable tasks for auto-dismiss:

```swift
@MainActor
final class NotchViewModel: ObservableObject {
    @Published var state: NotchState = .closed
    private var dismissTask: Task<Void, Never>?

    func showPeek(_ kind: PeekKind, duration: TimeInterval = 1.5) {
        dismissTask?.cancel()
        withAnimation(.smooth) { state = .peeking(kind) }
        dismissTask = Task { [weak self] in
            try? await Task.sleep(for: .seconds(duration))
            guard !Task.isCancelled else { return }
            await MainActor.run {
                withAnimation(.smooth) { self?.state = .closed }
            }
        }
    }

    func open(_ panel: OpenPanel = .home) {
        dismissTask?.cancel()
        withAnimation(.interactiveSpring(response: 0.38, dampingFraction: 0.8)) {
            state = .open(panel)
        }
    }

    func close() {
        dismissTask?.cancel()
        withAnimation(.spring(response: 0.45, dampingFraction: 1.0)) {
            state = .closed
        }
    }
}
```

---

## 7. Root View Composition

Structure the SwiftUI root view around top alignment:

```swift
struct NotchRootView: View {
    @EnvironmentObject var model: NotchViewModel
    @State private var isHovering = false
    @State private var hoverTask: Task<Void, Never>?

    var body: some View {
        ZStack(alignment: .top) {
            notchBody
                .frame(width: currentWidth, height: currentHeight, alignment: .top)
                .background(.black)
                .clipShape(currentShape)
                .shadow(color: shadowColor, radius: shadowRadius, y: 2)
                .contentShape(Rectangle())
                .onHover(perform: handleHover)
                .onTapGesture { model.open() }
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .top)
    }
}
```

The visible body should be clipped, but the outer panel should be large enough to contain shadows and open content.

---

## 8. Interaction Design

### Hover

Hover should feel intentional, not twitchy.

Recommended behavior:

- On hover enter: set `isHovering = true` immediately and optionally show a tiny highlight/haptic.
- Wait `0.25–0.6s` before opening.
- If the pointer leaves before the delay, cancel opening.
- On hover exit: wait `75–150ms`, then close unless a popover, drag operation, or sharing flow is active.

```swift
private func handleHover(_ hovering: Bool) {
    hoverTask?.cancel()

    if hovering {
        isHovering = true
        guard model.state == .closed else { return }
        hoverTask = Task {
            try? await Task.sleep(for: .milliseconds(350))
            guard !Task.isCancelled else { return }
            await MainActor.run {
                if isHovering { model.open() }
            }
        }
    } else {
        hoverTask = Task {
            try? await Task.sleep(for: .milliseconds(100))
            guard !Task.isCancelled else { return }
            await MainActor.run {
                isHovering = false
                model.close()
            }
        }
    }
}
```

### Tap

Tap should open immediately. A second tap may close, but do not make this the only close method.

### Drag down / up

A downward pan from the notch should stretch the shape and then open. An upward pan should collapse.

Good pattern:

- Track `gestureProgress`.
- Map translation to vertical scale and height.
- On release, open if threshold exceeded; otherwise spring back.

### Drop target

A file-shelf notch feels magical when dragging files toward the notch opens it.

Implementation pattern:

- Add a transparent top-center drag detector region at the AppKit level, or use SwiftUI `.onDrop` if the drag reaches the visible panel.
- Region should be wider than the closed notch, often matching the open width.
- On drag enters region: open shelf view.
- On drop: load file URLs, plain text, URLs, and data providers.

### Haptics

Use haptics sparingly. Trigger on open threshold, drop accepted, or successful command. Do not vibrate on every hover tick.

---

## 9. Animation Rules

A notch effect lives or dies by animation quality.

Recommended defaults:

```swift
let openAnimation = Animation.spring(response: 0.42, dampingFraction: 0.8, blendDuration: 0)
let closeAnimation = Animation.spring(response: 0.45, dampingFraction: 1.0, blendDuration: 0)
let dragAnimation = Animation.smooth
```

Use:

- `matchedGeometryEffect` for album art, icons, and small visualizers moving between closed and open states.
- Separate opacity and scale transitions for content that appears after expansion.
- Stagger content slightly: shape expands first, controls fade/slide in after `40–90ms`.
- Keep the top edge visually pinned; expansion should mostly grow downward.

Avoid:

- Bouncy cartoon movement for utility apps.
- Overlong animations above `500ms`.
- Animating every child independently with unrelated springs.
- Opening instantly on accidental pointer fly-by.

---

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

## 11. Content Modules That Work Well

### Music / Now Playing

Closed:

- Album art thumbnail.
- Tiny visualizer.
- Optional play/pause glyph.

Open:

- Album art.
- Track title and artist.
- Previous/play-next buttons.
- Progress bar.
- Volume or output route shortcut.

Polish:

- Use average album color for visualizer gradient or soft glow.
- Use `matchedGeometryEffect` for album art between closed and open.
- Avoid scrolling marquee unless text is truly clipped.

### System HUD replacement

Closed/peek:

- Volume, brightness, keyboard backlight, mic, battery, or download progress.
- Auto-dismiss after `1.2–2s`.

Important:

- Only intercept media keys or suppress system HUDs with user consent and required accessibility permissions.
- Provide a setting to disable HUD replacement.
- Fall back gracefully if permission is denied.

### File shelf

Behavior:

- Drag file toward notch.
- Notch opens into shelf.
- Drop files, URLs, text, or images.
- Allow quick share, AirDrop, copy, reveal in Finder, remove.

Design:

- Use small file cards.
- Show file type icon, name, and size.
- Make the drop zone feel like a tray sliding out of the notch.

### Calendar / reminders

Best as a small glanceable dashboard:

- Next event.
- Time until event.
- Join button.
- Today’s remaining events.

Do not build a full calendar app inside the notch.

### Camera mirror

Good as a utility module:

- Quick mirror before calls.
- Small preview only.
- Explicit camera permission request.
- Clear privacy indicator and exit.

### Weather / Bluetooth / charging

These should usually be peek or compact modules, not dominant panels.

---

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

## Related topics

- [layout-and-windowing.md](layout-and-windowing.md) — safe areas vs notch apps; when not to fake a notch in standard windows
- [appkit-patterns.md](appkit-patterns.md) — `NSPanel`, screen geometry, safe-area helpers
- [toolbars-and-menus.md](toolbars-and-menus.md) — menu bar extra fallback controls
- [accessibility.md](accessibility.md) — Reduce Motion, permissions, keyboard access
- [swiftui-patterns.md](swiftui-patterns.md) — SwiftUI hosting and composition patterns
- [critique-checklists.md](critique-checklists.md) — launch checklist and anti-patterns
