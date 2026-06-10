from constants.messages import MSG_BALANCE, MSG_PAYMENT_SUCCESS
from models.service_results import BalanceResult, PaymentResult
from services.base_billing_service import BillingServiceABC


class BillingService(BillingServiceABC):
    _CURRENT_BALANCE: float = 150.00
    _POST_PAYMENT_BALANCE: float = 0.00

    def view_balance(self) -> BalanceResult:
        return BalanceResult(
            amount=self._CURRENT_BALANCE,
            message=MSG_BALANCE,
        )

    def pay_bill(self) -> PaymentResult:
        return PaymentResult(
            success=True,
            new_balance=self._POST_PAYMENT_BALANCE,
            message=MSG_PAYMENT_SUCCESS,
        )
