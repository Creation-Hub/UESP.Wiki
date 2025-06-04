import os
from . import parser
from . import code
from . import normalize
from app import papyrus
from app.papyrus.code import Script


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


# Generator
#---------------------------------------------

def read(targets: list) -> list[Script]:
    context = []
    for target_name, script_dir, output_dir, output_sort, output_objects, output_members in targets:
        paths = papyrus.find_files(script_dir)
        for path in paths:
            script:Script = papyrus.parser.parse(path)
            context.append(script)
    return context
