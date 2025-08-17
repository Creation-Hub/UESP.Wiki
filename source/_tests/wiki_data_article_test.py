import unittest
from wiki.data.title import Title
from wiki.data.namespaces import Namespace
from wiki.data.common import Namespaces
from scribe.publisher.article import Article

class TestArticle(unittest.TestCase):

    def test_new_page(self) -> None:
        article:Article = Article(Title("Test Page", Namespaces.Main))
        # Assert
        self.assertEqual(article.title.name, "Test_Page")
        self.assertEqual(article.title.namespace.name, "")
        self.assertEqual(article.title.value, "Test_Page")
        self.assertEqual(article.title.link, "[[Test_Page]]")


    def test_new_category(self) -> None:
        article:Article = Article(Title("Test Category", Namespaces.Category))
        # Assert
        self.assertEqual(article.title.name, "Test_Category")
        self.assertEqual(article.title.namespace.name, "Category")
        self.assertEqual(article.title.value, "Category:Test_Category")
        self.assertEqual(article.title.link, "[[Category:Test_Category]]")
        self.assertEqual(article.title.link_visible, "[[:Category:Test_Category|Test Category]]")


    def test_new_template(self) -> None:
        article:Article = Article(Title("Test Template", Namespaces.Template))
        # Assert
        self.assertEqual(article.title.name, "Test_Template")
        self.assertEqual(article.title.namespace.name, "Template")
        self.assertEqual(article.title.value, "Template:Test_Template")
        self.assertEqual(article.title.link, "[[Template:Test_Template]]")


    def test_name_empty(self) -> None:
        """Test Article with empty name raises an error."""
        with self.assertRaises(ValueError):
            _ = Article(Title("", Namespaces.Main))


    def test_namespace(self) -> None:
        article:Article = Article(Title(" Test Page: With Symbols & More", Namespace("Starfield_Mod", "SFM")))
        # Assert
        self.assertEqual(article.title.name, "_Test_Page:_With_Symbols_&_More")
        self.assertEqual(article.title.namespace.name, "Starfield_Mod")
        self.assertEqual(article.title.value, "Starfield_Mod:_Test_Page:_With_Symbols_&_More")
        self.assertEqual(article.title.link, "[[SFM:_Test_Page:_With_Symbols_&_More]]")


    def test_namespace_empty(self) -> None:
        """Test Article with empty namespace."""
        article:Article = Article(Title("Home Page", Namespace("")))
        # Assert
        self.assertEqual(article.title.value, "Home_Page")
        self.assertEqual(article.title.link, "[[Home_Page]]")


    def test_content_and_categories(self) -> None:
        """Test Article content and category management."""
        article:Article = Article(Title("TestArticle", Namespaces.Main))
        article.content = [
            "Line 1",
            "Line 2",
            "Line 3"
        ]

        # Add a category
        article.categories.append(Title("TestCategory", Namespaces.Category))

        self.assertEqual(len(article.content), 3)
        self.assertEqual(len(article.categories), 1)
        self.assertEqual(article.categories[0].name, "TestCategory")


    def test_compose(self) -> None:
        """Test Article composition with content and categories."""
        article:Article = Article(Title("TestPage", Namespaces.Main))
        article.content = [
            "Some content",
            "More content"
        ]

        # Add categories
        category1:Title = Title("Category1", Namespaces.Category)
        category2:Title = Title("Category2", Namespaces.Category)
        article.categories.extend([category1, category2])

        # Compose the text content.
        composed:list[str] = article.compose()

        # Should have content + newline + categories + newlines
        self.assertIn("Some content", composed)
        self.assertIn("More content", composed)
        self.assertIn("[[Category:Category1]]", composed)
        self.assertIn("[[Category:Category2]]", composed)


    def test_compose_empty(self) -> None:
        """Test compose with no content or categories."""
        article:Article = Article(Title("EmptyPage", Namespaces.Main))

        # Compose the text content.
        composed:list[str] = article.compose()

        self.assertEqual(len(composed), 1)  # Just the newline
        self.assertEqual(composed[0], "\n")


    def test_compose_formatting(self) -> None:
        """Test compose produces correct MediaWiki format."""
        article:Article = Article(Title("TestPage", Namespaces.Main))
        article.content = [
            "First line",
            "Second line"
        ]

        article.categories.append(Title("TestCat", Namespaces.Category))

        # Compose the text content.
        composed:list[str] = article.compose()

        # Check structure: content + newline + categories + newlines
        self.assertEqual(composed[0], "First line")
        self.assertEqual(composed[1], "Second line")
        self.assertEqual(composed[2], "\n")
        self.assertEqual(composed[3], "[[Category:TestCat]]")
        self.assertEqual(composed[4], "\n")



# Unit Test Runner
#---------------------------------------------

if __name__ == "__main__":
    _ = unittest.main()
