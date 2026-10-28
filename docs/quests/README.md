# 🎮 Quest Mode

You write the RAG core. Each quest is one module, split into **30-minute stages**. A stage is done when its
tests are green and committed, so you can stop after any stage without leaving anything half-broken.

## Start here

From the `quests` folder:

```
uv run quest              # run the current stage's tests and show the scoreboard
uv run quest hint 1       # log a hint you used (1, 2 or 3)
uv run quest award 10     # log XP (correct predictions, interview card)
```

Each stage lives in its own folder, e.g. `quests/q0_warmup/stage_a/`, with a `BRIEF.md` (start here),
`predict.py` (level 1), the file with the `# TODO` gaps, its tests, and `HINTS.md` (hints 1 and 2).
When every test in the stage is green, `uv run quest` clears it, adds the XP and moves you to the next
stage. The streak counts stages in a row cleared without any hints.

## Levels inside a stage

| Level | What you do |
|---|---|
| **1 · Predict** | Read a small test and guess whether it passes or fails, and why. Takes about 2 minutes. |
| **2 · Fill the gaps** | Fill in the 5–15 lines marked `# TODO` until the tests go green. |
| **3 · Solo** | A new failing test (an edge case). You write the fix with no skeleton. |

Early quests are mostly level 2. Later quests shift to level 3.

## Hint ladder

Hints are always available and there's no shame in using them. They cost a little XP, which only shows
your progress over time.

- 🟢 **Hint 1** (−5 XP): the concept
- 🟡 **Hint 2** (−10 XP): pseudo-code
- 🔴 **Hint 3** (−20 XP): the actual line

## Errors are part of it

When you hit an error, paste it. Claude walks you through it: **which line, what Python expected, what to
check**, and doesn't hand you the fix. Reading error messages is the fastest way back into coding.

## XP

| Event | XP |
|---|---|
| Level 1 guess correct | +10 |
| Level 2 stage green | +50 |
| Level 3 stage green | +100 |
| Boss fight: the eval score goes up after your quest | +50 per extra question passed |
| Interview card answered | +30 |

`uv run quest` shows the scoreboard. Progress is saved in `quests/progress.json`, so a fresh session picks
up where you stopped.

## Interview card

Each quest ends with three questions an interviewer might ask about that module. Answer in your own words.
The answers go into `docs/interview-notes.md`, which becomes your interview prep sheet.

## Quest map (Phase 1)

| # | Quest | Stages | What you'll see after |
|---|---|---|---|
| 0 | **Warm-up**: 0a reading Python · 0b lists, dicts, comprehensions · 0c dataclasses, pytest, reading errors | 3 | Your first green tests |
| 1 | **The Chunker**: split documents by headings | 3 | The app shows a document's chunks |
| 2 | **Keyword Hunter**: Postgres full-text search | 2 | Questions with exact names start working |
| 3 | **Vector Seeker**: pgvector similarity search | 2 | Questions that rely on meaning start working |
| 4 | **🐉 Fusion Boss**: Reciprocal Rank Fusion | 3 | The eval score jumps |
| 5 | **The Answer Smith**: prompt + Claude citations | 3 | Answers with clickable sources |
| 6 | **Truth Guard**: is each quote really in its source? | 2 | Bad citations get blocked |
| 7 | **The Honest No**: say "couldn't find it" when the evidence is weak | 2 | Unanswerable-question tests pass |
| 8 | **Time Keeper**: the newest document wins | 2 | Freshness traps pass. v1 bar met. |

That's 22 stages, about 11 hours in total. At 2–3 sessions a week it fits the end-of-January target.
