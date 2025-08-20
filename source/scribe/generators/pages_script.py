"""
Generates MediaWiki pages for Papyrus scripts.
"""
from collections import defaultdict
from papyrus.client import PapyrusClient
from papyrus.project import PapyrusProject
from papyrus.code import Event, Function, Guard, Property, PropertyGroup, Script, Structure, Variable
from papyrus.code import Member
from papyrus.text.parsing import State
from scribe.composer.article import Article
from scribe.composer.wiki import Wiki
from scribe.composer.builder import ArticleBuilder
from wiki.data.section import SectionLevel
from .templates import Script_Object_Member_Summary, Script_Object_Summary

class PageScript:
    """
    Generates MediaWiki pages for Papyrus scripts.
    """

    @staticmethod
    def create(wiki:Wiki, papyrus:PapyrusClient, project:PapyrusProject, script:Script) -> Article:
        game_version:str = ""
        source_file_path:str = script.header.name.file_path() + ".psc"

        # Builder
        builder:ArticleBuilder = ArticleBuilder(wiki)
        builder.title(PageScript.get_title(script), Wiki.NAMESPACE_MODDING)
        builder.category(Wiki.CATEGORY_PAPYRUS.name)
        builder.line(Script_Object_Summary.template(papyrus, project, script, game_version))
        builder.line("\n\n")
        builder.section("Definition", SectionLevel.H2)
        builder.lines([
            f"The header definition for this script comes from the <code>{source_file_path}</code> source file.\n\n",
            "<source lang=\"papyrus\">\n",
            f"{script.header.definition}\n",
            "</source>\n",
            "\n\n"
        ])

        # Documentation
        builder.section("Documentation", SectionLevel.H2)
        if not script.header.documentation:
            builder.line(f"No documentation comments were provided in the <code>{source_file_path}</code> source file.\n")
            builder.line("\n\n")
        else:
            builder.lines([
                f"The documentation comments for this script come from the <code>{source_file_path}</code> source file.\n\n",
                "<source>\n",
                f"{script.header.documentation}\n",
                "</source>\n",
                "\n\n"
            ])

        # Member
        builder.section("Member", SectionLevel.H2)
        if not script.members:
            builder.lines([
                f"No members were defined in the <code>{source_file_path}</code> source file.\n",
                "\n\n"
            ])
        else:
            builder.lines([
                "These are the members that belong to this script, grouped by kind.\n",
                "\n\n"
            ])

            # Write each section of members by kind
            members_by_kind:defaultdict[str, list[Member]] = PageScript.sort_members_by_kind(script)
            for kind, members in members_by_kind.items():
                builder.section(kind, SectionLevel.H3)
                builder.lines([
                    f"These are the {kind.lower()} members for this script.\n",
                    "\n"
                ])
                for member in members:
                    builder.line(Script_Object_Member_Summary.template(script, member, game_version)+"\n")
                builder.line("\n\n")

        return builder.build()


    @staticmethod
    def get_title(script:Script) -> str:
        return script.header.name.file_path().replace("\\", "/")


    @staticmethod
    def sort_members_by_kind(script:Script) -> defaultdict[str, list[Member]]:
        sorted:defaultdict[str, list[Member]] = defaultdict(list)
        for key in script.members:
            member:Member = script.members[key]
            sorted[member.kind].append(member)
        return sorted


    @staticmethod
    def item_member(member:Member) -> str:
        if isinstance(member, Function):
            return PageScript.item_function(member)

        elif isinstance(member, Event):
            return PageScript.item_event(member)

        elif isinstance(member, Variable):
            return PageScript.item_variable(member)

        elif isinstance(member, Guard):
            return PageScript.item_guard(member)

        elif isinstance(member, Structure):
            return PageScript.item_structure(member)

        elif isinstance(member, Property):
            return PageScript.item_property(member)

        elif isinstance(member, PropertyGroup):
            return PageScript.item_property_group(member)

        elif isinstance(member, State):
            return PageScript.item_state(member)

        else:
            raise Exception(f"Unhandled member of {member.__class__.__name__} type.")


    @staticmethod
    def item_function(function:Function) -> str:
        content:str = f"* {function.definition}"
        return content

    @staticmethod
    def item_event(event:Event) -> str:
        content:str = f"* {event.definition}"
        return content

    @staticmethod
    def item_property(property:Property) -> str:
        content:str = f"* {property.definition}"
        return content

    @staticmethod
    def item_state(state:State) -> str:
        content:str = f"* {state.definition}"
        return content

    @staticmethod
    def item_variable(variable:Variable) -> str:
        content:str = f"* {variable.definition}"
        return content

    @staticmethod
    def item_guard(guard:Guard) -> str:
        content:str = f"* {guard.definition}"
        return content

    @staticmethod
    def item_structure(structure:Structure) -> str:
        content:str = f"* {structure.definition}\n"
        for key in structure.variables:
            variable:Variable = structure.variables[key]
            content += f"** {variable.definition}\n"
        content += f"\n"
        return content


    @staticmethod
    def item_property_group(property_group:PropertyGroup) -> str:
        content:str = f"* {property_group.definition}"
        return content
