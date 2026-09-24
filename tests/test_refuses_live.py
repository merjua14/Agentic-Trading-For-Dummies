"""The public runner refuses live mode and keeps paper defaults."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "runner" / "runner.py"


def run(args):
    return subprocess.run(
        [sys.executable, str(RUNNER), *args],
        cwd=ROOT / "runner",
        text=True,
        capture_output=True,
        check=False,
    )


def test_live_flag_is_refused():
    result = run(["--live"])
    assert result.returncode == 2
    assert "REFUSED" in result.stderr
    assert "--live" in result.stderr
    assert result.stdout == ""


def test_live_env_is_refused():
    result = subprocess.run(
        [sys.executable, str(RUNNER), "--check"],
        cwd=ROOT / "runner",
        text=True,
        capture_output=True,
        check=False,
        env={**dict(**{k: v for k, v in __import__("os").environ.items()}), "MODE": "live"},
    )
    assert result.returncode == 2
    assert "REFUSED" in result.stderr


def test_check_prints_paper_defaults():
    result = run(["--check"])
    assert result.returncode == 0, result.stderr
    text = result.stdout
    assert "mode=paper" in text
    assert "riskFrac=0.015" in text
    assert "softHalt=on" in text
    assert "hardHalt=on" in text
    assert "liveFlag=refused" in text
    assert "rulebook=ok" in text
