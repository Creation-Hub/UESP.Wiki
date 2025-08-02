from scribe.wiki.data.article import Article

class Category(Article):
    """
    Represents a MediaWiki category type.
    """
    def __init__(self) -> None:
        super().__init__()


    @staticmethod
    def create(file_path:str) -> 'Category':
        raise NotImplementedError("Category creation is not implemented yet.")
        this:Category = Category()
        this.file_path = file_path
        return this
