# Interactions and Motion

> Read when: Root view composition, interaction design, and animation rules. Back to [SKILL.md](SKILL.md).

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
