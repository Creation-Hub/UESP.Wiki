import logging
import os
from typing import Dict, List
from app.papyrus import source
from app.papyrus.code import Script
from app.papyrus.collections import ScriptDictionary


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
    def __init__(self):
        self.identifier:str = ""
        """The project identifier is used for Papyrus imports."""

        self.root:str = ""
        """The root directory of the project containing Papyrus scripts."""

        self.imports:List[str] = []
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
            logging.warning(f"[{self.identifier}] No scripts found in this project.")
            return False

        # Parser: Deserialize each source file into application data.
        logging.info(f"[{self.identifier}] Loading {len(paths)} scripts for this project...")
        count:int = 0
        for path in paths:
            count += 1
            # Start parsing the script file.
            script:Script = source.parse(path)
            if script:
                self.scripts.add(script)
                logging.debug(f"[{self.identifier}] #{count} {script.header.name.file_path()}")
            else:
                logging.warning(f"[{self.identifier}] #{count} The script could not be parsed: {path}")

        logging.info(f"[{self.identifier}] Done loading scripts for this project. ({len(self.scripts)} of {len(paths)})")
        return True


# Context
#---------------------------------------------

class PapyrusContext:
    def __init__(self):
        self.projects:Dict[str, PapyrusProject] = {}

    def add(self, project:PapyrusProject):
        """Adds a project to the Papyrus context."""
        self.projects[project.identifier] = project

    def load(self) -> bool:
        """Load all projects in the Papyrus context."""
        if not self.projects:
            logging.warning("No projects found in the Papyrus context.")
            return False

        for project in self.projects.values():
            if not project.load():
                logging.warning(f"[{project.identifier}] Failed to load scripts from the project root directory: '{project.root}'")

        logging.info(f"Loaded {len(self.projects)} projects in the Papyrus context.")
        return True
