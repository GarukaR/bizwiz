# Stage 0a hints

Log each hint you read: `uv run quest hint 1` (−5 XP) or `uv run quest hint 2` (−10 XP).
For Hint 3, the actual line (−20 XP), ask Claude.

## TODO 1 · greet

- 🟢 **Hint 1:** An f-string is a string with an `f` in front. Anything inside `{curly braces}` is replaced
  with that variable's value.
- 🟡 **Hint 2:** `return f"<start>{<variable>}<end>"`

## TODO 2 · word_count

- 🟢 **Hint 1:** Strings have a `.split()` method that turns `"a b c"` into the list `["a", "b", "c"]`.
  `len(...)` tells you how long a list is.
- 🟡 **Hint 2:** split the text → get the length of the result → return it

## TODO 3 · size_label

- 🟢 **Hint 1:** `if` checks the first condition, `elif` is only checked if the ones above were false,
  and `else` catches everything left. Look closely at the edges: is 100 "short" or "medium"?
- 🟡 **Hint 2:**
  ```
  if word_total is less than 100: return "short"
  elif word_total is at most 500: return "medium"
  else: return "long"
  ```

## TODO 4 · total_kilometres

- 🟢 **Hint 1:** `for x in some_list:` runs the indented lines once per item, with `x` set to that item.
  `total` already starts at 0 above the TODO.
- 🟡 **Hint 2:**
  ```
  for each trip in trips:
      total = total + trip
  ```

## TODO 5 · count_mentions

- 🟢 **Hint 1:** `"IronBark".lower()` gives `"ironbark"`. Compare two lowered strings with `==`.
- 🟡 **Hint 2:**
  ```
  for each word in words:
      if lowered word == lowered target:
          count = count + 1
  ```
