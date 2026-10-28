# Level 1: predict what each numbered line prints BEFORE you run this file.
# Write your three guesses down, then run:  uv run python q0_warmup/stage_c/predict.py

from dataclasses import dataclass


@dataclass
class Truck:
    rego: str
    capacity_t: int = 20


a = Truck("IRB-001")
b = Truck("IRB-001")

# 1
print("1:", a.capacity_t)

# 2
print("2:", a == b)

# 3
b.capacity_t = 34
print("3:", a.capacity_t, b.capacity_t)
