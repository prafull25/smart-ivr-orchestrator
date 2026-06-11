from __future__ import annotations

from typing import Callable, Dict

from engine.state_base import BaseState
from services.service_container import ServiceContainer


class StateFactory:
    _registry: Dict[str, Callable] = {}

    @classmethod
    def register(cls, key: str, builder: Callable) -> None:
        cls._registry[key] = builder

    def __init__(self, container: ServiceContainer) -> None:
        self._container = container

    def create(self, key: str) -> BaseState:
        if key not in self._registry:
            raise KeyError(f"No state registered for key: '{key}'")
        return self._registry[key](self._container)
