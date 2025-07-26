import logging
from logging import Formatter, Logger
from logging import FileHandler, StreamHandler
from typing import TextIO


DATE_FORMAT:str = "%Y-%m-%d %H:%M:%S"
"""The date format for log messages."""


def configure() -> None:
    """
    Configure the logging system with both console and file handlers.
    """
    # Create root logger
    logger:Logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Log File handler
    file_formatter:Formatter = Formatter('%(asctime)s - %(levelname)s - %(module)s:%(funcName)s - %(message)s', DATE_FORMAT)
    file_handler:FileHandler = FileHandler("app.log", mode='w')
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    # Console Stream handler
    console_formatter:Formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s', DATE_FORMAT)
    console_handler:StreamHandler[TextIO] = StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)

    logging.info("Application log started.")
