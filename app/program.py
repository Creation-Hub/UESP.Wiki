import os
import logging
from app import wiki, papyrus
from app.settings import AppProject, Sort
from app.papyrus.code import Script

# Project
#---------------------------------------------

def project_load(project:AppProject) -> bool:
    # Parser: Search for source files in the project script directory.
    paths = papyrus.find_files(project.root)
    if not paths:
        logging.warning(f"[{project.name}] No scripts found in this project.")
        return False

    # Parser: Deserialize each source file into application data.
    logging.info(f"[{project.name}] Loading {len(paths)} scripts for this project...")
    count:int = 0
    for path in paths:
        count += 1
        script:Script = papyrus.parser.parse(path)
        if script:
            project.scripts.append(script)
            logging.debug(f"[{project.name}] #{count} {script.header.name.file_path()}")
        else:
            logging.warning(f"[{project.name}] #{count} The script could not be parsed: {path}")

    logging.info(f"[{project.name}] Done loading scripts for this project. ({len(project.scripts)} of {len(paths)})")
    return True


def project_start(project:AppProject) -> bool:
    # Skip any disabled projects.
    if not project.option_publish_enable:
        logging.info(f"[{project.name}] Skipping this project. The project is disabled.")
        return False

    # Validate provided project configuration.
    if not project.root or not project.output:
        logging.warning(f"[{project.name}] Skipping this project. The path values were not set in the project options.")
        return False

    # Ensure the project input directory exist, else skip.
    if not os.path.exists(project.root):
        logging.warning(f"[{project.name}] Skipping this project. The project `root` directory does not exist: '{project.root}'")
        return False

    # Deserialize the project scripts.
    if not project_load(project):
        logging.warning(f"[{project.name}] Skipping this project. Failed to load scripts from the project root directory: '{project.root}'")
        return False

    # Wiki: Generate wiki pages for each project script.
    for script in project.scripts:
        script_file_name = script.header.name.file_name()
        script_file_path = script.header.name.file_path()
        script_file_path_full = os.path.join(project.root, f"{script_file_path}.psc")

        # Get the output file path based on the project sorting option.
        output_file_path = ""
        if project.option_publish_sort == None:
            logging.warning(f"[{project.name}][{script_file_path}] Skipping this script. The project sorting property cannot be a None value.")
            continue
        elif project.option_publish_sort == Sort.DEFAULT:
            output_file_path = os.path.join(project.output, f"{script_file_path}.wiki")
        elif project.option_publish_sort == Sort.FLAT:
            output_file_path = os.path.join(project.output, f"{str(script.header.name).replace(":", "-")}.wiki")
        elif project.option_publish_sort == Sort.TREE:
            output_file_path = os.path.join(project.output, script_file_path, f"{script_file_name}.wiki")
        else:
            logging.warning(f"[{project.name}][{script_file_path}] Skipping this script. The project sorting property could not be determined.")
            continue

        # Create the project output directory.
        output_file_directory = os.path.dirname(output_file_path)
        if not os.path.exists(output_file_directory):
            os.makedirs(output_file_directory)
            logging.debug(f"[{project.name}][{script_file_path}] Created the output directory: {output_file_directory}")

        # Write a wiki page for this script object.
        if project.option_publish_enable_objects:
            # parse_write(script_file_path_full, output_file_path)
            wiki.page.write_script(script, output_file_path)
            logging.debug(f"[{project.name}]<{script_file_path}> -> {script_file_path_full} -> {output_file_path}")

        # Write a wiki page for this script member.
        if project.option_publish_enable_members:
            for member in script.members:
                member_file_name = f"{script_file_name}-{member.name}.wiki"
                member_file_path = os.path.join(os.path.dirname(output_file_path), member_file_name)
                wiki.page.write_member(script, member, member_file_path)
                logging.debug(f"[{project.name}]<{script_file_path}>::{member.name} -> {member_file_path}")

    logging.info(f"[{project.name}] All scripts processed successfully.")
    return True


# Program
#---------------------------------------------

def start(projects: list[AppProject]) -> None:
    if not projects:
        logging.info(f"No projects found.")
        return
    else:
        logging.info(f"Found {len(projects)} projects.")

    for project in projects:
        project_start(project)
