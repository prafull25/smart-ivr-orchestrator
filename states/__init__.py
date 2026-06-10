from states.root_menu_state import RootMenuState
from states.billing_state import BillingState
from states.tech_support_state import TechSupportState
from factory.state_factory import StateFactory

StateFactory.register("ROOT",         lambda b, d: RootMenuState())
StateFactory.register("BILLING",      lambda b, d: BillingState(b))
StateFactory.register("TECH_SUPPORT", lambda b, d: TechSupportState(d))

__all__ = ["RootMenuState", "BillingState", "TechSupportState"]
