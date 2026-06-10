from __future__ import annotations

from typing import TYPE_CHECKING

from audit.audit_event import AuditEvent, EventType, Outcome
from audit.event_bus import EventBus
from models.session import Session

if TYPE_CHECKING:
    from engine.state_base import BaseState
    from factory.state_factory import StateFactory


class StateEngine:
    def __init__(
        self,
        initial_state: BaseState,
        session: Session,
        event_bus: EventBus,
        state_factory: StateFactory,
    ) -> None:
        self._current_state: BaseState = initial_state
        self._session = session
        self._event_bus = event_bus
        self._state_factory = state_factory
        self._running: bool = True

    @property
    def current_state(self) -> BaseState:
        return self._current_state

    @property
    def is_running(self) -> bool:
        return self._running

    @property
    def session(self) -> Session:
        return self._session

    @property
    def event_bus(self) -> EventBus:
        return self._event_bus

    @property
    def state_factory(self) -> StateFactory:
        return self._state_factory

    def transition_to(self, new_state: BaseState) -> None:
        self._event_bus.emit(AuditEvent(
            session_id=self._session.session_id,
            event_type=EventType.TRANSITION,
            outcome=Outcome.SUCCESS,
            state_name=f"{self._current_state.name} -> {new_state.name}",
        ))
        self._current_state = new_state
        self._current_state.on_enter(self)

    def terminate(self, reason: str) -> None:
        self._event_bus.emit(AuditEvent(
            session_id=self._session.session_id,
            event_type=EventType.SESSION_END,
            outcome=Outcome.TERMINATED,
            details=reason,
        ))
        self._session.is_active = False
        self._running = False

    def escalate(self) -> None:
        self._event_bus.emit(AuditEvent(
            session_id=self._session.session_id,
            event_type=EventType.SESSION_END,
            outcome=Outcome.ESCALATED,
            details="OPERATOR_ESCALATION",
        ))
        self._session.is_active = False
        self._running = False
