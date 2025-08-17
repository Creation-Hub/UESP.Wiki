"""
Provides a dictionary-like collection for objects whose keys are embedded in the values.
"""
from abc import abstractmethod
from collections.abc import Callable, Iterator
from typing import Generic, TypeVar, override

TKey = TypeVar('TKey')
TValue = TypeVar('TValue')
class KeyedCollection(Generic[TKey, TValue]):
    """
    A dictionary-like collection for objects whose keys are embedded in the values.
    Provides a flexible keyed collection supporting two key extraction strategies.
    """


    def __init__(self, items:list[TValue]|None = None, key_extract:Callable[[TValue], TKey]|None = None) -> None:
        super().__init__()

        self._items:dict[TKey, TValue] = {}
        """The internal dictionary of items."""

        self._key_extract:Callable[[TValue], TKey]|None = key_extract
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

    def _get_key(self, item:TValue) -> TKey:
        """
        Extracts a key from the provided item using an appropriate strategy.

        Implementation Strategy:
        1. Uses the provided `key_extract` lambda function.
        2. Uses the abstract `key_for()` method as implemented by subclasses.
        """
        if self._key_extract:
            return self._key_extract(item)
        else:
            return self.key_for(item)


    @abstractmethod
    def key_for(self, item:TValue) -> TKey:
        """
        Abstract method for collections that define their own key extraction logic.

        **Override this method in subclasses for custom key extraction.**
        """
        raise NotImplementedError(
            f"Cannot extract key from {type(item).__name__}. " +
            "Provide constructor with `key_extract` lambda function or override this `key_for()` method in an extending class."
        )


    # Access Methods
    #---------------------------------------------

    def get(self, key:TKey) -> TValue|None:
        """Get an item by key."""
        return self._items.get(key)

    def __getitem__(self, key:TKey) -> TValue:
        """Provides item access by key through dictionary sub-script notation."""
        if key not in self._items:
            raise KeyError(f"Item '{key}' not found")
        return self._items[key]

    def __contains__(self, key:TKey) -> bool:
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

    def __iter__(self) -> Iterator[TValue]:
        """Provides support for item value iteration in this collection."""
        return iter(self._items.values())


    # Collection Operations
    #---------------------------------------------

    def keys(self) -> list[TKey]:
        """Gets a copy of all keys in this collection."""
        return list(self._items.keys())

    def values(self) -> list[TValue]:
        """Gets a copy of all items in this collection."""
        return list(self._items.values())

    def items(self) -> list[tuple[TKey, TValue]]:
        """Gets the key-value pairs for this collection."""
        return list(self._items.items())


    # Mutation Methods
    #---------------------------------------------

    def add(self, item:TValue) -> None:
        """Adds an item to this collection."""
        key:TKey = self._get_key(item)
        if key in self._items:
            raise KeyError(f"Item with key '{key}' already exists")
        self._items[key] = item

    def update(self, other:'KeyedCollection[TKey, TValue]') -> None:
        """Add all items from the given collection to this collection"""
        for item in other:
            self.add(item)

    def remove(self, key:TKey) -> bool:
        """Removes an item from this collection by key."""
        if key in self._items:
            del self._items[key]
            return True
        return False

    def clear(self) -> None:
        """Remove all identifiers from this collection."""
        self._items.clear()
