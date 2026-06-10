import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(BASE_DIR, "logs")

LOG_PATH = os.path.join(LOGS_DIR, "ivr_operational.log")
DB_PATH = os.path.join(LOGS_DIR, "ivr_audit.db")

LOG_MAX_BYTES = 5 * 1024 * 1024
LOG_BACKUP_COUNT = 3
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(session_id)s | %(message)s"
