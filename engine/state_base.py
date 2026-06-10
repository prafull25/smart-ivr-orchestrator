from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine.state_engine import StateEngine


class BaseState(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    def on_enter(self, engine: StateEngine) -> None:
        pass

    @abstractmethod
    def display(self) -> None: ...

    @abstractmethod
    def handle(self, choice: str, engine: StateEngine) -> BaseState: ...
