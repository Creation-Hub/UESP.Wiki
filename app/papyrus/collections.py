from typing import Iterator
from typing import List
from typing import Dict
from typing import Optional
from app.papyrus.code import Script


# Specialized
#---------------------------------------------

class ScriptDictionary:
    """
    A keyed collection for Script objects.
    """

    def __init__(self):
        self._scripts:Dict[str, Script] = {}

    def __str__(self) -> str:
        """Gets the string representation of this collection."""
        return f"ScriptDictionary({len(self._scripts)} scripts)"

    def key(self, script:Script) -> str:
        """Gets the key for this script value."""
        return str(script.header.name).upper()

    def add(self, script:Script) -> None:
        """Adds a script to this collection."""
        key:str = self.key(script)
        self._scripts[key] = script

    def get(self, name:str) -> Optional[Script]:
        """Get a script by name (case-insensitive)"""
        key:str = name.upper()
        return self._scripts.get(key)

    def __getitem__(self, name:str) -> Script:
        """Allow dictionary-like sub-script key access: scripts['Actor']"""
        key:str = name.upper()
        if key not in self._scripts:
            raise KeyError(f"Script '{name}' not found")
        return self._scripts[key]

    def __contains__(self, name:str) -> bool:
        """Allow 'in' operator: 'Actor' in scripts."""
        return name.upper() in self._scripts

    def __len__(self) -> int:
        """Return the number of scripts in this collection."""
        return len(self._scripts)

    def __iter__(self) -> Iterator[Script]:
        """Iterate over all scripts in this collection."""
        return iter(self._scripts.values())

    def keys(self) -> List[str]:
        """Return all keys within this collection."""
        return list(self._scripts.keys())

    def values(self) -> List[Script]:
        """Return all script objects in this collection."""
        return list(self._scripts.values())

    def clear(self) -> None:
        """Remove all scripts from this collection."""
        self._scripts.clear()

    def names(self) -> List[str]:
        """Return all script names within this collection."""
        return [str(script.header.name) for script in self._scripts.values()]
