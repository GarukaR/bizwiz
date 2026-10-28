"""Stage 0b: lists, dicts and comprehensions.

Each chunk is a dict like:
    {"id": "c1", "doc": "fleet-policy.md", "text": "...", "score": 0.82}

Fill in each TODO so the tests in test_0b_data.py go green.
"""


def chunk_ids(chunks):
    """The id of every chunk, in the same order. Example: ["c1", "c2", "c3"]."""
    # TODO 1: one list comprehension
    return []


def from_doc(chunks, doc):
    """Only the chunks that come from the document named `doc`, in the same order."""
    # TODO 2: one list comprehension with an `if`
    return []


def top_k(chunks, k):
    """The `k` chunks with the highest scores, best first."""
    # TODO 3: sort by score (highest first), then keep the first k
    return []


def group_by_doc(chunks):
    """A dict from each document name to the ids of its chunks, in order.

    Example: {"fleet-policy.md": ["c1", "c3"], "rates-2026.md": ["c2"]}
    """
    groups = {}
    # TODO 4: loop over the chunks. The first time you see a doc, give it an empty list.
    #         Then append the chunk's id to that doc's list.
    return groups


def average_score(chunks):
    """The mean score of the chunks. An empty list averages to 0.0."""
    # TODO 5: handle the empty list first.
    #         Then add up the scores and divide by how many chunks there are.
    return -1.0
