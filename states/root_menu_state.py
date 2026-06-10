from __future__ import annotations

from typing import Dict, TYPE_CHECKING

from constants.choices import RootMenuChoice
from constants.messages import MENU_ROOT_HEADER, MSG_INVALID_OPTION
from engine.state_base import BaseState

if TYPE_CHECKING:
    from engine.state_engine import StateEngine


class RootMenuState(BaseState):
    _DESTINATIONS: Dict[RootMenuChoice, str] = {
        RootMenuChoice.BILLING: "BILLING",
        RootMenuChoice.TECH_SUPPORT: "TECH_SUPPORT",
    }

    @property
    def name(self) -> str:
        return "RootMenu"

    def display(self) -> None:
        print(f"\n{MENU_ROOT_HEADER}")
        print("1. Billing & Accounts")
        print("2. Technical Support")

    def handle(self, choice: str, engine: StateEngine) -> BaseState:
        try:
            option = RootMenuChoice(choice)
        except ValueError:
            print(MSG_INVALID_OPTION)
            return self

        return engine.state_factory.create(self._DESTINATIONS[option])
