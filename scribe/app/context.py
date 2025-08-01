"""
Used to configure the application context.
This includes command line arguments application settings, and domain context.
"""
import logging
from scribe.app.cli import AppArguments
from scribe.app.log import AppLog
from scribe.app.settings import AppSettings
from scribe.papyrus.context import PapyrusContext
from scribe.wiki.context import WikiContext

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

        self.wiki:WikiContext = WikiContext()
        """The application wiki context."""


    @staticmethod
    def create() -> 'AppContext':
        """
        Configure the application context.
        """
        this:AppContext = AppContext()
        this.arguments = AppArguments.create()
        this.log = AppLog.create(this.arguments)
        this.settings = AppSettings.create(this.arguments)
        this.wiki = WikiContext.create()

        # Log application startup details.
        logging.info(str(this.arguments))
        logging.info(str(this.log))
        logging.info(str(this.settings))
        return this
