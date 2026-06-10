import unittest
from unittest.mock import MagicMock

import states
from constants.messages import MSG_INVALID_OPTION
from services.billing_service import BillingService
from services.diagnostic_service import DiagnosticService
from states.billing_state import BillingState
from states.root_menu_state import RootMenuState
from states.tech_support_state import TechSupportState


def _make_engine():
    engine = MagicMock()
    engine.session.session_id = "test-sid"
    return engine


class TestRootMenuState(unittest.TestCase):
    def setUp(self):
        self.state = RootMenuState()
        self.engine = _make_engine()

    def test_name_is_root_menu(self):
        self.assertEqual(self.state.name, "RootMenu")

    def test_invalid_choice_returns_self(self):
        result = self.state.handle("9", self.engine)
        self.assertIs(result, self.state)

    def test_invalid_choice_does_not_call_factory(self):
        self.state.handle("9", self.engine)
        self.engine.state_factory.create.assert_not_called()

    def test_choice_1_creates_billing(self):
        self.state.handle("1", self.engine)
        self.engine.state_factory.create.assert_called_once_with("BILLING")

    def test_choice_2_creates_tech_support(self):
        self.state.handle("2", self.engine)
        self.engine.state_factory.create.assert_called_once_with("TECH_SUPPORT")

    def test_empty_input_returns_self(self):
        result = self.state.handle("", self.engine)
        self.assertIs(result, self.state)


class TestBillingState(unittest.TestCase):
    def setUp(self):
        self.state = BillingState(BillingService())
        self.engine = _make_engine()

    def test_name_is_billing(self):
        self.assertEqual(self.state.name, "Billing")

    def test_invalid_choice_returns_self(self):
        result = self.state.handle("9", self.engine)
        self.assertIs(result, self.state)

    def test_choice_1_view_balance_returns_self(self):
        result = self.state.handle("1", self.engine)
        self.assertIs(result, self.state)

    def test_choice_1_emits_audit_event(self):
        self.state.handle("1", self.engine)
        self.engine.event_bus.emit.assert_called()

    def test_choice_2_pay_bill_returns_self(self):
        result = self.state.handle("2", self.engine)
        self.assertIs(result, self.state)

    def test_choice_3_go_back_creates_root(self):
        self.state.handle("3", self.engine)
        self.engine.state_factory.create.assert_called_once_with("ROOT")


class TestTechSupportState(unittest.TestCase):
    def setUp(self):
        self.state = TechSupportState(DiagnosticService())
        self.engine = _make_engine()

    def test_name_is_tech_support(self):
        self.assertEqual(self.state.name, "TechSupport")

    def test_on_enter_runs_diagnostic_and_emits_event(self):
        self.state.on_enter(self.engine)
        self.engine.event_bus.emit.assert_called()

    def test_invalid_choice_returns_self(self):
        result = self.state.handle("9", self.engine)
        self.assertIs(result, self.state)

    def test_choice_1_reboot_returns_self(self):
        result = self.state.handle("1", self.engine)
        self.assertIs(result, self.state)

    def test_choice_1_emits_audit_event(self):
        self.state.handle("1", self.engine)
        self.engine.event_bus.emit.assert_called()

    def test_choice_2_go_back_creates_root(self):
        self.state.handle("2", self.engine)
        self.engine.state_factory.create.assert_called_once_with("ROOT")


if __name__ == "__main__":
    unittest.main()
