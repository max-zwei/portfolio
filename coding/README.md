# Coding

Coding challenges and exercises, kept in the open.

I'm a designer who codes rather than an engineer, and this folder is the part of
that I'm not hiding. The solutions here are exercises — written to learn
something, not to be production code. Some of them are clumsy. That's the point
of keeping them.

## The challenges

_Nothing here yet._

<!-- Add a row per challenge:
| Challenge | Language | What it was for |
| --------- | -------- | --------------- |
| [two-sum](./two-sum/) | Python | Getting comfortable with hash maps |
-->

## How this is organised

One folder per challenge, named after it:

```
coding/
  <challenge-slug>/
    README.md       What the problem was, how I approached it, what I learned
    <solution files>
```

The `README.md` matters more than the code. A solution on its own says what I
typed; the write-up says what I understood, and that's the bit worth reading
back in six months.

Keep it short — a paragraph on the problem, a paragraph on the approach, and an
honest line on what tripped me up.

## Two things to know if you're editing this

**These files are exempt from Prettier.** `coding/` is in `.prettierignore`, so
solutions stay exactly as they were written. A challenge solution is a record of
what I did at the time, not repo code to be tidied up afterwards.

**TypeScript files here aren't type-checked.** `coding` is excluded in
`tsconfig.json`. The site's config is strict on purpose, and a quick exercise
shouldn't have to satisfy it — or fail `npm run verify` when it doesn't.

Neither of those is laziness. They keep the checks meaningful for the code that
actually ships, instead of training everyone to ignore a permanently red build.
