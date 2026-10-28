import pytest
import shapes
from shapes import KeywordSearcher, Passage, Searcher, total_score

PASSAGES = [
    Passage("p1", "fleet-policy.md", "Trucks are serviced every 20,000 km.", 0.8),
    Passage("p2", "rates-2026.md", "Melbourne to Sydney costs $2,150 per load.", 0.4),
    Passage("p3", "fleet-policy.md", "Refrigerated trucks are checked weekly.", 0.6),
]


class FakeSearcher:
    """A stand-in, like the fakes BizWiz's own tests use. Note: it doesn't inherit from Searcher."""

    def search(self, question: str, k: int) -> list[Passage]:
        return PASSAGES[:k]


def test_citation_has_a_passage_id_and_a_quote():
    citation = shapes.Citation(passage_id="p1", quote="every 20,000 km")
    assert citation.passage_id == "p1"
    assert citation.quote == "every 20,000 km"


def test_citations_with_the_same_fields_are_equal():
    assert shapes.Citation("p1", "weekly") == shapes.Citation("p1", "weekly")


def test_keyword_searcher_finds_passages_sharing_a_word():
    found = KeywordSearcher(PASSAGES).search("How often are trucks serviced?", k=5)
    assert [p.id for p in found] == ["p1", "p3"]


def test_keyword_searcher_ignores_case():
    found = KeywordSearcher(PASSAGES).search("MELBOURNE", k=5)
    assert [p.id for p in found] == ["p2"]


def test_keyword_searcher_returns_at_most_k():
    assert len(KeywordSearcher(PASSAGES).search("trucks", k=1)) == 1


def test_both_searchers_fit_the_protocol():
    assert isinstance(KeywordSearcher(PASSAGES), Searcher)
    assert isinstance(FakeSearcher(), Searcher)


def test_total_score():
    assert total_score(PASSAGES) == pytest.approx(1.8)


def test_your_own():
    # TODO 4: write a test that checks KeywordSearcher returns an empty list
    #         when no passage shares a word with the question. Then delete the line below.
    pytest.fail("TODO 4: write this test yourself")
