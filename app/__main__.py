import logging
import app

# Main
#---------------------------------------------

if __name__ == "__main__":
    app.settings.configure_logging()

    # Setup for arguments and settings.
    arguments = app.settings.arguments()
    base_dir, publish_info, projects = app.settings.read(arguments.settings)

    # Get content data for game and editor.
    game_info = publish_info.get("game", {})
    editor_info = publish_info.get("editor", {})

    # Log some application startup details.
    logging.info(f"Directory: {base_dir}")
    logging.info(f"Game: {game_info}")
    logging.info(f"Editor: {editor_info}")

    # Start processing any projects
    app.generator.process(projects)
