# Grok

Grok can call a custom connector, including inside an automation. The automation schedule is daily at the finest, which is a slow loop for this rulebook.

Use [the runner](api-runner.md) with `PROVIDER=xai` if you want the hourly paper clock. The runner refuses `--live`.

## If you want one manual look

1. Add the Liquid connector.
2. Send `enable_paper_trading`, then `paper_trading_status`.
3. Paste [the rulebook](../rulebook/liquid-v77-lite.txt).
4. Read the report. Paper on, both halts mentioned, a reason for every skip.

The xAI API does not have an approval switch you can lean on. The allow-list inside `runner.py` is the limit: paper tools only, no tool that turns paper off.
