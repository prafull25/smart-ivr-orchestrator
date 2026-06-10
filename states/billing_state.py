from __future__ import annotations

from typing import TYPE_CHECKING

from audit.audit_event import AuditEvent, EventType, Outcome
from commands.pay_bill_command import PayBillCommand
from commands.view_balance_command import ViewBalanceCommand
from constants.choices import BillingChoice
from constants.messages import MENU_BILLING_HEADER, MSG_INVALID_OPTION
from engine.state_base import BaseState
from services.base_billing_service import BillingServiceABC

if TYPE_CHECKING:
    from engine.state_engine import StateEngine


class BillingState(BaseState):
    def __init__(self, billing_svc: BillingServiceABC) -> None:
        self._billing_svc = billing_svc

    @property
    def name(self) -> str:
        return "Billing"

    def display(self) -> None:
        print(f"\n{MENU_BILLING_HEADER}")
        print("1. View Balance")
        print("2. Pay Bill")
        print("3. Go Back")

    def handle(self, choice: str, engine: StateEngine) -> BaseState:
        try:
            option = BillingChoice(choice)
        except ValueError:
            print(MSG_INVALID_OPTION)
            return self

        if option == BillingChoice.VIEW_BALANCE:
            result = ViewBalanceCommand(self._billing_svc).execute()
            print(result.message)
            engine.event_bus.emit(AuditEvent(
                session_id=engine.session.session_id,
                event_type=EventType.SERVICE_CALL,
                outcome=Outcome.SUCCESS,
                state_name=self.name,
                details="billing.view_balance",
            ))
            return self

        if option == BillingChoice.PAY_BILL:
            result = PayBillCommand(self._billing_svc).execute()
            print(result.message)
            engine.event_bus.emit(AuditEvent(
                session_id=engine.session.session_id,
                event_type=EventType.SERVICE_CALL,
                outcome=Outcome.SUCCESS,
                state_name=self.name,
                details="billing.pay_bill",
            ))
            return self

        return engine.state_factory.create("ROOT")


