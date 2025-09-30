from typing import final
from papyrus.code import Script
from scribe.services.composer import ComposerService
from wiki.data.common import Namespaces
from wiki.data.title import Title, Namespace
from wiki.data.formatting import Text
from wiki.data.section import SectionLevel
from .wiki import Wiki
from .article import Article

@final
class ArticleBuilder:

    def __init__(self, composer:ComposerService) -> None:
        super().__init__()
        self._composer:ComposerService = composer
        self._title:Title|None = None
        self._categories:list[Title] = []
        self._content:list[str] = []


    def title(self, name:str, namespace:Namespace) -> 'ArticleBuilder':
        self._title = Title(name, namespace)
        return self


    def category(self, title:Title) -> 'ArticleBuilder':
        self._categories.append(title)
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

        return article



# Example Usage:
def create_script_page(composer:ComposerService, script:Script) -> Article:
    return (ArticleBuilder(composer)
        .title(f"Script-{script.name}", Wiki.SFM_NAMESPACE)
        .section("Definition", SectionLevel.H2)
        .lines([
            f"<source lang=\"papyrus\">",
            f"{script.header.definition}",
            f"</source>"
        ])
        .section("Documentation", SectionLevel.H2)
        .line(script.header.documentation or "No documentation provided.")
        .category(Title("Starfield_Mod-Papyrus", Namespaces.Category))
        .build()
    )
