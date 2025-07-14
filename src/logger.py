import os
import logging
import logging.handlers
import time

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.WARNING)

    if not logger.hasHandlers():
        os.makedirs("logs", exist_ok=True)

        logging.Formatter.converter = time.gmtime
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        )

        file_handler = logging.handlers.RotatingFileHandler(
            "logs/errors.log", maxBytes=5*1024*1024, backupCount=3,
        )
        file_handler.setLevel(logging.ERROR)
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(logging.WARNING)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger