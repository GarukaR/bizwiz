# Stage 0c hints

Log each hint you read: `uv run quest hint 1` (−5 XP) or `uv run quest hint 2` (−10 XP).
For Hint 3, the actual line (−20 XP), ask Claude.

## TODO 1 · Citation

- 🟢 **Hint 1:** Copy the shape of `Passage` just above it: the `@dataclass` line, a `class` line, then
  one `name: type` line per field.
- 🟡 **Hint 2:**
  ```
  @dataclass
  class Citation:
      <first field>: <type>
      <second field>: <type>
  ```

## TODO 2 · KeywordSearcher.search

- 🟢 **Hint 1:** Dataclass fields are read with a dot: `passage.text`, not `passage["text"]`. To check
  "any word matches", lower-case both sides, split the question into words, and use `any(...)` or an
  inner loop. `word in some_text` is True when the word appears anywhere in the text.
- 🟡 **Hint 2:**
  ```
  words = the question, lowered, split into words
  matches = [p for p in self.passages if any(<word is in p's lowered text> for word in words)]
  return the first k matches
  ```
  Careful: the question "How often are trucks serviced?" ends with a `?`. Does `"serviced?"` appear in
  the passage text? Does it need to, given that `"trucks"` already matches?

## TODO 3 · total_score (the broken function)

- 🟢 **Hint 1:** The last line of the traceback names the error type. `TypeError: ... is not
  subscriptable` means "you used `[...]` on something that doesn't support it". What kind of thing is
  `p` here: a dict like in 0b, or something else?
- 🟡 **Hint 2:** Change how the score is read from each passage, using the same style as TODO 2's
  Hint 1.

## TODO 4 · your own test

- 🟢 **Hint 1:** A test is a function whose name starts with `test_`. It sets something up, calls the
  code, and uses `assert` to check the result. The tests above it are good examples.
- 🟡 **Hint 2:**
  ```
  found = <a KeywordSearcher over PASSAGES>.search(<a question with no matching words>, k=5)
  assert found == <an empty list>
  ```
