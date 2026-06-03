# Foundations

> Read when: NSPanel window layer, geometry, custom shape, and state machine. Back to [SKILL.md](SKILL.md).

Use this spoke when building the notch **shell** — window, geometry, custom shape, and state machine — before adding content modules.

GPL note: public reference implementations exist ([ecosystem-landscape.md](ecosystem-landscape.md)). Do not copy GPL source unless your project complies. Prefer original code using these patterns.

For standard windowed apps that should avoid the camera housing, see [macos-design layout-and-windowing](../macos-design/layout-and-windowing.md) instead.

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

### Open and expanded targets

Keep panel routing explicit so SwiftUI does not branch on loose strings:

```swift
enum OpenPanel: Equatable {
    case home
    case music
    case shelf
    case calendar
    case settings
}

enum ExpandedKind: Equatable {
    case shelf
    case calendar
    case camera
    case dashboard
}
```

Use `open(.music)` for tab-like modules and `expanded(.shelf)` when the shell grows taller than a standard open card.

---
