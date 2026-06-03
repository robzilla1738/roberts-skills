# Calendar Glance

> Read when: compact next-event and join affordances. Back to [SKILL.md](SKILL.md).

## The core insight

Calendar belongs in the notch as a **glance**, not a replacement for Calendar.app. One next event, time-to-start, and a join action beat a month grid.

---

## Layout

Best as a small glanceable dashboard:

- Next event.
- Time until event.
- Join button (video link when EventKit provides it).
- Today’s remaining events (compact list, not a full agenda).

**Reminders:** boring.notch and NotchIA integrate macOS Reminders alongside events — show next due item as a row, not a full reminders app.

---

## Data and permissions

- Request Calendar (and Reminders if enabled) access **when the user turns on the module**.
- Refresh on a modest timer or `EKEventStoreChanged` — avoid hammering EventKit.

---

## OSS examples

- **boring.notch** — calendar + reminders integration (GPL).
- **NotchIA** — calendar tab with events + reminders.
- **NotchMac** — expanded date/week progress/time chip (lighter than full EventKit dashboard).

---

## Pitfalls

- Building month/week views inside the notch.
- Join buttons without checking conference URL availability.
- Showing stale events after timezone or sleep — refresh on wake and screen unlock.

Do not build a full calendar app inside the notch.

See also: [integration-shipping.md](integration-shipping.md) §14, [visual-system.md](visual-system.md).
