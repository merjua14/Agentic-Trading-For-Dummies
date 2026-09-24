# Claude

Use this if you want Claude to hold the rulebook. For a clock that refuses `--live` in code, use [the runner](api-runner.md) instead. The runner is the safer default.

## Paper, first

Connect Liquid. In the chat, before anything else:

```
enable_paper_trading
paper_trading_status
```

Stop if paper is not on.

## Paste the rulebook whole

Open [rulebook/liquid-v77-lite.txt](../rulebook/liquid-v77-lite.txt). Paste it as the task prompt. Do not ask Claude to shorten it.

Tell the task:

- Paper mode stays on.
- Do not call `disable_paper_trading`.
- Do not call `enable_automated_trading`.
- riskFrac stays 0.015. Both halts stay on.

## Schedule

An hourly cloud routine or scheduled task is enough. Set sub-ticks to 2 for the first day so you can read the report. Attach only the Liquid connector.

If the product offers an approval mode, pick the one that can run while you are away **only after** you have watched one paper report and it obeyed the halts.

## Do not

Do not type "go live", "disable paper", or "raise size." This page will not stop you. The runner will, which is why the runner is the path this tutorial stands behind.
