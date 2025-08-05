"""
Provides features for application configuration management.
"""
from scribe.app.log.level import LogLevel
from scribe.app.cli.arguments import AppArguments
from scribe.app.settings import AppSettings
from scribe.shared.objects import Dump

class AppConfiguration:
    """
    Represents the application configuration after all the configuration providers have resolved their overrides.
    """

    def __init__(self) -> None:
        # Application
        self.base_directory:str|None = None
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

        # Generator
        self.generator_configuration_file:str|None = None
        """The json file path for the generator configuration file."""

        # Uploader
        self.upload_configuration_file:str|None = None
        """The json file path for the uploader configuration file."""

        # Uploader
        self.upload_environment:str|None = None
        """The environment to use for the uploader."""


    def __str__(self) -> str:
        return Dump.get(self)


    @staticmethod
    def create(arguments:AppArguments, settings:AppSettings) -> 'AppConfiguration':
        this:AppConfiguration = AppConfiguration()

        # Apply any application settings to the configuration overrides.
        if settings:
            # this._base_directory = settings._base_directory
            this.log_date_format = settings.log_date_format or this.log_date_format
            this.log_console_level = settings.log_console_level or this.log_console_level
            this.log_file_level = settings.log_file_level or this.log_file_level
            this.log_file_path = settings.log_file_path or this.log_file_path
            this.generator_configuration_file = settings.generator_file_path or this.generator_configuration_file
            this.upload_configuration_file = settings.uploader_file_path or this.upload_configuration_file
            this.upload_environment = settings.uploader_environment or this.upload_environment

        # Apply any command line arguments to the configuration overrides.
        if arguments:
            this.log_date_format = arguments.log_date_format or this.log_date_format
            this.log_console_level = arguments.log_console_level or this.log_console_level
            this.log_file_level = arguments.log_file_level or this.log_file_level
            this.log_file_path = arguments.log_file_path or this.log_file_path
            this.generator_configuration_file = arguments.generator_configuration_file or this.generator_configuration_file
            this.upload_configuration_file = arguments.upload_configuration_file or this.upload_configuration_file
            this.upload_environment = arguments.upload_environment or this.upload_environment

        return this
