# Basana -- Development Guide

## Setup

### Using uv (recommended)

```bash
uv sync --all-extras
```

### Using Invoke

```bash
inv create-virtualenv
```

## Testing

```bash
# Run all tests with coverage
uv run pytest -vv --cov --cov-config=setup.cfg --durations=10

# Run specific test file
uv run pytest tests/test_specific_file.py -vv

# Run specific test
uv run pytest tests/test_file.py::test_function_name -vv

# With HTML coverage report
inv test --html-report
```

Coverage requirement: **100%** (enforced in `setup.cfg`).

## Static Analysis

```bash
# Type checking
uv run mypy basana

# Linting
uv run ruff check

# Combined lint + test
inv test
```

## Code Standards

- **Line length**: 120 characters
- **Linter**: Ruff
- **Type hints**: Required, validated with mypy
- **Async/await**: All I/O operations must be async
- **Timezone awareness**: All datetimes must have timezone info
- **Python version**: 3.13+

## Building a Backtest Strategy

```python
import asyncio
from decimal import Decimal
from basana.backtesting import exchange as backtesting_exchange
from basana.external.common.csv import bars as csv_bars
from basana import backtesting_dispatcher, Pair

async def on_bar_event(event):
    # Strategy logic here
    if event.bar.close > event.bar.open:
        await exchange.create_market_order(
            Pair("BTC", "USDT"),
            basana.OrderOperation.BUY,
            Decimal("0.001")
        )

async def main():
    dispatcher = backtesting_dispatcher()
    
    pair = Pair("BTC", "USDT")
    exchange = backtesting_exchange.Exchange(
        dispatcher,
        {pair: backtesting_exchange.PairInfo(Decimal("0.001"), Decimal("0.01"))},
        initial_balances={"USDT": Decimal("10000")},
    )
    
    # Load CSV data
    exchange.add_bar_source(
        csv_bars.BarSource(pair, "btc_usdt_1h.csv", "1h")
    )
    
    exchange.subscribe_to_bar_events(pair, on_bar_event)
    
    await dispatcher.run()

asyncio.run(main())
```

## Live Trading with Binance

```python
import asyncio
from decimal import Decimal
from basana import realtime_dispatcher, Pair
from basana.external.binance import exchange as binance_exchange, config

async def on_bar_event(event):
    # Strategy logic
    pass

async def main():
    dispatcher = realtime_dispatcher()
    
    exchange = binance_exchange.Exchange(
        dispatcher,
        config.Defaults(api_key="...", api_secret="...")
    )
    
    pair = Pair("BTC", "USDT")
    exchange.subscribe_to_bar_events(pair, "1h", on_bar_event)
    
    await dispatcher.run()

asyncio.run(main())
```

## Implementing a Custom EventSource

```python
from basana.core import event

class MyEvent(event.Event):
    def __init__(self, when, data):
        super().__init__(when)
        self.data = data

class MySource(event.EventSource):
    def __init__(self):
        super().__init__()
        self._events = []
    
    def push(self, event):
        self._events.append(event)
    
    def pop(self):
        if self._events:
            return self._events.pop(0)
        return None
```

## Implementing a Custom Producer

```python
from basana.core import event

class MyProducer(event.Producer):
    def __init__(self, source):
        super().__init__()
        self._source = source
    
    async def initialize(self):
        # Open connections, load data
        pass
    
    async def finalize(self):
        # Clean up connections
        pass
    
    async def main(self):
        # Active data generation loop
        while True:
            data = await self.fetch_data()
            self._source.push(MyEvent(basana.utc_now(), data))
```

## Downloading Historical Data

```bash
# Binance
python -m basana.external.binance.tools.download_bars \
  -c BTC/USDT -p 1h -s 2024-01-01 -e 2024-01-31 -o data.csv

# Bitstamp
python -m basana.external.bitstamp.tools.download_bars \
  -c BTC/USD -p 1h -s 2024-01-01 -e 2024-01-31 -o data.csv
```

## Configuring Backtesting

### Custom Fees

```python
from basana.backtesting import fees

exchange = backtesting_exchange.Exchange(
    dispatcher,
    pair_info,
    initial_balances=balances,
    fee_strategy=fees.Percentage(Decimal("0.001")),  # 0.1% fee
)
```

### Custom Liquidity Model

```python
from basana.backtesting import liquidity

exchange = backtesting_exchange.Exchange(
    dispatcher,
    pair_info,
    initial_balances=balances,
    liquidity_strategy=liquidity.VolumeShareSlippage(
        volume_limit=Decimal("0.025"),
        price_impact=Decimal("0.1")
    ),
)
```

## Important Notes

- All datetime objects must have timezone information (use `basana.utc_now()`)
- Event processing in backtesting is strictly chronological
- WebSocket connections require proper lifecycle management via Producer
- Rate limits are enforced via `TokenBucketLimiter` for live exchanges
- Use `Decimal` for all monetary amounts (not float)

## Configuration Reference

