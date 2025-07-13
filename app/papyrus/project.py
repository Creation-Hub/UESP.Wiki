import logging
import os
from app.papyrus.code import Script
from app.papyrus.collections import ScriptDictionary
from app.papyrus.text import FileReader


# Files
#---------------------------------------------

def find_files(directory:str) -> list[str]:
    """Searches for Papyrus scripts in the given Papyrus root import directory."""
    search:list[str] = []
    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.lower().endswith(".psc"):
                search.append(os.path.join(root, file_name))
    return search


# Project
#---------------------------------------------

class PapyrusProject:
    def __init__(self) -> None:
        self.identifier:str = ""
        """The project identifier is used for Papyrus imports."""

        self.root:str = ""
        """The root directory of the project containing Papyrus scripts."""

        self.imports:list[str] = []
        """A list of other project identifiers to import scripts from."""

        self.scripts:ScriptDictionary = ScriptDictionary()
        """A list of Papyrus scripts in this project."""


    def load(self) -> bool:
        """
        Loads the Papyrus scripts from the project root directory.
        Returns:
            bool: `True` if scripts were loaded successfully, `False` otherwise.
        """
        # Clear any existing scripts.
        self.scripts.clear()

        # Parser: Search for source files in the project script directory.
        paths:list[str] = find_files(self.root)
        if not paths:
            logging.error(f"[{self.identifier}] No scripts found in '{self.root}'")
            return False

        # Parser: Deserialize each source file into application data.
        for path in paths:
            # Start parsing the script file.
            reader:FileReader = FileReader(path)
            script:Script = reader.read()
            if script:
                self.scripts.add(script)
                logging.debug(f"[{self.identifier}] Added '{path}'")
            else:
                logging.error(f"[{self.identifier}] Failed '{path}'")
                return False

        logging.info(f"[{self.identifier}] Loaded ({len(self.scripts)} of {len(paths)}) scripts from '{self.root}'")
        return True


# Context
#---------------------------------------------

class PapyrusContext:
    def __init__(self) -> None:
        self.projects:dict[str, PapyrusProject] = {}


    def add(self, project:PapyrusProject) -> None:
        """Adds a project to the Papyrus context."""
        self.projects[project.identifier] = project


    def _valid_imports(self, project:PapyrusProject) -> bool:
        for imported in project.imports:
            if imported not in self.projects:
                logging.error(f"[{project.identifier}] The imported '{imported}' project dependency does not exist.")
                return False
        return True


    def load(self) -> bool:
        if not self.projects:
            logging.warning("No projects found in this Papyrus context.")
            return False

        for project in self.projects.values():
            if not self._valid_imports(project):
                logging.error(f"[{project.identifier}] There was a problem with one or more imported projects.")
                return False

            if not project.load():
                logging.error(f"[{project.identifier}] Failed to load project scripts.")

        return True
