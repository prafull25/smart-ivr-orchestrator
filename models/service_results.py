from dataclasses import dataclass


@dataclass(frozen=True)
class BalanceResult:
    amount: float
    message: str


@dataclass(frozen=True)
class PaymentResult:
    success: bool
    new_balance: float
    message: str


@dataclass(frozen=True)
class DiagnosticResult:
    device_status: str
    message: str


@dataclass(frozen=True)
class RebootResult:
    success: bool
    message: str
