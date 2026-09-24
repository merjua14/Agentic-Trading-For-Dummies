# ChatGPT

ChatGPT can hold a conversation with a connector. A scheduled task starts a fresh conversation, and write approvals usually do not carry over. The run will wait for a tap.

Use [the runner](api-runner.md) with `PROVIDER=openai`. That is the path this tutorial supports.

## If you still want to practice in chat

1. Connect Liquid in developer mode.
2. Send `enable_paper_trading`, then `paper_trading_status`.
3. Paste [the rulebook](../rulebook/liquid-v77-lite.txt).
4. Read one report. Check that it says paper, and that it names a reason when it skips.

Do not schedule that chat as if it were unattended. When it asks for approval, that is the product working as designed.

The runner refuses `--live`. A chat box does not. Do not ask it to.
