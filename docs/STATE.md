# BizWiz state

_Last updated: 2026-10-28 (Quest 0 tooling session)_

## Where we are

Planning is done: decisions in `PLAN.md`, Phase 1 split into issues #1–#16.

**Slice 1 (#1) is built** on branch `slice-1-walking-skeleton` (PR open): ask a question in the web app,
get an answer with a citation chip, click it to see the source passage with the quote highlighted.
22 backend tests + 1 Playwright e2e test green. **Not merged yet: the real-API smoke test hasn't run**,
because BizWiz has no Anthropic API key yet. Garuka: put `ANTHROPIC_API_KEY` in `.env`, then run
`cd backend && uv run python scripts/smoke.py`. It must print `SMOKE OK` before merging.

**Quest 0 (#4) tooling is built** on branch `quest-0-warmup`, stacked on the slice 1 branch (PR open,
based on `slice-1-walking-skeleton`; GitHub retargets it to `main` when slice 1 merges).
`uv run quest` works and all three warm-up stages are ready to play. **Garuka plays 0a, 0b, 0c next**,
on the same branch, then answers the interview card in `stage_c/BRIEF.md`. The PR merges after that.

## Order of work (Phase 1 = v1, target end of January 2027)

Claude's plumbing slices and Garuka's quests run **in parallel**. Quest 0 doesn't depend on any slice.

| Order | Issue | Who | Status |
|---|---|---|---|
| 1 | #1 Slice 1: walking skeleton | Claude | built, PR open, needs smoke test |
| 1 (parallel) | #4 Quest 0: warm-up + scoreboard | Claude builds tooling, Garuka plays | tooling done; **Garuka plays 0a–0c next** |
| 2 | #2 Slice 2: deploy | Claude | |
| 3 | #3 Slice 3: Ironbark corpus + golden set + Eval page | Claude (Garuka hand-grades 10) | |
| 4 | #5 Quest 1: Chunker | Garuka | needs #1, #3 |
| 5 | #6 Quest 2: Keyword Hunter | Garuka | |
| 6 | #7 Quest 3: Vector Seeker | Claude plumbing + Garuka | |
| 7 | #8 Quest 4: Fusion Boss | Garuka | |
| 8 | #9 Quest 5: Answer Smith | Claude plumbing + Garuka | |
| 9 | #10 Quest 6: Truth Guard | Garuka | |
| 10 | #11 Quest 7: Honest No | Garuka | |
| 11 | #12 Quest 8: Time Keeper | Garuka | v1 bar should be met here |
| any time after #9 | #13 Cited tables | Claude | |
| after #9 | #14 Google Drive + True Theorem instance | Claude | True Theorem starts real use, and the 2-week clock starts |
| after #12 | #15 Model comparison + cost | Claude | |
| last | #16 Ship v1 | both | |

## Open items (not blocking)

- Garuka: delete the plain-text passwords file in the personal Drive and change those passwords (found
  2026-10-25).
- Check Voyage AI's data-use terms before indexing real True Theorem documents (#14).
- ABN Lookup check for "Ironbark Line Freight" (#3). A web search on 2026-10-25 found no operator by that
  name.
- The `BizWiz` folder in the truetheorem@gmail.com Drive doesn't exist yet. Garuka creates it and copies
  documents in before #14.

## Notes for the next session

- **Quest Mode layout.** `quests/` is its own small uv project (`quests/pyproject.toml`, only pytest).
  The scoreboard is `quests/quest_tool/` (its own tests: `cd quests && uv run pytest`). Stages are found
  by folder name, `quests/q<N>_<name>/stage_<x>/`, each with `BRIEF.md` (its first line is the title and
  `**Clear reward:** N XP` sets the XP), `predict.py`, a skeleton with `# TODO`s, `test_<unique>.py`
  (test and skeleton file names must be unique across all stages, since pytest imports them by bare
  name), and `HINTS.md` (hints 1 and 2 only; Claude gives Hint 3 on request).
- `uv run quest` clears a stage automatically the first time all its tests pass, adds its XP and
  updates `progress.json`. Claude logs predictions and the interview card with `uv run quest award N`
  (+10 per correct guess, +30 for the card). Streak = stages in a row cleared with no hints.
- Quest 1+ tests will need the backend code (`bizwiz.chunking` etc.). When writing them, add
  `bizwiz` as a path dependency in `quests/pyproject.toml` (`[tool.uv.sources]`, `../backend`).
- Reference solutions for Quest 0 were checked in a scratchpad and deliberately not committed.

- **Slice 1 layout.** Backend code is in `backend/bizwiz/` (flat, not `src/`): `domain.py` (types),
  `seams.py` (the four Protocols), `pipeline.py` (`index_source`, `ask`), `fakes.py`, `wiring.py`
  (the only place concrete classes are chosen), `api.py`. Naive placeholders are marked
  `# replaced by Quest N`: `chunking.py` (Q1), `search_words.py` + `PostgresIndex.search` (Q2-4),
  `SYSTEM_PROMPT` in `answerers/claude.py` (Q5).
- **Seam details settled in slice 1** (small additions to PLAN.md section 8): `Index` also has
  `get(passage_id)` for `GET /passages/{id}`; `Index.search` has no `filters` argument yet (add it with
  permissions); `Source.list_changed(since)` exists but ingest always passes `None` (full re-index).
- **Ports:** db 5442, API 8010, web 3010; the e2e run uses 8011/3011. Other projects on this machine
  hold 8000, 5000, 3100 and 55437.
- The API indexes `corpus/ironbark/` at start-up (idempotent: re-adding a document replaces its
  chunks). #14 moves indexing into its own job.
- The fake embedder is used for real until Quest 3; vectors are 8-dim hashes with
  `model_id = fake-embedder-v0`. The `embedding` column is `vector` with no fixed size for now.
- `ClaudeAnswerer` uses the beta Messages endpoint with `fallbacks="default"` (server-side refusal
  fallback) and effort `medium`. Anthropic SDK is 2.3.
- Integration tests use a separate `bizwiz_test` database (created by `db/init/`). If the db volume
  existed before that script, create it by hand.

- Local tools present: Docker 29, uv 0.11, Python 3.14 (uv can pin 3.12+), Node 24. No `psql`; use the
  Docker container.
- This folder sits inside the `Projects` umbrella git repo but is its **own** repo (remote
  `GarukaR/bizwiz`). Always run git from inside `BizWiz/`.
