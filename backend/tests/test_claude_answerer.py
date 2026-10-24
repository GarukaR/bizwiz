"""ClaudeAnswerer against a fake client. No API calls; the real call is smoke-tested by hand."""

from types import SimpleNamespace as NS

from bizwiz.answerers.claude import ClaudeAnswerer
from bizwiz.domain import Citation, Passage

PASSAGES = [
    Passage("rates.md#0", "Rate card", "Fuel levy 12%. Tolls extra.", "whole document"),
    Passage("fleet.md#0", "Fleet list", "We run 40 prime movers.", "whole document"),
]


class FakeClient:
    """Looks like `anthropic.Anthropic()` as far as ClaudeAnswerer cares."""

    def __init__(self, response):
        self.response = response
        self.sent = None
        self.beta = NS(messages=NS(create=self._create))

    def _create(self, **kwargs):
        self.sent = kwargs
        return self.response


def cite(document_index, text):
    return NS(
        type="char_location",
        document_index=document_index,
        cited_text=text,
        document_title=None,
        start_char_index=0,
        end_char_index=len(text),
    )


def response(*blocks, stop_reason="end_turn"):
    return NS(content=list(blocks), stop_reason=stop_reason)


def test_sends_each_passage_as_a_cited_document_then_the_question():
    client = FakeClient(response(NS(type="text", text="ok", citations=None)))

    ClaudeAnswerer(client, model="claude-test").answer("What is the levy?", PASSAGES)

    assert client.sent["model"] == "claude-test"
    [message] = client.sent["messages"]
    *docs, question = message["content"]
    assert [d["type"] for d in docs] == ["document", "document"]
    assert docs[0]["source"] == {
        "type": "text",
        "media_type": "text/plain",
        "data": "Fuel levy 12%. Tolls extra.",
    }
    assert docs[0]["title"] == "Rate card"
    assert all(d["citations"] == {"enabled": True} for d in docs)
    assert question == {"type": "text", "text": "What is the levy?"}


def test_joins_text_blocks_and_maps_citations_back_to_passages():
    client = FakeClient(
        response(
            NS(type="thinking", thinking=""),
            NS(type="text", text="The levy is ", citations=None),
            NS(type="text", text="12%", citations=[cite(0, "Fuel levy 12%.")]),
            NS(
                type="text",
                text=" and the fleet is 40 trucks.",
                citations=[cite(1, "40 prime movers")],
            ),
        )
    )

    answer = ClaudeAnswerer(client, model="m").answer("q", PASSAGES)

    assert answer.text == "The levy is 12% and the fleet is 40 trucks."
    assert answer.citations == [
        Citation("rates.md#0", "Fuel levy 12%.", "Rate card", "whole document"),
        Citation("fleet.md#0", "40 prime movers", "Fleet list", "whole document"),
    ]


def test_a_refusal_comes_back_as_a_plain_answer_without_citations():
    client = FakeClient(response(stop_reason="refusal"))

    answer = ClaudeAnswerer(client, model="m").answer("q", PASSAGES)

    assert answer.citations == []
    assert "couldn't answer" in answer.text
