from .namespaces import Namespace

class Namespaces:
    """
    Represents the built-in MediaWiki namespaces.
    """

    Main:Namespace = Namespace("")

    Media:Namespace = Namespace("Media")
    """Alias for direct links to media files."""

    Special:Namespace = Namespace("Special")
    """Holds special pages."""

    Talk:Namespace = Namespace("Talk")

    User:Namespace = Namespace("User")
    User_Talk:Namespace = Namespace("User_talk")

    Project:Namespace = Namespace("Project")
    Project_Talk:Namespace = Namespace("Project_talk")

    File:Namespace = Namespace("File")
    File_Talk:Namespace = Namespace("File_talk")

    MediaWiki:Namespace = Namespace("MediaWiki")
    MediaWiki_Talk:Namespace = Namespace("MediaWiki_talk")

    Template:Namespace = Namespace("Template")
    Template_Talk:Namespace = Namespace("Template_talk")

    Help:Namespace = Namespace("Help")
    Help_Talk:Namespace = Namespace("Help_talk")

    Category:Namespace = Namespace("Category")
    Category_Talk:Namespace = Namespace("Category_talk")
