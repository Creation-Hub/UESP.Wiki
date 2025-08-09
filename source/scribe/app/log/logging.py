"""
Used to configure the logging system.

Help:
    - https://docs.python.org/3/library/logging.html
"""
import logging
from logging import Formatter, Logger
from logging import FileHandler, StreamHandler
from typing import TextIO, override
from sharp.objects import Dump
from ..configuration import AppConfiguration
from . import LogLevel

class AppLog:
    """
    Represents the logging system for the application.
    """

    DATE_FORMAT:str = "%Y-%m-%d %H:%M:%S"
    """The default date format for log messages."""

    CONSOLE_LEVEL:LogLevel = LogLevel.INFO
    """The default logging level for console output."""

    FILE_LEVEL:LogLevel = LogLevel.DEBUG
    """The default logging level for file output."""

    FILE_PATH:str = "scribe.log"
    """The default logging file path."""


    def __init__(self) -> None:
        super().__init__()

        self.date_format:str = self.DATE_FORMAT
        """The date format for log messages."""

        self.console_level:LogLevel = self.CONSOLE_LEVEL
        """The logging level for the console output."""

        self.file_level:LogLevel = self.FILE_LEVEL
        """The logging level for the log file."""

        self.file_path:str = self.FILE_PATH
        """The file path for the log file."""


    @override
    def __str__(self) -> str:
        return Dump.get(self)


    @staticmethod
    def create(configuration:AppConfiguration|None = None) -> 'AppLog':
        """
        Configure the logging system with both console and file handlers.
        """
        this:AppLog = AppLog()

        # Apply any settings from the AppSettings object.
        if configuration:
            this.date_format = configuration.log_date_format or this.date_format
            this.console_level = configuration.log_console_level or this.console_level
            this.file_level = configuration.log_file_level or this.file_level
            this.file_path = configuration.log_file_path or this.file_path

        # Configure the log handler.
        logger:Logger = logging.getLogger()
        logger.handlers.clear()
        logger.setLevel(logging.DEBUG)

        # Configure the console stream handler.
        console_formatter:Formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s', this.date_format)
        console_handler:StreamHandler[TextIO] = StreamHandler()
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(int(this.console_level))
        logger.addHandler(console_handler)

        # Configure the log file handler.
        file_formatter:Formatter = Formatter('%(asctime)s - %(levelname)s - %(module)s:%(funcName)s - %(message)s', this.date_format)
        file_path:str = this.file_path if this.file_path else AppLog.FILE_PATH
        file_handler:FileHandler = FileHandler(file_path, mode='w')
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)

        return this
