import logging
import os
import json
from enum import Enum
from typing import Any
from app.papyrus.code import Script

# Types
#---------------------------------------------

class Sort(Enum):
    DEFAULT = 1
    FLAT = 2
    TREE = 3


# Changes the base output directory path to sort into script name folders.
# option_publish_sort:
#   Default: `Base-Native\MyNamespace\Action.wiki`
#   Flat:    `Base-Native\MyNamespace-Action.wiki`
#   Tree:    `Base-Native\MyNamespace\Action\Action.wiki`
class AppProject:
    def __init__(self):
        self.name:str = ""
        self.root:str = ""
        self.output:str = ""
        self.option_publish_sort:Sort = Sort.DEFAULT
        self.option_publish_enable:bool = False
        self.option_publish_enable_objects:bool = False
        self.option_publish_enable_members:bool = False
        self.scripts:list[Script] = []


class AppSettings:
    def __init__(self):
        self.base_dir:str = ""
        self.publish_info:dict[str, Any] = {}
        self.projects:list[AppProject] = []


# Data
#---------------------------------------------

# TODO: Add support for full paths specified in json. Only resolve paths without a drive letter.
def path_resolve(directory:str, path:str) -> str:
    if path: return os.path.abspath(os.path.join(directory, path))
    else: return path


def get_property_path(data:dict[str, Any], property:str, directory:str) -> str:
    value = data.get(property, None)
    if value: return path_resolve(directory, value)
    else: return ""


def get_property_sort(data:dict[str, Any]) -> Sort:
    value = data.get("output.sort", "DEFAULT")
    if value is None: value = "DEFAULT"
    try: return Sort[value.upper()]
    except KeyError: return Sort.DEFAULT


def read_project(data_project:dict[str, Any], base_dir:str) -> AppProject:
    project:AppProject = AppProject()
    project.name = data_project.get("name", "UNNAMED")
    project.root = get_property_path(data_project, "source.directory", base_dir)
    project.output = get_property_path(data_project, "output.directory", base_dir)
    project.option_publish_enable = data_project.get("output.enabled", False)
    project.option_publish_sort = get_property_sort(data_project)
    project.option_publish_enable_objects = data_project.get("output.objects", False)
    project.option_publish_enable_members = data_project.get("output.members", False)
    return project


# Settings
#---------------------------------------------

def read(settings_file_path:str):
    """
    Reads application settings file.

    Returns (publish_info, targets) where:
      - base_dir: the base directory of the settings file
      - publish_info: dict with 'game' and 'editor' info
      - projects: a list of Project information classes
    """
    settings:AppSettings = AppSettings()
    settings.base_dir = os.path.dirname(os.path.abspath(settings_file_path))
    settings.publish_info = {}
    settings.projects = []

    if os.path.exists(settings_file_path):
        with open(settings_file_path, encoding="utf-8") as file:
            data:dict[str, Any] = json.load(file)
            logging.debug(f"Read settings file: {settings_file_path}")

        settings.publish_info = data.get("publish", {})

        for data_project in data.get("projects", []):
            project:AppProject = read_project(data_project, settings.base_dir)
            settings.projects.append(project)
    return settings
