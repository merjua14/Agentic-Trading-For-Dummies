# The runner

This is the path that works on any model with an API. The runner does not decide trades. It reads the rulebook, asks the model to follow it, and stores ledger lines the model prints.

```
your clock  →  runner.py  →  model API  →  Liquid paper  →  ledger.csv
```

`--live` is refused. A normal start is paper.

## Install

Follow [START HERE](../README.md#start-here) in the README. Same order: clone, venv, `.env`, `--check`, `--live` (you want `REFUSED`), then one paper run.

On Windows PowerShell, use `py -m venv .venv` and `.venv\Scripts\Activate.ps1` instead of `python3` and `source`, and `copy .env.example .env` instead of `cp`.

Fill in `.env`:

```bash
PROVIDER=anthropic          # anthropic | openai | xai
MODEL=claude-opus-4-6       # or gpt-5.6-sol, or grok-4
ANTHROPIC_API_KEY=sk-ant-...
LIQUID_MCP_URL=https://<your-liquid-connector>/mcp
LIQUID_MCP_TOKEN=...
SUBTICKS=2
SUBTICK_SECONDS=300
RULEBOOK=../rulebook/liquid-v77-lite.txt
LEDGER=./ledger.csv
```

## Check, then refuse, then paper

```bash
python runner.py --check
python runner.py --live
python runner.py
```

`--check` prints the locked defaults and exits. It does not spend API calls. Success is `mode=paper`, `riskFrac=0.015`, `softHalt=on`, `hardHalt=on`.

`--live` must print `REFUSED` and exit with status 2. The same refusal happens if `.env` contains `LIVE=1`, `MODE=live`, or `TRADING_MODE=real`. That refusal is success. Nothing is sent.

`python runner.py` and `python runner.py --paper` are the paper run. Two looks is the default so the first pass stays short. The two looks run one after the other. `SUBTICK_SECONDS` is in `.env` and is not a pause yet. Success is a line with `PAPER ONLY`, then a `PAPER REPORT`. The runner will not place an order itself. It tells the model to confirm `paper_trading_status` first.

If the run stops, the usual causes are a missing key, paper turned off, or the wrong folder. The exact fixes are in the README under [If something breaks](../README.md#if-something-breaks).

## Schedule it, still on paper

cron is the Mac and Linux timer. It runs a command on a clock.

```bash
crontab -e
```

```cron
# hourly, at :05, paper only. Use the venv Python so the libraries are found.
5 * * * * cd /path/to/Agentic-Trading-For-Dummies/runner && .venv/bin/python runner.py >> run.log 2>&1
```

One cron line. The runner does its own looks. Do not add a second cron that overlaps, or two runs will write the same ledger.

On Windows, Task Scheduler can run the same command. Point it at `runner\.venv\Scripts\python.exe` and start in the `runner` folder. The run is still paper.

If the machine sleeps, a missed hour is a missed look. Stops you already placed stay at the exchange.

## What the runner will not do

- It will not call `disable_paper_trading`.
- It will not call `enable_automated_trading`.
- It will not call `update_leverage`.
- It will not start a live session, even if you pass `--live`.
