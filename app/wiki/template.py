from typing import Iterable
from app import wiki
from app.context import AppContext
from app.papyrus.code import Script, Member
from app.papyrus import inheritance
from app.project import PapyrusProject

# Inheritance
#---------------------------------------------

def to_names(scripts:list[Script]) -> list[str]:
    return [str(script.header.name) for script in scripts] if scripts else []


def to_names_linked(scripts:list[Script]) -> list[str]:
    return [wiki.style.link_script_object(str(script.header.name)) for script in scripts] if scripts else []


# Used for the extends field on script templates.
def get_inheritance_extends_string(inheritance_chain:list[Script]) -> str:
    if not inheritance_chain:
        return "Nothing"
    else:
        names:list[str] = to_names_linked(inheritance_chain)
        return " → ".join(names)


# Used to build the script index page.
def get_inheritance_string(script:Script, inheritance_chain:list[Script]) -> str:
    chain_reversed:Iterable[Script] = reversed(inheritance_chain)
    inheritance_list:list[Script] = list(chain_reversed) + [script]
    names:list[str] = to_names(inheritance_list)
    return " ← ".join(names)


def get_script_extends_link(script:Script) -> str:
    if script.header.name.value == "ScriptObject":
        return "Nothing"
    elif script.header.extends.value:
        return wiki.style.link_script_object(str(script.header.extends))
    else:
        return wiki.style.link_script_object("ScriptObject")


# Script Object
#---------------------------------------------

def script_object_summary(context:AppContext, project:PapyrusProject, script:Script, game_version:str):
    """
    Return the 'Script_Object_Summary' wiki template as a string.
    https://starfieldwiki.net/wiki/Template:Script_Object_Summary
    """
    script_title = script.header.name
    script_name = wiki.style.link_script_object(str(script.header.name))
    inheritance_chain:list[Script] = inheritance.get_chain(context, project, script)
    script_extends = get_inheritance_extends_string(inheritance_chain)
    script_flags = wiki.style.to_list_csv(script.header.flags)

    #---------------------------------------------
    template_text = ""
    template_text += "{{Script_Object_Summary\n"

    if script_title:
        template_text += f"| title = {script_title}\n"

    if script_name:
        template_text += f"| name = {script_name}\n"

    if script_extends:
        template_text += f"| extends = {script_extends}\n"

    if script_flags:
        template_text += f"| flags = {script_flags}\n"

    if game_version:
        template_text += f"| game_version = {game_version}\n"

    template_text += "}}\n"
    return template_text


def script_object_member_summary(script:Script, member:Member, game_version:str):
    """
    Return the 'Script_Object_Member_Summary' wiki template as a string.
    See https://starfieldwiki.net/wiki/Template:Script_Object_Member_Summary
    """
    script_name = wiki.style.link_script_object(str(script.header.name))
    member_title = member.name
    member_name = wiki.style.link_script_member(str(script.header.name), member.name)
    member_kind = member.kind
    member_returns = member.type
    member_flags_string = " ".join(member.flags)
    member_parameters_string = ", ".join(member.parameters)
    member_documentation = member.documentation

    template_text = ""
    template_text += "{{Script_Object_Member_Summary\n"

    if member_title:
        template_text += f"| title = {member_title}\n"

    if script_name:
        template_text += f"| script = {script_name}\n"

    if member_name:
        template_text += f"| name = {member_name}\n"

    if member_kind:
        template_text += f"| kind = {member_kind}\n"

    if member_flags_string:
        template_text += f"| flags = {member_flags_string}\n"

    if member_returns:
        template_text += f"| returns = {member_returns}\n"

    if member_parameters_string:
        template_text += f"| parameters = {member_parameters_string}\n"

    if member_documentation:
        template_text += f"| documentation = {member_documentation}\n"

    if game_version:
        template_text += f"| game_version = {game_version}\n"

    template_text += "}}\n"
    return template_text


# Script Member
#---------------------------------------------

# Not implemented yet, for standalone member pages
def script_member_summary(script:Script, member:Member, game_version:str) -> str:
    """
    Return the 'Script_Member_Summary' wiki template as a string.
    https://starfieldwiki.net/wiki/Template:Script_Member_Summary
    """
    script_name = wiki.style.link_script_object(str(script.header.name))
    member_title = member.name
    member_name = wiki.style.link_script_member(str(script.header.name), member.name)
    member_kind = member.kind
    member_returns = member.type
    member_flags_string = " ".join(member.flags)
    member_parameters_string = ", ".join(member.parameters)
    member_documentation = member.documentation

    template_text = ""
    template_text += "{{Script_Member_Summary\n"

    if member_title:
        template_text += f"| title = {member_title}\n"

    if script_name:
        template_text += f"| script = {script_name}\n"

    if member_name:
        template_text += f"| name = {member_name}\n"

    if member_kind:
        template_text += f"| kind = {member_kind}\n"

    if member_flags_string:
        template_text += f"| flags = {member_flags_string}\n"

    if member_returns:
        template_text += f"| returns = {member_returns}\n"

    if member_parameters_string:
        template_text += f"| parameters = {member_parameters_string}\n"

    if member_documentation:
        template_text += f"| documentation = {member_documentation}\n"

    if game_version:
        template_text += f"| game_version = {game_version}\n"

    template_text += "}}\n"
    return template_text
