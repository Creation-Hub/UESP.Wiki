from typing import List, Set
from app.context import AppContext
from app.project import PapyrusProject
from app.papyrus.code import Script


def find_extends(context:AppContext, project:PapyrusProject, script:Script, script_name:str) -> Script:
    """Find a script by its name in the current project or any imported projects.

    Arguments:
        context: The application context containing all projects
        project: The current project containing the script
        script: The script to find the parent for
        script_name: The name of the script to find

    Returns:
        The found script if it exists in the current project or its imports, otherwise None

    Raises:
        ValueError: If the script cannot be found in the current project or its imports
    """
    # First check in the current project
    if script_name in project.scripts:
        return project.scripts[script_name]

    # Check in imported projects
    for identifier in project.imports:
        if identifier in context.papyrus.projects:
            imported:PapyrusProject = context.papyrus.projects[identifier]
            if script_name in imported.scripts:
                return imported.scripts[script_name]

    # Not found in any project
    imports_list:str = ", ".join(project.imports)
    error:str = ""
    error += f"Cannot find parent script '{script_name}' for '{script.header.name}' in project '{project.identifier}' "
    error += f"or its imports: [{imports_list}]. "
    error += "Check your project imports configuration or add the missing dependency project."
    raise ValueError(error)


def get_chain(context:AppContext, project:PapyrusProject, script:Script) -> List[Script]:
    """
    Get the inheritance chain for a script, excluding the script itself.
    Searches across projects using the project's imports list.

    All Papyrus scripts inherit from ScriptObject from the Base-Native import.
    The only exception is ScriptObject itself.

    Args:
        context: The application context containing all projects
        project: The current project containing the script
        script: The script to get the inheritance chain for

    Returns:
        A list of Script objects in the inheritance chain, excluding the script itself

    Raises:
        ValueError: If a parent script cannot be found in the current project or its imports
    """
    chain:List[Script] = []
    visited:Set[str] = set()

    script_object:Script | None = None

    # Skip if this is ScriptObject itself
    script_name = str(script.header.name)
    if script_name == "ScriptObject":
        return chain

    # Start with the parent of the current script
    parent_name: str | None = getattr(script.header.extends, "value", None)
    if not parent_name:
        # If no parent is specified but this isn't ScriptObject,
        # then it implicitly extends ScriptObject
        if script_name != "ScriptObject":
            # Find ScriptObject script
            try:
                script_object = find_extends(context, project, script, "ScriptObject")
                chain.append(script_object)
            except ValueError:
                # ScriptObject not found, but we'll continue anyway
                pass
        return chain

    # Try to find the parent script
    current_script:Script = find_extends(context, project, script, parent_name)

    # Add the first parent to the chain
    chain.append(current_script)
    visited.add(script_name)  # Mark current script as visited
    visited.add(parent_name)  # Mark parent as visited

    # Continue chain if parent was found
    while current_script:
        next_parent_name = getattr(current_script.header.extends, "value", None)
        if not next_parent_name:
            # If we've reached a script with no explicit parent and it's not ScriptObject,
            # add ScriptObject as the ultimate parent
            if str(current_script.header.name) != "ScriptObject" and "ScriptObject" not in visited:
                try:
                    script_object = find_extends(context, project, script, "ScriptObject")
                    chain.append(script_object)
                    visited.add("ScriptObject")
                except ValueError:
                    # ScriptObject not found, but we'll continue anyway
                    pass
            break

        if next_parent_name in visited:
            break

        # Find the next parent
        next_script:Script = find_extends(context, project, script, next_parent_name)
        chain.append(next_script)
        visited.add(next_parent_name)

        # Move to the next parent
        current_script = next_script

    return chain
