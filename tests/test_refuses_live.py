"""The public runner refuses live mode and keeps paper defaults."""

import os
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


def test_blank_env_names_the_missing_key():
    env = os.environ.copy()
    for key in (
        "ANTHROPIC_API_KEY",
        "OPENAI_API_KEY",
        "XAI_API_KEY",
        "LIQUID_MCP_URL",
        "LIQUID_MCP_TOKEN",
        "MODE",
        "LIVE",
        "TRADING_MODE",
    ):
        env[key] = ""
    env["PROVIDER"] = "anthropic"
    result = subprocess.run(
        [sys.executable, str(RUNNER)],
        cwd=ROOT / "runner",
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )
    assert result.returncode == 1, result.stderr
    assert "Missing key:" in result.stderr
    assert "ANTHROPIC_API_KEY" in result.stderr
    assert "LIQUID_MCP_URL" in result.stderr
    assert "LIQUID_MCP_TOKEN" in result.stderr
    assert "REFUSED" not in result.stderr


def test_check_outside_runner_folder_says_wrong_directory():
    result = subprocess.run(
        [sys.executable, str(RUNNER), "--check"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 1
    assert "wrong directory" in result.stderr
    assert "mode=paper" not in result.stdout
