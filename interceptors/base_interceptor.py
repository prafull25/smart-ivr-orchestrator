from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from engine.state_engine import StateEngine


class BaseInterceptor(ABC):
    def __init__(self) -> None:
        self._next: Optional[BaseInterceptor] = None

    def set_next(self, interceptor: BaseInterceptor) -> BaseInterceptor:
        self._next = interceptor
        return interceptor

    def intercept(self, raw_input: str, engine: StateEngine) -> bool:
        if self._matches(raw_input):
            self._execute(engine)
            return True
        if self._next:
            return self._next.intercept(raw_input, engine)
        return False

    @abstractmethod
    def _matches(self, raw_input: str) -> bool: ...

    @abstractmethod
    def _execute(self, engine: StateEngine) -> None: ...
