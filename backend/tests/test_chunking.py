from bizwiz.chunking import chunk_document
from bizwiz.domain import Document


def test_placeholder_chunker_makes_one_chunk_per_document():
    doc = Document("ironbark/rates.md", "Rate card", "# Rate card\n\nFuel levy 12%.")

    [chunk] = chunk_document(doc)

    assert chunk.id == "ironbark/rates.md#0"
    assert chunk.document_id == "ironbark/rates.md"
    assert chunk.doc_title == "Rate card"
    assert chunk.text == doc.text
    assert chunk.position == 0
