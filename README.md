# Agentic Trading for Dummies

A beginner tutorial for a **paper-only** trading agent on Liquid. You paste a rulebook. A small Python runner hands that rulebook to a model on a schedule. The model looks, sizes, and places **paper** orders.

This repo cannot turn live trading on. The runner refuses `--live`.

## START HERE

You need three things:

1. Python 3.10 or newer.
2. An API key from Anthropic, OpenAI, or xAI.
3. A Liquid connector, started in **paper** mode. Setup notes are in [setup/00-connectors.md](setup/00-connectors.md).

Paste this:

```bash
git clone https://github.com/merjua14/Agentic-Trading-For-Dummies
cd Agentic-Trading-For-Dummies/runner
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

On Windows PowerShell, use `py -m venv .venv` and `.venv\Scripts\Activate.ps1` instead of the `source` line.

Open `.env`. Fill in your key, the Liquid URL, and the Liquid token. Leave every other line alone.

Then run:

```bash
python runner.py --check
python runner.py --live
python runner.py
```

| Command | What you should see |
|---|---|
| `python runner.py --check` | `mode=paper`, `riskFrac=0.015`, both halts `on` |
| `python runner.py --live` | The word `REFUSED`, then the program stops. Nothing is sent. |
| `python runner.py` | One paper run. |

If `--live` does anything other than refuse, stop. Do not continue.

Five words, once:

| Word | Meaning |
|---|---|
| Paper | Simulated. Not real money. |
| Equity | Account value. |
| Stop | The price that exits a bad trade. |
| Halt | A brake that shrinks or blocks new trades after a drop. |
| riskFrac | The slice of equity one trade is allowed to lose if the stop is hit. |

## Defaults that ship in this repo

| Knob | Setting |
|---|---|
| Paper | **ON** |
| riskFrac | **1.5%** (`0.015`) |
| Soft halt | **ON** (20% below the equity peak, new trades shrink to a quarter) |
| Hard halt | **ON** (35% below the equity peak, no new trades) |
| Leverage ceiling | **2** |
| `--live` | **Refused** |

Leave these alone until you have read [the rulebook](rulebook/liquid-v77-lite.txt) and [the disclaimer](DISCLAIMER.md).

## What each file is

```
README.md                      you are here
POST.md                        one X post, ready to paste
THREAD.md                      optional longer thread
DISCLAIMER.md                  read before you run anything
rulebook/liquid-v77-lite.txt   the instructions the model follows
runner/runner.py               the clock. It refuses --live
setup/                         connectors and Claude, ChatGPT, Grok, or the runner
docs/index.html                the same defaults, as a one-page configurator
assets/decision-flow.svg       the picture of the decision
assets/og.png                  share image
```

## The picture

![Decision flow: paper on, both halts on, a real stop, size at 1.5 percent, paper order only. Live is refused.](assets/decision-flow.svg)

## After the first paper run

Read the report. You want three things:

- It says paper mode is on.
- When it skips a trade, it names the one reason.
- Any paper position it opens has a stop, and it checked that the stop is actually there.

This tutorial still has no live switch. A real-money bot is a different project. It is not this repo.

## More, still plain

- [Connectors](setup/00-connectors.md)
- [Which app can schedule it](setup/PLATFORM-MATRIX.md)
- [The runner, step by step](setup/api-runner.md)
- [Claude](setup/claude.md) · [ChatGPT](setup/chatgpt.md) · [Grok](setup/grok.md)
- [Disclaimer](DISCLAIMER.md)
- [One-page configurator](docs/index.html)

Share link: https://github.com/merjua14/Agentic-Trading-For-Dummies

MIT license. Built by [@ITSJCMERLO](https://x.com/ITSJCMERLO).
