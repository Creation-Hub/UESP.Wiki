import os
from . import parser
from . import code
from . import normalize

# Files
#---------------------------------------------

def find_files(directory: str) -> list[str]:
    """Searches for Papyrus scripts in the given Papyrus root import directory."""
    search = []
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name.lower().endswith(".psc"):
                search.append(os.path.join(root, file_name))
    return search
