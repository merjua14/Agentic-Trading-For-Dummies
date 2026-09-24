# Which app can run this

You need three abilities: reach the Liquid connector, run on a schedule, and do that without a tap from you at each step. A terminal is useful and not required.

| App | Custom connector | Schedule | Unattended | Practical answer |
|---|---|---|---|---|
| Claude Code routines | yes | hourly | yes | Works, if you paste the rulebook whole |
| Claude scheduled tasks | yes | hourly | yes, if you skip approvals | Works |
| Claude in the browser | yes | no | you click allow | Manual practice only |
| ChatGPT scheduled tasks | maybe | hourly on paid plans | approvals reset | Use the runner instead |
| Grok automations | yes | daily at best | no approval gate | Use the runner instead |
| This repo's Python runner | yes | your cron | yes | The path this tutorial documents |

## ChatGPT

A scheduled chat is a new conversation. Write-action approvals usually reset. That means the 3am run waits for you. Use [the runner](api-runner.md).

## Grok

Connectors can run inside an automation. The schedule does not go hourly. Use [the runner](api-runner.md) if you want more than one look a day.

## Claude

Cloud routines and scheduled tasks can call tools without stopping to ask, once you choose that mode. Only attach the Liquid connector to a task you actually want placing **paper** orders. Paste [the rulebook](../rulebook/liquid-v77-lite.txt) as the prompt. Do not let the model rewrite it.

## All of them

Stay in paper. This tutorial's runner refuses `--live`. A chat window will not refuse a bad prompt you type yourself, so do not type one.
