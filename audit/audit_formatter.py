from typing import Tuple

from audit.audit_event import AuditEvent


class AuditFormatter:
    @staticmethod
    def to_log_message(event: AuditEvent) -> str:
        parts = [
            f"[{event.event_type.value}]",
            f"state={event.state_name or '-'}",
            f"input={event.raw_input or '-'}",
            f"outcome={event.outcome.value}",
        ]
        if event.details:
            parts.append(f"details={event.details}")
        return " | ".join(parts)

    @staticmethod
    def to_db_row(event: AuditEvent) -> Tuple:
        return (
            event.timestamp,
            event.session_id,
            event.event_type.value,
            event.state_name,
            event.raw_input,
            event.details,
            event.outcome.value,
        )
