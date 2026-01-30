import logging
import sys


def setup_logger():
    """
    Sets up the root logger with a specific format and handler.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    logging.getLogger("azure").setLevel(logging.WARNING)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    )
    handler.setFormatter(formatter)

    # Avoid adding multiple handlers if setup_logger is called multiple times
    if not logger.handlers:
        logger.addHandler(handler)

    return logger
