# Camera Mirror

> Read when: quick camera preview with privacy indicators. Back to [SKILL.md](SKILL.md).

## The core insight

Camera mirror is a **utility module**: check hair/lighting before a call, not a photo studio. Small preview, obvious recording state, fast exit.

---

## Layout and behavior

Good as a utility module:

- Quick mirror before calls.
- Small preview only.
- Explicit camera permission request (just-in-time).
- Clear privacy indicator and exit.

**OSS — MacCam-NotchIsland (MIT):**

- Panel deploys from notch with concave curves matching hardware language.
- Live preview via AVFoundation; one-click capture with flash feedback.
- Optional full-screen frosted glass backdrop when open.
- Menu bar only (no dock icon); ESC or click-outside to dismiss.
- Custom save location (default Desktop).

boring.notch also lists mirror on its roadmap/shipped features (GPL — patterns only).

---

## Privacy

- Camera permission only when user opens the module.
- Show recording indicator while preview is active.
- Stop capture session on close — do not leave camera warm in background.
- Document behavior in preferences if preview can appear during screen sharing.

---

## Pitfalls

- Full-resolution preview in the closed notch — wastes GPU and feels creepy.
- Opening camera on hover without explicit user action.
- Missing indicator when macOS screen recording is active.

See also: [integration-shipping.md](integration-shipping.md) §14, [foundations.md](foundations.md).
