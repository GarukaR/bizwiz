# Stage 0a: Reading Python

**Clear reward:** 50 XP · about 30 minutes · variables, functions, `if`, `for`

Ironbark Line Freight is the fictional trucking company in BizWiz's demo documents. This stage gives you
five small helper functions about it to finish.

## Level 1 · Predict (about 5 minutes, +10 XP for each correct guess)

Open `predict.py` and read it. **Before running it**, write down what you think each of the three
numbered lines prints. Then run it from the `quests` folder:

```
uv run python q0_warmup/stage_a/predict.py
```

Tell Claude how many you got right, or log them yourself with `uv run quest award 10` for each one.

## Level 2 · Fill the gaps (about 25 minutes)

Open `reading.py`. Each function has a `# TODO` comment and a placeholder `return` that's deliberately
wrong. Replace the placeholder with real code. The tests in `test_0a_reading.py` say exactly what each
function must do. Read them, they're short.

Run the tests and see the scoreboard (from the `quests` folder):

```
uv run quest
```

Red tests are normal at the start. Work through them one function at a time. When they're all green the
stage clears and you get the XP.

## Stuck?

`HINTS.md` has Hint 1 (the concept) and Hint 2 (pseudo-code) for each TODO. Log what you use with
`uv run quest hint 1` or `uv run quest hint 2`. For Hint 3 (the actual line), ask Claude. If you get an
error, paste it to Claude.
