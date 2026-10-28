"""The two jobs BizWiz does: index documents, and answer questions from them.

Both depend only on the seams, so any Source, Embedder, Index or Answerer can be plugged in.
"""

from dataclasses import replace

from bizwiz.chunking import chunk_document
from bizwiz.domain import Answer
from bizwiz.seams import Answerer, Embedder, Index, Source


def index_source(source: Source, embedder: Embedder, index: Index) -> int:
    """Load every document from `source`, chunk and embed it, and add it to `index`.

    Returns how many documents were indexed.
    """
    refs = source.list_changed(since=None)
    for ref in refs:
        chunks = chunk_document(source.load(ref))
        vectors = embedder.embed([c.text for c in chunks])
        index.add(
            [
                replace(c, embedding=v, model_id=embedder.model_id)
                for c, v in zip(chunks, vectors, strict=True)
            ]
        )
    return len(refs)


def ask(question: str, *, index: Index, answerer: Answerer, k: int = 5) -> Answer:
    passages = index.search(question, k=k)
    return answerer.answer(question, passages)
