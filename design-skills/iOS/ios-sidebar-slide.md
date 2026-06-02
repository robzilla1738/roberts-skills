# iOS Sidebar Slide Effect Recipe

This documents the current Joyflow-style compact sidebar interaction in an app-agnostic way so it can be rebuilt elsewhere.

## Goal

Create a mobile sidebar where the sidebar is a full-height underlay and the main app/chat surface slides right on top of it. The foreground surface becomes a large rounded card while opening, with a light shadow and subtle dimming. The sidebar itself does not slide over the app; the app moves away to reveal the sidebar beneath it.

## Layer Model

Use two sibling layers inside a full-screen leading-aligned container:

1. Sidebar underlay
   - `zIndex = 0`
   - Full height, ignores vertical safe area.
   - Fixed drawer width.
   - Does not move during open/close.
   - Draws behind the main app surface.

2. Foreground app surface
   - `zIndex = 1`
   - Full screen width and height.
   - Contains the normal navigation/chat/content stack.
   - Moves horizontally to reveal the sidebar.
   - Gets rounded corners, light edge shadow, and a very subtle overlay as it opens.

The important detail: do not animate the sidebar over the chat. Animate the chat/main surface over a stationary sidebar.

## Geometry

Recommended constants:

```swift
let drawerWidth = min(screenWidth * 0.86, 372)
let foregroundOverlap: CGFloat = 48
let foregroundOpenOffset = drawerWidth - foregroundOverlap
```

The overlap keeps the foreground card sitting on top of the sidebar instead of stopping exactly at the sidebar edge.

Progress:

```swift
let progress = clamp(foregroundOffset / foregroundOpenOffset, 0, 1)
```

Use `progress` to drive corner radius, overlay opacity, and shadow opacity.

## Open/Close State

Track two drag offsets:

```swift
var isDrawerOpen: Bool
var closeDragOffset: CGFloat // negative while closing
var openDragOffset: CGFloat  // positive while opening
```

Foreground offset:

```swift
let foregroundOffset =
  isDrawerOpen
    ? max(0, foregroundOpenOffset + closeDragOffset)
    : max(0, min(foregroundOpenOffset, openDragOffset))
```

Closing drag clamps from `0` to `-foregroundOpenOffset`.
Opening drag clamps from `0` to `foregroundOpenOffset`.

## Motion

Use a non-spring ease-out timing curve. This keeps the motion fluid and free without rubbery bounce.

Current tuning:

```swift
duration: 0.40
cubic bezier: (0.16, 1, 0.30, 1)
```

For reduced motion:

```swift
duration: 0.01
```

Open/close should use the same animation. Any navigation action after closing should be delayed by the same duration so the drawer finishes before pushing a new screen.

## Gesture Rules

Open gesture:

```swift
DragGesture(minimumDistance: 12)
```

Only start opening when:

```swift
startX < 28
dx > 0
verticalMovement < horizontalMovement * 0.8
no pushed navigation path is active
drawer is closed
```

Open if:

```swift
dx > foregroundOpenOffset * 0.28
predictedEndDx > foregroundOpenOffset * 0.45
```

Close gesture:

Only close when:

```swift
drawer is open
dx < 0
verticalMovement < horizontalMovement * 0.9
```

Close if:

```swift
dx < -70
predictedEndDx < -foregroundOpenOffset * 0.45
```

Also allow tapping the foreground dim layer to close.

## Foreground Card Treatment

The foreground app surface should be full-screen even while rounded. Do not shrink or safe-area-frame the content. Clip the whole full-screen foreground layer.

Current visual constants:

```swift
cornerRadius = 52 * progress
dimOverlayOpacity = 0.04 * progress
highlightStrokeOpacity = 0.05 * progress
highlightStrokeWidth = 0.75
sideShadow = black.opacity(0.08 * progress), radius: 12, x: -5, y: 0
dropShadow = black.opacity(0.05 * progress), radius: 18, x: -2, y: 8
```

The shadows should be light. Heavy shadows create a dirty gray band over the sidebar.

