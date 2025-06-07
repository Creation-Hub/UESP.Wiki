import os
import argparse
import logging
from . import settings
from . import generator

# Configuration
#---------------------------------------------

def configure_logging():
    # Create root logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Log File handler
    file_handler = logging.FileHandler("app.log", mode='w')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    # Console Stream handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)


# Arguments
#---------------------------------------------

def arguments():
    """
    Parses command line arguments to for this application.
    """
    argument_parser = argparse.ArgumentParser(description="UESP Wiki Generator")
    argument_parser.add_argument(
        "--settings",
        type=str,
        default=os.path.join(os.path.dirname(__file__), "settings_default.json"),
        help="Path to the application settings JSON file."
    )
    return argument_parser.parse_args()
