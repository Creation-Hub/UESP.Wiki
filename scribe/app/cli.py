"""
Used to configure the command line system.

Help:
    - https://docs.python.org/3/library/argparse.html
"""
from argparse import ArgumentParser, Namespace
from enum import Enum


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
        # The following attributes are set by the parser values.
        self.configuration_file:str|None = None
        self.mode:AppMode|None = None
        self.log_date_format:str|None = None
        self.log_console_level:int|None = None
        self.log_file_level:int|None = None
        self.log_file_path:str|None = None
        self.upload_configuration_file:str|None = None
        self.upload_environment:str|None = None


    def __str__(self) -> str:
        string:str = f"{self.__class__.__name__}"
        string += f"\n - parser:"
        string += f"\n   - prog: {AppArguments.parser.prog}"
        string += f"\n   - description: {AppArguments.parser.description}"
        string += f"\n - arguments: {len(self.values.__dict__)}"
        for key in self.values.__dict__:
            value = getattr(self.values, key)
            string += f"\n  - {key}: {value}"
        return string


    @staticmethod
    def create() -> 'AppArguments':
        """
        Create the command line arguments from the parser.
        """
        this:AppArguments = AppArguments()
        this.values = AppArguments.parser.parse_args()
        this.configuration_file = getattr(this.values, "settings", this.configuration_file)
        this.log_date_format = getattr(this.values, "log_date_format", this.log_date_format)
        this.log_console_level = getattr(this.values, "log_console_level", this.log_console_level)
        this.log_file_level = getattr(this.values, "log_file_level", this.log_file_level)
        this.log_file_path = getattr(this.values, "log_file_path", this.log_file_path)
        this.mode = AppArguments.to_AppMode(this.values, "mode")
        this.upload_configuration_file = getattr(this.values, "config", this.upload_configuration_file)
        this.upload_environment = getattr(this.values, "environment", this.upload_environment)
        return this


    @staticmethod
    def to_AppMode(arguments:Namespace, attribute:str) -> AppMode:
        value:str|None = getattr(arguments, attribute)
        if not value: return AppMode.NONE
        else: return AppMode[value.upper()]
