"""
Generates MediaWiki pages for Papyrus scripts.
    Module: `app.wiki.page.script`
"""
from collections import defaultdict
from app import wiki
from app.context import AppContext
from app.papyrus.project import PapyrusProject
from app.papyrus.code import Event, Function, Guard, Property, PropertyGroup, Script, Structure, Variable
from app.papyrus.code import Member
from app.papyrus.text.parsing import State


def sort_members_by_kind(script:Script) -> defaultdict[str, list[Member]]:
    sorted:defaultdict[str, list[Member]] = defaultdict(list)
    for key in script.members:
        member:Member = script.members[key]
        sorted[member.kind].append(member)
    return sorted


def item_member(member:Member) -> str:
    if not member:
        raise Exception("Member cannot be 'None'.")

    elif isinstance(member, Function):
        return item_function(member)

    elif isinstance(member, Event):
        return item_event(member)

    elif isinstance(member, Variable):
        return item_variable(member)

    elif isinstance(member, Guard):
        return item_guard(member)

    elif isinstance(member, Structure):
        return item_structure(member)

    elif isinstance(member, Property):
        return item_property(member)

    elif isinstance(member, PropertyGroup):
        return item_property_group(member)

    elif isinstance(member, State):
        return item_state(member)

    else:
        raise Exception(f"Unhandled member of {member.__class__.__name__} type.")


def item_function(function:Function) -> str:
    content:str = f"* {function.definition}"
    return content

def item_event(event:Event) -> str:
    content:str = f"* {event.definition}"
    return content

def item_property(property:Property) -> str:
    content:str = f"* {property.definition}"
    return content

def item_state(state:State) -> str:
    content:str = f"* {state.definition}"
    return content

def item_variable(variable:Variable) -> str:
    content:str = f"* {variable.definition}"
    return content

def item_guard(guard:Guard) -> str:
    content:str = f"* {guard.definition}"
    return content

def item_structure(structure:Structure) -> str:
    content:str = f"* {structure.definition}\n"
    for key in structure.variables:
        variable:Variable = structure.variables[key]
        content += f"** {variable.definition}\n"
    content += f"\n"
    return content

def item_property_group(property_group:PropertyGroup) -> str:
    content:str = f"* {property_group.definition}"
    return content


def content(context:AppContext, project:PapyrusProject, script:Script) -> list[str]:
    lines:list[str] = []
    game_version:str = ""
    source_file_path:str = script.header.name.file_path() + ".psc"

    # Script Summary Template
    lines.append(wiki.template.generator.script_object_summary(context, project, script, game_version))
    lines.append("\n\n")

    # Script Definition
    lines.append("== Definition ==\n")
    lines.append(f"The header definition for this script comes from the <code>{source_file_path}</code> source file.\n\n")
    lines.append("<source lang=\"papyrus\">\n")
    lines.append(f"{script.header.definition}\n")
    lines.append("</source>\n")
    lines.append("\n\n")

    # Script Documentation
    lines.append("== Documentation ==\n")
    if not script.header.documentation:
        lines.append(f"No documentation comments were provided in the <code>{source_file_path}</code> source file.\n")
        lines.append("\n\n")
    else:
        lines.append(f"The documentation comments for this script come from the <code>{source_file_path}</code> source file.\n\n")
        lines.append("<source>\n")
        lines.append(f"{script.header.documentation}\n")
        lines.append("</source>\n")
        lines.append("\n\n")

    # Script Members
    lines.append("== Member ==\n")
    if not script.members:
        lines.append(f"No members were defined in the <code>{source_file_path}</code> source file.\n")
        lines.append("\n\n")
    else:
        lines.append("These are the members that belong to this script, grouped by kind.\n")
        lines.append("\n\n")

        # Write each section of members by kind
        members_by_kind:defaultdict[str, list[Member]] = sort_members_by_kind(script)
        for kind, members in members_by_kind.items():
            lines.append(f"=== {kind} ===\n")
            lines.append(f"These are the {kind.lower()} members for this script.\n")
            lines.append("\n")
            for member in members:
                lines.append(wiki.template.generator.script_object_member_summary(script, member, game_version))
                # lines.append(item_member(member))
                lines.append("\n")
            lines.append("\n\n")

    # Page Categories
    lines.append("\n")
    lines.append("[[Category:Starfield_Mod-Papyrus]]\n")
    return lines


# Write
#---------------------------------------------

def write(context:AppContext, project:PapyrusProject, script:Script, output_file_path:str) -> None:
    """Generates a MediaWiki page for a given Papyrus script source file."""
    lines:list[str] = content(context, project, script)
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.writelines(lines)
