import os
from typing import Any

class JSON:
    """Utility class for JSON operations."""

    # TODO: UNUSED: Consider for deletion.
    @staticmethod
    def decode_path_absolute(data:dict[str, Any], property:str, directory:str) -> str:
        path:str = data.get(property, "")
        if not path: return ""
        elif os.path.isabs(path): return path
        else: return os.path.join(directory, path)
