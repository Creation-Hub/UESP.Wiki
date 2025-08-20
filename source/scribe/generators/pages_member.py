"""
Generates MediaWiki pages for Papyrus members.
"""
from papyrus.project import PapyrusProject
from papyrus.code import Script
from papyrus.code import Member
from papyrus.code import Function
from papyrus.code import Event
from papyrus.code import Variable
from papyrus.code import Property
from wiki.data.section import SectionLevel
from scribe.composer.article import Article
from scribe.composer.builder import ArticleBuilder
from scribe.composer.wiki import Wiki
from .templates import Script_Member_Summary
from .scripts import WikiDataScript

class PageMember:
    """
    Generates a MediaWiki page for a Papyrus member.
    """

    @staticmethod
    def create(wiki:Wiki, file_path:str, project:PapyrusProject, script:Script, member:Member) -> Article:
        game_version:str = ""
        source_file_path:str = script.header.name.file_path() + ".psc"

        # Builder
        builder:ArticleBuilder = ArticleBuilder(wiki)
        builder.title(PageMember.get_title(script, member), Wiki.NAMESPACE_MODDING)
        builder.category(Wiki.CATEGORY_PAPYRUS.name)

        # Summary Template
        builder.line(Script_Member_Summary.template(script, member, game_version))
        builder.line("\n\n")

        # Documentation
        builder.section("Documentation", SectionLevel.H2)
        if not member.documentation:
            builder.line(f"No documentation comments were provided for this member.\n")
            builder.line("\n\n")
        else:
            builder.line(f"The <code>{source_file_path}</code> source file documentation comments for this script.\n\n")
            builder.line("<source>\n")
            builder.line(f"{member.documentation}\n")
            builder.line("</source>\n")
            builder.line("\n\n")

        # Member Auto Value
        if isinstance(member, Property) or isinstance(member, Variable):
            builder.section("Field Initializer", SectionLevel.H2)
            if not member.value:
                builder.line(f"This {str.lower(member.kind)} member has no field initialized value.\n\n")
            else:
                builder.line("* " + member.value)
                builder.line("\n")

        # Member Parameters
        if isinstance(member, Function) or isinstance(member, Event):
            builder.section("Parameters", SectionLevel.H2)
            if not member.parameters:
                builder.line(f"This {str.lower(member.kind)} member has no parameters.\n\n")
            else:
                builder.line("The parameters that belong to this script.\n\n")
                items = WikiDataScript.variable_to_string_list(member.parameters)
                for item in items:
                    builder.line(f"* {item}\n")


        return builder.build()


    @staticmethod
    def get_title(script:Script, member:Member) -> str:
        path:str = script.header.name.file_path().replace("\\", "/")
        return f"{path}/{member.name}"
