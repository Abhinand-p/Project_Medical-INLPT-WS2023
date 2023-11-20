"""Configuration Settings"""

# Directory to store log files
LOG_DIR = "logs"

# Default user settings. Can be overridden by command line arguments.
DEFAULT_SETTINGS = {
    "log_file": f"{LOG_DIR}/system.log",
    "log_level": "INFO",
}

MAX_LOOP = 10
START_LOOP = 0
