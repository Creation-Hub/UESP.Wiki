from argparse import Namespace
import logging
from typing import Any
import scribe
import scribe.app.log
import scribe.app.cli
import scribe.app.context
import scribe.bot.generator
import scribe.bot.uploader
from scribe.app.context import AppContext


def main(arguments:Namespace) -> None:
    """
    Main entry point for this application.
    """
    scribe.app.log.configure()
    if arguments.mode == "generate":
        main_generate(arguments)
    elif arguments.mode == "upload":
        main_upload(arguments)
    else:
        logging.error(f"Unknown mode: {arguments.mode}")


def main_generate(arguments:Namespace) -> None:
    context:AppContext = scribe.app.context.read(arguments.settings)

    # Get content data for game and editor.
    game_info:dict[str, Any] = context.publish_info.get("game", {})
    editor_info:dict[str, Any] = context.publish_info.get("editor", {})

    # Log some application startup details.
    logging.info(f"Arguments: {arguments}")
    logging.info(f"Directory: {context.base_directory}")
    logging.info(f"Game: {game_info}")
    logging.info(f"Editor: {editor_info}")

    # Start processing any projects
    scribe.bot.generator.start(context)


def main_upload(arguments:Namespace) -> None:
    scribe.bot.uploader.start()


# Main
#---------------------------------------------
if __name__ == "__main__":
    arguments:Namespace = scribe.app.cli.arguments()
    main(arguments)
