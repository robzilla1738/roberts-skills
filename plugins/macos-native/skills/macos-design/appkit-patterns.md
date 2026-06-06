# AppKit Patterns

> Read when: AppKit split views, responder chain, safe areas, or Mac Catalyst. Back to [SKILL.md](SKILL.md).

## 1. AppKit-specific guidance

### 1.1 Use AppKit strengths

AppKit remains powerful for mature desktop patterns:

- `NSWindow`, `NSWindowController`
- `NSDocument`, document architecture
- `NSToolbar`
- `NSMenu`, responder chain, menu validation
- `NSSplitViewController`
- `NSTableView`, `NSOutlineView`, `NSCollectionView`
- `NSTextView`
- `NSPopover`, `NSPanel`
- `NSStatusItem` / menu bar extras
- Advanced event tracking and custom drawing

### 1.2 Split view and sidebar pattern

```swift
import AppKit

final class RootSplitViewController: NSSplitViewController {
    override func viewDidLoad() {
        super.viewDidLoad()

        let sidebar = NSSplitViewItem(sidebarWithViewController: SidebarViewController())
        sidebar.minimumThickness = 220
        sidebar.maximumThickness = 320

        let content = NSSplitViewItem(viewController: ContentViewController())
        content.minimumThickness = 420

        let inspector = NSSplitViewItem(inspectorWithViewController: InspectorViewController())
        inspector.minimumThickness = 260
        inspector.maximumThickness = 380
        inspector.isCollapsed = true

        addSplitViewItem(sidebar)
        addSplitViewItem(content)
        addSplitViewItem(inspector)

        if #available(macOS 26.0, *) {
            sidebar.automaticallyAdjustsSafeAreaInsets = true
            inspector.automaticallyAdjustsSafeAreaInsets = true
        }
    }
}
```

### 1.3 Avoid legacy material conflicts

When adopting the current design language:

- Remove unnecessary custom `NSVisualEffectView` backgrounds in sidebars if the standard split/sidebar controller now provides the correct material.
- Remove custom toolbar backgrounds unless needed.
- Avoid drawing opaque bars behind toolbars if the system provides the scroll edge effect.
- Use `NSBackgroundExtensionView` for extending media/canvas backgrounds outside safe areas where appropriate.

### 1.4 Responder chain and validation

Rules:

- Use the responder chain for document/window commands.
- Validate menu and toolbar items based on selection and state.
- Keep toolbar, menu, and context-menu command implementations unified.
- Use undo managers at the document or window level.


## 2. Mac Catalyst guidance

Mac Catalyst can bring an iPad app to macOS, but a good Mac Catalyst app still needs Mac behavior.

Rules:

- Add a real macOS menu bar command structure.
- Review toolbar and sidebar behavior for Mac density and pointer use.
- Add keyboard shortcuts.
- Support resizable windows and multiwindow if appropriate.
- Replace touch-only gestures with pointer and keyboard alternatives.
- Use Mac idioms for settings, file import/export, drag and drop, and context menus.
- Avoid shipping a stretched iPad layout without Mac-specific refinement.


### 2.4 AppKit safe-area helper

Use code like this as a conceptual pattern. Verify exact API availability and behavior against the target SDK.

```swift
import AppKit

extension NSRect {
    func inset(by insets: NSEdgeInsets) -> NSRect {
        NSRect(
            x: origin.x + insets.left,
            y: origin.y + insets.bottom,
            width: width - insets.left - insets.right,
            height: height - insets.top - insets.bottom
        )
    }
}

func updateFullScreenLayout(for window: NSWindow) {
    guard let screen = window.screen else { return }

    if #available(macOS 12.0, *) {
        let safeInsets = screen.safeAreaInsets
        let safeFrame = screen.frame.inset(by: safeInsets)
        let topLeftVisibleArea = screen.auxiliaryTopLeftArea
        let topRightVisibleArea = screen.auxiliaryTopRightArea

        // Place meaningful controls inside safeFrame.
        // Use topLeftVisibleArea/topRightVisibleArea only for optional full-screen chrome.
        // Never place required controls behind the camera housing.
        _ = (safeFrame, topLeftVisibleArea, topRightVisibleArea)
    }
}
```

### 2.6 AppKit toolbar pattern

```swift
import AppKit

final class MainWindowController: NSWindowController, NSToolbarDelegate {
    private let toolbarID = NSToolbar.Identifier("MainToolbar")

    override func windowDidLoad() {
        super.windowDidLoad()

        let toolbar = NSToolbar(identifier: toolbarID)
        toolbar.delegate = self
        toolbar.allowsUserCustomization = true
        toolbar.displayMode = .default
        window?.toolbar = toolbar
    }

    func toolbarAllowedItemIdentifiers(_ toolbar: NSToolbar) -> [NSToolbarItem.Identifier] {
        [.toggleSidebar, .flexibleSpace, .search, .addItem, .share]
    }

    func toolbarDefaultItemIdentifiers(_ toolbar: NSToolbar) -> [NSToolbarItem.Identifier] {
        [.toggleSidebar, .flexibleSpace, .search, .addItem]
    }
}

extension NSToolbarItem.Identifier {
    static let search = NSToolbarItem.Identifier("Search")
    static let addItem = NSToolbarItem.Identifier("AddItem")
    static let share = NSToolbarItem.Identifier("Share")
}
```

### 2.8 AppKit menu validation pattern

```swift
import AppKit

final class DocumentViewController: NSViewController, NSMenuItemValidation {
    @IBAction func exportSelection(_ sender: Any?) {
        // Export currently selected object.
    }

    func validateMenuItem(_ menuItem: NSMenuItem) -> Bool {
        switch menuItem.action {
        case #selector(exportSelection(_:)):
            return hasExportableSelection
        default:
            return true
        }
    }

    private var hasExportableSelection: Bool {
        // Return true only when the current selection can be exported.
        true
    }
}
```

### 2.5 Info.plist compatibility key

`NSPrefersDisplaySafeAreaCompatibilityMode` affects whether the system avoids the camera housing area for an app. Treat this as an advanced full-screen decision.

Rules:

- Leave default compatibility behavior alone unless the app has a strong reason to draw into the full display area.
- Do not set compatibility behavior casually to gain a few pixels.
- If disabling compatibility, prove the app handles the camera housing, menu bar, safe areas, and full-screen transitions correctly.
- Use this only with real-device testing.

## Related topics

- [swiftui-patterns.md](swiftui-patterns.md) — SwiftUI-first shells with AppKit islands
- [layout-and-windowing.md](layout-and-windowing.md) — safe areas and split views
- [toolbars-and-menus.md](toolbars-and-menus.md) — menu validation and toolbar grouping
