from enum import Enum


class RootMenuChoice(str, Enum):
    BILLING = "1"
    TECH_SUPPORT = "2"


class BillingChoice(str, Enum):
    VIEW_BALANCE = "1"
    PAY_BILL = "2"
    GO_BACK = "3"


class TechSupportChoice(str, Enum):
    REBOOT_ROUTER = "1"
    GO_BACK = "2"
