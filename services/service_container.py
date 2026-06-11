from typing import Any, Dict


class ServiceContainer:
    def __init__(self) -> None:
        self._services: Dict[str, Any] = {}

    def register(self, key: str, service: Any) -> None:
        self._services[key] = service

    def get(self, key: str) -> Any:
        if key not in self._services:
            raise KeyError(f"Service '{key}' not registered in ServiceContainer")
        return self._services[key]
