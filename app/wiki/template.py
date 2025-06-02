from papyrus.script import Script, Member
import wiki.link

# Script Object
#---------------------------------------------

# TODO: Script namespace and flags are not implemented by the parser yet.
def script_object_summary(script:Script, game_version):
    """
    Return the 'Script_Object_Summary' wiki template as a string.
    https://starfieldwiki.net/wiki/Template:Script_Object_Summary
    """
    script_title = script.header.name
    script_name = wiki.link.script_object(script.header.name)
    script_extends = wiki.link.script_object(script.header.extends)
    script_namespace = script.header.namespace
    script_flags = script.header.flags
    return (
        "{{Script_Object_Summary\n"
        f"| title = {script_title}\n"
        f"| script = {script_name}\n"
        f"| namespace = {script_namespace}\n"
        f"| extends = {script_extends}\n"
        f"| flags = {script_flags}\n"
        f"| game_version = {game_version}\n"
        "}}\n"
    )


def script_object_member_summary(script:Script, member:Member, game_version):
    """
    Return the 'Script_Object_Member_Summary' wiki template as a string.
    See https://starfieldwiki.net/wiki/Template:Script_Object_Member_Summary
    """
    script_name = wiki.link.script_object(script.header.name)
    member_title = member.name
    member_name = wiki.link.script_member(script.header.name, member.name)
    member_kind = member.kind
    member_returns = member.type
    member_flags_string = " ".join(member.flags) if isinstance(member.flags, list) else member.flags
    member_parameters_string = ", ".join(member.parameters) if isinstance(member.parameters, list) else member.parameters
    member_documentation = member.documentation
    return (
        "{{Script_Object_Member_Summary\n"
        f"| title = {member_title}\n"
        f"| script = {script_name}\n"
        f"| name = {member_name}\n"
        f"| kind = {member_kind}\n"
        f"| flags = {member_flags_string}\n"
        f"| returns = {member_returns}\n"
        f"| parameters = {member_parameters_string}\n"
        f"| documentation = {member_documentation}\n"
        f"| game_version = {game_version}\n"
        "}}\n"
    )


# Script Member
#---------------------------------------------

# Not implemented yet, for standalone member pages
def script_member_summary(member_title, script_name, member_name, member_kind, member_returns, member_flags, member_parameters, documentation, game_version):
    """
    Return the 'Script_Member_Summary' wiki template as a string.
    https://starfieldwiki.net/wiki/Template:Script_Member_Summary
    """
    return (
        "{{Script_Member_Summary\n"
        f"| title = {member_title}\n"
        f"| script = {wiki.link.script_object(script_name)}\n"
        f"| name = {wiki.link.script_member(script_name, member_name)}\n"
        f"| kind = {member_kind}\n"
        f"| flags = {member_flags}\n"
        f"| returns = {member_returns}\n"
        f"| parameters = {member_parameters}\n"
        f"| documentation = {game_version}\n"
        f"| game_version = {documentation}\n"
        "}}\n"
    )
