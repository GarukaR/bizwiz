import pytest
from data import average_score, chunk_ids, from_doc, group_by_doc, top_k

CHUNKS = [
    {"id": "c1", "doc": "fleet-policy.md", "text": "Trucks are serviced every 20,000 km.", "score": 0.82},
    {"id": "c2", "doc": "rates-2026.md", "text": "Melbourne to Sydney costs $2,150 per load.", "score": 0.35},
    {"id": "c3", "doc": "fleet-policy.md", "text": "Drivers rest 30 minutes every 5 hours.", "score": 0.67},
    {"id": "c4", "doc": "clients.md", "text": "Gumleaf Grocers ship twice a week.", "score": 0.91},
]


def test_chunk_ids_keeps_the_order():
    assert chunk_ids(CHUNKS) == ["c1", "c2", "c3", "c4"]


def test_from_doc_keeps_only_that_document():
    assert [c["id"] for c in from_doc(CHUNKS, "fleet-policy.md")] == ["c1", "c3"]


def test_from_doc_with_an_unknown_document_is_empty():
    assert from_doc(CHUNKS, "nope.md") == []


def test_top_k_is_best_first():
    assert [c["id"] for c in top_k(CHUNKS, 2)] == ["c4", "c1"]


def test_top_k_does_not_change_the_original_list():
    before = list(CHUNKS)
    top_k(CHUNKS, 2)
    assert CHUNKS == before


def test_top_k_larger_than_the_list_returns_everything():
    assert len(top_k(CHUNKS, 10)) == 4


def test_group_by_doc():
    assert group_by_doc(CHUNKS) == {
        "fleet-policy.md": ["c1", "c3"],
        "rates-2026.md": ["c2"],
        "clients.md": ["c4"],
    }


def test_average_score():
    assert average_score(CHUNKS) == pytest.approx(0.6875)


def test_average_score_of_nothing_is_zero():
    assert average_score([]) == 0.0
