# Read this before you run anything

**This is not financial advice.** Nothing in this repository is a recommendation to buy or sell anything. Nobody here is your broker, advisor, or fiduciary.

**The runner is paper-only.** `python runner.py --live` is refused. That refusal is a tutorial guard, not a promise that a model can never be pointed at a live account by some other program you write yourself.

**Perpetual futures are leveraged.** On a live account they can go to zero, and they can do it quickly. Liquidation is a real outcome. The stops and halts in the rulebook reduce how casually a paper agent adds risk. They do not remove risk, and they do not apply to money this repo never touches.

**There are no performance numbers in this tutorial.** No win rate, no expected return, no "typical week," no example account size. If a sentence sounds like a forecast, it does not belong here.

**An agent does what the file says, including a mistake in the file.** Read the rulebook. If a line is unclear, do not run it until it is clear.

**Paper first is the whole point.** `enable_paper_trading` on Liquid is the mode this tutorial knows how to use. Stay there.

**You are responsible for your own rules.** Whether you may use Liquid, perps, or an automated agent depends on where you live. Check that yourself.

**No warranty.** The rulebook and the runner are provided as-is under the MIT license. Models misread instructions. Exchange APIs change. If you later point some other system at real money, the loss is yours.
