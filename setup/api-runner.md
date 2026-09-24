# The runner

This is the path that works on any model with an API. The runner does not decide trades. It reads the rulebook, asks the model to follow it, and stores ledger lines the model prints.

```
your clock  →  runner.py  →  model API  →  Liquid paper  →  ledger.csv
```

`--live` is refused. A normal start is paper.

## Install

```bash
git clone https://github.com/merjua14/Agentic-Trading-For-Dummies
cd Agentic-Trading-For-Dummies/runner
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

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

`--check` prints the locked defaults and exits. It does not spend API calls.

`--live` must print `REFUSED` and exit with status 2. The same refusal happens if `.env` contains `LIVE=1`, `MODE=live`, or `TRADING_MODE=real`.

`python runner.py` and `python runner.py --paper` are the paper run. Two sub-ticks is the default so the first pass stays short. The runner will not place an order itself. It tells the model to confirm `paper_trading_status` first.

## Schedule it, still on paper

```bash
crontab -e
```

```cron
# hourly, at :05, paper only
5 * * * * cd /path/to/Agentic-Trading-For-Dummies/runner && /usr/bin/python3 runner.py >> run.log 2>&1
```

One cron line. The runner does its own sub-ticks. Do not add a second cron that overlaps, or two runs will write the same ledger.

If the machine sleeps, a missed hour is a missed look. Stops you already placed stay at the exchange.

## What the runner will not do

- It will not call `disable_paper_trading`.
- It will not call `enable_automated_trading`.
- It will not call `update_leverage`.
- It will not start a live session, even if you pass `--live`.
