from typing import override
from ..shared.collections import KeyedCollection, KeyedCollectionAbstract, KeyedObject


# Test
#---------------------------------------------
# The `KeyedObject` pattern.

class MyItem(KeyedObject):
    def __init__(self, key:str):
        super().__init__(key)

items:KeyedCollection[MyItem] = KeyedCollection[MyItem]()
items.add(MyItem("my_key"))


# Test
#---------------------------------------------
# The function-based key extraction pattern.

names:KeyedCollection[str] = KeyedCollection[str](key_extract=lambda item: item.upper())
names.add("Name1")
names.add("Name2")


# Test
#---------------------------------------------
# The function-based key extraction pattern for complex objects.

class MyScriptHeader:
    def __init__(self):
        super().__init__()
        self.name:str = ""

class MyScript:
    def __init__(self):
        super().__init__()
        self.header:MyScriptHeader = MyScriptHeader()

# For complex objects without KeyedObject
scripts:KeyedCollection[MyScript] = KeyedCollection[MyScript](key_extract=lambda script: str(script.header.name))


# Test
#---------------------------------------------
# The sub-classing pattern.

class SomeItem:
    def __init__(self):
        super().__init__()
        self.name:str = ""

class SomeItemCollection(KeyedCollectionAbstract[SomeItem]):
    @override
    def key_for(self, item:SomeItem) -> str:
        return str(item.name)

# Usage
some_items:SomeItemCollection = SomeItemCollection()
some_items.add(SomeItem())
