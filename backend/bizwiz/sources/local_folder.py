from datetime import datetime
from pathlib import Path

from bizwiz.domain import Document

TEXT_SUFFIXES = {".md", ".txt"}


class LocalFolderSource:
    """Reads .md and .txt files from a folder and its subfolders."""

    def __init__(self, root: Path | str):
        self.root = Path(root)

    def list_changed(self, since: datetime | None) -> list[str]:
        cutoff = since.timestamp() if since else None
        return sorted(
            p.relative_to(self.root).as_posix()
            for p in self.root.rglob("*")
            if p.is_file()
            and p.suffix.lower() in TEXT_SUFFIXES
            and (cutoff is None or p.stat().st_mtime > cutoff)
        )

    def load(self, ref: str) -> Document:
        path = self.root / ref
        text = path.read_text(encoding="utf-8")
        return Document(id=ref, title=_title(text) or path.stem, text=text)


def _title(text: str) -> str | None:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None