### Exchange Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `dispatcher` | BacktestingDispatcher | -- | Event dispatcher instance (required) |
| `initial_balances` | dict[str, Decimal] | -- | Starting balances per currency, e.g. `{"USDT": Decimal("10000")}` |
| `fee_strategy` | FeeStrategy | `NoFee()` | Fee calculation strategy |
| `liquidity_strategy_factory` | callable | `InfiniteLiquidity` | Factory for per-pair liquidity model |

### PairInfo Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `base_precision` | int | -- | Decimal places for base currency amounts |
| `quote_precision` | int | -- | Decimal places for quote currency amounts |

### Fee Strategies (`basana.backtesting.fees`)

| Class | Parameters | Description |
|-------|------------|-------------|
| `NoFee` | -- | No fees applied (default) |
| `Percentage` | `percentage: Decimal`, `min_fee: Decimal = 0` | Fixed percentage fee in quote currency |

### Liquidity Strategies (`basana.backtesting.liquidity`)

| Class | Parameters | Description |
|-------|------------|-------------|
| `InfiniteLiquidity` | -- | No volume limit, no price impact (default) |
| `VolumeShareImpact` | `volume_limit_pct: Decimal = 25`, `price_impact: Decimal = 10` | Limits fill to percentage of bar volume; price impact scales quadratically with volume used |

### CSV BarSource Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `pair` | Pair | -- | Trading pair (e.g., `Pair("BTC", "USDT")`) |
| `csv_path` | str | -- | Path to CSV file with columns: `datetime,open,high,low,close,volume` |
| `period` | str | -- | Bar period: `"1m"`, `"1h"`, `"1d"` |
| `sort` | bool | `False` | Sort rows by datetime before processing |
| `tzinfo` | tzinfo | `UTC` | Timezone for datetime parsing |

### Dispatcher Settings

| Class | Description |
|-------|-------------|
| `BacktestingDispatcher` | Processes events in strict chronological order from historical data |
| `RealtimeDispatcher` | Processes events as they arrive; used for live trading |

## Troubleshooting

### `AssertionError: All datetimes must have timezone info`
Basana enforces timezone-aware datetimes everywhere. Use `datetime.timezone.utc` or `basana.core.dt` utilities. CSV data is parsed as UTC by default; pass `tzinfo` to `BarSource` if your data uses a different timezone.

### `decimal.InvalidOperation` or `Decimal` conversion errors
All monetary amounts must use `Decimal`, not `float`. Write `Decimal("0.001")` instead of `Decimal(0.001)` -- the string form avoids floating-point representation issues.

### Backtest produces no trades or events
Bars with zero volume are silently skipped by the CSV parser. Verify your CSV data has non-zero volume values. Also check that the `datetime` column format matches `%Y-%m-%d %H:%M:%S`.

### `Error: Not enough liquidity`
When using `VolumeShareImpact`, orders exceeding the `volume_limit_pct` of the bar's volume will be rejected. Reduce order size or increase `volume_limit_pct`. Switch to `InfiniteLiquidity` for testing without volume constraints.

### `RuntimeError: Event loop is already running`
This occurs when calling `asyncio.run()` inside Jupyter notebooks or another async context. Use `await dispatcher.run()` directly, or use `nest_asyncio` to patch the event loop: `import nest_asyncio; nest_asyncio.apply()`.

### Live exchange WebSocket disconnects
WebSocket connections can drop due to network issues or exchange maintenance. Implement reconnection logic in your `Producer.main()` loop with exponential backoff. Check `TokenBucketLimiter` configuration to avoid rate-limit bans.

### `ImportError: No module named 'basana.external.binance'`
Install with extras: `pip install basana[binance]` or `uv sync --all-extras`. The exchange integrations are optional dependencies.

### Orders not filling in backtesting
Limit orders only fill when the bar's price range covers the limit price. StopLimit orders require the stop price to be hit first. Check your order prices against the bar's high/low range.

## Security Considerations

- **API key management**: For live trading on Binance or Bitstamp, pass API keys via constructor parameters or environment variables. Never hardcode keys in source files. Use read-only keys for data-only access.
- **Rate limiting**: The `TokenBucketLimiter` enforces exchange rate limits to prevent IP bans. Do not bypass or increase rate limits beyond exchange-specified thresholds.
- **WebSocket TLS**: All live exchange connections use encrypted WebSocket (wss://) and HTTPS. The framework does not support unencrypted connections.
- **Decimal precision**: Using `Decimal` instead of `float` prevents rounding exploits and ensures order amounts match exchange expectations exactly. Always construct Decimals from strings.
- **Input validation**: CSV data loaded for backtesting is parsed but not sanitized. Ensure CSV files come from trusted sources. Malformed rows will raise parsing exceptions rather than silently corrupting data.
- **Dependency audit**: Review `aiohttp` and exchange client dependencies periodically. Pin versions in `uv.lock` to prevent supply-chain attacks via transitive dependencies.
- **Margin trading**: Margin/lending simulation in backtesting does not enforce real exchange margin rules. Do not use backtesting margin results to size live margin positions without additional validation.

---
## See Also
- [README](README.md) — Project overview and quick start
- [Architecture](architecture.md) — System design and components
- [Workflow](workflow.md) — Event flows and processing pipelines
- [State Management](state-management.md) — State lifecycle and data models
