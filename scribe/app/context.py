"""
Used to configure the application context.
This includes application settings, command line arguments, and domain context.
"""
import logging
from scribe.app.cli import AppArguments
from scribe.app.log import AppLog
from scribe.app.settings import AppSettings
from scribe.papyrus.project import PapyrusContext

class AppContext():
    """
    Provides features for the application context.
    """
    def __init__(self) -> None:
        self.arguments:AppArguments = AppArguments()
        """The application command line."""

        self.log:AppLog = AppLog()
        """The application log settings."""

        self.settings:AppSettings = AppSettings()
        """The application settings object."""

        self.papyrus:PapyrusContext = PapyrusContext()
        """The application Papyrus context."""


    @staticmethod
    def create() -> 'AppContext':
        """
        Configure the application context.
        """
        this:AppContext = AppContext()
        this.arguments = AppArguments.create()
        this.log = AppLog.create(this.arguments)

        # Initialize application settings.
        if this.arguments and this.arguments.configuration_file:
            this.settings = AppSettings.read(this.arguments.configuration_file)

        # Initialize uploader settings.
        if this.arguments:
            this.settings.environment = this.arguments.upload_environment

        # Log application startup details.
        logging.info(f"Arguments: {this.arguments}")
        logging.info(f"Settings: {this.settings.file_path}")
        logging.info(f"Log: {this.log.file_path}")
        logging.info(f"Directory: {this.settings.base_directory}")
        logging.info(f"Providers: {len(this.settings.providers)}")
        for provider in this.settings.providers:
            logging.info(f"- {provider}")

        return this
