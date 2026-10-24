"""The things BizWiz talks about: documents, chunks, passages and answers."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Document:
    """One whole file from a source, as plain text."""

    id: str  # stable across re-indexing, e.g. "ironbark/rate-card.md"
    title: str
    text: str


@dataclass(frozen=True)
class Chunk:
    """A piece of a document that gets indexed and searched."""

    id: str
    document_id: str
    doc_title: str
    text: str
    position: int  # 0 for the first chunk of a document, 1 for the next, ...
    embedding: list[float] | None = None
    model_id: str | None = None  # which embedding model made `embedding`


@dataclass(frozen=True)
class Passage:
    """A chunk that came back from a search, with how well it matched."""

    id: str  # the chunk id
    doc_title: str
    text: str
    location: str  # where it sits in the document, for people to read
    score: float = 0.0


@dataclass(frozen=True)
class Citation:
    """One quote that backs up part of an answer."""

    passage_id: str
    quoted_text: str
    doc_title: str
    location: str


@dataclass(frozen=True)
class Answer:
    text: str
    citations: list[Citation] = field(default_factory=list)
