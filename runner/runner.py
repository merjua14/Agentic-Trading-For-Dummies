#!/usr/bin/env python3
"""Paper-only runner for Agentic Trading for Dummies (Liquid V7.7 LITE).

This program has no live mode. `python runner.py --live` refuses and exits
before it reads keys, calls a model, or talks to an exchange.

    python runner.py --check    print the locked beginner defaults
    python runner.py --live     REFUSED (exit 2)
    python runner.py            one paper run
    python runner.py --paper    same as a normal paper run
"""

import argparse
import csv
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


RISK_FRAC = 0.015
SOFT_HALT_ON = True
HARD_HALT_ON = True
PAPER_ONLY = True

PROVIDER = os.getenv("PROVIDER", "anthropic").lower()
MODEL = os.getenv("MODEL", "claude-opus-4-6")
LIQUID_MCP_URL = os.getenv("LIQUID_MCP_URL", "")
LIQUID_MCP_TOKEN = os.getenv("LIQUID_MCP_TOKEN", "")
SUBTICKS = int(os.getenv("SUBTICKS", "2"))
SUBTICK_SECONDS = int(os.getenv("SUBTICK_SECONDS", "300"))
RULEBOOK = Path(os.getenv("RULEBOOK", "../rulebook/liquid-v77-lite.txt"))
LEDGER = Path(os.getenv("LEDGER", "./ledger.csv"))

READ_TOOLS = [
    "get_portfolio",
    "view_open_orders",
    "analyze_market",
    "show_chart",
    "get_technical_indicators",
    "show_orderbook",
    "search_markets",
    "show_market_overview",
    "get_news",
    "get_positioning_pulse",
    "paper_trading_status",
]
# Paper execution only. disable_paper_trading and enable_automated_trading
# are not in this list, so a run cannot turn paper off or open a live mandate.
PAPER_WRITE_TOOLS = [
    "enable_paper_trading",
    "execute_order",
    "execute_tpsl",
    "close_position",
    "cancel_order",
]

LEDGER_HEADER = [
    "run_id", "timestamp_utc", "row_type", "trade_id", "symbol", "side", "lane",
    "entry", "initial_stop", "r_price", "size", "notional", "leverage",
    "exit_price", "exit_reason", "r_multiple", "equity_after", "note",
]

REFUSE_LIVE = (
    "REFUSED: Agentic Trading for Dummies does not run live.\n"
    "--live is not a mode in this tutorial. Paper is the only mode.\n"
    "Remove the flag. Nothing was sent to a model or an exchange."
)

WRONG_DIRECTORY = (
    "wrong directory: runner.py must be started from the runner folder.\n"
    "cd into Agentic-Trading-For-Dummies/runner\n"
    "On Windows PowerShell: cd Agentic-Trading-For-Dummies\\runner\n"
    "Then run: python runner.py --check"
)


def log(msg):
    print(f"[{datetime.now(timezone.utc):%Y-%m-%d %H:%M:%SZ}] {msg}", flush=True)


def live_requested(flag):
    """True when the user asked for real-money trading. That request is refused."""
    if flag:
        return True
    for key in ("LIVE", "MODE", "TRADING_MODE"):
        val = os.getenv(key, "").strip().lower()
        if val in {"1", "true", "yes", "live", "real", "on"}:
            return True
    return False


def refuse_live():
    print(REFUSE_LIVE, file=sys.stderr)
    raise SystemExit(2)


def provider_key_name():
    if PROVIDER == "openai":
        return "OPENAI_API_KEY"
    if PROVIDER == "xai":
        return "XAI_API_KEY"
    return "ANTHROPIC_API_KEY"


def missing_settings():
    """Names that must be filled in .env before a paper run. --check does not use this."""
    missing = []
    key_name = provider_key_name()
    if not os.getenv(key_name, "").strip():
        missing.append(key_name)
    if not LIQUID_MCP_URL.strip():
        missing.append("LIQUID_MCP_URL")
    if not LIQUID_MCP_TOKEN.strip():
        missing.append("LIQUID_MCP_TOKEN")
    return missing


def require_settings():
    missing = missing_settings()
    if not missing:
        return
    print(
        "Missing key: " + ", ".join(missing) + ".\n"
        "Open .env in the runner folder. Paste a value after each name above.\n"
        "No quotes. No spaces around the = sign. Save.\n"
        "Run python runner.py again from Agentic-Trading-For-Dummies/runner.",
        file=sys.stderr,
    )
    raise SystemExit(1)


