import logging
import os
from .code import Script
from .collections import ScriptDictionary
from .text.parsing import FileReader

class PapyrusProject:
    def __init__(self) -> None:
        super().__init__()

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
        paths:list[str] = PapyrusProject.find_files(self.root)
        if not paths:
            logging.error(f"[{self.identifier}] No scripts found in '{self.root}'")
            return False

        # Parser: Deserialize each source file into application data.
        for path in paths:
            # Start parsing the script file.
            reader:FileReader = FileReader(path)
            script:Script = reader.read()
            self.scripts.add(script)
            logging.debug(f"[{self.identifier}] Added '{path}'")

        logging.info(f"[{self.identifier}] Loaded ({len(self.scripts)} of {len(paths)}) scripts from '{self.root}'")
        return True


    @staticmethod
    def find_files(directory:str) -> list[str]:
        """Searches for Papyrus scripts in the given Papyrus root import directory."""
        search:list[str] = []
        for root, _, files in os.walk(directory):
            for file_name in files:
                if file_name.lower().endswith(".psc"):
                    search.append(os.path.join(root, file_name))
        return search
