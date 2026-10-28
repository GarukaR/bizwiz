# Stage 0c: Dataclasses, Protocol, pytest and reading errors

**Clear reward:** 50 XP · about 30 minutes · `@dataclass`, `typing.Protocol`, writing a test, tracebacks

In 0b a chunk was a dict. Real BizWiz code uses **dataclasses**: a small class whose fields are written
out, so a typo like `passage.scroe` fails loudly instead of quietly giving nothing.

BizWiz is also built around four **seams** (`Source`, `Embedder`, `Index`, `Answerer`). Each one is a
`Protocol`: a description of the methods something must have, with no code inside. Any class that has
those methods fits, so a test can swap the real Postgres index for a tiny fake one. You'll see that here
with a `Searcher`.

## Level 1 · Predict (about 5 minutes, +10 XP for each correct guess)

```
uv run python q0_warmup/stage_c/predict.py
```

Read it first and write down your three guesses.

## Level 2 · Fill the gaps (about 25 minutes)

Open `shapes.py`. There are four jobs:

1. **TODO 1:** write the `Citation` dataclass.
2. **TODO 2:** finish `KeywordSearcher.search`.
3. **TODO 3: the broken function.** `total_score` has a real bug and no TODO marker. Run `uv run quest`,
   find the **traceback** for `test_total_score`, and read it from the bottom up: the last line says what
   went wrong, and the lines above it say where. Fix the bug from what the traceback tells you.
4. **TODO 4:** in `test_0c_shapes.py`, replace the `pytest.fail(...)` line with a real test of your
   own.

## Stuck?

`HINTS.md` has Hints 1 and 2. Log them with `uv run quest hint 1|2`. Ask Claude for Hint 3, or paste the
traceback and Claude will walk you through it.

## After this stage: interview card (+30 XP)

Answer these in your own words to Claude. They go into `docs/interview-notes.md`.

1. What's the difference between a dict and a dataclass, and when would you pick each?
2. What is a `Protocol`, and why does BizWiz use them for its four seams?
3. How do you read a Python traceback?