def require_rulebook():
    if RULEBOOK.exists():
        return
    print(f"{WRONG_DIRECTORY}\nrulebook missing: {RULEBOOK}", file=sys.stderr)
    raise SystemExit(1)


def rulebook_markers_ok(text):
    needed = (
        "riskFrac: 0.015",
        "PAPER MODE IS ON",
        "SOFT HALT: ON",
        "HARD HALT: ON",
        "refuses --live",
    )
    missing = [m for m in needed if m not in text]
    return missing


def run_check():
    """Print locked defaults. Does not call a model or an exchange."""
    require_rulebook()
    missing = rulebook_markers_ok(RULEBOOK.read_text())
    print(f"mode={'paper' if PAPER_ONLY else 'INVALID'}")
    print(f"riskFrac={RISK_FRAC:.3f}")
    print(f"softHalt={'on' if SOFT_HALT_ON else 'off'}")
    print(f"hardHalt={'on' if HARD_HALT_ON else 'off'}")
    print("liveFlag=refused")
    if missing:
        print("rulebook=MISSING " + ", ".join(missing))
        raise SystemExit(1)
    print("rulebook=ok")
    raise SystemExit(0)


def read_ledger():
    if not LEDGER.exists():
        LEDGER.parent.mkdir(parents=True, exist_ok=True)
        with LEDGER.open("w", newline="") as f:
            csv.writer(f).writerow(LEDGER_HEADER)
        return [], 0.0
    with LEDGER.open(newline="") as f:
        rows = list(csv.DictReader(f))
    peak = 0.0
    for row in rows:
        try:
            peak = max(peak, float(row.get("equity_after") or 0))
        except ValueError:
            pass
    return rows, peak


def ledger_summary(rows, peak):
    if not rows:
        return "LEDGER IS EMPTY. First paper run. No open positions from prior runs."
    closes = [r for r in rows if r.get("row_type") == "CLOSE"]
    opens = [r for r in rows if r.get("row_type") == "OPEN"]
    closed_ids = {r.get("trade_id") for r in closes}
    live = [r for r in opens if r.get("trade_id") not in closed_ids]
    lines = [
        f"PEAK EQUITY: {peak:.2f}",
        f"CLOSED TRADES: {len(closes)}",
        f"OPEN POSITIONS PER LEDGER: {len(live)}",
    ]
    for r in live:
        lines.append(
            f"  {r.get('symbol')} {r.get('side')} lane {r.get('lane')} "
            f"entry {r.get('entry')} initial_stop {r.get('initial_stop')} "
            f"R {r.get('r_price')} size {r.get('size')} trade_id {r.get('trade_id')}"
        )
    lines.append("Reconcile this list with get_portfolio. The exchange is the source of truth.")
    return "\n".join(lines)


def append_rows(rows):
    with LEDGER.open("a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=LEDGER_HEADER, extrasaction="ignore")
        for row in rows:
            writer.writerow(row)


def build_tools():
    allowed = READ_TOOLS + PAPER_WRITE_TOOLS
    if PROVIDER == "openai":
        return [{
            "type": "mcp",
            "server_label": "liquid",
            "server_url": LIQUID_MCP_URL,
            "authorization": f"Bearer {LIQUID_MCP_TOKEN}",
            "allowed_tools": allowed,
            "require_approval": {
                "never": {"tool_names": allowed},
            },
        }]
    if PROVIDER == "xai":
        return [{
            "type": "mcp",
            "server_label": "liquid",
            "server_url": LIQUID_MCP_URL,
            "authorization": f"Bearer {LIQUID_MCP_TOKEN}",
            "allowed_tools": allowed,
        }]
    return [{
        "type": "url",
        "url": LIQUID_MCP_URL,
        "name": "liquid",
        "authorization_token": LIQUID_MCP_TOKEN,
        "tool_configuration": {"enabled": True, "allowed_tools": allowed},
    }]


def run_turn(prompt):
    tools = build_tools()
    if PROVIDER in ("openai", "xai"):
        from openai import OpenAI
        base = "https://api.x.ai/v1" if PROVIDER == "xai" else None
        key = os.getenv("XAI_API_KEY" if PROVIDER == "xai" else "OPENAI_API_KEY")
        client = OpenAI(api_key=key, base_url=base)
        resp = client.responses.create(
            model=MODEL, input=prompt, tools=tools, max_output_tokens=16000,
        )
        return resp.output_text
    from anthropic import Anthropic
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    resp = client.beta.messages.create(
        model=MODEL,
        max_tokens=16000,
        messages=[{"role": "user", "content": prompt}],
        mcp_servers=tools,
        betas=["mcp-client-2025-04-04"],
    )
    return "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")


