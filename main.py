
from datetime import datetime
from uuid import uuid4

import states

from app.application import IVRApplication
from models.session import Session
from audit.audit_logger import AuditLogger
from audit.event_bus import EventBus
from engine.state_engine import StateEngine
from factory.state_factory import StateFactory
from interceptors.exit_interceptor import ExitInterceptor
from interceptors.operator_interceptor import OperatorInterceptor
from services.base_billing_service import BillingServiceABC
from services.base_diagnostic_service import DiagnosticServiceABC
from services.billing_service import BillingService
from services.diagnostic_service import DiagnosticService


def main() -> None:
    session = Session(
        session_id=str(uuid4())[:8],
        start_time=datetime.now(),
    )

    event_bus = EventBus()
    audit_logger = AuditLogger(session_id=session.session_id)
    event_bus.subscribe(audit_logger.handle_event)

    billing_svc: BillingServiceABC = BillingService()
    diagnostic_svc: DiagnosticServiceABC = DiagnosticService()

    from services.service_container import ServiceContainer
    container = ServiceContainer()
    container.register("billing_svc", billing_svc)
    container.register("diagnostic_svc", diagnostic_svc)

    state_factory = StateFactory(container)
    initial_state = state_factory.create("ROOT")

    engine = StateEngine(
        initial_state=initial_state,
        session=session,
        event_bus=event_bus,
        state_factory=state_factory,
    )

    exit_interceptor = ExitInterceptor()
    operator_interceptor = OperatorInterceptor()
    exit_interceptor.set_next(operator_interceptor)

    app = IVRApplication(engine=engine, interceptor_chain=exit_interceptor)
    app.run()

    audit_logger.close()


if __name__ == "__main__":
    main()
