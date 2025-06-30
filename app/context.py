from typing import Any, Dict
from app.project import PapyrusProject

# Context
#---------------------------------------------

class AppContext:
    def __init__(self):
        self.base_directory:str = ""
        """The base directory of the settings file."""

        self.export_directory:str = ""
        """The export directory for wiki pages."""

        self.publish_info:dict[str, Any] = {}
        """Information about the game and editor for publishing."""

        self.projects:Dict[str, PapyrusProject] = {}
        """A list of Papyrus projects defined in the application settings file."""

    def add(self, project:PapyrusProject):
        """Adds a project to the application context."""
        self.projects[project.identifier] = project
