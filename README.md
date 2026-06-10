# Smart IVR & Customer Support Orchestrator

A production-grade, purely deterministic IVR routing engine for TelcoConnect built with Python 3.x and zero external dependencies.

## How to Run

```bash
python main.py
```

## How to Run Tests

```bash
python -m unittest discover -s tests -v
```

## Architecture

The system is built on three pillars, each implemented with a formal GoF design pattern:

| Pillar | Pattern | Location |
|---|---|---|
| A — Menu Routing | State Pattern | `engine/`, `states/` |
| B — Global Commands | Chain of Responsibility | `interceptors/` |
| C — Service Actions | Command Pattern | `commands/`, `services/` |

Cross-cutting audit logging uses the **Observer Pattern** via `audit/event_bus.py`.

State creation uses a **Registry-based Factory** (`factory/state_factory.py`) that is fully OCP-compliant — new states register themselves via `states/__init__.py` and `StateFactory` is never modified.

## Project Structure

```
IVR_Project_LLD/
├── main.py                    # Composition root
├── app/
│   └── application.py         # Main IVR loop
├── engine/
│   ├── state_base.py          # BaseState ABC
│   └── state_engine.py        # State Pattern Context
├── states/
│   ├── root_menu_state.py
│   ├── billing_state.py
│   └── tech_support_state.py
├── factory/
│   └── state_factory.py       # Registry-based Factory
├── interceptors/
│   ├── base_interceptor.py    # Chain of Responsibility ABC
│   ├── exit_interceptor.py
│   └── operator_interceptor.py
├── commands/
│   ├── base_command.py
│   ├── view_balance_command.py
│   ├── pay_bill_command.py
│   ├── run_diagnostic_command.py
│   └── reboot_router_command.py
├── services/
│   ├── base_billing_service.py    # DIP ABC
│   ├── base_diagnostic_service.py # DIP ABC
│   ├── billing_service.py
│   └── diagnostic_service.py
├── audit/
│   ├── event_bus.py           # Observer Pattern
│   ├── audit_event.py
│   ├── audit_formatter.py
│   └── audit_logger.py        # Dual-channel: SQLite + RotatingFileHandler
├── models/
│   ├── session.py
│   └── service_results.py
├── constants/
│   ├── messages.py
│   ├── choices.py             # Menu choice Enums
│   └── config.py
└── tests/
    ├── test_commands.py
    ├── test_services.py
    ├── test_interceptors.py
    ├── test_states.py
    └── test_audit.py
```

## Design Principles

- **SOLID** — OCP via registry factory, DIP via service ABCs, SRP throughout
- **No external libraries** — stdlib only (`abc`, `dataclasses`, `enum`, `sqlite3`, `logging`, `uuid`, `unittest`)
- **Fully deterministic** — all service responses are fixed mocks; no randomness or I/O beyond console
- **Dual-channel audit** — every user action, state transition, and service call is logged to both SQLite (`logs/ivr_audit.db`) and a rotating file (`logs/ivr_operational.log`)
- **70 unit tests** — all layers independently testable without mocking production code
