from abc import ABC, abstractmethod
from typing import Any


class BaseCommand(ABC):
    @abstractmethod
    def execute(self) -> Any: ...
