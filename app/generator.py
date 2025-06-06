import os
import logging
from app import wiki, papyrus
from app.papyrus import Project, Script, Sort

# Generator
#---------------------------------------------

def process(projects: list[Project]) -> None:
    if not projects:
        logging.info(f"No projects found.")
        return
    else:
        logging.info(f"Found {len(projects)} projects.")

    for project in projects:
        # Skip any disabled projects.
        if not project.option_publish_enabled:
            logging.info(f"[{project.name}] Skipping this project. The project is disabled.")
            continue

        # Validate provided project configuration.
        if not project.root or not project.output:
            logging.warning(f"[{project.name}] Skipping this project. The path values were not set in the project options.")
            continue

        # Ensure the project input directory exist, else skip.
        if not os.path.exists(project.root):
            logging.warning(f"[{project.name}] Skipping this project. The project `root` directory does not exist: '{project.root}'")
            continue

        # Parser: Search for source files in the project script directory.
        paths = papyrus.find_files(project.root)
        if not paths:
            logging.info(f"[{project.name}] No scripts found in this project.")
            continue
        else:
            logging.info(f"[{project.name}] Found {len(paths)} scripts in this project.")

        # Parser: Deserialize each source file into application data.
        for path in paths:
            script:Script = papyrus.parser.parse(path)
            project.scripts.append(script)
            logging.info(f"  - {script.header.name} ({script.header.name.file_path()})")

        # Wiki: Generate wiki pages for each project script.
        for script in project.scripts:
            script_file_name = script.header.name.file_name()
            script_file_path = script.header.name.file_path()
            script_file_path_full = os.path.join(project.root, f"{script_file_path}.psc")

            # option_publish_sort: Changes the base output directory path to sort into script name folders.
            #   Default: `Base-Native\MyNamespace\Action.wiki`
            #   Flat:    `Base-Native\MyNamespace-Action.wiki`
            #   Tree:    `Base-Native\MyNamespace\Action\Action.wiki`
            output_file_path = ""
            if project.option_publish_sort == None:
                logging.warning(f"[{project.name}] Skipping this project. The sorting property cannot be a None value.")
                continue
            elif project.option_publish_sort == Sort.DEFAULT:
                output_file_path = os.path.join(project.output, f"{script_file_path}.wiki")
            elif project.option_publish_sort == Sort.FLAT:
                output_file_path = os.path.join(project.output, f"{script.header.name.replace(":", "-")}.wiki")
            elif project.option_publish_sort == Sort.TREE:
                output_file_path = os.path.join(project.output, script_file_path, f"{script_file_name}.wiki")
                pass
            else:
                logging.warning(f"[{project.name}] Skipping this project. The sorting property could not be determined.")
                continue

            # Create the project output directory.
            output_file_directory = os.path.dirname(output_file_path)
            if not os.path.exists(output_file_directory):
                os.makedirs(output_file_directory)
                logging.debug(f"[{project.name}] Created the output directory: {output_file_directory}")

            # Write a wiki page for this script object.
            if project.option_publish_objects:
                wiki.page.parse_write(script_file_path_full, output_file_path)
                logging.info(f"[{project.name}] {script}:\n  -> in:  {project.root}\n  -> out: {output_file_path}")

            # Write a wiki page for this script member.
            if project.option_publish_members:
                logging.warning("Not implemented yet for output_members.")
                pass