## Sidebar Layout

The sidebar is a full-height underlay:

```swift
frame(width: drawerWidth)
frame(maxHeight: .infinity)
ignoresSafeArea(.container, edges: .vertical)
background(sidebarBackground)
```

Do not round or clip the sidebar itself. The foreground card provides the rounded popout.

Content should respect safe areas manually:

```swift
top padding = max(88, topSafeArea + 42)
bottom padding = max(12, bottomSafeArea + 8)
```

Add a trailing protected inset so text and controls do not disappear under the foreground card overlap:

```swift
trailingProtectedInset = 48
horizontal padding = leading 22, trailing 22 + trailingProtectedInset
```

Footer CTA:

```swift
height: 40
footer height: 76
button y offset: -8
```

Keep the CTA on the trailing side, but inside the protected area.

## Sidebar Content

Current compact drawer structure:

1. Header
   - Workspace/app name on left.
   - Account/avatar button on right.

2. Primary rows
   - Overview
   - Channels disclosure
   - Tasks
   - Notes

3. Chats
   - Show up to 5 recent chats.
   - Sort by most recent activity.
   - Add a final "Show all chats" or "All chats" row.

4. More
   - Memory
   - Approvals
   - Agents
   - Skills

5. Footer
   - New Chat CTA.

## SwiftUI Skeleton

```swift
GeometryReader { proxy in
    let drawerWidth = min(proxy.size.width * 0.86, 372)
    let foregroundOpenOffset = drawerWidth - 48
    let foregroundOffset = ...
    let progress = ...

    ZStack(alignment: .leading) {
        SidebarView(
            topInset: proxy.safeAreaInsets.top,
            bottomInset: proxy.safeAreaInsets.bottom,
            trailingProtectedInset: 48
        )
        .frame(width: drawerWidth)
        .frame(maxHeight: .infinity, alignment: .leading)
        .ignoresSafeArea(.container, edges: .vertical)
        .zIndex(0)

        ZStack {
            NavigationStack {
                MainContent()
            }

            Color.black
                .opacity(0.04 * progress)
                .allowsHitTesting(isDrawerOpen)
                .onTapGesture { closeDrawer() }
        }
        .frame(width: proxy.size.width, height: proxy.size.height)
        .background(pageBackground)
        .clipShape(RoundedRectangle(cornerRadius: 52 * progress, style: .continuous))
        .overlay {
            RoundedRectangle(cornerRadius: 52 * progress, style: .continuous)
                .strokeBorder(Color.white.opacity(0.05 * progress), lineWidth: 0.75)
        }
        .offset(x: foregroundOffset)
        .shadow(color: .black.opacity(0.08 * progress), radius: 12, x: -5, y: 0)
        .shadow(color: .black.opacity(0.05 * progress), radius: 18, x: -2, y: 8)
        .zIndex(1)
    }
}
.ignoresSafeArea(.container, edges: .vertical)
```

## Quality Checks

Before calling it done:

- Closed state: main screen is normal full-height, no rounded/inset look.
- Open state: sidebar is visible top-to-bottom.
- Open state: foreground card sits on top of sidebar, overlapping its right edge.
- Open state: top and bottom foreground card corners are visibly rounded.
- Open state: sidebar text and footer CTA do not sit under the foreground card.
- Header clears status bar/Dynamic Island/notch.
- Gesture opening follows the finger, not just snaps open after release.
- Close drag follows the finger leftward.
- Shadow is visible but light; no thick gray band.
- Reduce Motion uses near-instant linear animation.

## Common Mistakes

- Sliding the sidebar over the chat instead of sliding the chat over the sidebar.
- Giving the foreground a safe-area height, which makes the chat no longer top-to-bottom.
- Rounding/clipping the sidebar; the foreground should be the rounded card.
- Letting sidebar labels or CTA extend under the foreground card edge.
- Using a spring that bounces; the target feel is smooth, fluid, and controlled.
- Using too much shadow or dimming, which makes the sidebar look dirty.
