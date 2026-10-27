FOUR DECADE VOICES — POSTER EDITION v3.5
15 October 2026

START HERE
poster-edition/poster-voices.html — comparison viewer, final prompts, all 72 drafts and five reviews.
agents/ — four current standalone prompts, intentionally exaggerated for side-by-side poster text.

USE
Paste one complete agent prompt into each agent's instructions. Give all four the same data, audience and requested format. Default: 2–5-word headline plus 30–65-word body. These are prompting resources, not fine-tuned models or deployed agents.

TEST RECORD
poster-edition/rounds/01–05.json — actual drafts, revision instructions and qualitative reviews.
Rounds 1–3: original three briefs. Round 4: three fresh statistical edge cases. Round 5: all six briefs retested. 72 total drafts, 24 final outputs.
poster-edition/rounds/01–04-drafting-instructions.txt — reconstructed cumulative instruction record from the recorded revision deltas, not external model invocation logs.
poster-edition/rounds/05-*-prompt.txt — final production prompt snapshots.
poster-edition/review-log.txt — readable findings and revisions.
poster-edition/checks.json — headline/body word counts; not automated factual validation.
All numerical examples are FICTIONAL TEST DATA. One assistant authored and reviewed them. No independent model run, blind reviewer or recognition accuracy is claimed. Actual poster data and layout remain untested.

ARCHIVE
research-report.html — original research report, 40 annotated samples, 16 exemplars, original conservative guides and earlier review. Banner links to the current poster edition.
poster-edition/previous-prompts/ — archived v2.1 instructions.
research/ and evaluation/ — original research and original evaluation, unchanged.

INTERPRETATION
The new voices are deliberate creative selections: 1990s alternative-zine deadpan; 2000s glossy pop presenter; 2010s earnest mini-blogger; 2020s meme-literate group chat. They exaggerate selected Anglophone cultural strands rather than describe all youth. Distinctive markers overlap historically. 2020s provisional through 15 October 2026.

BUILD NOTE
build_poster_edition.py rebuilds the poster viewer from retained round records and current prompts. The earlier build_decade_report.py belongs to the original research edition and must not be rerun over current agents without restoring the v3.5 snapshots afterward.

COMBINED AGENT
agents/four-decade-poster-agent.txt — one standalone instruction set returning four decade versions of a requested title or paragraph.
poster-edition/four-decade-agent-quick-start.txt — usage and example requests.
