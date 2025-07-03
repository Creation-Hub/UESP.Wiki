from collections import Counter
from collections.abc import ItemsView
from typing import TextIO
from app import wiki
from app.context import AppContext
from app.papyrus.code import Member
from app.papyrus.project import PapyrusProject


# Information
#---------------------------------------------

def statistics_project(project:PapyrusProject) -> \
    tuple[int, int, Counter[str], Counter[str]]:
    # Initialize count trackers
    script_extends_counter:Counter[str] = Counter()
    script_member_kind_counter:Counter[str] = Counter()

    # Iterate through each script to count each use of extends
    for script in project.scripts:
        script_name:str = script.header.extends.key
        if not script_name: script_name = "ScriptObject"
        script_extends_counter[script_name] += 1

        # Iterate through each member in the script to count their kinds
        for member_key in script.members:
            member:Member = script.members[member_key]
            script_member_kind_counter[member.kind] += 1

    return (
        len(project.imports),
        len(project.scripts),
        script_extends_counter,
        script_member_kind_counter
    )


# MediaWiki
#---------------------------------------------

def wiki_list_project_imports(project:PapyrusProject):
    return ", ".join(project.imports) if project.imports else "Nothing"


def wiki_list_member_kinds(script_member_kind_counter:Counter[str]) -> str:
    kinds:ItemsView[str, int] = script_member_kind_counter.items()
    if not kinds:
        return "There are no members defined in this project."
    entries:list[str] = []
    for kind, count in kinds:
        entries.append(f"* {kind} was used {count} times.")
    return "\n".join(entries)


def wiki_list_extends_most_common(script_extends_counter:Counter[str]) -> str:
    common_parent_names:list[tuple[str, int]] = script_extends_counter.most_common(3)
    if not common_parent_names:
        return "There are no common scripts in this project."
    entries:list[str] = []
    for script_name, count in common_parent_names:
        entries.append(f"* The {wiki.style.link_script_object(script_name)} script was extended {count} times.")
    return "\n".join(entries)


def wiki_list_script_names(project:PapyrusProject) -> str:
    if not project.scripts:
        return "There are no scripts defined in this project."
    entries:list[str] = []
    for script in project.scripts:
        entries.append(f"* {wiki.style.link_script_object(str(script.header.name))}")
    return "\n".join(entries)


# Write
#---------------------------------------------

def write_section(file:TextIO, project:PapyrusProject) -> None:
    ( # Collect information for this project
        project_imports_count,
        project_scripts_count,
        script_extends_counter,
        script_member_kind_counter
    ) = statistics_project(project)

    # Add project summary information
    file.write(f"== {project.identifier} ==\n")
    file.write(f"* Imports: {project_imports_count} ({wiki_list_project_imports(project)})\n")
    file.write(f"* Scripts: {project_scripts_count}\n")
    file.write("\n")

    # Add script member statistics section
    file.write("==== Member Statistics ====\n")
    if project_scripts_count:
        file.write(f"This project overall contains {script_member_kind_counter.total()} total members spread over {project_scripts_count} scripts.\n")
        file.write(wiki_list_member_kinds(script_member_kind_counter)+"\n")
    else:
        file.write("There are no scripts defined in this project, so no member statistics can be provided.\n")
    file.write("\n")

    # Add script inheritance statistics section
    file.write("==== Inheritance Statistics ====\n")
    if project_scripts_count:
        file.write(f"The most common extended parent scripts:\n")
        file.write(wiki_list_extends_most_common(script_extends_counter)+"\n")
    else:
        file.write("There are no scripts defined in this project, so no inheritance statistics can be provided.\n")
    file.write("\n")

    # List script statistics section
    file.write("\n")
    file.write("==== Scripts ====\n")
    if project_scripts_count:
        file.write(f"There are {project_scripts_count} scripts that belong to this project:\n")
        file.write(wiki_list_script_names(project))
    else:
        file.write("There are no scripts defined in this project.\n")
    file.write("\n")


def write(context:AppContext, output_file_path:str) -> None:
    with open(output_file_path, "w", encoding="utf-8") as file:
        # Write the wiki page header.
        file.write("= Projects =\n")
        file.write("This page lists all Papyrus project information for each import.\n")
        file.write("\n\n")

        # Write each project wiki section.
        for identifier in context.papyrus.projects:
            project:PapyrusProject = context.papyrus.projects[identifier]
            write_section(file, project)
            file.write("\n\n")
