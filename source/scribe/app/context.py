"""
Used to configure the application context.
This includes command line arguments application settings, and domain context.
"""
import logging
from .cli.arguments import AppArguments
from .settings import AppSettings
from .configuration import AppConfiguration
from .log.logging import AppLog

class AppContext():
    """
    Provides features for the application context.
    """
    def __init__(self) -> None:
        super().__init__()

        self.arguments:AppArguments = AppArguments()
        """The application command line. This is a configuration provider."""

        self.settings:AppSettings = AppSettings()
        """The application settings object. This is a configuration provider."""

        self.configuration:AppConfiguration = AppConfiguration()
        """The application configuration resolves setting providers."""

        self.log:AppLog = AppLog()
        """The application log settings."""


    @staticmethod
    def create() -> 'AppContext':
        """
        Configure the application context.
        """
        this:AppContext = AppContext()
        this.arguments = AppArguments.create()
        this.settings = AppSettings.create(this.arguments)
        this.configuration = AppConfiguration.create(this.arguments, this.settings)
        this.log = AppLog.create(this.configuration)

        # Log application startup details.
        logging.debug(str(this.arguments))
        logging.debug(str(this.settings))
        logging.debug(str(this.configuration))
        logging.debug(str(this.log))
        return this
