"""PostgresIndex against the real database. Start it first: `docker compose up -d db`."""

import os

import psycopg
import pytest

from bizwiz.domain import Chunk
from bizwiz.index.postgres import PostgresIndex

pytestmark = pytest.mark.integration

DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL", "postgresql://bizwiz:bizwiz@localhost:5442/bizwiz_test"
)


@pytest.fixture
def index():
    try:
        conn = psycopg.connect(DATABASE_URL, connect_timeout=3)
    except psycopg.OperationalError as e:
        pytest.skip(f"Postgres not reachable ({e}); run `docker compose up -d db`")
    conn.execute("DROP TABLE IF EXISTS chunks")
    conn.commit()
    conn.close()
    return PostgresIndex(DATABASE_URL)


def chunk(doc_id, text, position=0, title=None):
    return Chunk(
        f"{doc_id}#{position}",
        doc_id,
        title or doc_id,
        text,
        position,
        embedding=[0.1, 0.2, 0.3],
        model_id="fake-embedder-v0",
    )


def test_search_finds_chunks_containing_words_from_the_question(index):
    index.add(
        [
            chunk("rates.md", "The fuel levy is 12% this month."),
            chunk("fleet.md", "We run 40 prime movers out of Laverton."),
        ]
    )

    passages = index.search("What is the fuel levy?", k=5)

    assert [p.id for p in passages] == ["rates.md#0"]
    assert passages[0].doc_title == "rates.md"


def test_search_ranks_chunks_matching_more_words_first(index):
    index.add(
        [chunk("a.md", "Fuel prices rose."), chunk("b.md", "The fuel levy is reviewed monthly.")]
    )

    passages = index.search("fuel levy", k=5)

    assert [p.id for p in passages] == ["b.md#0", "a.md#0"]


def test_search_returns_at_most_k(index):
    index.add([chunk(f"{n}.md", "fuel") for n in range(5)])

    assert len(index.search("fuel", k=2)) == 2


def test_get_returns_a_stored_chunk_as_a_passage(index):
    index.add([chunk("rates.md", "Fuel levy 12%.", title="Rate card")])

    passage = index.get("rates.md#0")

    assert passage.text == "Fuel levy 12%."
    assert passage.doc_title == "Rate card"
    assert index.get("missing#0") is None


def test_adding_a_document_again_replaces_its_old_chunks(index):
    index.add([chunk("rates.md", "old levy", 0), chunk("rates.md", "old tolls", 1)])
    index.add([chunk("rates.md", "new levy", 0)])

    assert index.get("rates.md#1") is None
    assert index.get("rates.md#0").text == "new levy"


def test_stores_the_vector_and_its_model_id(index):
    index.add([chunk("rates.md", "Fuel levy 12%.")])

    with psycopg.connect(DATABASE_URL) as conn:
        model_id, dims = conn.execute(
            "SELECT model_id, vector_dims(embedding) FROM chunks"
        ).fetchone()
    assert (model_id, dims) == ("fake-embedder-v0", 3)
