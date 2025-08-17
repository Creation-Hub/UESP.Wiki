"""
`testing/sharp_collections_test.py`
Unit tests for the `sharp.collections` module.
"""
import unittest
from typing import override
from sharp.collections import KeyedCollection


class TestKeyedCollection(unittest.TestCase):
    """Test cases for KeyedCollection functionality."""


    # Implementation Patterns
    #---------------------------------------------

    def test_imp_lambda_key(self) -> None:
        """Test function-based key extraction for built-in types."""

        names:KeyedCollection[str, str] = KeyedCollection[str, str](key_extract=lambda item: item.upper())
        names.add("Name1")
        names.add("Name2")

        self.assertEqual(len(names), 2)
        # Keys are upper cased
        self.assertIn("NAME1", names)
        self.assertIn("NAME2", names)


    def test_imp_lambda_key_complex(self) -> None:
        """Test function-based key extraction for complex objects."""

        class MyScriptHeader:
            def __init__(self, name:str = "") -> None:
                super().__init__()
                self.name:str = name

        class MyScript:
            def __init__(self, name:str = "") -> None:
                super().__init__()
                self.header:MyScriptHeader = MyScriptHeader(name)

        scripts:KeyedCollection[str, MyScript] = KeyedCollection[str, MyScript](key_extract=lambda item: str(item.header.name))

        script:MyScript = MyScript("TestScript")
        scripts.add(script)

        self.assertEqual(len(scripts), 1)
        self.assertIn("TestScript", scripts)


    def test_imp_inherit(self) -> None:
        """Test the abstract sub-classing pattern."""

        class MyItem:
            def __init__(self, name:str = "") -> None:
                super().__init__()
                self.name:str = name

        class MyItemCollection(KeyedCollection[str, MyItem]):
            @override
            def key_for(self, item:MyItem) -> str:
                return str(item.name)

        some_items:MyItemCollection = MyItemCollection()
        item:MyItem = MyItem("test_item")  # Give it a proper name
        some_items.add(item)

        self.assertEqual(len(some_items), 1)
        self.assertIn("test_item", some_items)


    # Keys
    #---------------------------------------------

    def test_key_empty_allowed(self) -> None:
        """Test that empty string keys are allowed."""

        class MyItem:
            def __init__(self, name:str = "") -> None:
                super().__init__()
                self.name:str = name

        class MyItemCollection(KeyedCollection[str, MyItem]):
            @override
            def key_for(self, item:MyItem) -> str:
                return str(item.name)

        some_items:MyItemCollection = MyItemCollection()
        empty_item:MyItem = MyItem("")  # Empty name

        # This should NOT raise an exception
        some_items.add(empty_item)

        # Verify the empty key item was added successfully
        self.assertEqual(len(some_items), 1)
        self.assertIn("", some_items)
        self.assertEqual(some_items.get(""), empty_item)
        self.assertEqual(some_items[""], empty_item)


    def test_key_duplicate_error(self) -> None:
        """Test that duplicate keys raise appropriate errors."""

        class MyItem:
            def __init__(self, key:str) -> None:
                super().__init__()
                self.key:str = key

        items:KeyedCollection[str, MyItem] = KeyedCollection[str, MyItem](key_extract=lambda o: o.key)
        item1:MyItem = MyItem("duplicate_key")
        item2:MyItem = MyItem("duplicate_key")

        items.add(item1)

        with self.assertRaises(KeyError) as context:
            items.add(item2)

        self.assertIn("already exists", str(context.exception))


    def test_key_retrieval(self) -> None:
        """Test various ways to retrieve items by key."""

        items:KeyedCollection[str, str] = KeyedCollection[str, str](key_extract=lambda o: o)
        items.add("test_item")

        # Test get() with existing key
        self.assertEqual(items.get("test_item"), "test_item")

        # Test get() with non-existing key
        self.assertIsNone(items.get("nonexistent"))

        # Test __getitem__ with existing key
        self.assertEqual(items["test_item"], "test_item")

        # Test __getitem__ with non-existing key raises KeyError
        with self.assertRaises(KeyError):
            _ = items["nonexistent"]


    def test_key_preserve_case_sensitivity(self) -> None:
        """Test that keys are case-sensitive by default (no auto-upper-casing)."""

        items:KeyedCollection[str, str] = KeyedCollection[str, str](key_extract=lambda o: o)
        items.add("Test")
        items.add("test")  # Should be allowed - different keys
        items.add("TEST")  # Should be allowed - different keys

        self.assertEqual(len(items), 3)
        self.assertIn("Test", items)
        self.assertIn("test", items)
        self.assertIn("TEST", items)

        # Verify they're actually different
        self.assertNotEqual(items.get("Test"), items.get("test"))


# Unit Test Runner
#---------------------------------------------

if __name__ == "__main__":
    _ = unittest.main()
