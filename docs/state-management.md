# Basana -- State Management

## Event Dispatcher State Machine

```mermaid
stateDiagram-v2
    [*] --> Created: dispatcher()
    Created --> SourcesRegistered: add_source() / subscribe_to_*
    SourcesRegistered --> Running: await run()
    
    state Running {
        [*] --> CheckScheduler
        CheckScheduler --> ExecuteJob: Scheduled job ready
        CheckScheduler --> PopEvent: No jobs due
        ExecuteJob --> CheckScheduler
        PopEvent --> DispatchEvent: Event available
        PopEvent --> CheckIdle: No event
        DispatchEvent --> CheckScheduler
        CheckIdle --> ExecuteIdle: Idle handlers exist
        ExecuteIdle --> CheckScheduler
    }
    
    Running --> Stopped: No more events/jobs
    Running --> Stopped: Signal received (SIGINT/SIGTERM)
    Stopped --> [*]
```

## Backtesting vs Realtime Dispatcher

| Behavior | BacktestingDispatcher | RealtimeDispatcher |
|----------|----------------------|-------------------|
| Event ordering | Strict chronological | As they arrive |
| Time advancement | Jump to next event time | Real wall-clock time |
| Idle behavior | Skip (no waiting) | Execute idle handlers |
| Termination | All sources exhausted | Signal or manual stop |
| Scheduling | Simulated time | Real-time cron |

## Order State Machine

```mermaid
stateDiagram-v2
    [*] --> Accepted: create_*_order()
    
    state "Backtesting" as bt {
        Accepted --> Open: Order registered
        Open --> Filled: Bar price meets condition
        Open --> Cancelled: cancel_order()
    }
    
    state "Live Trading" as live {
        Accepted --> Pending: REST API submitted
        Pending --> Open: Exchange confirms
        Open --> PartiallyFilled: Partial execution
        PartiallyFilled --> Filled: Complete execution
        Open --> Filled: Full execution
        Open --> Cancelled: cancel_order()
        Pending --> Rejected: Exchange rejects
    }
    
    Filled --> [*]
    Cancelled --> [*]
    Rejected --> [*]
```

## Account Balance State

```mermaid
stateDiagram-v2
    [*] --> Initialized: Set initial balances
    
    state "Balance Tracking" as bt {
        [*] --> Available
        Available --> Reserved: Order placed (funds locked)
        Reserved --> Available: Order cancelled (funds released)
        Reserved --> Transferred: Order filled (funds moved)
        Transferred --> Available: New balance settled
    }
    
    state "Margin Tracking" as mt {
        [*] --> NoLoan
        NoLoan --> Borrowed: Insufficient balance + lending pool
        Borrowed --> AccruingInterest: Time passes
        AccruingInterest --> Repaid: Position closed
        Repaid --> NoLoan
    }
```

## Producer Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Created: Producer instantiated
    Created --> Initializing: dispatcher calls initialize()
    Initializing --> Active: Connections established
    
    state Active {
        [*] --> Producing
        Producing --> EventQueued: push_event()
        EventQueued --> Producing
    }
    
    Active --> Finalizing: dispatcher calls finalize()
    Finalizing --> Cleaned: Connections closed
    Cleaned --> [*]
```

Producers manage external resource lifecycles (WebSocket connections, file handles). The dispatcher calls `initialize()` before processing starts and `finalize()` after processing ends.

## SchedulerQueue

The scheduler uses a min-heap priority queue ordered by execution time:

```mermaid
graph TB
    subgraph "SchedulerQueue (Priority Queue)"
        direction TB
        J1["Job A: 10:00:00"]
        J2["Job B: 10:05:00"]
        J3["Job C: 10:10:00"]
        J4["Job D: 10:15:00"]
    end

    J1 --> J2
    J2 --> J3
    J3 --> J4
```

- `push(when, job)` -- Add job with execution time
- `peek_next_event_dt()` -- Check earliest pending job
- `pop()` -- Remove and return earliest job

All datetimes must be timezone-aware (enforced by assertion).

## WebSocket Connection State (Live Trading)

```mermaid
stateDiagram-v2
    [*] --> Disconnected
    Disconnected --> Connecting: Producer.initialize()
    Connecting --> Connected: WebSocket handshake
    Connected --> Subscribed: Subscribe to streams
    
    state Subscribed {
        [*] --> Receiving
        Receiving --> Processing: Message received
        Processing --> Receiving
    }
    
    Subscribed --> Reconnecting: Connection lost
    Reconnecting --> Connected: Reconnect success
    Reconnecting --> Failed: Max retries
    Subscribed --> Disconnected: Producer.finalize()
    Failed --> Disconnected
    Disconnected --> [*]
```

## Event Flow State

```mermaid
stateDiagram-v2
    [*] --> Produced: EventSource.pop() returns Event
    Produced --> Multiplexed: EventMultiplexer merges
    Multiplexed --> Queued: Added to dispatcher queue
    Queued --> Dispatched: Handler(s) called
    Dispatched --> Processed: All handlers complete
    Processed --> [*]
```

---
## See Also
- [README](README.md) — Project overview and quick start
- [Architecture](architecture.md) — System design and components
- [Workflow](workflow.md) — Event flows and processing pipelines
- [Development](development.md) — Development guide and best practices
