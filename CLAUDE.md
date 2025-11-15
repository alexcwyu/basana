# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Basana is a Python **async and event-driven** framework for **algorithmic trading**, with a focus on crypto currencies. It supports both backtesting and live trading at Binance and Bitstamp exchanges.

**Key Characteristics:**
- ~22,000 lines of Python code
- Async/await throughout (asyncio-based)
- Event-driven architecture with time-ordered event processing
- 100% test coverage requirement enforced

## Development Commands

### Environment Setup

**Using uv (recommended):**
```bash
uv sync --all-extras
```

**Using Invoke (alternative):**
```bash
inv create-virtualenv
```

### Testing

**Run all tests:**
```bash
uv run pytest -vv --cov --cov-config=setup.cfg --durations=10
```

**Run a single test file:**
```bash
uv run pytest tests/test_specific_file.py -vv
```

**Run a single test:**
```bash
uv run pytest tests/test_file.py::test_function_name -vv
```

**With HTML coverage report:**
```bash
inv test --html-report
# Opens coverage report in cov_html/
```

### Static Analysis

**Type checking:**
```bash
uv run mypy basana
```

**Linting:**
```bash
uv run ruff check
```

**Combined lint + test:**
```bash
inv test
```

### Documentation

```bash
inv build-docs
# Output in docs/_build/html/
```

### Cleanup

```bash
inv clean
```

## Architecture

### Event-Driven Core

The framework is built around three fundamental concepts:

1. **Events** (`basana.core.event.Event`) - Something that occurs at a specific point in time (order book update, trade, bar, etc.). All events have a `when` attribute (timezone-aware datetime).

2. **EventSource** (`basana.core.event.EventSource`) - Abstract interface that provides events to the dispatcher. Event sources can optionally have a `Producer` that actively generates events.

3. **EventDispatcher** (`basana.core.dispatcher.EventDispatcher`) - Orchestrates event processing:
   - `BacktestingDispatcher` - Processes events in chronological order from historical data
   - `RealtimeDispatcher` - Processes events as they arrive in real-time

**Key architectural patterns:**
- Event sources are passive interfaces; producers are active event generators
- Events are processed in strict chronological order during backtesting
- The dispatcher uses an `EventMultiplexer` to merge events from multiple sources
- A `SchedulerQueue` (priority queue) manages scheduled jobs by execution time

### Module Structure

```
basana/
├── core/                      # Core event-driven framework
│   ├── dispatcher.py         # Event dispatchers (backtesting & realtime)
│   ├── event.py              # Event, EventSource, Producer base classes
│   ├── bar.py                # Bar/candlestick events
│   ├── helpers.py            # Decimal rounding/truncation utilities
│   ├── token_bucket.py       # Rate limiting
│   └── event_sources/        # Built-in event sources
│
├── backtesting/              # Backtesting exchange simulation
│   ├── exchange.py           # Simulated exchange (fills orders, manages balances)
│   ├── orders.py             # Order types (Market, Limit, StopLimit)
│   ├── order_mgr.py          # Order lifecycle management
│   ├── account_balances.py   # Balance tracking
│   ├── fees.py               # Trading fee calculation
│   ├── liquidity.py          # Liquidity/slippage simulation
│   ├── charts.py             # Plotly-based visualization
│   └── lending/              # Margin lending simulation
│
└── external/                 # Exchange integrations
    ├── binance/              # Binance exchange
    │   ├── exchange.py       # Main exchange interface
    │   ├── spot.py           # Spot trading
    │   ├── margin.py         # Margin trading
    │   ├── isolated_margin.py
    │   ├── cross_margin.py
    │   ├── order_book.py     # Order book management
    │   ├── websockets.py     # WebSocket streams
    │   ├── client/           # REST API client
    │   └── tools/            # CLI tools (download_bars, etc.)
    │
    ├── bitstamp/             # Bitstamp exchange
    │   ├── exchange.py
    │   ├── client.py
    │   └── tools/
    │
    ├── yahoo/                # Yahoo Finance data
    └── common/               # Shared utilities (CSV parsing, etc.)
```

### Exchange Abstractions

**Backtesting Exchange** (`basana.backtesting.exchange.Exchange`):
- Simulates order execution using bar data
- Manages account balances (base and quote currencies)
- Supports margin trading with lending pools
- Configurable fees and liquidity models

**Live Exchanges** (`basana.external.{binance,bitstamp}.exchange.Exchange`):
- Unified interface across exchanges
- WebSocket-based real-time data (order books, trades, user data)
- REST API for order submission and account queries
- Rate limiting via `TokenBucketLimiter`

### Order Types and Execution

All exchanges support:
- **Market Orders** - Immediate execution at best available price
- **Limit Orders** - Execute only at specified price or better
- **Stop Limit Orders** - Limit order triggered when stop price is reached

Order lifecycle managed by `OrderManager` (backtesting) or exchange-specific managers (live trading).

## Testing Standards

- **Coverage requirement:** 100% (enforced in `setup.cfg`)
- Use `pytest` fixtures for common test setup
- Mock external APIs using `aioresponses` for HTTP and `pytest-mock` for WebSockets
- Test data in `tests/data/` and `tests/fixtures/`
- Backtesting test data generation: `tests/backtesting_exchange_orders_test_data.py`

## Code Style

- **Line length:** 120 characters (configured in `pyproject.toml`)
- **Linter:** Ruff (replaces flake8)
- **Type hints:** Required, validated with mypy
- **Async/await:** All I/O operations must be async
- **Timezone awareness:** All datetimes must have timezone info (use `basana.core.dt` utilities)

## Common Patterns

### Running a Backtest

```python
from basana import backtesting_dispatcher
from basana.backtesting import exchange

# 1. Create dispatcher
dispatcher = backtesting_dispatcher()

# 2. Create exchange with bar sources
exch = exchange.Exchange(dispatcher, ...)

# 3. Subscribe to events and implement strategy
exch.subscribe_to_bar_events(..., on_bar_event)

# 4. Run
await dispatcher.run()
```

### Downloading Historical Data

```bash
python -m basana.external.binance.tools.download_bars \
  -c BTC/USDT \
  -p 1h \
  -s 2024-01-01 \
  -e 2024-01-31 \
  -o data.csv
```

### Implementing a Custom EventSource

1. Extend `basana.core.event.EventSource`
2. Implement `pop()` to return next event (or None)
3. Optionally implement `Producer` for active data generation
4. Register with dispatcher via `add_source()` or through a producer

## Important Notes

- All datetime objects **must** have timezone information (enforced via assertions)
- Event processing in backtesting is strictly chronological
- WebSocket connections require proper lifecycle management (initialize/finalize in Producer)
- Rate limits are enforced via `TokenBucketLimiter` for live exchanges
- Margin trading requires careful balance management (base, quote, and borrowed amounts)

## Dependencies

**Core:**
- Python 3.13+
- aiohttp (with speedups)
- python-dateutil

**Optional:**
- plotly + kaleido (for charts)
- talipp (technical indicators, used in examples)
- textual (TUI, used in order book mirror example)

**Development:**
- uv (dependency management)
- pytest + pytest-cov + pytest-mock
- mypy (type checking)
- ruff (linting)
- Invoke (optional task runner)

## Documentation

- **Online:** https://basana.readthedocs.io/en/latest/
- **Build locally:** `inv build-docs` → `docs/_build/html/index.html`
- **Examples:** See `samples/` directory (pairs trading, RSI, SMA, order book mirroring, etc.)