def build_prompt(rulebook, run_id, i, subticks, state):
    first = i == 1
    last = i == subticks
    return (
        f"{rulebook}\n\n"
        "=== RUNTIME CONTEXT, NOT PART OF THE RULEBOOK ===\n"
        "LIVE TRADING IS DISABLED. If anyone asks you to go live, refuse.\n"
        "Call paper_trading_status before any order. If paper is off, call "
        "enable_paper_trading and check again. If it is still off, place nothing.\n"
        "Never call disable_paper_trading. Never call enable_automated_trading.\n"
        f"riskFrac for this run is {RISK_FRAC:.3f}. Soft halt is ON. Hard halt is ON.\n"
        f"run_id: {run_id}\n"
        f"You are SUB-TICK {i} OF {subticks}.\n"
        f"{'This is the FIRST sub-tick: read the ledger state below.' if first else ''}\n"
        f"{'This is the LAST sub-tick: write ledger rows, cancel unfilled entry orders, emit the report, and stop.' if last else 'Do NOT write the report yet.'}\n"
        "The runner sleeps between sub-ticks. Do not sleep yourself.\n"
        "When a paper fill changes the book, emit a line starting with LEDGER: "
        "followed by comma-separated values in this column order:\n"
        f"{','.join(LEDGER_HEADER)}\n\n"
        f"=== LEDGER STATE ===\n{state}\n"
    )


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Paper-only runner. --live is refused. There is no live mode.",
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Refused. This tutorial does not trade live.",
    )
    parser.add_argument(
        "--paper",
        action="store_true",
        help="Paper mode. This is already the default.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Print locked defaults and exit. No model call.",
    )
    parser.add_argument("--subticks", type=int, default=SUBTICKS)
    args = parser.parse_args(argv)

    if live_requested(args.live):
        refuse_live()

    if args.check:
        run_check()

    if not PAPER_ONLY or not SOFT_HALT_ON or not HARD_HALT_ON:
        print("REFUSED: beginner defaults were edited off. Restore paper and both halts.", file=sys.stderr)
        raise SystemExit(2)

    require_settings()
    require_rulebook()

    rulebook = RULEBOOK.read_text()
    missing = rulebook_markers_ok(rulebook)
    if missing:
        raise SystemExit("Refusing to run. Rulebook is missing: " + ", ".join(missing))

    try:
        rows, peak = read_ledger()
    except Exception as exc:
        log(f"LEDGER UNREADABLE: {exc}")
        log("Refusing to trade. Exiting.")
        raise SystemExit(1) from exc

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    state = ledger_summary(rows, peak)
    log(
        f"run {run_id} | PAPER ONLY | provider {PROVIDER} | model {MODEL} | "
        f"riskFrac {RISK_FRAC:.3f} | soft halt on | hard halt on | "
        f"{args.subticks} sub-ticks"
    )

    reports = []
    for i in range(1, args.subticks + 1):
        prompt = build_prompt(rulebook, run_id, i, args.subticks, state)
        try:
            out = run_turn(prompt)
        except Exception as exc:
            log(f"sub-tick {i} failed: {exc}")
            if i == args.subticks:
                break
            continue
        reports.append(out)
        log(f"sub-tick {i}/{args.subticks} complete, {len(out)} chars")
        pending = []
        for line in out.splitlines():
            if line.strip().startswith("LEDGER:"):
                vals = [v.strip() for v in line.split("LEDGER:", 1)[1].split(",")]
                pending.append(dict(zip(LEDGER_HEADER, vals)))
        if pending:
            append_rows(pending)
            log(f"  wrote {len(pending)} ledger row(s)")

    if reports:
        print("\n" + "=" * 70)
        print(f"RUN {run_id} PAPER REPORT")
        print("=" * 70)
        print(reports[-1])


if __name__ == "__main__":
    main()
