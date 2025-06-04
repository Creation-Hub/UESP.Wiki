import os
import app
from app import papyrus
from app.papyrus import Script


# Main
#---------------------------------------------

if __name__ == "__main__":
    # Read the application configuration settings
    base_dir, publish_info, targets = app.settings.settings_read(app.settings.app_arguments())
    game_info = publish_info.get("game", {})
    editor_info = publish_info.get("editor", {})
    print("Directory:", base_dir)
    print("Game:", game_info)
    print("Editor:", editor_info)

    scripts:list[Script] = papyrus.read(targets)
    if scripts:
        print(f"Found {len(scripts)} scripts in the targets.")
        for script in scripts:
            print(f"  - {script.header} ({script.header.name.path()})")

    # TODO: This is a condition to avoid running the process in the main block temporarily
    if True == False: app.generator.process(targets)
