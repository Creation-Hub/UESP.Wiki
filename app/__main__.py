import logging
import app
from app.context import AppContext

# Main
#---------------------------------------------

if __name__ == "__main__":
    app.log.configure()
    arguments = app.cli.arguments()
    context:AppContext = app.settings.read(arguments.settings)

    # Get content data for game and editor.
    game_info = context.publish_info.get("game", {})
    editor_info = context.publish_info.get("editor", {})

    # Log some application startup details.
    logging.info(f"Arguments: {arguments}")
    logging.info(f"Directory: {context.base_directory}")
    logging.info(f"Game: {game_info}")
    logging.info(f"Editor: {editor_info}")

    # Start processing any projects
    app.program.start(context)
