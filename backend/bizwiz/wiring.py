"""The one place where concrete classes are chosen and plugged into the seams."""

import logging
import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI

from bizwiz.api import create_app
from bizwiz.fakes import FakeAnswerer, FakeEmbedder
from bizwiz.index.postgres import PostgresIndex
from bizwiz.pipeline import index_source
from bizwiz.seams import Answerer
from bizwiz.sources.local_folder import LocalFolderSource

log = logging.getLogger("bizwiz")

REPO_ROOT = Path(__file__).resolve().parents[2]


def build_answerer() -> Answerer:
    if os.environ.get("ANSWERER", "claude") == "fake":
        return FakeAnswerer()

    import anthropic

    from bizwiz.answerers.claude import ClaudeAnswerer

    return ClaudeAnswerer(
        anthropic.Anthropic(), model=os.environ.get("ANSWER_MODEL", "claude-opus-5-5")
    )


def build_app() -> FastAPI:
    load_dotenv(find_dotenv(usecwd=True))
    index = PostgresIndex(
        os.environ.get("DATABASE_URL", "postgresql://bizwiz:bizwiz@localhost:5442/bizwiz")
    )

    # Index the demo corpus on start-up. Cheap while it is a few local files; Drive sync (#14)
    # moves this into its own scheduled job.
    corpus = Path(os.environ.get("CORPUS_DIR", REPO_ROOT / "corpus" / "ironbark"))
    count = index_source(LocalFolderSource(corpus), FakeEmbedder(), index)
    log.warning("Indexed %d documents from %s", count, corpus)

    return create_app(
        index=index,
        answerer=build_answerer(),
        web_origin=os.environ.get("WEB_ORIGIN", "http://localhost:3010"),
    )
