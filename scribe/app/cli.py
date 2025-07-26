"""
Defines the command line interface for this application.

Help:
    - https://docs.python.org/3/library/argparse.html
"""
import os
from argparse import ArgumentParser, Namespace


def arguments() -> Namespace:
    """
    Parses the command line arguments for this application.
    """
    argument_parser:ArgumentParser = ArgumentParser(
        prog="app",
        description="Provides a command line interface for generating and uploading UESP Wiki files from Papyrus scripts."
    )
    argument_parser.add_argument(
        "--settings",
        type=str,
        default=os.path.join(os.getcwd(), "settings_default.json"),
        help="Path to the application settings JSON file."
    )

    modes = argument_parser.add_subparsers(
        dest="mode",
        help="Start this application in 'generate' mode or 'upload' mode.",
        required=True
    )

    modes.add_parser(
        "generate",
        help="Parse Papyrus scripts and generate MediaWiki files."
    )

    upload = modes.add_parser(
        "upload",
        help="Upload generated MediaWiki files to the wiki via API."
    )
    upload.add_argument(
        "--environment",
        type=str,
        default="local",
    )

    return argument_parser.parse_args()
