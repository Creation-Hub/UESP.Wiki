"""
Generates MediaWiki pages for Papyrus members.
"""
from scribe.papyrus.project import PapyrusProject
from scribe.papyrus.code import Script
from scribe.papyrus.code import Member
from scribe.papyrus.code import Function
from scribe.papyrus.code import Event
from scribe.papyrus.code import Variable
from scribe.papyrus.code import Property
from scribe.wiki.data.article import Page
from .wiki import Wiki
from .templates import Script_Member_Summary
from .scripts import WikiDataScript

class PageMember:
    """
    Generates a MediaWiki page for a Papyrus member.
    """

    @staticmethod
    def create(file_path:str, project:PapyrusProject, script:Script, member:Member) -> Page:
        this:Page = Page()
        this.namespace = Wiki.NAMESPACE_MODDING
        this.name = PageMember.get_title(script, member)
        this.categories.append(Wiki.CATEGORY_PAPYRUS)

        game_version:str = ""
        source_file_path:str = script.header.name.file_path() + ".psc"

        # Member Summary Template
        this.content.append(Script_Member_Summary.template(script, member, game_version))
        this.content.append("\n\n")

        # Member Documentation
        this.content.append("== Documentation ==\n")
        if not member.documentation:
            this.content.append(f"No documentation comments were provided for this member.\n")
            this.content.append("\n\n")
        else:
            this.content.append(f"The <code>{source_file_path}</code> source file documentation comments for this script.\n\n")
            this.content.append("<source>\n")
            this.content.append(f"{member.documentation}\n")
            this.content.append("</source>\n")
            this.content.append("\n\n")

        # Member Auto Value
        if isinstance(member, Property) or isinstance(member, Variable):
            this.content.append("== Field Initializer ==\n")
            if not member.value:
                this.content.append(f"This {str.lower(member.kind)} member has no field initialized value.\n\n")
            else:
                this.content.append("* " + member.value)
                this.content.append("\n")

        # Member Parameters
        if isinstance(member, Function) or isinstance(member, Event):
            this.content.append("== Parameters ==\n")
            if not member.parameters:
                this.content.append(f"This {str.lower(member.kind)} member has no parameters.\n\n")
            else:
                this.content.append("The parameters that belong to this script.\n\n")
                items = WikiDataScript.variable_to_string_list(member.parameters)
                for item in items:
                    this.content.append(f"* {item}\n")
        return this


    @staticmethod
    def get_title(script:Script, member:Member) -> str:
        path:str = script.header.name.file_path().replace("\\", "/")
        return f"{path}/{member.name}"
