import unittest
from wiki.data.title import Title
from wiki.data.namespaces import Namespace


class TestTitle(unittest.TestCase):

    def test_new(self) -> None:
        title:Title = Title("Hello World!", Namespace("Test Namespace", "NS TEST"))
        self.assertEqual(title.name, "Hello_World!")
        self.assertEqual(title.display, "Hello World!")
        self.assertEqual(title.namespace.name, "Test_Namespace")
        self.assertEqual(title.namespace.alias, "NS_TEST")
        self.assertEqual(title.link, "[[NS_TEST:Hello_World!]]")
        self.assertEqual(title.value, "Test_Namespace:Hello_World!")
        self.assertEqual(str(title), "Hello World!")


    def test_name_empty(self) -> None:
        """Test empty name raises an error."""
        with self.assertRaises(ValueError):
            _ = Title("")


    def test_equals(self) -> None:
        title1:Title = Title("Title 1", Namespace("Namespace 1", "N1"))
        title2:Title = Title("Title 1", Namespace("Namespace 1", "N1"))
        self.assertEqual(title1, title2)



class TestNamespace(unittest.TestCase):

    def test_new_none(self) -> None:
        namespace:Namespace = Namespace("", None)
        self.assertEqual(namespace.name, "")
        self.assertIsNone(namespace.alias)


    def test_new_empty(self) -> None:
        namespace:Namespace = Namespace("", "")
        self.assertEqual(namespace.name, "")
        self.assertEqual(namespace.alias, "")


    def test_alias(self) -> None:
        namespace:Namespace = Namespace("Test_Namespace", "NS_TEST")
        self.assertEqual(namespace.name, "Test_Namespace")
        self.assertEqual(namespace.alias, "NS_TEST")


    def test_alias_with_name_empty(self) -> None:
        namespace:Namespace = Namespace("", "NS_TEST")
        self.assertEqual(namespace.name, "")
        self.assertEqual(namespace.alias, "NS_TEST")



# Unit Test Runner
#---------------------------------------------

if __name__ == "__main__":
    _ = unittest.main()
