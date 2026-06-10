from abc import ABC, abstractmethod

from models.service_results import BalanceResult, PaymentResult


class BillingServiceABC(ABC):
    @abstractmethod
    def view_balance(self) -> BalanceResult: ...

    @abstractmethod
    def pay_bill(self) -> PaymentResult: ...
