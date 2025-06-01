import os
import argparse
import json
import wiki.page

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


def settings_read(settings_path: str) -> tuple[str | None, str | None]:
    """
    Reads application settings from a JSON file.
    """
    script_dir = None
    output_dir = None
    if os.path.exists(settings_path):
        with open(settings_path, encoding="utf-8") as file:
            data = json.load(file)
            script_dir = data.get("SCRIPT_DIR")
            output_dir = data.get("OUTPUT_DIR")
        # Resolve relative paths based on the settings file location
        base_dir = os.path.dirname(os.path.abspath(settings_path))
        if script_dir:
            script_dir = os.path.abspath(os.path.join(base_dir, script_dir))
        if output_dir:
            output_dir = os.path.abspath(os.path.join(base_dir, output_dir))
    return script_dir, output_dir


SETTINGS_FILE = app_arguments()
SCRIPT_DIR, OUTPUT_DIR = settings_read(SETTINGS_FILE)


# Main
#---------------------------------------------

if __name__ == "__main__":
    if not SCRIPT_DIR or not OUTPUT_DIR:
        print("SCRIPT_DIR or OUTPUT_DIR not set in settings.json")
        exit(1)
    if not os.path.exists(SCRIPT_DIR):
        print(f"Script directory does not exist: '{SCRIPT_DIR}'")
        exit(1)
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    for filename in os.listdir(SCRIPT_DIR):
        if filename.lower().endswith(".psc"):
            script_path = os.path.join(SCRIPT_DIR, filename)
            script_name = os.path.splitext(filename)[0]
            output_file_name = f"{script_name}.wiki"
            output_directory = os.path.join(OUTPUT_DIR, script_name)
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)
            output_path = os.path.join(output_directory, output_file_name)
            try:
                wiki.page.write(script_path, output_path)
                print(f"{script_name}:\n  -> in:  {script_path}\n  -> out: {output_path}")
            except Exception as e:
                print(f"Error processing '{script_path}': {e}")
