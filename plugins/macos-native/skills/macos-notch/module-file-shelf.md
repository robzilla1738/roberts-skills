# File Shelf

> Read when: drag-to-open shelf and drop targets. Back to [SKILL.md](SKILL.md).

## The core insight

The file shelf turns the notch into a **drop target and staging tray** — files “slide out” of the hardware shell. Magic comes from drag proximity opening the shelf before the user hits a tiny closed target.

---

## Behavior

- Drag file toward notch.
- Notch opens into shelf (often `expanded(.shelf)` — see [foundations.md](foundations.md)).
- Drop files, URLs, text, or images.
- Allow quick share, AirDrop, copy, reveal in Finder, remove.

**Interaction:** Wider transparent drag detector than closed notch width — see [interactions-and-motion.md](interactions-and-motion.md) § Drop target.

---

## Design

- Use small file cards.
- Show file type icon, name, and size.
- Make the drop zone feel like a tray sliding out of the notch.

---

## OSS extensions (optional)

NotchIA adds patterns beyond a minimal shelf:

- Persistent shelf with thumbnails, selection, Quick Look, invalid-item cleanup.
- Copy-on-drag and auto-remove after drag-out.
- Built-in format conversion (images, PDF, audio, video) — **run conversions off the main thread**; write to Downloads with unique names.

boring.notch ships shelf + AirDrop (GPL — patterns only). NexNotch (Linux) validates “file shelf in a pill” as a cross-platform UX idea.

---

## Pitfalls

- Opening shelf on every hover — reserve for drag enter or explicit module tab.
- Blocking drops while animating open — queue drops or expand detector early.
- AirDrop/share without explaining privacy in preferences.

See also: [integration-shipping.md](integration-shipping.md), [visual-system.md](visual-system.md).
