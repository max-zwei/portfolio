# Behind the scenes

How this site actually gets built.

Most portfolios show you the finished thing. This folder shows the process
underneath it — including the fact that a lot of the code was written by an AI
agent working from my direction.

I'd rather say that plainly than have you wonder.

## Why this is here

I'm a designer, not an engineer. The design decisions on this site are mine —
the palette, the type, the layout, the framing of every case study, and every
judgement call about what the site is *for*. The implementation is largely
delegated to [Claude Code](https://claude.com/claude-code), an AI coding agent,
working from designs I make in Figma and instructions I write.

That's a real shift in how design work gets made, and pretending otherwise
would be both dishonest and boring. The interesting question isn't *"did you
use AI?"* — it's *"what does the work look like when you do?"*. So:

- **[`skills/`](./skills/)** — the reusable instruction sets I've written to
  make the agent work the way I want. These are the actual files, not
  descriptions of them.
- **[`agent-runs/`](./agent-runs/)** — a short log of each working session: what
  the agent was pointed at, what came out, and which calls stayed mine.

## What I'm claiming, and what I'm not

**Mine:** the design system, the visual decisions, the content, the
architecture choices, and the judgement about what's worth building. Also every
decision recorded in the run logs — the agent proposes, I decide.

**Not mine:** most of the lines of code in this repository. An agent wrote
them. I reviewed them, pushed back on them, and I'm accountable for what
shipped — but I didn't type them.

**Still true either way:** if something here is broken, that's on me.

## An honest note on the limits

The agent is good at scaffolding, at consistency, and at not getting bored
halfway through renaming ninety-four design tokens. It is not good at knowing
what this site should feel like. Every time I've let it decide something
aesthetic, the result has been competent and forgettable.

The division of labour that works: I decide *what* and *why*, it handles a lot
of *how*, and I stay close enough to catch it when the *how* quietly changes
the *what*.
