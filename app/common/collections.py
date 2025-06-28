from typing import Iterator
from typing import List
from typing import Dict
from typing import Generic, TypeVar, Optional


# Keyed
#---------------------------------------------

class KeyedObject:
    """
    Represents an object with a unique identifying key.
    The key is for use with `KeyedCollections`.
    """
    def __init__(self, key:str):
        self._key = key

    def __str__(self) -> str:
        """Returns a string that represents the current object."""
        return self._key

    def __repr__(self) -> str:
        """Returns a string that represents the current object."""
        return self.__str__()

    @property
    def key(self) -> str:
        return self._key


T = TypeVar('T', bound=KeyedObject)
class KeyedCollection(Generic[T]):
    """
    Provides a dictionary-like collection for objects whose keys are embedded in the values.
    """
    def __init__(self):
        self._items:Dict[str, T] = {}

    def __str__(self) -> str:
        """Gets the string representation of this collection."""
        return f"{KeyedCollection.__name__}({len(self._items)})"

    def __repr__(self) -> str:
        """Gets the string representation of this collection."""
        return self.__str__()

    def add(self, item:T) -> None:
        """Adds an item to this collection."""
        key:str = item.key.upper()
        self._items[key] = item

    def get(self, key:str) -> Optional[T]:
        """Get an item by key (case-insensitive)"""
        key = key.upper()
        return self._items.get(key)

    def __getitem__(self, key:str) -> T:
        """
        Provides item access by key through dictionary sub-script notation.

        Example: `items['MyItem']`
        """
        key = key.upper()
        if key not in self._items:
            raise KeyError(f"Item '{key}' not found")
        return self._items[key]

    def __contains__(self, key:str) -> bool:
        """Provides support for the 'in' Python operator."""
        return key.upper() in self._items

    def __len__(self) -> int:
        """Gets the number of items in this collection."""
        return len(self._items)

    def __iter__(self) -> Iterator[T]:
        """Provides support for item value iteration in this collection."""
        return iter(self._items.values())

    def keys(self) -> List[str]:
        """Gets a copy of all keys in this collection."""
        return list(self._items.keys())

    def values(self) -> List[T]:
        """Gets a copy of all items in this collection."""
        return list(self._items.values())

    def clear(self) -> None:
        """Remove all identifiers from this collection."""
        self._items.clear()
