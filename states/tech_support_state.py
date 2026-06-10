from __future__ import annotations

from typing import TYPE_CHECKING

from audit.audit_event import AuditEvent, EventType, Outcome
from commands.reboot_router_command import RebootRouterCommand
from commands.run_diagnostic_command import RunDiagnosticCommand
from constants.choices import TechSupportChoice
from constants.messages import MENU_TECH_HEADER, MSG_INVALID_OPTION
from engine.state_base import BaseState
from services.base_diagnostic_service import DiagnosticServiceABC

if TYPE_CHECKING:
    from engine.state_engine import StateEngine


class TechSupportState(BaseState):
    def __init__(self, diagnostic_svc: DiagnosticServiceABC) -> None:
        self._diagnostic_svc = diagnostic_svc

    @property
    def name(self) -> str:
        return "TechSupport"

    def on_enter(self, engine: StateEngine) -> None:
        result = RunDiagnosticCommand(self._diagnostic_svc).execute()
        print(result.message)
        engine.event_bus.emit(AuditEvent(
            session_id=engine.session.session_id,
            event_type=EventType.SERVICE_CALL,
            outcome=Outcome.SUCCESS,
            state_name=self.name,
            details=f"diagnostic.run_diagnostic -> {result.device_status}",
        ))

    def display(self) -> None:
        print(f"\n{MENU_TECH_HEADER}")
        print("1. Reboot Router")
        print("2. Go Back")

    def handle(self, choice: str, engine: StateEngine) -> BaseState:
        try:
            option = TechSupportChoice(choice)
        except ValueError:
            print(MSG_INVALID_OPTION)
            return self

        if option == TechSupportChoice.REBOOT_ROUTER:
            result = RebootRouterCommand(self._diagnostic_svc).execute()
            print(result.message)
            engine.event_bus.emit(AuditEvent(
                session_id=engine.session.session_id,
                event_type=EventType.SERVICE_CALL,
                outcome=Outcome.SUCCESS,
                state_name=self.name,
                details="diagnostic.reboot",
            ))
            return self

        return engine.state_factory.create("ROOT")


