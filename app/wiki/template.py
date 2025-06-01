import wiki.link

# Script Object
#---------------------------------------------

# TODO: Script namespace and flags are not implemented by the parser yet.
def script_object_summary(script_title, script_name, extends_name, script_namespace=None, script_flags=None, game_version="v0.0.0+"):
    """
    Return the 'Script_Object_Summary' wiki template as a string.
    https://starfieldwiki.net/wiki/Template:Script_Object_Summary
    """
    return (
        "{{Script_Object_Summary\n"
        f"| title = {script_title}\n"
        f"| script = {wiki.link.script_object(script_name)}\n"
        f"| namespace = {script_namespace}\n"
        f"| extends = {wiki.link.script_object(extends_name)}\n"
        f"| flags = {script_flags}\n"
        f"| game_version = {game_version}\n"
        "}}\n"
    )

# member_title, member_name, member_kind, member_return, member_flags, member_parameters, member_documentation,
def script_object_member_summary(script_name, member, game_version):
    """
    Return the 'Script_Object_Member_Summary' wiki template as a string.
    See https://starfieldwiki.net/wiki/Template:Script_Object_Member_Summary
    """
    member_title = member["name"]
    member_name = member["name"]
    member_kind = member["kind"]
    member_returns = member.get("rtype", "")
    member_flags = member.get("flags", [])
    member_flags_string = " ".join(member_flags) if isinstance(member_flags, list) else member_flags
    member_parameters = member.get("params", [])
    member_parameters_string = ", ".join(member_parameters) if isinstance(member_parameters, list) else member_parameters
    member_documentation = member.get("doc", "")
    return (
        "{{Script_Object_Member_Summary\n"
        f"| title = {member_title}\n"
        f"| script = {wiki.link.script_object(script_name)}\n"
        f"| name = {wiki.link.script_member(script_name, member_name)}\n"
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
