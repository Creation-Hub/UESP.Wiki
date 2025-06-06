import os
import argparse
import json
from app.papyrus import Project, Sort
import logging


# Configuration
#---------------------------------------------

def configure_logging():
    # Create root logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Log File handler
    file_handler = logging.FileHandler("app.log", mode='w')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    # Console Stream handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)


# Arguments
#---------------------------------------------

def arguments():
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
    return argument_parser.parse_args()


# Settings
#---------------------------------------------

# TODO: Add support for full paths specified in json. Only resolve paths without a drive letter.
def path_resolve(directory:str, path:str) -> str:
    if path: return os.path.abspath(os.path.join(directory, path))
    else: return path

def get_property_path(data: dict, property:str, directory:str) -> str:
    value = data.get(property, None)
    if value: return path_resolve(directory, value)
    else: return ""

def get_property_sort(data: dict) -> Sort:
    value = data.get("output.sort", "DEFAULT")
    try: return Sort[value.upper()]
    except KeyError: return Sort.DEFAULT


def read(settings_path: str):
    """
    Reads application settings file.
    Returns (publish_info, targets) where:
      - base_dir: the base directory of the settings file
      - publish_info: dict with 'game' and 'editor' info
      - projects: a list of Project information classes
    """
    base_dir = ""
    publish_info = {}
    projects:list[Project] = []
    if os.path.exists(settings_path):
        with open(settings_path, encoding="utf-8") as file:
            data = json.load(file)
            base_dir = os.path.dirname(os.path.abspath(settings_path))
            publish_info = data.get("publish", {})
            for data_project in data.get("projects", []):
                project:Project = Project()
                project.name = data_project.get("name", "UNNAMED")
                project.root = get_property_path(data_project, "source.directory", base_dir)
                project.output = get_property_path(data_project, "output.directory", base_dir)
                project.option_publish_enabled = data_project.get("output.enabled", False)
                project.option_publish_sort = get_property_sort(data_project)
                project.option_publish_objects = data_project.get("output.objects", False)
                project.option_publish_members = data_project.get("output.members", False)
                projects.append(project)
    return base_dir, publish_info, projects
