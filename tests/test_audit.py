import unittest

from audit.audit_event import AuditEvent, EventType, Outcome
from audit.audit_formatter import AuditFormatter
from audit.audit_logger import AuditLogger
from audit.event_bus import EventBus


class TestEventBus(unittest.TestCase):
    def setUp(self):
        self.bus = EventBus()

    def test_subscriber_receives_emitted_event(self):
        received = []
        self.bus.subscribe(received.append)
        event = AuditEvent(
            session_id="abc",
            event_type=EventType.INPUT,
            outcome=Outcome.SUCCESS,
        )
        self.bus.emit(event)
        self.assertEqual(len(received), 1)
        self.assertIs(received[0], event)

    def test_multiple_subscribers_all_receive_event(self):
        received_a = []
        received_b = []
        self.bus.subscribe(received_a.append)
        self.bus.subscribe(received_b.append)
        self.bus.emit(AuditEvent(
            session_id="abc",
            event_type=EventType.TRANSITION,
            outcome=Outcome.SUCCESS,
        ))
        self.assertEqual(len(received_a), 1)
        self.assertEqual(len(received_b), 1)

    def test_no_subscribers_does_not_raise(self):
        try:
            self.bus.emit(AuditEvent(
                session_id="abc",
                event_type=EventType.SESSION_END,
                outcome=Outcome.TERMINATED,
            ))
        except Exception as e:
            self.fail(f"emit() raised unexpectedly: {e}")


class TestAuditFormatter(unittest.TestCase):
    def _make_event(self, **kwargs):
        defaults = dict(session_id="s1", event_type=EventType.INPUT, outcome=Outcome.SUCCESS)
        defaults.update(kwargs)
        return AuditEvent(**defaults)

    def test_log_message_contains_event_type(self):
        event = self._make_event(event_type=EventType.SERVICE_CALL)
        msg = AuditFormatter.to_log_message(event)
        self.assertIn("SERVICE_CALL", msg)

    def test_log_message_contains_outcome(self):
        event = self._make_event(outcome=Outcome.ESCALATED)
        msg = AuditFormatter.to_log_message(event)
        self.assertIn("ESCALATED", msg)

    def test_log_message_contains_details_when_present(self):
        event = self._make_event(details="billing.pay_bill")
        msg = AuditFormatter.to_log_message(event)
        self.assertIn("billing.pay_bill", msg)

    def test_log_message_omits_details_when_absent(self):
        event = self._make_event(details=None)
        msg = AuditFormatter.to_log_message(event)
        self.assertNotIn("details=", msg)

    def test_db_row_has_correct_length(self):
        event = self._make_event()
        row = AuditFormatter.to_db_row(event)
        self.assertEqual(len(row), 7)

    def test_db_row_session_id_position(self):
        event = self._make_event(session_id="my-session")
        row = AuditFormatter.to_db_row(event)
        self.assertEqual(row[1], "my-session")

    def test_db_row_outcome_is_string_not_enum(self):
        event = self._make_event(outcome=Outcome.SUCCESS)
        row = AuditFormatter.to_db_row(event)
        self.assertEqual(row[6], "SUCCESS")
        self.assertIsInstance(row[6], str)


class TestAuditLogger(unittest.TestCase):
    def setUp(self):
        self.logger = AuditLogger(
            session_id="test-123",
            db_path=":memory:",
            log_path="/tmp/ivr_test.log",
        )

    def tearDown(self):
        self.logger.close()

    def test_handle_event_persists_to_db(self):
        event = AuditEvent(
            session_id="test-123",
            event_type=EventType.INPUT,
            outcome=Outcome.SUCCESS,
            raw_input="1",
        )
        self.logger.handle_event(event)
        rows = self.logger._conn.execute(
            "SELECT session_id, event_type FROM audit_events"
        ).fetchall()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], "test-123")
        self.assertEqual(rows[0][1], "INPUT")

    def test_multiple_events_all_persisted(self):
        for i in range(5):
            self.logger.handle_event(AuditEvent(
                session_id="test-123",
                event_type=EventType.INPUT,
                outcome=Outcome.SUCCESS,
            ))
        rows = self.logger._conn.execute(
            "SELECT count(*) FROM audit_events"
        ).fetchone()
        self.assertEqual(rows[0], 5)


if __name__ == "__main__":
    unittest.main()
