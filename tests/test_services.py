import unittest

from models.service_results import BalanceResult, DiagnosticResult, PaymentResult, RebootResult
from services.billing_service import BillingService
from services.diagnostic_service import DiagnosticService


class TestBillingService(unittest.TestCase):
    def setUp(self):
        self.svc = BillingService()

    def test_view_balance_returns_correct_type(self):
        result = self.svc.view_balance()
        self.assertIsInstance(result, BalanceResult)

    def test_view_balance_amount(self):
        result = self.svc.view_balance()
        self.assertEqual(result.amount, 150.00)

    def test_pay_bill_returns_correct_type(self):
        result = self.svc.pay_bill()
        self.assertIsInstance(result, PaymentResult)

    def test_pay_bill_success_flag(self):
        result = self.svc.pay_bill()
        self.assertTrue(result.success)

    def test_pay_bill_new_balance(self):
        result = self.svc.pay_bill()
        self.assertEqual(result.new_balance, 0.00)

    def test_results_are_immutable(self):
        result = self.svc.view_balance()
        with self.assertRaises(Exception):
            result.amount = 999.00


class TestDiagnosticService(unittest.TestCase):
    def setUp(self):
        self.svc = DiagnosticService()

    def test_run_diagnostic_returns_correct_type(self):
        result = self.svc.run_diagnostic()
        self.assertIsInstance(result, DiagnosticResult)

    def test_device_status_is_always_offline(self):
        result = self.svc.run_diagnostic()
        self.assertEqual(result.device_status, "OFFLINE")

    def test_reboot_returns_correct_type(self):
        result = self.svc.reboot()
        self.assertIsInstance(result, RebootResult)

    def test_reboot_always_succeeds(self):
        result = self.svc.reboot()
        self.assertTrue(result.success)

    def test_diagnostic_is_deterministic(self):
        result_a = self.svc.run_diagnostic()
        result_b = self.svc.run_diagnostic()
        self.assertEqual(result_a.device_status, result_b.device_status)


if __name__ == "__main__":
    unittest.main()
