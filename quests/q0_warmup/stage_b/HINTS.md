# Stage 0b hints

Log each hint you read: `uv run quest hint 1` (−5 XP) or `uv run quest hint 2` (−10 XP).
For Hint 3, the actual line (−20 XP), ask Claude.

## TODO 1 · chunk_ids

- 🟢 **Hint 1:** You read a value out of a dict with square brackets and the key: `chunk["id"]`. A list
  comprehension does that for every chunk.
- 🟡 **Hint 2:** `return [<the id of chunk> for chunk in chunks]`

## TODO 2 · from_doc

- 🟢 **Hint 1:** A comprehension can end with `if <condition>`. Only items where the condition is true
  are kept.
- 🟡 **Hint 2:** `return [chunk for chunk in chunks if <chunk's doc equals doc>]`

## TODO 3 · top_k

- 🟢 **Hint 1:** `sorted(a_list, key=..., reverse=True)` returns a **new** sorted list (the original is
  untouched). `key` is a small function that picks what to sort by, e.g. `lambda c: c["score"]`.
  Slicing with `[:k]` keeps the first k items, and it doesn't mind if k is bigger than the list.
- 🟡 **Hint 2:** sort the chunks by score, highest first → slice off the first k → return it

## TODO 4 · group_by_doc

- 🟢 **Hint 1:** `key in a_dict` tells you whether the dict already has that key. Lists have `.append()`.
- 🟡 **Hint 2:**
  ```
  for each chunk:
      if its doc is not in groups yet: groups[doc] = []
      append the chunk's id to groups[doc]
  ```

## TODO 5 · average_score

- 🟢 **Hint 1:** Dividing by `len([])` crashes with `ZeroDivisionError`, so check for an empty list first
  (`if not chunks:`). `sum(...)` adds up numbers, and it accepts a comprehension inside it.
- 🟡 **Hint 2:**
  ```
  if there are no chunks: return 0.0
  return (sum of every chunk's score) / (how many chunks)
  ```
