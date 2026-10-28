# Stage 0b: Lists, dicts and comprehensions

**Clear reward:** 50 XP · about 30 minutes · lists, dicts, list comprehensions, sorting

When BizWiz answers a question, it first finds **chunks**: small pieces of documents, each with a score
saying how well it matches the question. In this stage each chunk is a plain dict:

```python
{"id": "c1", "doc": "fleet-policy.md", "text": "Trucks are serviced every 20,000 km.", "score": 0.82}
```

You'll write the small list and dict operations BizWiz does with chunks all the time: pull out the ids,
filter by document, keep the best few, group them and average them.

## Level 1 · Predict (about 5 minutes, +10 XP for each correct guess)

Read `predict.py` and write down what each numbered line prints. Then check:

```
uv run python q0_warmup/stage_b/predict.py
```

## Level 2 · Fill the gaps (about 25 minutes)

Fill in the five TODOs in `data.py`. The tests are in `test_0b_data.py`. Run `uv run quest` until it's
green.

**New idea: the list comprehension.** It's a one-line way to build a list from another list:

```python
[chunk["id"] for chunk in chunks]                         # every id
[chunk for chunk in chunks if chunk["score"] > 0.5]      # only the good ones
```

Read it as "give me ___ for each chunk in chunks (if ___)".

## Stuck?

`HINTS.md` has Hints 1 and 2. Log them with `uv run quest hint 1|2`. Ask Claude for Hint 3, or paste any
error.
