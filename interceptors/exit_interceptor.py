from audit.audit_event import AuditEvent, EventType, Outcome
from constants.messages import CMD_EXIT_MSG, SESSION_TERMINATED
from engine.state_engine import StateEngine
from interceptors.base_interceptor import BaseInterceptor


class ExitInterceptor(BaseInterceptor):
    _KEYWORD: str = "exit"

    def _matches(self, raw_input: str) -> bool:
        return raw_input.strip().lower() == self._KEYWORD

    def _execute(self, engine: StateEngine) -> None:
        engine.event_bus.emit(AuditEvent(
            session_id=engine.session.session_id,
            event_type=EventType.GLOBAL_CMD,
            outcome=Outcome.TERMINATED,
            raw_input=self._KEYWORD,
        ))
        print(CMD_EXIT_MSG)
        print(SESSION_TERMINATED)
        engine.terminate("EXIT_COMMAND")
