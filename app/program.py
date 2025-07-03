import os
import logging
from app import wiki
from app.context import AppContext
from app.papyrus.code import Member
from app.publishing import Sort
from app.settings import Configuration

# Project
#---------------------------------------------

def project_start(context:AppContext, configuration:Configuration) -> bool:
    project = configuration.project

    # Skip any disabled projects.
    if not configuration.publish.enable:
        logging.info(f"[{project.identifier}] Skipping this project. The project is disabled.")
        return False

    # Skip any projects without a publish sorting option.
    if not configuration.publish.sort:
        logging.warning(f"[{project.identifier}] Skipping this project. The project publish sorting property cannot be a None value.")
        return False

    # Validate provided project configuration.
    if not project.root or not configuration.publish.output:
        logging.warning(f"[{project.identifier}] Skipping this project. The path values were not set in the project options.")
        return False

    # Ensure the project input directory exist, else skip.
    if not os.path.exists(project.root):
        logging.warning(f"[{project.identifier}] Skipping this project. The project `root` directory does not exist: '{project.root}'")
        return False

    # Deserialize the project scripts.
    if not project.load():
        logging.warning(f"[{project.identifier}] Skipping this project. Failed to load scripts from the project root directory: '{project.root}'")
        return False

    # Wiki: Generate wiki pages for each project script.
    for script in project.scripts:
        script_file_name = script.header.name.file_name()
        script_file_path = script.header.name.file_path()
        script_file_path_full = os.path.join(project.root, f"{script_file_path}.psc")

        # Get the output file path based on the project sorting option.
        output_file_path = ""
        if configuration.publish.sort == Sort.DEFAULT:
            output_file_path = os.path.join(configuration.publish.output, f"{script_file_path}.wiki")
        elif configuration.publish.sort == Sort.FLAT:
            output_file_path = os.path.join(configuration.publish.output, f"{str(script.header.name).replace(":", "-")}.wiki")
        elif configuration.publish.sort == Sort.TREE:
            output_file_path = os.path.join(configuration.publish.output, script_file_path+".psc", f"{script_file_name}.wiki")
        else:
            logging.warning(f"[{project.identifier}][{script_file_path}] Skipping this script. The project sorting property could not be determined.")
            continue

        # Create the project output directory.
        output_file_directory = os.path.dirname(output_file_path)
        if not os.path.exists(output_file_directory):
            os.makedirs(output_file_directory)
            logging.debug(f"[{project.identifier}][{script_file_path}] Created the output directory: {output_file_directory}")

        # Write a wiki page for this script object.
        if configuration.publish.enable_objects:
            wiki.page.write_script(context, project, script, output_file_path)
            logging.debug(f"[{project.identifier}]<{script_file_path}> -> {script_file_path_full} -> {output_file_path}")

        # Write a wiki page for this script member.
        if configuration.publish.enable_members:
            for key in script.members:
                member:Member = script.members[key]
                member_file_name = f"{script_file_name}-{member.name}.wiki"
                member_file_path = os.path.join(os.path.dirname(output_file_path), member_file_name)
                wiki.page.write_member(context, project, script, member, member_file_path)
                logging.debug(f"[{project.identifier}]<{script_file_path}>::{member.name} -> {member_file_path}")

    logging.info(f"[{project.identifier}] Processed all scripts.")
    return True


# Program
#---------------------------------------------

def start(context:AppContext) -> None:
    if not context.configurations:
        logging.warning(f"No configurations found.")
        return
    else:
        logging.info(f"Found {len(context.configurations)} configurations.")

    # Generate wiki pages for each project.
    for key in context.configurations:
        configuration:Configuration = context.configurations[key]
        project_start(context, configuration)

    # Generate the wiki index page.
    index_path = os.path.join(context.export_directory, "Script_Information.wiki")
    if not os.path.exists(os.path.dirname(index_path)):
        os.makedirs(os.path.dirname(index_path))
        logging.debug(f"Created index directory: {os.path.dirname(index_path)}")
    try:
        wiki.index.write(context, index_path)
    except Exception as e:
        logging.error(f"Failed to write projects index: {str(e)}")
