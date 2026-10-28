"""Stage 0a: reading Python.

Fill in each TODO so the tests in test_0a_reading.py go green. Each placeholder `return` is
deliberately wrong. Replace it.
"""


def greet(name):
    """Return a greeting like "G'day, Mia!"."""
    # TODO 1: return an f-string that puts `name` between "G'day, " and "!"
    return ""


def word_count(text):
    """How many words are in `text`? Words are separated by spaces."""
    # TODO 2: split the text into words, then count them
    return 0


def size_label(word_total):
    """Label a document by its length.

    Under 100 words is "short", 100 to 500 is "medium", more than 500 is "long".
    """
    # TODO 3: use if / elif / else to return the right label
    return ""


def total_kilometres(trips):
    """Add up the distance of every trip. `trips` is a list of numbers, e.g. [120, 85, 400]."""
    total = 0
    # TODO 4: write a for loop that adds each trip's distance to `total`
    return total


def count_mentions(words, target):
    """How many times does `target` appear in the list `words`? Ignore upper and lower case."""
    count = 0
    # TODO 5: loop over the words; when one matches `target` (ignoring case), add 1 to `count`
    return count
