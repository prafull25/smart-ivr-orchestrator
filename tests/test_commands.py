import unittest

from commands.pay_bill_command import PayBillCommand
from commands.reboot_router_command import RebootRouterCommand
from commands.run_diagnostic_command import RunDiagnosticCommand
from commands.view_balance_command import ViewBalanceCommand
from models.service_results import BalanceResult, DiagnosticResult, PaymentResult, RebootResult
from services.billing_service import BillingService
from services.diagnostic_service import DiagnosticService


class TestViewBalanceCommand(unittest.TestCase):
    def setUp(self):
        self.cmd = ViewBalanceCommand(BillingService())

    def test_returns_balance_result(self):
        result = self.cmd.execute()
        self.assertIsInstance(result, BalanceResult)

    def test_balance_amount_is_correct(self):
        result = self.cmd.execute()
        self.assertEqual(result.amount, 150.00)

    def test_balance_message_is_present(self):
        result = self.cmd.execute()
        self.assertIn("$150.00", result.message)


class TestPayBillCommand(unittest.TestCase):
    def setUp(self):
        self.cmd = PayBillCommand(BillingService())

    def test_returns_payment_result(self):
        result = self.cmd.execute()
        self.assertIsInstance(result, PaymentResult)

    def test_payment_succeeds(self):
        result = self.cmd.execute()
        self.assertTrue(result.success)

    def test_new_balance_is_zero(self):
        result = self.cmd.execute()
        self.assertEqual(result.new_balance, 0.00)

    def test_payment_message_present(self):
        result = self.cmd.execute()
        self.assertIn("$0.00", result.message)


class TestRunDiagnosticCommand(unittest.TestCase):
    def setUp(self):
        self.cmd = RunDiagnosticCommand(DiagnosticService())

    def test_returns_diagnostic_result(self):
        result = self.cmd.execute()
        self.assertIsInstance(result, DiagnosticResult)

    def test_device_status_is_offline(self):
        result = self.cmd.execute()
        self.assertEqual(result.device_status, "OFFLINE")

    def test_diagnostic_message_contains_offline(self):
        result = self.cmd.execute()
        self.assertIn("OFFLINE", result.message)


class TestRebootRouterCommand(unittest.TestCase):
    def setUp(self):
        self.cmd = RebootRouterCommand(DiagnosticService())

    def test_returns_reboot_result(self):
        result = self.cmd.execute()
        self.assertIsInstance(result, RebootResult)

    def test_reboot_succeeds(self):
        result = self.cmd.execute()
        self.assertTrue(result.success)

    def test_reboot_message_present(self):
        result = self.cmd.execute()
        self.assertIn("Success", result.message)


if __name__ == "__main__":
    unittest.main()
