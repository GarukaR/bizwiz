# BizWiz state

_Last updated: 2026-10-25 (planning session)_

## Where we are

Planning is done: decisions in `PLAN.md`, Phase 1 split into issues #1–#16. **No code yet.**

## Order of work (Phase 1 = v1, target end of January 2027)

Claude's plumbing slices and Garuka's quests run **in parallel**. Quest 0 doesn't depend on any slice.

| Order | Issue | Who | Status |
|---|---|---|---|
| 1 | #1 Slice 1: walking skeleton | Claude | **next** |
| 1 (parallel) | #4 Quest 0: warm-up + scoreboard | Claude builds tooling, Garuka plays | next. Tooling first, then stage 0a. |
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

- Local tools present: Docker 29, uv 0.11, Python 3.14 (uv can pin 3.12+), Node 24. No `psql`; use the
  Docker container.
- This folder sits inside the `Projects` umbrella git repo but is its **own** repo (remote
  `GarukaR/bizwiz`). Always run git from inside `BizWiz/`.
