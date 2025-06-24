import logging
from typing import List
from app import papyrus
from app.papyrus.code import Script
from app.papyrus.collections import ScriptDictionary
from app.publishing import PublishOption


# Types
#---------------------------------------------

class PapyrusProject:
    def __init__(self):
        self.identifier:str = ""
        """ The project identifier is used for Papyrus imports. """
        self.root:str = ""
        """ The root directory of the project containing Papyrus scripts. """
        self.imports:List[str] = []
        """ A list of other project identifiers to import scripts from. """
        self.scripts:ScriptDictionary = ScriptDictionary()
        """ A list of Papyrus scripts in this project. """
        self.publish:PublishOption = PublishOption()
        """ Options for publishing the project scripts. """

    def load(self) -> bool:
        """ Loads the Papyrus scripts from the project root directory.
        Returns:
            bool: True if scripts were loaded successfully, False otherwise.
        """
        # Clear any existing scripts.
        self.scripts.clear()

        # Parser: Search for source files in the project script directory.
        paths = papyrus.find_files(self.root)
        if not paths:
            logging.warning(f"[{self.identifier}] No scripts found in this project.")
            return False

        # Parser: Deserialize each source file into application data.
        logging.info(f"[{self.identifier}] Loading {len(paths)} scripts for this project...")
        count:int = 0
        for path in paths:
            count += 1
            script:Script = papyrus.parser.parse(path)
            if script:
                self.scripts.add(script)
                logging.debug(f"[{self.identifier}] #{count} {script.header.name.file_path()}")
            else:
                logging.warning(f"[{self.identifier}] #{count} The script could not be parsed: {path}")

        logging.info(f"[{self.identifier}] Done loading scripts for this project. ({len(self.scripts)} of {len(paths)})")
        return True
