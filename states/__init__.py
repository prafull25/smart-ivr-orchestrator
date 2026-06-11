from states.root_menu_state import RootMenuState
from states.billing_state import BillingState
from states.tech_support_state import TechSupportState
from factory.state_factory import StateFactory

StateFactory.register("ROOT",         lambda c: RootMenuState())
StateFactory.register("BILLING",      lambda c: BillingState(c.get("billing_svc")))
StateFactory.register("TECH_SUPPORT", lambda c: TechSupportState(c.get("diagnostic_svc")))

__all__ = ["RootMenuState", "BillingState", "TechSupportState"]
