import os
import logging
from app import wiki
from app.context import AppContext
from app.papyrus.code import Member
from app.papyrus.project import PapyrusProject
from app.publishing import Sort
from app.settings import Configuration


DIV_WIDTH:int = 50
"""The width of divider lines in the log output."""


def project_start(context:AppContext, configuration:Configuration) -> bool:
    project:PapyrusProject = context.papyrus.projects[configuration.identifier]

    # Skip any disabled projects.
    if not configuration.publish.enable:
        logging.info(f"[{project.identifier}] has disabled publishing. Skipping wiki page generation.")
        return True # Not an error, successfully did nothing.

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

    # Wiki: Generate wiki pages for each project script.
    for script in project.scripts:
        script_file_name:str = script.header.name.file_name()
        script_file_path:str = script.header.name.file_path()
        script_file_path_full:str = os.path.join(project.root, f"{script_file_path}.psc")

        # Get the output file path based on the project sorting option.
        output_file_path:str = ""
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
        output_file_directory:str = os.path.dirname(output_file_path)
        if not os.path.exists(output_file_directory):
            os.makedirs(output_file_directory)
            logging.debug(f"[{project.identifier}][{script_file_path}] Created the output directory: {output_file_directory}")

        # Write a wiki page for this script object.
        if configuration.publish.enable_objects:
            wiki.page.generator.write_script(context, project, script, output_file_path)
            logging.debug(f"[{project.identifier}]<{script_file_path}> -> {script_file_path_full} -> {output_file_path}")

        # Write a wiki page for this script member.
        if configuration.publish.enable_members:
            for key in script.members:
                member:Member = script.members[key]
                member_file_name:str = f"{script_file_name}-{member.name}.wiki"
                member_file_path:str = os.path.join(os.path.dirname(output_file_path), member_file_name)
                wiki.page.generator.write_member(context, project, script, member, member_file_path)
                logging.debug(f"[{project.identifier}]<{script_file_path}>::{member.name} -> {member_file_path}")

    return True


def write_page_index(context:AppContext) -> None:
    index_path:str = os.path.join(context.export_directory, "Script_Information.wiki")
    if not os.path.exists(os.path.dirname(index_path)):
        os.makedirs(os.path.dirname(index_path))
        logging.debug(f"Created index directory: {os.path.dirname(index_path)}")
    try:
        wiki.page.index.write(context, index_path)
    except Exception as exception:
        logging.error(f"Failed to write projects index: {str(exception)}")


# Program
#---------------------------------------------

def start(context:AppContext) -> None:
    # Ensure that configurations exist.
    logging.info(" Configurations ".center(DIV_WIDTH, "-"))
    if not context.configurations:
        logging.error(f"Aborting program. No configurations found.")
        return

    # Load each configuration.
    logging.info(f"Found {len(context.configurations)} configurations.")
    for key in context.configurations:
        configuration:Configuration = context.configurations[key]

        # Ensure the project root directory exists, else skip.
        if not configuration.root:
            logging.warning(f"[{configuration.identifier}] Skipping this project. The path values were not set in the project options.")
            continue
        elif not os.path.exists(configuration.root):
            logging.warning(f"[{configuration.identifier}] Skipping this project. The project `root` directory does not exist: '{configuration.root}'")
            continue

        # Create a Papyrus project for this configuration.
        project:PapyrusProject = PapyrusProject()
        project.identifier = configuration.identifier
        project.imports = configuration.imports
        project.root = configuration.root
        context.papyrus.add(project)
        logging.info(f"[{project.identifier}] Loaded project from configuration.")


    # Ensure that projects exist.
    logging.info(" Papyrus ".center(DIV_WIDTH, "-"))
    logging.info(f"Loading {len(context.papyrus.projects)} projects.")
    if not context.papyrus.load():
        logging.error(f"Aborting program. Failed to load one or more Papyrus projects.")
        return

    # Begin writing wiki pages.
    logging.info(" Wiki Generation ".center(DIV_WIDTH, "-"))
    logging.info(f"Writing wiki pages for {len(context.configurations)} configurations.")

    # Generate the wiki index summary page.
    write_page_index(context)

    # Generate wiki pages for each project.
    for key in context.configurations:
        configuration:Configuration = context.configurations[key]
        if not project_start(context, configuration):
            logging.error(f"[{configuration.identifier}] Failed to generate one or more wiki pages.")
