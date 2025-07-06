import logging

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def configure():
    # Create root logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Log File handler
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s:%(funcName)s - %(message)s', datefmt=DATE_FORMAT)
    file_handler = logging.FileHandler("app.log", mode='w')
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    # Console Stream handler
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt=DATE_FORMAT)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)
