from bizwiz.domain import Answer, Citation, Document, Passage
from bizwiz.fakes import FakeAnswerer, FakeEmbedder, InMemoryIndex
from bizwiz.pipeline import ask, index_source


class ListSource:
    def __init__(self, docs: list[Document]):
        self.docs = {d.id: d for d in docs}

    def list_changed(self, since):
        return list(self.docs)

    def load(self, ref):
        return self.docs[ref]


class SpyAnswerer:
    def __init__(self):
        self.calls = []

    def answer(self, question, passages):
        self.calls.append((question, list(passages)))
        return Answer("spy answer", [Citation("p1", "quote", "Doc", "whole document")])


def test_ask_passes_found_passages_to_the_answerer():
    index = InMemoryIndex()
    index_source(
        ListSource(
            [
                Document("a.md", "Rates", "The fuel levy is 12%."),
                Document("b.md", "Fleet", "We run 40 prime movers."),
            ]
        ),
        FakeEmbedder(),
        index,
    )
    answerer = SpyAnswerer()

    answer = ask("What is the fuel levy?", index=index, answerer=answerer)

    assert answer.text == "spy answer"
    question, passages = answerer.calls[0]
    assert question == "What is the fuel levy?"
    assert [p.doc_title for p in passages] == ["Rates"]


def test_ask_asks_the_index_for_at_most_k_passages():
    class CountingIndex(InMemoryIndex):
        def search(self, query, k):
            self.k = k
            return super().search(query, k)

    index = CountingIndex()
    ask("anything", index=index, answerer=FakeAnswerer(), k=3)

    assert index.k == 3


def test_index_source_embeds_chunks_and_records_the_model():
    index = InMemoryIndex()
    index_source(
        ListSource([Document("a.md", "Rates", "The fuel levy is 12%.")]), FakeEmbedder(), index
    )

    [chunk] = index.chunks.values()
    assert chunk.document_id == "a.md"
    assert chunk.embedding is not None
    assert chunk.model_id == FakeEmbedder.model_id


def test_fake_answerer_quotes_the_best_matching_sentence_of_the_top_passage():
    text = "# Fuel levy\n\nTolls are extra. The fuel levy is 12%. It changes monthly."
    passage = Passage("a.md#0", "Rates", text, "whole document")

    answer = FakeAnswerer().answer("What is the fuel levy?", [passage])

    assert answer.citations == [
        Citation("a.md#0", "The fuel levy is 12%.", "Rates", "whole document")
    ]
