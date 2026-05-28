# Accessibility

> Read when: VoiceOver, keyboard access, contrast, transparency settings, or localization. Back to [SKILL.md](SKILL.md).

## 1. Accessibility

### 1.1 Baseline requirements

Every macOS design should support:

- VoiceOver
- Keyboard-only navigation
- Full Keyboard Access
- Voice Control-friendly labels
- Switch Control compatibility where practical
- Sufficient contrast
- Reduce Motion
- Reduce Transparency
- Increase Contrast
- Larger text / dynamic text where supported
- Localization and text expansion

### 1.2 Accessibility structure

Rules:

- Group related elements into meaningful containers.
- Avoid exposing every decorative element to VoiceOver.
- Combine icon + label + value when they represent one control.
- Provide headings/landmarks for major regions.
- Give custom controls correct role, label, value, hint, and actions.
- Ensure table/list rows expose useful summaries.
- Make selection and focus states programmatically available.

SwiftUI examples:

```swift
HStack {
    Image(systemName: "externaldrive.connected.to.line.below")
    VStack(alignment: .leading) {
        Text("Backup Drive")
        Text("Last backup 12 minutes ago")
            .foregroundStyle(.secondary)
    }
}
.accessibilityElement(children: .combine)
.accessibilityLabel("Backup Drive, last backup 12 minutes ago")
```

```swift
Button("Delete Project", role: .destructive) {
    confirmDelete = true
}
.accessibilityHint("Shows a confirmation before permanently deleting the project")
```

### 1.3 Keyboard accessibility

Rules:

- Every critical action must be reachable by keyboard.
- Use standard shortcuts.
- Preserve focus rings.
- Set initial focus in dialogs and sheets.
- Provide Escape to cancel when appropriate.
- Provide Return for the default action when safe.
- Avoid trapping focus.
- Support arrow-key navigation in lists, tables, grids, and custom canvases.

### 1.4 VoiceOver

Rules:

- Test with VoiceOver, not only Accessibility Inspector.
- Ensure navigation order matches visual/logical order.
- Avoid unlabeled icon buttons.
- Avoid redundant labels like “button button.”
- Provide values for sliders, progress, ratings, and stateful controls.
- Provide custom accessibility actions for gestures, hover actions, drag actions, or swipe-only actions.

### 1.5 Contrast and transparency

Rules:

- Text over glass/material must remain readable over varied content.
- Use system colors so contrast adapts.
- Honor Increase Contrast and Reduce Transparency.
- Provide solid alternatives for custom translucent UI.
- Do not encode meaning with color alone.

### 1.6 Hover-only UI

Hover can reduce clutter, but it can also hide functionality.

Rules:

- Never make hover the only access path to an essential command.
- Pair hover controls with menu, toolbar, keyboard, or inspector access.
- Ensure VoiceOver users can trigger the same actions.
- Ensure touch/trackpad/keyboard workflows are not disadvantaged.


## 2. Localization and internationalization

Rules:

- Allow text expansion.
- Avoid fixed-width labels.
- Use localized strings for menus, buttons, alerts, tooltips, and accessibility labels.
- Do not compose sentences from fragments unless localization handles grammar.
- Support right-to-left layout where relevant.
- Format dates, times, numbers, currencies, units, and lists using locale-aware APIs.
- Avoid text embedded in images or icons.
## Related topics

- [foundations.md](foundations.md) — accessibility as a core design principle
- [swiftui-patterns.md](swiftui-patterns.md) — accessible custom row pattern
- [critique-checklists.md](critique-checklists.md) — accessibility audit checklist
