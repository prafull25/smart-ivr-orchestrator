from typing import Callable, List

from audit.audit_event import AuditEvent


class EventBus:
    def __init__(self) -> None:
        self._subscribers: List[Callable[[AuditEvent], None]] = []

    def subscribe(self, handler: Callable[[AuditEvent], None]) -> None:
        self._subscribers.append(handler)

    def emit(self, event: AuditEvent) -> None:
        for handler in self._subscribers:
            handler(event)
