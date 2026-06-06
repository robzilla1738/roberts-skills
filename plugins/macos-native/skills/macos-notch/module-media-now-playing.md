# Media / Now Playing

> Read when: music controls, album art, and visualizer in the notch. Back to [SKILL.md](SKILL.md).

## The core insight

Media is the most common “proof” that a notch app feels native: the closed shell shows a living surface (art, visualizer, or play glyph), and the open state expands into full transport without becoming a full music app.

---

## Layout

### Closed

- Album art thumbnail.
- Tiny visualizer.
- Optional play/pause glyph.

### Open

- Album art.
- Track title and artist.
- Previous / play / next buttons.
- Progress bar.
- Volume or output route shortcut.

### Polish

- Use average album color for visualizer gradient or soft glow.
- Use `matchedGeometryEffect` for album art between closed and open.
- Avoid scrolling marquee unless text is truly clipped.

---

## Data sources

| Source | Notes |
|--------|-------|
| macOS Now Playing / MediaRemote | System-wide “what’s playing” — good default |
| Apple Music / Spotify SDKs | Deeper metadata and controls; more integration work |
| Browser tabs | NotchMac-style: Safari, Chrome, Firefox, Arc for web players |

**OSS:** boring.notch centers on music + visualizer; NotchIA adds Apple Music, Spotify, YouTube Music, customizable control slots, optional lyrics under artist, and “Sneak Peek” on track change ([module-peek-transient.md](module-peek-transient.md)).

---

## Full-screen behavior

NotchIA exposes a useful product knob:

- Hide notch in full screen always.
- Hide only when the media app is full screen.
- Never hide for media.

Pick one default and expose in preferences — see [integration-shipping.md](integration-shipping.md).

---

## Pitfalls

- Polling Now Playing every frame — use reasonable intervals or push updates.
- Large open layout for a single track — keep glanceable.
- Stealing focus when opening transport controls.
- Lyrics or long titles without truncation in closed state.

See also: [visual-system.md](visual-system.md), [interactions-and-motion.md](interactions-and-motion.md).
