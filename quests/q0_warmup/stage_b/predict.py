# Level 1: predict what each numbered line prints BEFORE you run this file.
# Write your three guesses down, then run:  uv run python q0_warmup/stage_b/predict.py

depots = ["Melbourne", "Albury", "Sydney", "Brisbane"]

# 1
print("1:", depots[1], depots[-1])

# 2
chunk = {"id": "c7", "score": 0.4}
print("2:", chunk.get("doc", "unknown"))

# 3
print("3:", [len(d) for d in depots if d.startswith("A") or d.startswith("B")])
