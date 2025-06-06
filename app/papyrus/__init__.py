import os
from enum import Enum
from . import parser
from . import code
from . import normalize
from app import papyrus
from app.papyrus.code import Script


class Sort(Enum):
    DEFAULT = 1
    FLAT = 2
    TREE = 3


class Project:
    name: str = ""
    root: str = ""
    output: str = ""
    scripts: list[Script] = []
    option_publish_enabled: bool = False
    option_publish_sort: Sort = Sort.DEFAULT
    option_publish_objects: bool = False
    option_publish_members: bool = False


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
