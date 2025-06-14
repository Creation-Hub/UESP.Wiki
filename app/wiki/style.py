def link_script_object(script_name:str) -> str:
    """Return a MediaWiki link for script object page."""
    return f"[[SFM:Script-{script_name}|{script_name}]]"


def link_script_member(script_name:str, member_name:str) -> str:
    """Return a MediaWiki link for a script member page."""
    return f"[[SFM:Script-{script_name}/{member_name}|{member_name}]]"


def to_list_csv(items:list[str]) -> str:
    """Convert a list of items to a comma-separated string."""
    return ", ".join(items) if items else ""
