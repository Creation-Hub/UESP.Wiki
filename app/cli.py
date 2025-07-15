import os
from argparse import ArgumentParser, Namespace


def arguments() -> Namespace:
    """
    Parses the command line arguments for this application.
    """
    argument_parser = ArgumentParser(description="UESP Wiki Generator")
    argument_parser.add_argument(
        "--settings",
        type=str,
        default=os.path.join(os.path.dirname(__file__), "settings_default.json"),
        help="Path to the application settings JSON file."
    )
    return argument_parser.parse_args()
