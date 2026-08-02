# Agent runs

A log of each working session with the AI agent. One file per run.

The point isn't to document every keystroke — it's to leave an honest record of
what got delegated, what came back, and where I stepped in. If you want to know
how much of this site I actually decided, this is the folder that answers it.

## The runs

| Date | Run | What it was for |
| ---- | --- | --------------- |
| 2026-08-02 | [Infrastructure setup](./2026-08-02-infrastructure-setup.md) | Taking the repo from an empty README to a deployable site: build tooling, design tokens, content schema, CMS, CI/CD. |

## How to read these

Each entry records:

- **The ask** — what I actually pointed the agent at, in my words.
- **What it produced** — the concrete output, with commits.
- **What I decided** — the calls that stayed mine. This is the section that
  matters most; it's the difference between directing a tool and being handed
  something by one.
- **Where it needed correcting** — mistakes, wrong turns, things it got wrong
  and how. Left in deliberately. A log with no friction in it is marketing.
- **What it didn't do** — scope it declined, deferred, or couldn't reach.

## Why keep this at all

Two reasons.

The obvious one is transparency: this repo is public and linked from my
portfolio, and you deserve to know what you're looking at.

The less obvious one is that it's useful to *me*. Reading back over a run shows
where my instructions were vague — the agent's mistakes are usually a faithful
execution of something I under-specified. The `token-system` skill exists
because of things that went sideways before I wrote it down properly.

## Adding a run

Copy [`_template.md`](./_template.md), fill it in, add a row to the table above.

Write it after the session, not during. And keep the corrections section
honest — the failures are the informative part.
