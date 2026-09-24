# Rulebook changelog

## V7.7 LITE — beginner paper tutorial

Public tutorial cut. The shape follows a Liquid perps rulebook (two lanes, a resting stop, a small ladder, a ledger). The defaults do not.

**Locked on**

- Paper mode. The runner refuses `--live` and exits before any model or exchange call.
- `riskFrac: 0.015` (1.5 percent of equity if the stop is hit).
- Soft halt on at 20 percent below peak equity. New entries drop to a quarter of normal risk.
- Hard halt on at 35 percent below peak equity. No new entries.
- Leverage ceiling 2. No path in this file to raise it.
- Total notional cap 1.5 times equity. One new position at most 0.5 times equity. Lane B is half of that.

**Left out on purpose**

- A live trading mandate, and any instruction to renew one.
- Tools that turn paper mode off.
- Performance numbers, win rates, and example account sizes.
- A third entry lane and adding to winners.

This file describes rules for a paper exercise. It does not describe results.
