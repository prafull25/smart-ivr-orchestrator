from audit.audit_event import AuditEvent, EventType, Outcome
from constants.messages import PROMPT_CHOOSE
from engine.state_engine import StateEngine
from interceptors.base_interceptor import BaseInterceptor


class IVRApplication:
    def __init__(
        self,
        engine: StateEngine,
        interceptor_chain: BaseInterceptor,
    ) -> None:
        self._engine = engine
        self._interceptor_chain = interceptor_chain

    def run(self) -> None:
        while self._engine.is_running:
            self._engine.current_state.display()
            raw = input(PROMPT_CHOOSE).strip()

            self._engine.event_bus.emit(AuditEvent(
                session_id=self._engine.session.session_id,
                event_type=EventType.INPUT,
                outcome=Outcome.SUCCESS,
                state_name=self._engine.current_state.name,
                raw_input=raw,
            ))

            if self._interceptor_chain.intercept(raw, self._engine):
                continue

            next_state = self._engine.current_state.handle(raw, self._engine)

            if next_state is not self._engine.current_state:
                self._engine.transition_to(next_state)
