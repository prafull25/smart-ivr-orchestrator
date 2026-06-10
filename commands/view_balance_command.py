from commands.base_command import BaseCommand
from models.service_results import BalanceResult
from services.base_billing_service import BillingServiceABC


class ViewBalanceCommand(BaseCommand):
    def __init__(self, billing_svc: BillingServiceABC) -> None:
        self._billing_svc = billing_svc

    def execute(self) -> BalanceResult:
        return self._billing_svc.view_balance()
