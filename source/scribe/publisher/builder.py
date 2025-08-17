from typing import final
from papyrus.code import Script
from wiki.data.common import Namespaces
from wiki.data.title import Title, Namespace
from wiki.data.formatting import Text
from wiki.data.section import SectionLevel
from scribe.publisher.wiki import Wiki
from scribe.publisher.article import Article

@final
class ArticleBuilder:

    def __init__(self, wiki:Wiki) -> None:
        super().__init__()
        self._wiki:Wiki = wiki
        self._title:Title|None = None
        self._content:list[str] = []
        self._categories:list[str] = []


    def title(self, name:str, namespace:Namespace) -> 'ArticleBuilder':
        self._title = Title(name, namespace)
        return self


    def category(self, category_name:str) -> 'ArticleBuilder':
        self._categories.append(category_name)
        return self


    def line(self, content:str) -> 'ArticleBuilder':
        self._content.append(content)
        return self


    def lines(self, content:list[str]) -> 'ArticleBuilder':
        self._content.extend(content)
        return self


    def section(self, heading:str, level:SectionLevel) -> 'ArticleBuilder':
        self._content.append(f"{Text.section(heading, level)}\n")
        return self


    def build(self) -> Article:
        if not self._title:
            raise ValueError("Article must have a title.")

        article:Article = Article(self._title)
        article.content = self._content.copy()

        # Convert category names to category titles
        for category_name in self._categories:
            category:Title = Title(category_name, Namespaces.Category)
            article.categories.append(category)

        return article



# Usage:
def create_script_page(wiki:Wiki, script:Script) -> Article:
    return (ArticleBuilder(wiki)
        .title(f"Script-{script.name}", Wiki.NAMESPACE_MODDING)
        .section("Definition", SectionLevel.H2)
        .lines([
            f"<source lang=\"papyrus\">\n",
            f"{script.header.definition}\n",
            f"</source>\n"
        ])
        .section("Documentation", SectionLevel.H2)
        .line(script.header.documentation or "No documentation provided.")
        .category("Starfield_Mod-Papyrus")
        .build()
    )
