# A-Share Short-Term Quantitative Selection System

**English** | [简体中文](README.zh-CN.md)

A layered quantitative research project that pulls A-share daily bars via akshare, scores each
stock on short-term technicals, screens candidates, and backtests the resulting signals.

## Project Structure

```
量化分析/
├── data_layer/          # Data layer: market data fetching and local storage
├── strategy_layer/      # Strategy layer: scoring and signal logic
├── selection_layer/     # Selection layer: full-universe scan and ranking
├── backtest_layer/      # Backtest layer: single-stock and batch backtests
├── risk_layer/          # Risk layer: not implemented yet
├── database/            # SQLite database (stock.db)
└── .vscode/             # Editor configuration
```

## Requirements

- Python 3.11 (conda environment)
- `akshare`, `pandas`, `numpy`, `sqlalchemy`

## Data Preparation

All data lives in a single SQLite file:

| Table | Content |
| --- | --- |
| `stock_price` | Full-market spot snapshot (includes a `代码` / ticker column) |
| `kline_<code>` | Forward-adjusted daily bars, e.g. `kline_sz300368` |

Run in this order:

```bash
python data_layer/database_test.py         # spot snapshot -> stock_price
python data_layer/download_all_history.py  # batch daily bars (~0.2s per ticker)
python data_layer/show_tables.py           # verify: list all tables in the database
```

## Strategy

The core is `short_score(data)` in `strategy_layer/short_strategy.py`. It takes one stock's daily-bar
DataFrame (requires `close`, `high`, `low`, `volume`) and returns an integer score of 0–90. Fewer
than 30 bars returns 0 immediately.

| Factor | Condition | Score |
| --- | --- | --- |
| 5-day return | 3%–12% / 12%–20% / >20% | +15 / +10 / −10 |
| Moving averages | MA5 > MA10 > MA20 | +15 |
| Bias vs. MA20 | 0–10% / >20% | +10 / −10 |
| 10-day drawdown | −8%–−2% (pullback) / <−15% | +10 / −10 |
| Volume ratio (vs. 20-day avg) | 1.3–2.5 (healthy) / >4 (climax) | +20 / −15 |
| Candle strength | close in top 25% / bottom 25% of the day's range | +15 / −5 |
| RSI(14) | 45–70 / >80 | +10 / −10 |

Higher scores indicate healthier short-term price action. `selection_layer/stock_selector.py`
scores every `kline_*` table in the database and prints the top 20 by score.

## Backtesting

- Rule: buy at the close when score ≥ 80, sell at the close 5 trading days later; otherwise roll
  forward one day at a time.
- Capital: 10,000 CNY initial, fully invested and compounded. **Fees, stamp duty and slippage are
  not modelled.**
- Metrics: final capital, cumulative return, number of trades, win rate.
- Scripts: `backtest_layer/backtest.py` (single stock, parameters at the top of the file);
  `backtest_layer/all_stock_backtest.py` (batch; currently scans only the first 20 tables).

```bash
python backtest_layer/backtest.py
python backtest_layer/all_stock_backtest.py
```

## Known Limitations

1. `risk_layer/risk_control.py` is empty — position sizing and stop-loss are not implemented.
2. The database path is hard-coded as an absolute path in several scripts; moving or renaming the
   project directory requires updating them. A shared config module would be the cleaner fix.
3. Backtests treat each trade independently; capital occupancy and concurrent positions are not
   constrained.
4. `data_layer/ma_strategy.py` is an early moving-average experiment, unrelated to the current
   scoring framework.

## Disclaimer

This project is for quantitative method research and coding practice only. No score or backtest
result constitutes investment advice.
