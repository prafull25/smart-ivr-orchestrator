from commands.base_command import BaseCommand
from models.service_results import PaymentResult
from services.base_billing_service import BillingServiceABC


class PayBillCommand(BaseCommand):
    def __init__(self, billing_svc: BillingServiceABC) -> None:
        self._billing_svc = billing_svc

    def execute(self) -> PaymentResult:
        return self._billing_svc.pay_bill()
