"""
Used to configure the logging system.

Help:
    - https://docs.python.org/3/library/logging.html
"""
import logging
from logging import Formatter, Logger
from logging import FileHandler, StreamHandler
from typing import TextIO
from scribe.app.cli import AppArguments
from scribe.shared.objects import Dump

class AppLog:
    """
    Represents the logging system for the application.
    """

    DATE_FORMAT:str = "%Y-%m-%d %H:%M:%S"
    """The default date format for log messages."""

    CONSOLE_LEVEL:int = logging.INFO
    """The default logging level for console output."""

    FILE_LEVEL:int = logging.DEBUG
    """The default logging level for file output."""

    FILE_PATH:str = "scribe.log"
    """The default logging file path."""


    def __init__(self) -> None:
        self.date_format:str|None = self.DATE_FORMAT
        """The date format for log messages."""

        self.console_level:int|None = self.CONSOLE_LEVEL
        """The logging level for the console output."""

        self.file_level:int|None = self.FILE_LEVEL
        """The logging level for the log file."""

        self.file_path:str|None = self.FILE_PATH
        """The file path for the log file."""


    def __str__(self) -> str:
        return Dump.get(self)


    @staticmethod
    def create(arguments:AppArguments|None = None) -> 'AppLog':
        """
        Configure the logging system with both console and file handlers.
        """
        this:AppLog = AppLog()
        if arguments:
            this.date_format = arguments.log_date_format or this.date_format
            this.console_level = arguments.log_console_level or this.console_level
            this.file_level = arguments.log_file_level or this.file_level
            this.file_path = arguments.log_file_path or this.file_path

        # Configure the log handler.
        logger:Logger = logging.getLogger()
        logger.handlers.clear()
        logger.setLevel(logging.DEBUG)

        # Configure the console stream handler.
        console_formatter:Formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s', this.date_format)
        console_handler:StreamHandler[TextIO] = StreamHandler()
        console_handler.setFormatter(console_formatter)
        console_level:int = this.console_level if this.console_level else AppLog.CONSOLE_LEVEL
        console_handler.setLevel(console_level)
        logger.addHandler(console_handler)

        # Configure the log file handler.
        file_formatter:Formatter = Formatter('%(asctime)s - %(levelname)s - %(module)s:%(funcName)s - %(message)s', this.date_format)
        file_path:str = this.file_path if this.file_path else AppLog.FILE_PATH
        file_handler:FileHandler = FileHandler(file_path, mode='w')
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)

        return this
