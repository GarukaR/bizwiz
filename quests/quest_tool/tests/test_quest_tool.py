from pathlib import Path

import pytest

from quest_tool import (
    apply_award,
    apply_hint,
    apply_result,
    current_stage,
    find_stages,
    render_board,
    run_tests,
)


def make_stage(root: Path, name: str, title: str, reward: int = 50, tests: str = "") -> Path:
    folder = root / name
    folder.mkdir(parents=True)
    (folder / "BRIEF.md").write_text(f"# {title}\n\n**Clear reward:** {reward} XP\n")
    if tests:
        (folder / f"test_{folder.name}_{folder.parent.name}.py").write_text(tests)
    return folder


def fresh() -> dict:
    return {"xp": 0, "hints_used": 0, "streak": 0, "eval_history": [], "stages_done": []}


def test_stages_are_found_in_quest_then_stage_order(tmp_path):
    make_stage(tmp_path, "q1_chunker/stage_a", "Stage 1a")
    make_stage(tmp_path, "q0_warmup/stage_b", "Stage 0b")
    make_stage(tmp_path, "q0_warmup/stage_a", "Stage 0a")
    (tmp_path / "quest_tool").mkdir()

    stages = find_stages(tmp_path)

    assert [s.id for s in stages] == [
        "q0_warmup/stage_a",
        "q0_warmup/stage_b",
        "q1_chunker/stage_a",
    ]
    assert stages[0].title == "Stage 0a"


def test_stage_reward_comes_from_the_brief(tmp_path):
    make_stage(tmp_path, "q0_warmup/stage_a", "Solo stage", reward=100)

    assert find_stages(tmp_path)[0].reward == 100


def test_current_stage_is_the_first_not_done(tmp_path):
    make_stage(tmp_path, "q0_warmup/stage_a", "A")
    make_stage(tmp_path, "q0_warmup/stage_b", "B")
    progress = fresh() | {"stages_done": ["q0_warmup/stage_a"]}

    assert current_stage(find_stages(tmp_path), progress).id == "q0_warmup/stage_b"


def test_no_current_stage_when_everything_is_done(tmp_path):
    make_stage(tmp_path, "q0_warmup/stage_a", "A")
    progress = fresh() | {"stages_done": ["q0_warmup/stage_a"]}

    assert current_stage(find_stages(tmp_path), progress) is None


def test_all_green_clears_the_stage_and_awards_xp(tmp_path):
    stage = _one_stage(tmp_path, reward=50)

    progress, message = apply_result(fresh(), stage, passed=5, total=5)

    assert progress["stages_done"] == ["q0_warmup/stage_a"]
    assert progress["xp"] == 50
    assert progress["streak"] == 1
    assert "+50 XP" in message


def test_some_red_changes_nothing(tmp_path):
    stage = _one_stage(tmp_path)

    progress, message = apply_result(fresh(), stage, passed=3, total=5)

    assert progress == fresh()
    assert message == ""


def test_a_stage_with_no_tests_is_not_cleared(tmp_path):
    stage = _one_stage(tmp_path)

    progress, _ = apply_result(fresh(), stage, passed=0, total=0)

    assert progress["stages_done"] == []


def test_hint_costs_xp_and_counts(tmp_path):
    progress = apply_hint(fresh() | {"xp": 100}, level=2)

    assert progress["xp"] == 90
    assert progress["hints_used"] == 1
    assert progress["hints_this_stage"] == 1


def test_hint_costs_are_5_10_20():
    assert [apply_hint(fresh() | {"xp": 100}, level=n)["xp"] for n in (1, 2, 3)] == [95, 90, 80]


def test_xp_never_goes_below_zero():
    assert apply_hint(fresh(), level=3)["xp"] == 0


def test_unknown_hint_level_is_refused():
    with pytest.raises(ValueError):
        apply_hint(fresh(), level=4)


def test_clearing_a_hinted_stage_resets_the_streak(tmp_path):
    stage = _one_stage(tmp_path)
    progress = fresh() | {"streak": 3, "hints_this_stage": 1}

    progress, _ = apply_result(progress, stage, passed=2, total=2)

    assert progress["streak"] == 0
    assert progress["hints_this_stage"] == 0


def test_award_adds_xp():
    assert apply_award(fresh(), 30)["xp"] == 30


def test_board_shows_the_numbers(tmp_path):
    stage = _one_stage(tmp_path, title="Stage 0a: Reading Python")
    progress = fresh() | {"xp": 120, "hints_used": 2, "streak": 1}

    board = render_board(progress, stage, passed=3, total=5)

    assert "Stage 0a: Reading Python" in board
    assert "3/5" in board
    assert "120" in board
    assert "BRIEF.md" in board


def test_board_shows_recent_evals():
    progress = fresh() | {"eval_history": [{"date": "2026-11-01", "score": "12/30"}]}

    assert "12/30" in render_board(progress, None, passed=0, total=0)


def test_run_tests_counts_passes_and_failures(tmp_path):
    folder = make_stage(
        tmp_path,
        "q0_warmup/stage_a",
        "A",
        tests="def test_ok():\n    assert True\n\ndef test_bad():\n    assert False\n",
    )

    assert run_tests(folder, quiet=True) == (1, 2)


def _one_stage(tmp_path, reward=50, title="Stage 0a"):
    make_stage(tmp_path, "q0_warmup/stage_a", title, reward=reward)
    return find_stages(tmp_path)[0]
