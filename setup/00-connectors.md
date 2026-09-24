# Connectors

A connector is the link between this tutorial and an app.

You need one. It is Liquid, the exchange app, and you use it in **paper** mode. Paper means simulated, not real money.

## Where the URL and token go

Liquid shows you a connector URL and a token. Paste them into `runner/.env`:

```
LIQUID_MCP_URL=paste-the-url
LIQUID_MCP_TOKEN=paste-the-token
```

That file stays on your computer. The runner reads it. It does not turn live trading on.

| Connector | What it is for | Required |
|---|---|---|
| Liquid | Paper orders, stops, positions, charts | Yes |
| A ledger file | Memory between runs. The runner writes `ledger.csv` for you | Yes, and the runner already does this |
| Anything else | Optional second opinion. It must not invent trades | No |

## Liquid, in paper

In the Liquid connector, turn paper on:

```
enable_paper_trading
```

Check it:

```
paper_trading_status
```

You want paper **on** before the first run. The rulebook checks this again every run. If paper is off, it is not allowed to place an order.

Tools this tutorial uses:

```
Paper       enable_paper_trading, paper_trading_status
Account     get_portfolio, view_open_orders
Paper fills execute_order, execute_tpsl, close_position, cancel_order
Research    analyze_market, show_chart, get_technical_indicators, show_orderbook,
            search_markets, show_market_overview, get_news, get_positioning_pulse
```

Tools this tutorial does **not** use:

```
disable_paper_trading
enable_automated_trading
update_leverage
```

`show_market_overview` is a large payload. The rulebook tells the model to save it and parse it, not to read it raw.

Partial closes take size in coin units, not as a dollar amount.

## Optional second feeds

A news or options feed can confirm or veto a setup that already exists on the Liquid chart. If you do not have one, the model should say "Liquid data only" and keep going. Do not block the tutorial on extra feeds.

## The ledger

Each run starts blank. `runner/ledger.csv` is how the next run knows about open paper positions, peak equity, and the halts. Do not delete it mid-experiment unless you mean to forget the book. The file is gitignored.
