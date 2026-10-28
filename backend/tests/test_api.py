from fastapi.testclient import TestClient

from bizwiz.api import create_app
from bizwiz.domain import Chunk
from bizwiz.fakes import FakeAnswerer, InMemoryIndex


def client_with(*chunks):
    index = InMemoryIndex()
    index.add(chunks)
    return TestClient(create_app(index=index, answerer=FakeAnswerer()))


def test_ask_returns_the_answer_and_its_citations():
    client = client_with(
        Chunk("rates.md#0", "rates.md", "Rate card", "Fuel levy 12%. Tolls extra.", 0)
    )

    res = client.post("/ask", json={"question": "What is the fuel levy?"})

    assert res.status_code == 200
    body = res.json()
    assert body["answer"]
    assert body["citations"] == [
        {
            "passage_id": "rates.md#0",
            "quoted_text": "Fuel levy 12%.",
            "doc_title": "Rate card",
            "location": "whole document",
        }
    ]


def test_ask_rejects_an_empty_question():
    res = client_with().post("/ask", json={"question": "   "})

    assert res.status_code == 422


def test_get_passage_returns_its_text():
    client = client_with(Chunk("rates.md#0", "rates.md", "Rate card", "Fuel levy 12%.", 0))

    res = client.get("/passages/rates.md%230")

    assert res.status_code == 200
    assert res.json() == {
        "id": "rates.md#0",
        "doc_title": "Rate card",
        "text": "Fuel levy 12%.",
        "location": "whole document",
    }


def test_get_unknown_passage_is_404():
    assert client_with().get("/passages/nope").status_code == 404
