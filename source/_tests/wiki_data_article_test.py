import unittest
from wiki.data.article import Article, Category, Namespace

class TestArticle(unittest.TestCase):


    def test_creation(self) -> None:
        """Test Article creation and properties."""
        article:Article = Article()
        article.name = "Test Page"
        article.namespace = Namespace.Main

        self.assertEqual(article.name, "Test Page")
        self.assertEqual(article.namespace, "Main")
        self.assertEqual(article.title, "Main:Test Page")
        self.assertEqual(article.link, "[[Main:Test Page]]")



    def test_namespace_empty(self) -> None:
        """Test Article with empty namespace."""
        article:Article = Article()
        article.name = "Home Page"
        article.namespace = Namespace.Empty

        self.assertEqual(article.title, "Home Page")
        self.assertEqual(article.link, "[[Home Page]]")



    def test_name_empty(self) -> None:
        """Test Article with empty name."""
        article:Article = Article()
        article.name = ""
        article.namespace = Namespace.Main

        self.assertEqual(article.title, "Main:")
        self.assertEqual(article.link, "[[Main:]]")



    def test_name_special_characters(self) -> None:
        """Test Article with special characters in name."""
        article:Article = Article()
        article.name = "Test Page: With Symbols & More"
        article.namespace = Namespace.Main

        self.assertEqual(article.title, "Main:Test Page: With Symbols & More")
        self.assertEqual(article.link, "[[Main:Test Page: With Symbols & More]]")



    def test_content_and_categories(self) -> None:
        """Test Article content and category management."""
        article:Article = Article()
        article.name = "TestArticle"
        article.content = [
            "Line 1",
            "Line 2",
            "Line 3"
        ]

        # Add a category
        category:Category = Category()
        category.name = "TestCategory"
        article.categories.append(category)

        self.assertEqual(len(article.content), 3)
        self.assertEqual(len(article.categories), 1)
        self.assertEqual(article.categories[0].name, "TestCategory")



    def test_compose(self) -> None:
        """Test Article composition with content and categories."""
        article:Article = Article()
        article.name = "TestPage"
        article.content = [
            "Some content",
            "More content"
        ]

        # Add categories
        category1:Category = Category()
        category1.name = "Category1"

        category2:Category = Category()
        category2.name = "Category2"

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
        article:Article = Article()
        article.name = "EmptyPage"

        # Compose the text content.
        composed:list[str] = article.compose()

        self.assertEqual(len(composed), 1)  # Just the newline
        self.assertEqual(composed[0], "\n")



    def test_compose_formatting(self) -> None:
        """Test compose produces correct MediaWiki format."""
        article:Article = Article()
        article.name = "TestPage"
        article.content = [
            "First line",
            "Second line"
        ]

        category = Category()
        category.name = "TestCat"
        article.categories.append(category)

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
