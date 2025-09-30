"""
Provides features for application configuration management.
"""
from typing import override
from sharp.objects import Dump
from .log import LogLevel
from .cli.arguments import AppArguments
from .settings import AppSettings

class AppConfiguration:
    """
    Represents the application configuration after all the configuration providers have resolved their overrides.
    """

    def __init__(self) -> None:
        super().__init__()

        # Application
        self._base_directory:str|None = None
        """The base directory of the settings file."""

        # Log
        self.log_date_format:str|None = None
        """Date format for log messages."""

        self.log_console_level:LogLevel|None = None
        """The logging level for console output."""

        self.log_file_level:LogLevel|None = None
        """The logging level for file output."""

        self.log_file_path:str|None = None
        """The log file path to use."""

        # Wiki
        self.export_directory:str|None = None
        """The export directory for wiki pages."""

        # Papyrus
        self.papyrus_file_path:str|None = None
        """The json file path for the Papyrus configuration."""

        # Uploader
        self.uploader_file_path:str|None = None
        """The json file path for the uploader configuration."""

        # Uploader
        self.uploader_environment:str|None = None
        """The environment to use for the uploader."""


    @override
    def __str__(self) -> str:
        return Dump.get(self)


    @staticmethod
    def create(arguments:AppArguments, settings:AppSettings) -> 'AppConfiguration':
        this:AppConfiguration = AppConfiguration()
        # Apply any application settings to the configuration overrides.
        this.export_directory = settings.export_directory
        this.log_date_format = arguments.log_date_format or settings.log_date_format
        this.log_console_level = arguments.log_console_level or settings.log_console_level
        this.log_file_level = arguments.log_file_level or settings.log_file_level
        this.log_file_path = arguments.log_file_path or settings.log_file_path
        this.papyrus_file_path = arguments.papyrus_file_path or settings.papyrus_file_path
        this.uploader_file_path = arguments.uploader_file_path or settings.uploader_file_path
        this.uploader_environment = arguments.upload_environment or settings.uploader_environment
        return this
