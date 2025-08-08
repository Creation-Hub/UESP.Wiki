"""
Generates MediaWiki pages for Papyrus scripts.
"""
from collections import defaultdict
from scribe.papyrus.client import PapyrusClient
from scribe.papyrus.project import PapyrusProject
from scribe.papyrus.code import Event, Function, Guard, Property, PropertyGroup, Script, Structure, Variable
from scribe.papyrus.code import Member
from scribe.papyrus.text.parsing import State
from scribe.wiki.data.article import Page
from .wiki import Wiki
from .templates import Script_Object_Member_Summary, Script_Object_Summary

class PageScript:
    """
    Generates MediaWiki pages for Papyrus scripts.
    """

    @staticmethod
    def create(papyrus:PapyrusClient, project:PapyrusProject, script:Script) -> Page:
        this:Page = Page()
        this.namespace = Wiki.NAMESPACE_MODDING
        this.name = PageScript.get_title(script)
        this.categories.append(Wiki.CATEGORY_PAPYRUS)

        game_version:str = ""
        source_file_path:str = script.header.name.file_path() + ".psc"

        # Script Summary Template
        this.content.append(Script_Object_Summary.template(papyrus, project, script, game_version))
        this.content.append("\n\n")

        # Script Definition
        this.content.append("== Definition ==\n")
        this.content.append(f"The header definition for this script comes from the <code>{source_file_path}</code> source file.\n\n")
        this.content.append("<source lang=\"papyrus\">\n")
        this.content.append(f"{script.header.definition}\n")
        this.content.append("</source>\n")
        this.content.append("\n\n")

        # Script Documentation
        this.content.append("== Documentation ==\n")
        if not script.header.documentation:
            this.content.append(f"No documentation comments were provided in the <code>{source_file_path}</code> source file.\n")
            this.content.append("\n\n")
        else:
            this.content.append(f"The documentation comments for this script come from the <code>{source_file_path}</code> source file.\n\n")
            this.content.append("<source>\n")
            this.content.append(f"{script.header.documentation}\n")
            this.content.append("</source>\n")
            this.content.append("\n\n")

        # Script Members
        this.content.append("== Member ==\n")
        if not script.members:
            this.content.append(f"No members were defined in the <code>{source_file_path}</code> source file.\n")
            this.content.append("\n\n")
        else:
            this.content.append("These are the members that belong to this script, grouped by kind.\n")
            this.content.append("\n\n")

            # Write each section of members by kind
            members_by_kind:defaultdict[str, list[Member]] = PageScript.sort_members_by_kind(script)
            for kind, members in members_by_kind.items():
                this.content.append(f"=== {kind} ===\n")
                this.content.append(f"These are the {kind.lower()} members for this script.\n")
                this.content.append("\n")
                for member in members:
                    this.content.append(Script_Object_Member_Summary.template(script, member, game_version))

                    # TODO: Test with typed definitions.
                    # this.content.append(item_member(member))

                    this.content.append("\n")
                this.content.append("\n\n")
        return this


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
