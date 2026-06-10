from __future__ import annotations

from typing import Callable, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from engine.state_base import BaseState
    from services.base_billing_service import BillingServiceABC
    from services.base_diagnostic_service import DiagnosticServiceABC


class StateFactory:
    _registry: Dict[str, Callable] = {}

    @classmethod
    def register(cls, key: str, builder: Callable) -> None:
        cls._registry[key] = builder

    def __init__(
        self,
        billing_svc: BillingServiceABC,
        diagnostic_svc: DiagnosticServiceABC,
    ) -> None:
        self._billing_svc = billing_svc
        self._diagnostic_svc = diagnostic_svc

    def create(self, key: str) -> BaseState:
        if key not in self._registry:
            raise KeyError(f"No state registered for key: '{key}'")
        return self._registry[key](self._billing_svc, self._diagnostic_svc)
