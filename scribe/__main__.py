from argparse import Namespace
import logging
import scribe
import scribe.app.log
import scribe.app.cli
import scribe.app.settings
import scribe.bot.generator
import scribe.bot.uploader
from scribe.app.context import AppContext


def main(arguments:Namespace) -> None:
    """
    Main entry point for this application.
    """
    scribe.app.log.configure()
    app:AppContext = AppContext()
    app.settings = scribe.app.settings.read(arguments.settings)
    app.settings.environment = arguments.environment

    # Log application startup details.
    logging.info(f"Arguments: {arguments}")
    logging.info(f"Directory: {app.settings.base_directory}")
    logging.info(f"Game: {app.settings.game_info}")
    logging.info(f"Editor: {app.settings.editor_info}")

    if arguments.mode == "generate":
        scribe.bot.generator.start(app)
    elif arguments.mode == "upload":
        scribe.bot.uploader.start(app)
    else:
        logging.error(f"Unknown mode: {arguments.mode}")


# Main
#---------------------------------------------
if __name__ == "__main__":
    arguments:Namespace = scribe.app.cli.arguments()
    main(arguments)
