# core/logging_config.py
import logging
import os
from .config import settings

logger = logging.getLogger(__name__)

def setup_logging():
    """Cấu hình logging tập trung cho ứng dụng."""
    log_file_path = os.path.join(settings.LOGS_DIR, "system.log")

    root_logger = logging.getLogger()
    
    if root_logger.hasHandlers():
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
            handler.close()

    try:
        logging.basicConfig(
            filename=log_file_path,
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            filemode='w',
            encoding='utf-8'
        )
        logger.info(f"Logging configured to write to file: {log_file_path}")

    except Exception as e:
        logger.error(f"Failed to configure file logging to {log_file_path}: {e}", exc_info=True)
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
        logging.error(f"Switched to basic console logging due to configuration error.")