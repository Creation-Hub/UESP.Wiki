"""
Provides a dictionary-like collection for objects whose keys are embedded in the values.
Supports both intrinsic and extrinsic key strategies.
"""
from abc import ABC, abstractmethod
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from typing import Generic, TypeVar, override


@dataclass(frozen=True)
class KeyedObject:
    """
    Represents an object that provides a unique identifying key.
    The key is for use with a `KeyedCollection[T]` dictionary abstraction.
    Used to support the intrinsic key strategy for `KeyedCollection`.
    """

    _key:str
    """The unique key for this object."""

    @override
    def __str__(self) -> str:
        """Returns a string that represents the current object."""
        return self._key

    @property
    def key(self) -> str:
        return self._key


T = TypeVar('T')
class KeyedCollection(Generic[T]):
    """
    A dictionary-like collection for objects whose keys are embedded in the values.
    Provides a flexible keyed collection supporting both intrinsic and extrinsic key strategies.
    """
    def __init__(self, items:list[T]|None = None, key_extract:Callable[[T], str]|None = None) -> None:
        super().__init__()

        self._items:dict[str, T] = {}
        """The internal dictionary of items."""

        self._key_extract:Callable[[T], str]|None = key_extract
        """Optional function to extract a key from an item."""

        if items: # Initialize with any provided list items.
            for item in items:
                self.add(item)


    @override
    def __str__(self) -> str:
        """Returns a string that represents the current object."""
        return f"{KeyedCollection.__name__}({len(self._items)})"

    @override
    def __repr__(self) -> str:
        """Provides the debugger representation of this object."""
        return f"KeyedCollection({list(self._items.keys())})"


    # Keys
    #---------------------------------------------

    def _get_key(self, item:T) -> str:
        """Extracts a key from the provided item using an appropriate strategy."""
        if isinstance(item, KeyedObject):
            return item.key
        elif self._key_extract:
            return self._key_extract(item)
        else:
            raise ValueError(
                f"Item of type {type(item)} is not a `KeyedObject` and no `key_extract` provided"
            )

    # Access Methods
    #---------------------------------------------

    def get(self, key:str) -> T | None:
        """Get an item by key."""
        return self._items.get(key)

    def __getitem__(self, key:str) -> T:
        """Provides item access by key through dictionary sub-script notation."""
        if key not in self._items:
            raise KeyError(f"Item '{key}' not found")
        return self._items[key]

    def __contains__(self, key:str) -> bool:
        """Provides support for the 'in' Python operator."""
        return key in self._items


    # Iteration Support
    #---------------------------------------------

    def __len__(self) -> int:
        """Gets the number of items in this collection."""
        return len(self._items)

    def __bool__(self) -> bool:
        """Provides support for `if collection:` checks."""
        return len(self._items) > 0

    def __iter__(self) -> Iterator[T]:
        """Provides support for item value iteration in this collection."""
        return iter(self._items.values())


    # Collection Operations
    #---------------------------------------------

    def keys(self) -> list[str]:
        """Gets a copy of all keys in this collection."""
        return list(self._items.keys())

    def values(self) -> list[T]:
        """Gets a copy of all items in this collection."""
        return list(self._items.values())

    def items(self) -> list[tuple[str, T]]:
        """Gets the key-value pairs for this collection."""
        return list(self._items.items())


    # Mutation Methods
    #---------------------------------------------

    def add(self, item:T) -> None:
        """Adds an item to this collection."""
        key:str = self._get_key(item)
        if not key:
            raise ValueError("Cannot add item with empty key")
        elif key in self._items:
            raise KeyError(f"Item with key '{key}' already exists")
        self._items[key] = item

    def update(self, other:'KeyedCollection[T]') -> None:
        """Add all items from the given collection to this collection"""
        for item in other:
            self.add(item)

    def remove(self, key:str) -> bool:
        """Removes an item from this collection by key."""
        if key in self._items:
            del self._items[key]
            return True
        return False

    def clear(self) -> None:
        """Remove all identifiers from this collection."""
        self._items.clear()



class KeyedCollectionAbstract(KeyedCollection[T], ABC):
    """
    Abstract base for collections that define their own key extraction logic.
    Used to support the extrinsic key strategy via subclassing.
    """

    def __init__(self, items:list[T]|None = None) -> None:
        # Don't pass `key_extract` function, override with `_get_key` instead.
        super().__init__(items, None)

    @abstractmethod
    def key_for(self, item:T) -> str:
        """Extract key from the given item. Override this method."""
        raise NotImplementedError("Subclasses must implement the `key_for()` method.")

    @override
    def _get_key(self, item:T) -> str:
        """Use the subclass-defined key extraction."""
        return self.key_for(item)
