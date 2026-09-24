1/ Agentic Trading for Dummies is a paper-first Liquid tutorial for people who have never run an agent.

https://github.com/merjua14/Agentic-Trading-For-Dummies

2/ You paste one rulebook. A small Python runner wakes a model, hands it that rulebook, and writes a ledger. The model does not invent the risk rules. They are already written down.

3/ The runner refuses --live. Pass that flag and it stops before it calls a model or an exchange. A normal run is paper. Paper is the only mode in this repo.

4/ Defaults in the box: riskFrac 1.5%, paper on, soft halt on, hard halt on. After a 20% drop from the peak, new trades shrink. After 35%, no new trades. Leverage stays capped at 2.

5/ Every paper entry needs a real invalidation level (the price that proves the idea wrong), a stop that is actually resting, and a size that comes from that 1.5% risk. No level, no trade.

6/ Nothing here promises a return. Perps (leveraged contracts) can wipe an account. This tutorial stays on paper so you can watch the loop before any of that is your money. Read DISCLAIMER.md.

https://github.com/merjua14/Agentic-Trading-For-Dummies
