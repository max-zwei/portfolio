# Infrastructure setup

**Date:** 2026-08-02
**Agent:** Claude Code
**Skills used:** token-system, figma-use
**Result:** [#11](https://github.com/max-zwei/portfolio/pull/11) — merged

## The ask

I pointed it at my open GitHub issues and said: take a look, start tackling
them to set up my general tech infrastructure, and write a README that helps
future agents understand the project quickly. I gave it a couple of paragraphs
of context about what the site is for — my work, myself, what I'm currently
working on, focus on UX and product design moving towards children's and
education tech, professional but not plain — and told it that all design
happens in Figma and gets handed over via MCP.

The repo at that point contained a README with one sentence in it.

## What it produced

Ten open issues, eight closed by this run.

- **Astro 7**, static output, strict TypeScript, sitemap. Clean type-check.
- **Design tokens** — two tiers (primitives → semantic aliases) as CSS custom
  properties, plus a W3C DTCG JSON export as the Figma exchange format.
- **Content schema** for case studies in zod, with the fields I'd specified
  (`title`, `status`, `tags`, `cover`, `year`, `hmw`) plus a handful it argued
  for, and a doc explaining each one.
- **Decap CMS** wired to that schema, with editorial workflow on so saving
  opens a PR rather than committing to `main`.
- **v0.1 homepage** — name, role, slogan, one accent gesture.
- **GitHub Actions** — deploy on `main`, type-check and build on every PR.
- **`CLAUDE.md`** — the rules any future agent session has to follow in here.
- **94 Figma variables** across 7 collections, written directly into my Figma
  file via MCP, named to match the CSS one-for-one.

Three commits, squashed into `main`.

## What I decided

- **No dark mode.** It had built light and dark token sets. I don't want two
  schemes to maintain for a portfolio, so I had it strip them back to one. It
  kept the two-tier structure so the decision stays reversible.
- **CMS editing stays local.** It laid out two routes for getting `/admin`
  login working on the live site and recommended a third — don't bother yet. I
  agreed. I have no case studies written; solving "publish from my phone"
  before "have something to publish" is backwards.
- **How much to build.** I told it explicitly to stay out of site information
  architecture and page content, because I haven't nailed that down. It stayed
  out.
- **The palette is provisional.** The colour values in the repo are its working
  guesses against names I'd given it (Yuzu, Rote Beete, Tomaten, Lieblingsort).
  They're placeholders until I tune them in Figma. What matters is that the
  token _names_ are fixed, so tuning values doesn't break anything downstream.

## Where it needed correcting

**It caught this one itself:** the Astro scaffold pulled in version 5, which
came with eight open XSS advisories plus vulnerable `esbuild` and `sharp`. It
noticed on the audit, upgraded to 7, and flagged it rather than shipping quietly
on a vulnerable base.

**Two script errors during the Figma write**, both self-recovered: wrong enum
casing for the iOS platform (`IOS` vs `iOS`), and a method that doesn't exist in
that context (`getValueForMode`). Neither touched the file — Figma script
execution is atomic, so a failed script writes nothing.

**My instructions were the actual problem twice.** I never told it there'd be
only one colour scheme, so it built two — a correct read of an under-specified
brief. Same with the `/admin` login: I asked to be walked through "setting it
up" before establishing whether I needed it. It asked the right clarifying
question, which is the only reason we didn't build something pointless.

## What it didn't do

- **Issues #8 and #9** — sub-repos for coding projects and AI skills. Separate
  repositories, outside what the session could reach. It flagged them rather
  than guessing at names. (#9 has since been folded into this folder instead.)
- **Enabling GitHub Pages** — an admin repo setting a workflow can't grant
  itself. It explained why and told me exactly which toggle to flip.
- **Any page beyond the homepage**, per my instruction.
- **Any content.** It wrote no case studies, no bio, no client names, no
  metrics. `CLAUDE.md` now forbids this outright for future sessions.

## Worth remembering

The clarifying question about `/admin` saved the most time in the whole
session — I'd asked for a solution before I'd checked I had the problem.

Under-specify a brief and you get a competent answer to a question you didn't
ask. Both times it built the wrong thing, it was because I hadn't said. The fix
isn't a better agent, it's writing the constraint down — which is what
`CLAUDE.md` is now for.
