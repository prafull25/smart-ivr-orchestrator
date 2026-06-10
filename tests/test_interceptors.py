import unittest
from unittest.mock import MagicMock

from interceptors.exit_interceptor import ExitInterceptor
from interceptors.operator_interceptor import OperatorInterceptor


class TestExitInterceptor(unittest.TestCase):
    def setUp(self):
        self.interceptor = ExitInterceptor()
        self.engine = MagicMock()

    def test_matches_exit_keyword(self):
        self.assertTrue(self.interceptor._matches("exit"))

    def test_matches_exit_case_insensitive(self):
        self.assertTrue(self.interceptor._matches("EXIT"))
        self.assertTrue(self.interceptor._matches("Exit"))

    def test_matches_exit_with_whitespace(self):
        self.assertTrue(self.interceptor._matches("  exit  "))

    def test_does_not_match_partial_exit(self):
        self.assertFalse(self.interceptor._matches("ex"))
        self.assertFalse(self.interceptor._matches("exits"))

    def test_does_not_match_operator(self):
        self.assertFalse(self.interceptor._matches("operator"))

    def test_intercept_returns_true_on_match(self):
        result = self.interceptor.intercept("exit", self.engine)
        self.assertTrue(result)

    def test_intercept_calls_terminate(self):
        self.interceptor.intercept("exit", self.engine)
        self.engine.terminate.assert_called_once()

    def test_intercept_returns_false_on_no_match(self):
        result = self.interceptor.intercept("1", self.engine)
        self.assertFalse(result)


class TestOperatorInterceptor(unittest.TestCase):
    def setUp(self):
        self.interceptor = OperatorInterceptor()
        self.engine = MagicMock()

    def test_matches_operator_keyword(self):
        self.assertTrue(self.interceptor._matches("operator"))

    def test_matches_operator_case_insensitive(self):
        self.assertTrue(self.interceptor._matches("OPERATOR"))
        self.assertTrue(self.interceptor._matches("Operator"))

    def test_does_not_match_exit(self):
        self.assertFalse(self.interceptor._matches("exit"))

    def test_intercept_returns_true_on_match(self):
        result = self.interceptor.intercept("operator", self.engine)
        self.assertTrue(result)

    def test_intercept_calls_escalate(self):
        self.interceptor.intercept("operator", self.engine)
        self.engine.escalate.assert_called_once()


class TestInterceptorChain(unittest.TestCase):
    def test_chain_passes_through_to_next(self):
        exit_interceptor = ExitInterceptor()
        operator_interceptor = OperatorInterceptor()
        exit_interceptor.set_next(operator_interceptor)

        engine = MagicMock()
        result = exit_interceptor.intercept("operator", engine)

        self.assertTrue(result)
        engine.escalate.assert_called_once()

    def test_chain_returns_false_when_no_handler_matches(self):
        exit_interceptor = ExitInterceptor()
        operator_interceptor = OperatorInterceptor()
        exit_interceptor.set_next(operator_interceptor)

        engine = MagicMock()
        result = exit_interceptor.intercept("1", engine)

        self.assertFalse(result)

    def test_set_next_returns_next_interceptor(self):
        exit_interceptor = ExitInterceptor()
        operator_interceptor = OperatorInterceptor()
        returned = exit_interceptor.set_next(operator_interceptor)
        self.assertIs(returned, operator_interceptor)


if __name__ == "__main__":
    unittest.main()
