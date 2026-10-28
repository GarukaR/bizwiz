# Level 1: predict what each numbered line prints BEFORE you run this file.
# Write your three guesses down, then run:  uv run python q0_warmup/stage_a/predict.py

# 1
trucks = 3
trucks = trucks + 2
print("1:", trucks)


# 2
def double(n):
    return n * 2


print("2:", double("ab"))

# 3
total = 0
for km in [10, 20, 30]:
    if km > 15:
        total = total + km
print("3:", total)
