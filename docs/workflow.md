# Basana -- Workflow

## Backtesting Workflow

```mermaid
sequenceDiagram
    participant U as User Code
    participant D as BacktestingDispatcher
    participant E as BacktestExchange
    participant OM as OrderManager
    participant AB as AccountBalances

    U->>D: backtesting_dispatcher()
    U->>E: Exchange(dispatcher, initial_balances)
    U->>E: subscribe_to_bar_events(pair, on_bar)
    U->>D: await run()

    loop Chronological event processing
        D->>D: Pop next event from priority queue
        D->>E: Dispatch bar event
        E->>OM: Evaluate pending orders against bar
        OM->>AB: Update balances on fills
        E->>U: on_bar_event(event)
        U->>E: create_market_order(pair, amount)
        E->>OM: Queue new order
    end

    D->>U: Run complete (no more events)
```

## Live Trading Workflow (Binance)

```mermaid
sequenceDiagram
    participant U as User Code
    participant D as RealtimeDispatcher
    participant E as BinanceExchange
    participant WS as WebSocket
    participant API as REST API
    participant RL as RateLimiter

    U->>D: realtime_dispatcher()
    U->>E: Exchange(dispatcher, config)
    U->>E: subscribe_to_bar_events(pair, on_bar)
    U->>D: await run()

    E->>WS: Connect to kline stream
    E->>WS: Connect to user data stream

    loop Real-time event processing
        WS-->>E: Kline/bar data
        E->>U: on_bar_event(event)
        U->>RL: Check rate limit
        RL-->>U: Token available
        U->>API: Submit order
        API-->>E: Order confirmation
        WS-->>E: Order update
        E->>U: on_order_event(event)
    end
```

## Event Processing Pipeline

```mermaid
graph LR
    subgraph "Sources"
        S1[CSV BarSource]
        S2[WebSocket Trades]
        S3[WebSocket OrderBook]
        S4[Scheduled Jobs]
    end

    subgraph "Multiplexer"
        EM[EventMultiplexer<br/>Merge by timestamp]
    end

    subgraph "Dispatcher"
        PQ[Priority Queue<br/>SchedulerQueue]
        EH[Event Handlers]
    end

    subgraph "Strategy"
        CB[User Callbacks]
        OE[Order Execution]
    end

    S1 --> EM
    S2 --> EM
    S3 --> EM
    S4 --> PQ
    EM --> PQ
    PQ --> EH
    EH --> CB
    CB --> OE
```

## Order Lifecycle

```mermaid
sequenceDiagram
    participant U as Strategy
    participant E as Exchange
    participant OM as OrderManager
    participant AB as AccountBalances

    U->>E: create_limit_order(pair, operation, amount, price)
    E->>OM: Register order
    OM->>AB: Reserve funds (quote for buy, base for sell)

    loop On each bar event
        OM->>OM: Check if price meets order conditions
        alt Order can be filled
            OM->>AB: Transfer funds
            OM->>E: Emit OrderEvent (filled)
            E->>U: on_order_event callback
        else Price not met
            Note over OM: Order remains open
        end
    end

    opt User cancels
        U->>E: cancel_order(order_id)
        E->>OM: Cancel order
        OM->>AB: Release reserved funds
        OM->>E: Emit OrderEvent (cancelled)
    end
```

## Margin Trading Flow

```mermaid
sequenceDiagram
    participant U as Strategy
    participant E as Exchange
    participant LM as LoanManager
    participant AB as AccountBalances

    U->>E: create_market_order(pair, BUY, amount)
    E->>AB: Check available balance
    
    alt Insufficient balance
        E->>LM: Request loan from lending pool
        LM->>LM: Check available lending
        LM->>AB: Credit borrowed amount
    end
    
    E->>AB: Execute trade (deduct quote, add base)
    
    Note over LM: Interest accrues over time
    
    U->>E: create_market_order(pair, SELL, amount)
    E->>AB: Execute trade (deduct base, add quote)
    E->>LM: Repay loan + interest
    LM->>AB: Debit repayment
```

## Historical Data Download

```bash
# Download Binance bars
python -m basana.external.binance.tools.download_bars \
  -c BTC/USDT -p 1h -s 2024-01-01 -e 2024-01-31 -o data.csv

# Download Bitstamp bars
python -m basana.external.bitstamp.tools.download_bars \
  -c BTC/USD -p 1h -s 2024-01-01 -e 2024-01-31 -o data.csv
```

---
## See Also
- [README](README.md) — Project overview and quick start
- [Architecture](architecture.md) — System design and components
- [State Management](state-management.md) — State lifecycle and data models
- [Development](development.md) — Development guide and best practices
