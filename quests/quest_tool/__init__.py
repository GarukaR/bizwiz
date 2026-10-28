"""Quest Mode scoreboard: `uv run quest`.

Runs the tests of the current stage, clears the stage (and awards its XP) the first time they're all
green, and prints the scoreboard. Progress lives in `quests/progress.json`.

    uv run quest              run the current stage and show the scoreboard
    uv run quest hint 1|2|3   log a hint (-5 / -10 / -20 XP)
    uv run quest award N      add N XP (correct predictions, interview card, boss fights)
"""

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import pytest

QUESTS_DIR = Path(__file__).resolve().parent.parent
PROGRESS_FILE = QUESTS_DIR / "progress.json"
HINT_COST = {1: 5, 2: 10, 3: 20}


@dataclass(frozen=True)
class Stage:
    id: str  # e.g. "q0_warmup/stage_a"
    folder: Path
    title: str
    reward: int


def find_stages(root: Path) -> list[Stage]:
    """Every `q*/stage_*` folder with a BRIEF.md, in quest then stage order."""
    stages = []
    for brief in sorted(root.glob("q*/stage_*/BRIEF.md")):
        text = brief.read_text(encoding="utf-8")
        title = text.splitlines()[0].lstrip("# ").strip()
        reward = re.search(r"Clear reward:\*\* (\d+) XP", text)
        folder = brief.parent
        stages.append(
            Stage(
                id=f"{folder.parent.name}/{folder.name}",
                folder=folder,
                title=title,
                reward=int(reward.group(1)) if reward else 50,
            )
        )
    return stages


def current_stage(stages: list[Stage], progress: dict) -> Stage | None:
    return next((s for s in stages if s.id not in progress["stages_done"]), None)


def apply_result(progress: dict, stage: Stage, passed: int, total: int) -> tuple[dict, str]:
    """Clear the stage if every test passed. Returns the new progress and a message."""
    if total == 0 or passed < total:
        return progress, ""
    hinted = progress.get("hints_this_stage", 0) > 0
    progress = progress | {
        "xp": progress["xp"] + stage.reward,
        "stages_done": [*progress["stages_done"], stage.id],
        "streak": 0 if hinted else progress["streak"] + 1,
        "hints_this_stage": 0,
    }
    return progress, f"🎉 Stage cleared: {stage.title}  +{stage.reward} XP"


def apply_hint(progress: dict, level: int) -> dict:
    if level not in HINT_COST:
        raise ValueError(f"Hint level must be 1, 2 or 3, not {level}")
    return progress | {
        "xp": max(0, progress["xp"] - HINT_COST[level]),
        "hints_used": progress["hints_used"] + 1,
        "hints_this_stage": progress.get("hints_this_stage", 0) + 1,
    }


def apply_award(progress: dict, xp: int) -> dict:
    return progress | {"xp": progress["xp"] + xp}


def render_board(progress: dict, stage: Stage | None, passed: int, total: int) -> str:
    lines = ["", "🎮 BizWiz Quest Mode", "─" * 40]
    if stage is None:
        lines.append("Stage   all stages cleared 🏆")
    else:
        lines.append(f"Stage   {stage.title}")
        tests = f"{passed}/{total} passing" if total else "none could run (see the error above)"
        lines.append(f"Tests   {tests}")
        lines.append(f"Brief   quests/{stage.id}/BRIEF.md")
    lines.append(
        f"XP      {progress['xp']}    Hints {progress['hints_used']}    "
        f"Streak {progress['streak']} (stages in a row with no hints)"
    )
    lines.append(f"Done    {len(progress['stages_done'])} stage(s)")
    evals = progress["eval_history"][-3:]
    evals_text = ", ".join(f"{e['date']}: {e['score']}" for e in evals) if evals else "none yet"
    lines.append(f"Evals   {evals_text}")
    return "\n".join(lines)


class _Counter:
    def __init__(self) -> None:
        self.passed = 0
        self.total = 0

    def pytest_collection_finish(self, session) -> None:
        self.total = len(session.items)

    def pytest_runtest_logreport(self, report) -> None:
        if report.when == "call" and report.passed:
            self.passed += 1


def run_tests(folder: Path, quiet: bool = False) -> tuple[int, int]:
    """Run one stage's tests. Returns (passed, total)."""
    counter = _Counter()
    args = [str(folder), f"--rootdir={folder}", "-p", "no:cacheprovider", "--tb=short", "-q"]
    if quiet:
        args += ["-q", "--tb=no"]
    pytest.main(args, plugins=[counter])
    return counter.passed, counter.total


def load_progress() -> dict:
    return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))


def save_progress(progress: dict) -> None:
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2) + "\n", encoding="utf-8", newline="\n")


def main(argv: list[str] | None = None) -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    argv = sys.argv[1:] if argv is None else argv
    progress = load_progress()

    if argv[:1] == ["hint"] and len(argv) == 2:
        progress = apply_hint(progress, int(argv[1]))
        save_progress(progress)
        print(f"Hint {argv[1]} logged (-{HINT_COST[int(argv[1])]} XP). XP is now {progress['xp']}.")
        return
    if argv[:1] == ["award"] and len(argv) == 2:
        progress = apply_award(progress, int(argv[1]))
        save_progress(progress)
        print(f"+{argv[1]} XP. XP is now {progress['xp']}.")
        return
    if argv:
        print(__doc__)
        return

    stage = current_stage(find_stages(QUESTS_DIR), progress)
    passed = total = 0
    message = ""
    if stage is not None:
        passed, total = run_tests(stage.folder)
        progress, message = apply_result(progress, stage, passed, total)
        save_progress(progress)
    print(render_board(progress, stage, passed, total))
    if message:
        print(f"\n{message}")
        print("Commit your work, then run `uv run quest` again for the next stage.")
