"""Stage 0c: dataclasses, Protocol, and reading errors.

Fill in the TODOs so the tests in test_0c_shapes.py go green.
"""

from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@dataclass
class Passage:
    id: str
    doc: str
    text: str
    score: float = 0.0


# TODO 1: write a dataclass called Citation with two fields, both strings:
#         passage_id (which passage the answer used) and quote (the exact words it quoted).


@runtime_checkable
class Searcher(Protocol):
    """Anything with this search method counts as a Searcher. No inheriting needed."""

    def search(self, question: str, k: int) -> list[Passage]: ...


class KeywordSearcher:
    """Finds passages that share at least one word with the question."""

    def __init__(self, passages: list[Passage]):
        self.passages = passages

    def search(self, question: str, k: int) -> list[Passage]:
        # TODO 2: keep the passages whose text contains at least one word of the question
        #         (ignore upper and lower case), in their original order, then return the first k.
        return []


def total_score(passages: list[Passage]) -> float:
    """Add up the scores of the passages."""
    return sum(p["score"] for p in passages)
