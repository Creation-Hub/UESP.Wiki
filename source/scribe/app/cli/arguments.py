"""
Used to configure the command line system.

Help:
    - https://docs.python.org/3/library/argparse.html
"""
from argparse import ArgumentParser, Namespace
from typing import override
from sharp.objects import Dump
from .mode import AppMode
from .parameters import Parameters
from ..log import LogLevel

class AppArguments:
    """
    Represents the command line argument for the application.
    """

    parser:ArgumentParser = Parameters.create()
    """The command line argument parser. This is essentially static."""


    def __init__(self) -> None:
        super().__init__()

        self.values:Namespace|None = None
        """The command line argument values."""


    @override
    def __str__(self) -> str:
        return Dump.get(self)


    @staticmethod
    def create() -> 'AppArguments':
        """
        Create the command line arguments from the parser.
        """
        this:AppArguments = AppArguments()
        this.values = AppArguments.parser.parse_args()
        return this


    @property
    def configuration_file(self) -> str|None:
        """Path to the application settings JSON file."""
        if not self.values: return None
        return getattr(self.values, "settings", None)

    @property
    def log_date_format(self) -> str|None:
        """Date format for log messages."""
        if not self.values: return None
        return getattr(self.values, "log_date_format", None)

    @property
    def log_console_level(self) -> LogLevel|None:
        """The logging level for console output."""
        if not self.values: return None
        return LogLevel.convert(getattr(self.values, "log_console_level", None))

    @property
    def log_file_level(self) -> LogLevel|None:
        """The logging level for file output."""
        if not self.values: return None
        return LogLevel.convert(getattr(self.values, "log_file_level", None))

    @property
    def log_file_path(self) -> str|None:
        """The log file path to use."""
        if not self.values: return None
        return getattr(self.values, "log_file_path", None)

    @property
    def mode(self) -> AppMode|None:
        """The application mode (generate or upload)."""
        if not self.values: return None
        value:str|None = getattr(self.values, "mode")
        if not value: return AppMode.NONE
        else: return AppMode[value.upper()]

    @property
    def generator_file_path(self) -> str|None:
        """Path to the generator configuration file."""
        if not self.values: return None
        if self.mode is not AppMode.GENERATE:
            return None
        return getattr(self.values, "config", None)

    @property
    def uploader_file_path(self) -> str|None:
        """Path to the upload configuration file."""
        if not self.values: return None
        if self.mode is not AppMode.UPLOAD:
            return None
        return getattr(self.values, "config", None)

    @property
    def upload_environment(self) -> str|None:
        """The upload environment to use."""
        if not self.values: return None
        if self.mode is not AppMode.UPLOAD:
            return None
        return getattr(self.values, "environment", None)
