"""
Used to configure the command line system.

Help:
    - https://docs.python.org/3/library/argparse.html
"""
from argparse import ArgumentParser, Namespace
from enum import Enum
from scribe.shared.objects import Dump


class AppMode(str, Enum):
    NONE = ""
    GENERATE = "generate"
    UPLOAD = "upload"


def create_parser() -> ArgumentParser:
    """
    Defines the command line parameter parser.
    """

    parser:ArgumentParser = ArgumentParser(
        prog="scribe",
        description="Provides a command line interface for wiki automation tasks.",
    )

    # App
    parser.add_argument(
        "--settings",
        type=str,
        help="Path to the application settings JSON file."
    )


    # Logging
    parser.add_argument(
        "--log-date-format",
        type=str,
        help="Date format for log messages.",
    )

    parser.add_argument(
        "--log-console-level",
        type=str,
        help="The log level to use (DEBUG, INFO, WARNING, ERROR, CRITICAL)."
    )

    parser.add_argument(
        "--log-file-level",
        type=str,
        help="The log level to use (DEBUG, INFO, WARNING, ERROR, CRITICAL)."
    )

    parser.add_argument(
        "--log-file-path",
        type=str,
        help="The log file path to use."
    )


    # MODES
    modes = parser.add_subparsers(
        dest="mode",
        help="Start this application in 'generate' mode or 'upload' mode.",
        required=True
    )


    # Generator
    generate:ArgumentParser = modes.add_parser(
        "generate",
        help="Parse Papyrus scripts and generate MediaWiki files."
    )
    generate.add_argument(
        "--config",
        type=str
    )


    # Uploader
    upload:ArgumentParser = modes.add_parser(
        "upload",
        help="Upload generated MediaWiki files to the wiki via API."
    )

    upload.add_argument(
        "--config",
        type=str
    )

    upload.add_argument(
        "--environment",
        type=str
    )

    return parser


class AppArguments:
    """
    Represents the command line argument for the application.
    """

    parser:ArgumentParser = create_parser()
    """The command line argument parser. This is essentially static."""


    def __init__(self) -> None:
        self.values:Namespace|None = None
        """The command line argument values."""


    def __str__(self) -> str:
        return Dump.get(self)


    @property
    def configuration_file(self) -> str|None:
        """Path to the application settings JSON file."""
        return getattr(self.values, "settings", None) if self.values else None

    @property
    def mode(self) -> AppMode|None:
        """The application mode (generate or upload)."""
        if not self.values: return None
        return AppArguments.to_AppMode(self.values, "mode")

    @property
    def log_date_format(self) -> str|None:
        """Date format for log messages."""
        return getattr(self.values, "log_date_format", None) if self.values else None

    @property
    def log_console_level(self) -> int|None:
        """The logging level for console output."""
        return getattr(self.values, "log_console_level", None) if self.values else None

    @property
    def log_file_level(self) -> int|None:
        """The logging level for file output."""
        return getattr(self.values, "log_file_level", None) if self.values else None

    @property
    def log_file_path(self) -> str|None:
        """The log file path to use."""
        return getattr(self.values, "log_file_path", None) if self.values else None

    @property
    def upload_configuration_file(self) -> str|None:
        """Path to the upload configuration file."""
        return getattr(self.values, "config", None) if self.values else None

    @property
    def upload_environment(self) -> str|None:
        """The upload environment to use."""
        return getattr(self.values, "environment", None) if self.values else None


    @staticmethod
    def create() -> 'AppArguments':
        """
        Create the command line arguments from the parser.
        """
        this:AppArguments = AppArguments()
        this.values = AppArguments.parser.parse_args()
        return this


    @staticmethod
    def to_AppMode(arguments:Namespace, attribute:str) -> AppMode:
        value:str|None = getattr(arguments, attribute)
        if not value: return AppMode.NONE
        else: return AppMode[value.upper()]
