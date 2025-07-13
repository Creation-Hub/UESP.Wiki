import logging
from typing import Any
import app
from app.context import AppContext


if __name__ == "__main__":
    """
    Main entry point for this application.
    """
    app.log.configure()
    arguments = app.cli.arguments()
    context:AppContext = app.settings.read(arguments.settings)

    # Get content data for game and editor.
    game_info:dict[str, Any] = context.publish_info.get("game", {})
    editor_info:dict[str, Any] = context.publish_info.get("editor", {})

    # Log some application startup details.
    logging.info(f"Arguments: {arguments}")
    logging.info(f"Directory: {context.base_directory}")
    logging.info(f"Game: {game_info}")
    logging.info(f"Editor: {editor_info}")

    # Start processing any projects
    app.program.start(context)
