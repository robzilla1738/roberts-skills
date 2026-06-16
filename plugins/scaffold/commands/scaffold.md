---
description: Greenfield or extend web (Next.js) or native Apple (iOS/macOS) apps with product intake and recommended integrations
---

Scaffold or extend a project: **$ARGUMENTS**

Load and follow the **scaffold** skill at `${CLAUDE_PLUGIN_ROOT}/skills/scaffold/SKILL.md`:
start with **platform intake** (web vs iOS vs macOS), then product intake to pick the right profile.
**Recommend** add-ons from the product description (RevenueCat, Sparkle, Stripe, Sentry, etc.) and
confirm before install. Build boring infrastructure first, then wire every confirmed integration —
never README-only. Follow the phase bundle for the platform family and the verification checklist;
record platform family, profile, installed add-ons, and production habits in the README.

If $ARGUMENTS is empty, run platform + product intake to learn what's being built.
