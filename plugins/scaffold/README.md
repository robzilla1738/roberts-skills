# Scaffold

Product-driven greenfield Next.js: intake profiles (SaaS dashboard, internal tool, API-first),
typed env, Vitest, tRPC, TanStack Query, Neon/Drizzle, optional Clerk, Vercel.

**Author:** [Robert Courson](https://robertcourson.com) · Part of [Robert's Skills](https://github.com/robzilla1738/roberts-skills)

---

## Install

### Claude Code (plugin)

```text
/plugin marketplace add robzilla1738/roberts-skills
/plugin install scaffold@roberts-skills
```

Then use `/scaffold`.

### Cursor / Codex

```bash
cp -R plugins/scaffold/skills/scaffold ~/.agents/skills/   # Cursor + Codex (global)
cp -R plugins/scaffold/skills/scaffold ~/.cursor/skills/   # Cursor (global)
```

## Use it

```text
/scaffold a SaaS dashboard with auth and a Postgres database
```

See [`skills/scaffold/`](skills/scaffold/) for the hub and all reference spokes.
