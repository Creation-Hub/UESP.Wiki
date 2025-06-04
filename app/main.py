import os
import argparse
import json
from app import wiki


# Settings
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


def settings_read(settings_path: str) -> tuple[str | None, str | None, bool]:
    """
    Reads application settings from a JSON file.
    """
    script_dir = None
    output_dir = None
    output_sort = False
    if os.path.exists(settings_path):
        with open(settings_path, encoding="utf-8") as file:
            data = json.load(file)
            script_dir = data.get("SCRIPT_DIR")
            output_dir = data.get("OUTPUT_DIR")
            output_sort = data.get("OUTPUT_DIR_SORT", False)
        # Resolve relative paths based on the settings file location
        base_dir = os.path.dirname(os.path.abspath(settings_path))
        if script_dir:
            script_dir = os.path.abspath(os.path.join(base_dir, script_dir))
        if output_dir:
            output_dir = os.path.abspath(os.path.join(base_dir, output_dir))
    return script_dir, output_dir, bool(output_sort)


SETTINGS_FILE = app_arguments()
(
    SCRIPT_DIR,
    OUTPUT_DIR,
    OUTPUT_DIR_SORT
) = settings_read(SETTINGS_FILE)


# Files
#---------------------------------------------

def find_script_files(directory: str) -> list[str]:
    """Searches for Papyrus scripts in the given Papyrus root import directory."""
    search = []
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name.lower().endswith(".psc"):
                search.append(os.path.join(root, file_name))
    return search


# Main
#---------------------------------------------

if __name__ == "__main__":
    if not SCRIPT_DIR or not OUTPUT_DIR:
        print(f"SCRIPT_DIR or OUTPUT_DIR not set in '{SETTINGS_FILE}'")
        exit(1)
    if not os.path.exists(SCRIPT_DIR):
        print(f"Script directory does not exist: '{SCRIPT_DIR}'")
        exit(1)
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Search for Papyrus scripts in the script directory
    script_paths = find_script_files(SCRIPT_DIR)
    for script_path in script_paths:
        file_name = os.path.basename(script_path) # Get the base name of the file
        script_name = os.path.splitext(file_name)[0] # Remove the file extension
        output_file_name = f"{script_name}.wiki"
        output_directory = OUTPUT_DIR
        if OUTPUT_DIR_SORT:
            output_directory = os.path.join(OUTPUT_DIR, script_name)
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)
        output_path = os.path.join(output_directory, output_file_name)

        # Write the wiki page for the script
        wiki.page.write(script_path, output_path)
        print(f"{script_name}:\n  -> in:  {script_path}\n  -> out: {output_path}")

        # Uncomment the following lines to handle exceptions during processing.
        # By handle, I mean swallowing them and continuing
        # try:
        #   #code_here
        # except Exception as e:
        #     print(f"Error processing '{script_path}': {e}")
