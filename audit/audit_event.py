from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class EventType(str, Enum):
    INPUT = "INPUT"
    TRANSITION = "TRANSITION"
    SERVICE_CALL = "SERVICE_CALL"
    GLOBAL_CMD = "GLOBAL_CMD"
    SESSION_END = "SESSION_END"


class Outcome(str, Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    ESCALATED = "ESCALATED"
    TERMINATED = "TERMINATED"


@dataclass(frozen=True)
class AuditEvent:
    session_id: str
    event_type: EventType
    outcome: Outcome
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    state_name: Optional[str] = None
    raw_input: Optional[str] = None
    details: Optional[str] = None
