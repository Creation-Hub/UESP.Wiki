from typing import Any, Dict
from app.project import PapyrusContext, PapyrusProject
from app.settings import Configuration

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

        self.configurations:Dict[str, Configuration] = {}
        self.papyrus:PapyrusContext = PapyrusContext()


    def add(self, project:PapyrusProject):
        """Adds a project to the application context."""
        self.papyrus.add(project)
