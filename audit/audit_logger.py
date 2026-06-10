import logging
import os
import sqlite3
from logging.handlers import RotatingFileHandler

from audit.audit_event import AuditEvent
from audit.audit_formatter import AuditFormatter
from constants.config import DB_PATH, LOG_BACKUP_COUNT, LOG_FORMAT, LOG_MAX_BYTES, LOG_PATH


class AuditLogger:
    _CREATE_TABLE_SQL = """
        CREATE TABLE IF NOT EXISTS audit_events (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp   TEXT    NOT NULL,
            session_id  TEXT    NOT NULL,
            event_type  TEXT    NOT NULL,
            state_name  TEXT,
            raw_input   TEXT,
            details     TEXT,
            outcome     TEXT
        )
    """
    _INSERT_SQL = """
        INSERT INTO audit_events
            (timestamp, session_id, event_type, state_name, raw_input, details, outcome)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    def __init__(
        self,
        session_id: str,
        db_path: str = DB_PATH,
        log_path: str = LOG_PATH,
    ) -> None:
        self._session_id = session_id
        self._conn = self._init_db(db_path)
        self._logger = self._init_operational_logger(session_id, log_path)

    def _init_db(self, db_path: str) -> sqlite3.Connection:
        db_dir = os.path.dirname(db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
        conn = sqlite3.connect(db_path, check_same_thread=False)
        conn.execute(self._CREATE_TABLE_SQL)
        conn.commit()
        return conn

    def _init_operational_logger(self, session_id: str, log_path: str) -> logging.Logger:
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        logger = logging.getLogger(f"ivr.{session_id}")
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
            handler = RotatingFileHandler(
                log_path,
                maxBytes=LOG_MAX_BYTES,
                backupCount=LOG_BACKUP_COUNT,
            )
            handler.setFormatter(logging.Formatter(LOG_FORMAT))
            logger.addHandler(handler)
        return logger

    def handle_event(self, event: AuditEvent) -> None:
        self._persist_to_db(event)
        self._write_operational_log(event)

    def _persist_to_db(self, event: AuditEvent) -> None:
        self._conn.execute(self._INSERT_SQL, AuditFormatter.to_db_row(event))
        self._conn.commit()

    def _write_operational_log(self, event: AuditEvent) -> None:
        msg = AuditFormatter.to_log_message(event)
        self._logger.info(msg, extra={"session_id": self._session_id})

    def close(self) -> None:
        self._conn.close()
