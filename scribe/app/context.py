"""
Used to configure the application context.
This includes command line arguments application settings, and domain context.
"""
import logging
from scribe.app.configuration import AppConfiguration
from scribe.app.settings import AppSettings
from scribe.app.cli.arguments import AppArguments
from scribe.app.log.logging import AppLog

class AppContext():
    """
    Provides features for the application context.
    """
    def __init__(self) -> None:
        self.arguments:AppArguments = AppArguments()
        """The application command line. This is a configuration provider."""

        self.settings:AppSettings = AppSettings()
        """The application settings object. This is a configuration provider."""

        self.configuration:AppConfiguration = AppConfiguration()
        """The application configuration resolves settings providers."""

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
        logging.info(str(this.arguments))
        logging.info(str(this.settings))
        logging.info(str(this.configuration))
        logging.info(str(this.log))
        return this
