import os
import argparse
import json


# Arguments
#---------------------------------------------

def app_arguments() -> str:
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
    arguments = argument_parser.parse_args()
    return arguments.settings


# Settings
#---------------------------------------------

def settings_read(settings_path: str):
    """
    Reads application settings file.
    Returns (publish_info, targets) where:
      - base_dir: the base directory of the settings file
      - publish_info: dict with 'game' and 'editor' info
      - targets: list of (target_name, script_dir, output_dir, output_sort, output_objects, output_members) tuples
    """
    publish_info = {}
    targets = []
    if os.path.exists(settings_path):
        with open(settings_path, encoding="utf-8") as file:
            data = json.load(file)
            base_dir = os.path.dirname(os.path.abspath(settings_path))
            # Extract publish info (game/editor)
            publish_info = data.get("publish", {})
            for target in data.get("targets", []):
                target_name = target.get("name", "")
                script_dir = target.get("source.directory")
                output_dir = target.get("output.directory")
                output_sort = target.get("output.sort", False)
                output_objects = target.get("output.objects", False)
                output_members = target.get("output.members", False)
                if script_dir:
                    script_dir = os.path.abspath(os.path.join(base_dir, script_dir))
                if output_dir:
                    output_dir = os.path.abspath(os.path.join(base_dir, output_dir))
                targets.append((target_name, script_dir, output_dir, bool(output_sort), bool(output_objects), bool(output_members)))
    return base_dir, publish_info, targets
