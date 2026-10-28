"""The four seams. The pipeline depends only on these, never on a concrete class.

A seam is a `typing.Protocol`: it lists the methods something must have. Any class with those
methods fits, so tests can swap in a fake and production can swap in Postgres or Claude.
"""

from collections.abc import Sequence
from datetime import datetime
from typing import Protocol

from bizwiz.domain import Answer, Chunk, Document, Passage


class Source(Protocol):
    """Where documents come from (a local folder now, Google Drive later)."""

    def list_changed(self, since: datetime | None) -> list[str]:
        """Refs of documents changed after `since` (all of them when `since` is None)."""
        ...

    def load(self, ref: str) -> Document: ...


class Embedder(Protocol):
    """Turns text into vectors."""

    model_id: str

    def embed(self, texts: Sequence[str]) -> list[list[float]]: ...


class Index(Protocol):
    """Stores chunks and finds the ones that match a question."""

    def add(self, chunks: Sequence[Chunk]) -> None: ...

    def search(self, query: str, k: int) -> list[Passage]: ...

    def get(self, passage_id: str) -> Passage | None: ...


class Answerer(Protocol):
    """Writes an answer from passages, citing them."""

    def answer(self, question: str, passages: Sequence[Passage]) -> Answer: ...
