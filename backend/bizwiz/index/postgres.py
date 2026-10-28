from collections.abc import Sequence

import psycopg

from bizwiz.chunking import WHOLE_DOCUMENT
from bizwiz.domain import Chunk, Passage
from bizwiz.search_words import search_words

SCHEMA = """
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE IF NOT EXISTS chunks (
    id          text PRIMARY KEY,
    document_id text NOT NULL,
    doc_title   text NOT NULL,
    text        text NOT NULL,
    position    integer NOT NULL,
    embedding   vector,
    model_id    text
);
CREATE INDEX IF NOT EXISTS chunks_document_id ON chunks (document_id);
"""


class PostgresIndex:
    """Chunks stored in Postgres, with pgvector for the embeddings."""

    def __init__(self, database_url: str):
        self.database_url = database_url
        with self._connect() as conn:
            conn.execute(SCHEMA)

    def _connect(self) -> psycopg.Connection:
        return psycopg.connect(self.database_url)

    def add(self, chunks: Sequence[Chunk]) -> None:
        with self._connect() as conn:
            conn.execute(
                "DELETE FROM chunks WHERE document_id = ANY(%s)",
                [list({c.document_id for c in chunks})],
            )
            with conn.cursor() as cur:
                cur.executemany(
                    "INSERT INTO chunks (id, document_id, doc_title, text, position, embedding,"
                    " model_id) VALUES (%s, %s, %s, %s, %s, %s::vector, %s)",
                    [
                        (
                            c.id,
                            c.document_id,
                            c.doc_title,
                            c.text,
                            c.position,
                            _vector(c.embedding),
                            c.model_id,
                        )
                        for c in chunks
                    ],
                )

    # replaced by Quests 2-4: full-text search, vector search, then fusing the two.
    def search(self, query: str, k: int) -> list[Passage]:
        """Crude placeholder: score each chunk by how many question words it contains."""
        words = search_words(query)
        if not words:
            return []
        score = " + ".join(["(text ILIKE %s)::int"] * len(words))
        sql = (
            f"SELECT id, doc_title, text, score FROM ("
            f"  SELECT id, doc_title, text, {score} AS score FROM chunks"
            f") scored WHERE score > 0 ORDER BY score DESC, id LIMIT %s"
        )
        with self._connect() as conn:
            rows = conn.execute(sql, [*(f"%{w}%" for w in words), k]).fetchall()
        return [Passage(id, title, text, WHOLE_DOCUMENT, score) for id, title, text, score in rows]

    def get(self, passage_id: str) -> Passage | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT id, doc_title, text FROM chunks WHERE id = %s", [passage_id]
            ).fetchone()
        return Passage(row[0], row[1], row[2], WHOLE_DOCUMENT) if row else None


def _vector(embedding: list[float] | None) -> str | None:
    return None if embedding is None else "[" + ",".join(map(str, embedding)) + "]"
