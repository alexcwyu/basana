# Basana

> **Last Updated**: 2026-04-06T16:25:30Z  \
> **Git Hash**: `2b49cd4`

**Async, event-driven framework for algorithmic trading with backtesting and live exchange support.**

| Field | Details |
|-------|---------|
| Language | Python (async/await) |
| License | Apache-2.0 |
| Author | Gabriel Martin Becedillas Ruiz |
| Package | `pip install basana` |
| Docs | [basana.readthedocs.io](https://basana.readthedocs.io/en/latest/) |
| GitHub | [gbeced/basana](https://github.com/gbeced/basana) |

## Overview

Basana is a Python async and event-driven framework for algorithmic trading with a focus on crypto currencies. It supports both backtesting and live trading at Binance and Bitstamp exchanges. The framework processes events in strict chronological order during backtesting, and as they arrive in real-time during live trading.

## Key Features

### Trading Capabilities
- Event-driven architecture with async/await throughout
- Backtesting with simulated order execution and configurable fees/liquidity
- Live trading on Binance (spot, margin, cross-margin, isolated-margin) and Bitstamp
- Market, Limit, and StopLimit order types
- Rate limiting via TokenBucketLimiter

### Architecture
- Core event dispatcher with backtesting and realtime variants
- Priority queue scheduler for time-ordered event processing
- EventSource/Producer pattern for data generation
- Unified exchange interface across backtesting and live trading
- Pluggable fee and liquidity models

### Supported Venues
- **Binance**: Spot, margin, cross-margin, isolated margin trading
- **Bitstamp**: Spot trading
- **Yahoo Finance**: Historical data (read-only)
- **CSV**: Custom data loading for backtesting

### Data Management
- WebSocket-based real-time data (order books, trades, user data)
- REST API for order submission and account queries
- Bar/candlestick event processing
- CSV data import for backtesting
- Historical data download tools

### Risk Management
- Configurable trading fee calculation
- Liquidity/slippage simulation in backtesting
- Account balance tracking (base, quote, borrowed amounts)
- Margin lending simulation

## Architecture Summary

```
EventDispatcher (BacktestingDispatcher / RealtimeDispatcher)
         |
    EventSource / Producer
         |
    Exchange (Backtesting / Binance / Bitstamp)
         |
    OrderManager / BalanceTracker
```

## Component Table

| Component | Location | Purpose |
|-----------|----------|---------|
| EventDispatcher | `src/basana/core/dispatcher.py` | Orchestrates event processing |
| BacktestingDispatcher | `src/basana/core/dispatcher.py` | Chronological event replay |
| RealtimeDispatcher | `src/basana/core/dispatcher.py` | Real-time event processing |
| Event/EventSource | `src/basana/core/event.py` | Base event abstractions |
| Bar/BarEvent | `src/basana/core/bar.py` | Candlestick events |
| TradingSignal | `src/basana/core/event_sources/trading_signal.py` | Signal generation |
| BacktestExchange | `src/basana/backtesting/exchange.py` | Simulated exchange |
| OrderManager | `src/basana/backtesting/order_mgr.py` | Order lifecycle management |
| AccountBalances | `src/basana/backtesting/account_balances.py` | Balance tracking |
| BinanceExchange | `src/basana/external/binance/exchange.py` | Binance integration |
| BitstampExchange | `src/basana/external/bitstamp/exchange.py` | Bitstamp integration |
| TokenBucketLimiter | `src/basana/core/token_bucket.py` | Rate limiting |

## Quick Start

This example runs a complete backtest with inline CSV data -- no API keys or external files needed.

```python
import asyncio
import csv
import io
import tempfile
from decimal import Decimal
from basana.core.pair import Pair, PairInfo
from basana.backtesting import exchange as backtesting_exchange
from basana.backtesting import fees
from basana.external.binance.csv import bars as binance_csv_bars
from basana.core import dispatcher

# 1. Create inline OHLCV CSV data
csv_data = """datetime,open,high,low,close,volume
2024-01-01 00:00:00,100,105,99,104,5000
2024-01-02 00:00:00,104,108,103,107,6000
2024-01-03 00:00:00,107,110,106,109,5500
2024-01-04 00:00:00,109,112,107,111,7000
2024-01-05 00:00:00,111,113,108,108,4500
2024-01-06 00:00:00,108,110,105,106,5200
2024-01-07 00:00:00,106,109,104,108,4800
2024-01-08 00:00:00,108,114,107,113,6500
2024-01-09 00:00:00,113,116,112,115,7200
2024-01-10 00:00:00,115,118,114,117,8000
"""
csv_path = tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False)
csv_path.write(csv_data)
csv_path.flush()

# 2. Set up backtesting exchange
pair = Pair("BTC", "USDT")
pair_info = {pair: PairInfo(base_precision=8, quote_precision=2)}

async def main():
    disp = dispatcher.BacktestingDispatcher()
    exchange = backtesting_exchange.Exchange(
        disp,
        initial_balances={"BTC": Decimal("0"), "USDT": Decimal("10000")},
        fee_strategy=fees.Percentage(Decimal("0.1")),  # 0.1% fee
    )

    # 3. Load CSV bar data
    exchange.add_bar_source(
        binance_csv_bars.BarSource(pair, csv_path.name, "1d")
    )

    # 4. Simple momentum strategy
    async def on_bar(event):
        bar = event.bar
        if bar.close > bar.open:  # Bullish bar
            balance = exchange.get_balance("USDT")
            if balance.available > Decimal("100"):
                size = (balance.available / bar.close).quantize(Decimal("0.001"))
                if size > Decimal("0"):
                    await exchange.create_market_order(pair, "buy", size)
                    print(f"{bar.datetime}: BUY {size} @ {bar.close}")

    exchange.subscribe_to_bar_events(pair, on_bar)

    # 5. Run backtest
    await disp.run()

    # 6. Print final balances
    for symbol in ["BTC", "USDT"]:
        bal = exchange.get_balance(symbol)
        print(f"{symbol}: {bal.available}")

asyncio.run(main())
```

## Links

- [Architecture](architecture.md) -- System design and component diagrams
- [Workflow](workflow.md) -- Event flows and key workflows
- [State Management](state-management.md) -- State machines and lifecycle
- [Development](development.md) -- Setup, standards, and strategy development
