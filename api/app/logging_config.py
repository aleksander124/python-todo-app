import logging
from pythonjsonlogger import jsonlogger


def setup_logging():
    log_handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        fmt='%(asctime)s %(levelname)s %(message)s %(name)s %(filename)s %(lineno)s',
        datefmt='%Y-%m-%dT%H:%M:%S'
    )
    log_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(log_handler)