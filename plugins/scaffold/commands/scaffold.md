---
description: Greenfield or extend a Next.js app (Tailwind v4, tRPC, TanStack Query, optional Clerk, Neon/Drizzle, Vercel)
---

Scaffold or extend a project: **$ARGUMENTS**

Load and follow the **scaffold** skill at `${CLAUDE_PLUGIN_ROOT}/skills/scaffold/SKILL.md`:
start with product intake to pick the right profile, then build boring infrastructure first
(typed env, errors, tests, install, lint, build, database, API route, optional auth) before
any product features. Install every intake-selected add-on (AI SDK, Resend, Stripe, Sentry,
PostHog) in the integrations phase — never leave them README-only. Follow the phase bundle
and the verification checklist; record the scaffold profile, installed add-ons, and
production-habits checklist in the README.

If $ARGUMENTS is empty, run product intake to learn what's being built.
