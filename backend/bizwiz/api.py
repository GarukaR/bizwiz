"""The HTTP API: POST /ask and GET /passages/{id}."""

import os
from typing import Annotated

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, StringConstraints

from bizwiz.pipeline import ask
from bizwiz.seams import Answerer, Index


class AskRequest(BaseModel):
    question: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=1, max_length=2000)
    ]


class CitationOut(BaseModel):
    passage_id: str
    quoted_text: str
    doc_title: str
    location: str


class AskResponse(BaseModel):
    answer: str
    citations: list[CitationOut]


class PassageOut(BaseModel):
    id: str
    doc_title: str
    text: str
    location: str


def create_app(*, index: Index, answerer: Answerer, web_origin: str = "*") -> FastAPI:
    app = FastAPI(title="BizWiz")
    app.add_middleware(
        CORSMiddleware, allow_origins=[web_origin], allow_methods=["*"], allow_headers=["*"]
    )

    @app.post("/ask")
    def post_ask(req: AskRequest) -> AskResponse:
        answer = ask(req.question, index=index, answerer=answerer)
        return AskResponse(
            answer=answer.text,
            citations=[CitationOut(**vars(c)) for c in answer.citations],
        )

    # `:path` because passage ids contain slashes, e.g. "ironbark/rate-card.md#0".
    @app.get("/passages/{passage_id:path}")
    def get_passage(passage_id: str) -> PassageOut:
        passage = index.get(passage_id)
        if passage is None:
            raise HTTPException(404, "No passage with that id")
        return PassageOut(
            id=passage.id, doc_title=passage.doc_title, text=passage.text, location=passage.location
        )

    return app


def main() -> None:
    """`uv run bizwiz-api`: start the API with the real wiring."""
    import uvicorn

    uvicorn.run(
        "bizwiz.wiring:build_app",
        factory=True,
        host="127.0.0.1",
        port=int(os.environ.get("API_PORT", "8010")),
    )
