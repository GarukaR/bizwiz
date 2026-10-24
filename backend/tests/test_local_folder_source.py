import os
from datetime import datetime, timedelta

from bizwiz.sources.local_folder import LocalFolderSource


def test_lists_text_and_markdown_files_including_subfolders(tmp_path):
    (tmp_path / "rates.md").write_text("# Rate card\n", encoding="utf-8")
    (tmp_path / "policies").mkdir()
    (tmp_path / "policies" / "fatigue.txt").write_text("Fatigue policy\n", encoding="utf-8")
    (tmp_path / "logo.png").write_bytes(b"\x89PNG")

    refs = LocalFolderSource(tmp_path).list_changed(since=None)

    assert sorted(refs) == ["policies/fatigue.txt", "rates.md"]


def test_lists_only_files_changed_after_since(tmp_path):
    old = tmp_path / "old.md"
    new = tmp_path / "new.md"
    old.write_text("old", encoding="utf-8")
    new.write_text("new", encoding="utf-8")
    long_ago = (datetime.now() - timedelta(days=10)).timestamp()
    os.utime(old, (long_ago, long_ago))

    refs = LocalFolderSource(tmp_path).list_changed(since=datetime.now() - timedelta(days=1))

    assert refs == ["new.md"]


def test_load_uses_the_first_heading_as_the_title(tmp_path):
    (tmp_path / "rates.md").write_text("# Rate card 2026\n\nFuel levy 12%.\n", encoding="utf-8")

    doc = LocalFolderSource(tmp_path).load("rates.md")

    assert doc.id == "rates.md"
    assert doc.title == "Rate card 2026"
    assert doc.text == "# Rate card 2026\n\nFuel levy 12%.\n"


def test_load_falls_back_to_the_file_name_as_the_title(tmp_path):
    (tmp_path / "fleet-list.txt").write_text("40 prime movers", encoding="utf-8")

    assert LocalFolderSource(tmp_path).load("fleet-list.txt").title == "fleet-list"
