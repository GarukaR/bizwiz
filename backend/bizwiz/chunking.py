from bizwiz.domain import Chunk, Document

WHOLE_DOCUMENT = "whole document"  # a chunk's location until chunks know their heading


# replaced by Quest 1 (The Chunker): split by headings instead of one chunk per document.
def chunk_document(doc: Document) -> list[Chunk]:
    return [Chunk(f"{doc.id}#0", doc.id, doc.title, doc.text, position=0)]
