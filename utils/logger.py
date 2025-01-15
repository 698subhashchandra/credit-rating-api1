import logging
import os
from logging.handlers import RotatingFileHandler
from configs.constants import MAX_LOG_SIZE, BACKUP_COUNT, SERVICE_NAME, ERROR_MSG_LOGGER_SETUP, ERROR_MSG_LOG_DIR_CREATION


def setup_logger(
    name: str,
    log_file: str = None,
    level: int = logging.INFO,
    max_log_size: int = MAX_LOG_SIZE,
    backup_count: int = BACKUP_COUNT
) -> logging.Logger:
    """
    Function to configure and return a logger with rotating file handler and stream handler.

    Args:
        name (str): The name of the logger (usually the module name).
        log_file (str, optional): The name of the log file. If None, default to `SERVICE_NAME.log`.
        level (int, optional): The logging level. Defaults to `logging.INFO`.
        max_log_size (int, optional): The maximum size of the log file in bytes. Defaults to `MAX_LOG_SIZE`.
        backup_count (int, optional): The number of backup log files to retain. Defaults to `BACKUP_COUNT`.

    Returns:
        logging.Logger: The configured logger.
    """
    try:
        # Create log directory in the root of the project
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'log')
        if not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir)
            except Exception as e:
                raise ValueError(f"{ERROR_MSG_LOG_DIR_CREATION}: {e}")

        # If log_file is provided, ensure it is within the log directory
        if log_file:
            log_file_path = os.path.join(log_dir, log_file)
        else:
            log_file_path = os.path.join(log_dir, f'{SERVICE_NAME}.log')

        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # File handler with rotating log file (max size and backup count)
        rotating_handler = RotatingFileHandler(log_file_path, maxBytes=max_log_size, backupCount=backup_count)
        rotating_handler.setFormatter(formatter)
        logger.addHandler(rotating_handler)

        # Stream handler (for console output)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        return logger

    except Exception as e:
        raise ValueError(f"{ERROR_MSG_LOGGER_SETUP}: {e}")


# Initialize the logger for the project with log rotation
project_logger = setup_logger(name=SERVICE_NAME, log_file=f'{SERVICE_NAME}.log')
