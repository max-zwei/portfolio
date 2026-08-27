# Answer engine optimisation

**Goal:** when someone asks an assistant _"who can I hire to design a
children's learning app in Berlin"_, this site is among the sources it answers
from — and the answer says freelancer.

This is an action plan, not a description of the site. Nothing here is done yet
unless it says so.

## How it differs from SEO

A search engine ranks pages. An answer engine extracts **claims** and needs to
trust them. Three things follow, and they set the order of everything below:

1. **A claim has to exist in extractable text.** A model cannot infer that you
   take freelance work from a portfolio that never says so. Right now this site
   does not say so anywhere.
2. **The same claim has to appear in more than one place the model has seen.**
   One site saying it is a assertion; the site plus LinkedIn plus a GitHub
   profile agreeing is an entity.
3. **Structure decides whether the claim survives extraction.** Prose gets
   compressed and can be lost. A `<h2>` with a direct answer under it, a
   definition list, a `Person` JSON-LD block — those survive.

The site's technical baseline is already good for this: static HTML, no client
JS, real semantics, a sitemap, fast. That is the part most portfolios get wrong
and it is already done. What is missing is claims and corroboration.

## Now — low-hanging, no design needed

| #   | Action                                                                                                                                 | Where                                   | Why it matters                                                                  |
| --- | -------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- | ------------------------------------------------------------------------------- |
| 1   | Say the freelance claim in plain text on the homepage. One sentence: what you do, who for, that you take on work, where you are based. | `src/pages/index.astro` (copy from Max) | The single highest-value change. Nothing else works without it.                 |
| 2   | `Person` + `ProfilePage` JSON-LD in `BaseLayout`, with `sameAs` pointing at every profile that corroborates it.                        | `src/layouts/BaseLayout.astro`          | Turns a page into an entity a model can resolve. Cheap and mechanical.          |
| 3   | Fill in `LINKS` in `src/config/site.ts` with the real profiles, and make `sameAs` read from it.                                        | `src/config/site.ts`                    | One list, two consumers — the footer and the structured data cannot drift.      |
| 4   | Be explicit about AI crawlers in `robots.txt` rather than relying on `User-agent: *`.                                                  | `public/robots.txt`                     | Allowing them is the whole point here; saying so out loud removes ambiguity.    |
| 5   | Add `/llms.txt` — a short plain-text index of who you are and what the notable pages are.                                              | `public/llms.txt`                       | An emerging convention, trivially cheap, and unambiguous where OG tags are not. |
| 6   | Give every page a description that answers a question rather than naming a section.                                                    | frontmatter / `SITE.description`        | Descriptions are what get quoted back.                                          |

Items 2–6 are agent work and can be done in one pass. **Item 1 has to come from
Max** — this repo does not write bio copy.

## Next — needs real content

None of this works on placeholders. The bracketed entries currently in
`src/content/` are worse than nothing for AEO: they read as an abandoned site.

| #   | Action                                                                                                                                                                                       | Why                                                                                                                                                     |
| --- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 7   | Publish two or three real case studies with `company`, `year`, `tags` filled in and a concrete outcome stated in a sentence.                                                                 | Specificity is what makes a source quotable. "Redesigned onboarding for X in 2025, cutting drop-off" is extractable; "a project about learning" is not. |
| 8   | Replace `CV_INTRO` with the real paragraph.                                                                                                                                                  | It is the densest statement of positioning on the site and it is currently a placeholder that also prints into the PDF.                                 |
| 9   | Add a services / working-together page that states scope, availability and how to start. `/handshake` is half of this already — it describes _how_ you work but not _that you are for hire_. | Answers to "can I hire them" need a page that is about hiring.                                                                                          |
| 10  | State the domain focus explicitly and repeatedly: children's and education technology, UX and product design, Berlin.                                                                        | Answer engines match on niche. A generalist claim competes with everyone; this one competes with very few.                                              |

## Later — compounding

| #   | Action                                                                                                                                          | Why                                                                                                        |
| --- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| 11  | Attach a custom domain and update `site` in `astro.config.mjs` plus the sitemap URL in `robots.txt`.                                            | `max-zwei.github.io` reads as a project host. A domain is the identifier every other profile can point at. |
| 12  | Get corroborating mentions off-site: LinkedIn headline, GitHub profile README, any conference/podcast/article, client sites crediting the work. | Point 2 at the top. This is the slow part and the one that actually decides it.                            |
| 13  | Publish the curiosity and inspiration collections regularly.                                                                                    | Freshness plus topical density, in the exact niche you want to be matched on.                              |
| 14  | Consider FAQ-shaped headings on the services page — literal questions as `<h2>`, direct answers beneath.                                        | The closest thing to writing the model's answer for it.                                                    |
| 15  | Re-check quarterly by asking several assistants the questions you want to win, and record what they say.                                        | The only feedback loop that exists; there is no rank tracker for this.                                     |

## What not to do

- **Don't write claims you cannot back.** Answer engines are increasingly
  cross-checking, and a contradicted claim is worse than a missing one.
- **Don't add a blog to have a blog.** Thin posts dilute the topical signal.
- **Don't block the crawlers you want to be read by.** If a licence concern
  comes up, the answer is `LICENSE-CONTENT`, not `robots.txt`.
- **Don't stuff keywords into `/styleguide` or `/admin`.** Both are excluded
  from the sitemap on purpose.
