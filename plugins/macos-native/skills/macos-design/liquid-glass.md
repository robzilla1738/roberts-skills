# Liquid Glass

> Read when: Liquid Glass placement, hierarchy, tinting, or material restraint. Back to [SKILL.md](SKILL.md).

## 1. Liquid Glass and current material design

Liquid Glass is an adaptive material for modern Apple-platform UI. It can refract and reflect underlying content, respond to context, and provide separation while allowing content to feel more expansive. Used well, it makes app chrome lighter and more integrated. Used poorly, it becomes visual noise.

### 1.1 Where Liquid Glass belongs

Use Liquid Glass for:

- Toolbars and toolbar item groups
- Floating navigation controls
- Sidebars and inspectors through standard containers
- Top-level controls over media/canvas content
- Search fields and command controls where the system applies it
- Prominent buttons that represent primary actions in a suitable context
- Custom controls that genuinely function as top-level chrome

### 1.2 Where Liquid Glass usually does not belong

Avoid Liquid Glass for:

- Ordinary content cards
- Table rows
- List cells
- Every button in a form
- Background panels behind text-heavy content
- Decorative borders
- Nested glass layers
- Dense inspector sections
- Static labels or status text
- Anything that does not need the visual behavior of glass

### 1.3 Glass hierarchy

Think in layers:

```text
Content layer
  The user’s documents, media, tables, text, diagrams, records, messages, or data.

Functional glass layer
  Navigation, toolbar controls, floating controls, sidebar/inspector chrome, top-level actions.

Modal layer
  Sheets, popovers, alerts, dimming, confirmation UI.
```

Rules:

- Glass should usually float above content, not become the content.
- Do not place glass on top of glass in steady state.
- Do not let high-contrast content intersect awkwardly with glass edges.
- Do not use glass as a substitute for layout hierarchy.
- Use standard containers so the system samples and renders glass correctly.

### 1.4 Regular versus Clear glass

Use regular glass for most UI chrome. Clear glass is more transparent and should be reserved for media-rich contexts where the background can support it.

Rules:

- Do not mix regular and clear glass in the same control cluster unless Apple’s current SDK and design guidance explicitly supports it for that pattern.
- Use clear glass only with suitable dimming/contrast treatment behind it.
- Ensure labels and icons remain legible over varied content.

### 1.5 Tinting glass

Tint can communicate meaning, but it quickly becomes noisy.

Rules:

- Tint a primary action when it truly deserves emphasis.
- Use semantic colors for destructive, warning, success, or selected states.
- Do not tint all toolbar controls.
- Do not use brand color as a blanket glass tint.
- Test tint in light mode, dark mode, high contrast, and over varied backgrounds.

### 1.6 Glass grouping

When multiple custom glass views appear near each other, group them so the system can render them as a coherent effect and avoid incorrect sampling.

SwiftUI pattern:

```swift
import SwiftUI

struct FloatingCanvasControls: View {
    @State private var tool: Tool = .select

    var body: some View {
        if #available(macOS 26.0, *) {
            GlassEffectContainer {
                HStack(spacing: 8) {
                    Button("Select", systemImage: "cursorarrow") { tool = .select }
                    Button("Draw", systemImage: "pencil") { tool = .draw }
                    Button("Erase", systemImage: "eraser") { tool = .erase }
                }
                .labelStyle(.iconOnly)
                .padding(8)
                .glassEffect()
                .accessibilityLabel("Canvas tools")
            }
        } else {
            HStack(spacing: 8) {
                Button("Select", systemImage: "cursorarrow") { tool = .select }
                Button("Draw", systemImage: "pencil") { tool = .draw }
                Button("Erase", systemImage: "eraser") { tool = .erase }
            }
            .labelStyle(.iconOnly)
            .padding(8)
            .background(.regularMaterial, in: Capsule())
        }
    }
}

enum Tool { case select, draw, erase }
```

AppKit pattern:

```swift
import AppKit

@available(macOS 26.0, *)
final class FloatingControlCluster: NSViewController {
    override func loadView() {
        let container = NSGlassEffectContainerView()
        let glassView = NSGlassEffectView()

        glassView.cornerRadius = 18
        glassView.contentView = makeControls()
        container.addSubview(glassView)

        glassView.translatesAutoresizingMaskIntoConstraints = false
        NSLayoutConstraint.activate([
            glassView.leadingAnchor.constraint(equalTo: container.leadingAnchor),
            glassView.trailingAnchor.constraint(equalTo: container.trailingAnchor),
            glassView.topAnchor.constraint(equalTo: container.topAnchor),
            glassView.bottomAnchor.constraint(equalTo: container.bottomAnchor)
        ])

        view = container
    }

    private func makeControls() -> NSView {
        let stack = NSStackView()
        stack.orientation = .horizontal
        stack.spacing = 8
        stack.edgeInsets = NSEdgeInsets(top: 8, left: 8, bottom: 8, right: 8)
        return stack
    }
}
```

### 1.7 Glass anti-patterns

Reject designs that:

- Apply glass to every card or panel.
- Put glass behind long-form text.
- Use glass only because it looks trendy.
- Stack multiple translucent materials without purpose.
- Reduce contrast below accessible levels.
- Use custom blur/material code instead of system glass/material components.
- Hide hierarchy behind effects.
- Create motion-heavy glass effects that ignore Reduce Motion.
## Related topics

- [icons-and-visual-language.md](icons-and-visual-language.md) — materials, color, and shape vocabulary
- [layout-and-windowing.md](layout-and-windowing.md) — where glass does not belong in content
- [swiftui-patterns.md](swiftui-patterns.md) — GlassEffectContainer and glassEffect APIs
- [appkit-patterns.md](appkit-patterns.md) — NSGlassEffectView patterns
