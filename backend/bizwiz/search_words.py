import re

# Short common words that would match nearly every document.
STOP_WORDS = set(
    "the and for are was what who how when where which why does did our your this that with"
    " from have has about any can you there their they them its into than then will".split()
)


# replaced by Quest 2 (Keyword Hunter): Postgres full-text search does this properly.
def search_words(question: str) -> list[str]:
    """The words worth searching for: 3+ letters, not a stop word, no repeats."""
    words = re.findall(r"[a-z0-9]+", question.lower())
    return list(dict.fromkeys(w for w in words if len(w) >= 3 and w not in STOP_WORDS))
