"""Stand-ins for the seams: fast, free and predictable.

Used by unit tests, by the end-to-end test (ANSWERER=fake), and, until Quest 3, as the embedder.
"""

import hashlib
import re
from collections.abc import Sequence

from bizwiz.chunking import WHOLE_DOCUMENT
from bizwiz.domain import Answer, Chunk, Citation, Passage
from bizwiz.search_words import search_words


class FakeEmbedder:
    """Turns text into a small vector made from its hash. Same text, same vector."""

    model_id = "fake-embedder-v0"

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        return [[b / 255 for b in hashlib.sha256(t.encode()).digest()[:8]] for t in texts]


class InMemoryIndex:
    """Keeps chunks in a dict and ranks them by how many question words they contain."""

    def __init__(self):
        self.chunks: dict[str, Chunk] = {}

    def add(self, chunks: Sequence[Chunk]) -> None:
        for doc_id in {c.document_id for c in chunks}:
            self.chunks = {i: c for i, c in self.chunks.items() if c.document_id != doc_id}
        self.chunks.update({c.id: c for c in chunks})

    def search(self, query: str, k: int) -> list[Passage]:
        words = search_words(query)
        scored = [(sum(w in c.text.lower() for w in words), c) for c in self.chunks.values()]
        scored = [(s, c) for s, c in scored if s > 0]
        scored.sort(key=lambda sc: (-sc[0], sc[1].id))
        return [_passage(c, s) for s, c in scored[:k]]

    def get(self, passage_id: str) -> Passage | None:
        chunk = self.chunks.get(passage_id)
        return _passage(chunk) if chunk else None


class FakeAnswerer:
    """Quotes the sentence of the top passage that shares the most words with the question."""

    def answer(self, question: str, passages: Sequence[Passage]) -> Answer:
        if not passages:
            return Answer("I couldn't find that in your documents.")
        top = passages[0]
        words = search_words(question)
        # Split at sentence ends and blank lines; a sentence wrapped over two lines stays whole.
        parts = [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n\s*\n", top.text)]
        sentences = [s for s in parts if s and not s.startswith("#")] or [top.text]
        sentence = max(sentences, key=lambda s: sum(w in s.lower() for w in words))
        return Answer(
            f"According to {top.doc_title}: {sentence}",
            [Citation(top.id, sentence, top.doc_title, top.location)],
        )


def _passage(chunk: Chunk, score: float = 0.0) -> Passage:
    return Passage(chunk.id, chunk.doc_title, chunk.text, WHOLE_DOCUMENT, score)
