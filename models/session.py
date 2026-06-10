from dataclasses import dataclass
from datetime import datetime


@dataclass
class Session:
    session_id: str
    start_time: datetime
    is_active: bool = True
