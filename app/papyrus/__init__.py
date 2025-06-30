import os
from . import parser # type: ignore # noqa: F401
from . import code # type: ignore # noqa: F401
from . import normalize # type: ignore # noqa: F401


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
