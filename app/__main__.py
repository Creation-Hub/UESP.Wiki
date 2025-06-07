import logging
import app
from app.settings import AppSettings

# Main
#---------------------------------------------

if __name__ == "__main__":
    app.configure_logging()
    arguments = app.arguments()
    settings:AppSettings = app.settings.read(arguments.settings)

    # Get content data for game and editor.
    game_info = settings.publish_info.get("game", {})
    editor_info = settings.publish_info.get("editor", {})

    # Log some application startup details.
    logging.info(f"Directory: {settings.base_dir}")
    logging.info(f"Game: {game_info}")
    logging.info(f"Editor: {editor_info}")

    # Start processing any projects
    app.generator.process(settings.projects)
