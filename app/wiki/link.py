def script_object(script_name):
    """Return a MediaWiki link for script object page."""
    return f"[[SFM:Script-{script_name}|{script_name}]]"


def script_member(script_name, member_name):
    """Return a MediaWiki link for a script member page."""
    return f"[[SFM:Script-{script_name}/{member_name}|{member_name}]]"
