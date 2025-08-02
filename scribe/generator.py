"""
Used to generate wiki page content.
"""
import os
import logging
from scribe.app.context import AppContext
from scribe.app.settings import AppSettings, ProviderProject, Sort
from scribe.papyrus.code import Member, Script
from scribe.papyrus.context import PapyrusContext
from scribe.papyrus.project import PapyrusProject
from scribe.wiki.data.page import Page
from scribe.wiki.data.template import Template
from scribe.bots.generator.context import GeneratorContext
from scribe.bots.generator.constants import Wiki
from scribe.bots.generator.pages_index import PageIndex
from scribe.bots.generator.pages_member import PageMember
from scribe.bots.generator.pages_script import PageScript
from scribe.bots.generator.templates import Script_Object_Summary

class GenerateService:
    """
    The service responsible for generating wiki pages from Papyrus projects.
    """

    DIV_WIDTH:int = 50
    """The width of divider lines in the log output."""

    PAGE_SCRIPT_INDEX_FILE_NAME:str = "Script_Information.wiki"
    """The file name of the wiki page that summarizes all scripts in a Papyrus project."""


    @staticmethod
    def start(app:AppContext) -> bool:
        logging.info(" Configurations ".center(GenerateService.DIV_WIDTH, "-"))

        # Ensure that configurations exist.
        if not app.settings.configurations:
            logging.error(f"Aborting program. No configurations found.")
            return False

        if not GenerateService.papyrus_start(app.settings, app.papyrus):
            logging.error(f"Aborting program. Failed to load Papyrus projects.")
            return False

        if not GenerateService.wiki_start(app.settings, app.wiki, app.papyrus):
            logging.error(f"Aborting program. Failed to generate wiki pages.")
            return False

        return True


    @staticmethod
    def papyrus_start(settings:AppSettings, papyrus:PapyrusContext) -> bool:
        """
        Start the Papyrus context and load all projects.
        """
        # Load each configuration.
        logging.info(f"Found {len(settings.configurations)} configurations.")
        for key in settings.configurations:
            providerProject:ProviderProject = settings.configurations[key]

            # Ensure the project root directory exists, else skip.
            if not providerProject.root:
                logging.warning(f"[{providerProject.identifier}] Skipping this project. The path values were not set in the project options.")
                continue
            elif not os.path.exists(providerProject.root):
                logging.warning(f"[{providerProject.identifier}] Skipping this project. The project `root` directory does not exist: '{providerProject.root}'")
                continue

            # Create a Papyrus project for this configuration.
            project:PapyrusProject = PapyrusProject()
            project.identifier = providerProject.identifier
            project.imports = providerProject.imports
            project.root = providerProject.root

            # Add project to the Papyrus context.
            papyrus.add(project)
            logging.info(f"[{project.identifier}] Loaded project from configuration.")

        # Ensure that projects exist by loading each.
        logging.info(" Papyrus ".center(GenerateService.DIV_WIDTH, "-"))
        logging.info(f"Loading {len(papyrus.projects)} projects.")
        if not papyrus.load():
            logging.error(f"Aborting program. Failed to load one or more Papyrus projects.")
            return False
        else:
            return True


    @staticmethod
    def wiki_start(settings:AppSettings, wiki:GeneratorContext, papyrus:PapyrusContext) -> bool:
        """
        Start the wiki generation process.
        """
        logging.info(" Wiki Generation ".center(GenerateService.DIV_WIDTH, "-"))
        logging.info(f"Writing wiki pages for {len(settings.configurations)} configurations.")

        # Generate the wiki index summary page.
        page_file_path:str = os.path.join(settings.export_directory, GenerateService.PAGE_SCRIPT_INDEX_FILE_NAME)
        index_page:Page = GenerateService.wiki_page_create_index(page_file_path, settings, papyrus)
        wiki.add(index_page)

        # Generate wiki pages for each project.
        for key in settings.configurations:
            configuration:ProviderProject = settings.configurations[key]
            if not GenerateService.wiki_projects(wiki, papyrus, configuration):
                logging.error(f"[{configuration.identifier}] Failed to generate one or more wiki pages.")

        # Save the wiki file
        wiki_file_path:str = wiki.save(settings.export_directory)
        logging.info(f"Saved wiki: '{wiki_file_path}'")
        return True


    @staticmethod
    def wiki_projects(wiki:GeneratorContext, papyrus:PapyrusContext, configuration:ProviderProject) -> bool:
        project:PapyrusProject = papyrus.projects[configuration.identifier]

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
                script_page:Page = GenerateService.wiki_page_create_script(output_file_path, papyrus, project, script)
                wiki.add(script_page)
                logging.debug(f"[{project.identifier}]<{script_file_path}> -> {script_file_path_full} -> {output_file_path}")

            # Write a wiki page for this script member.
            if configuration.publish.enable_members:
                for key in script.members:
                    member:Member = script.members[key]
                    member_file_name:str = f"{script_file_name}-{member.name}.wiki"
                    member_file_path:str = os.path.join(os.path.dirname(output_file_path), member_file_name)
                    script_member_page:Page = GenerateService.wiki_page_create_script_member(member_file_path, project, script, member)
                    wiki.add(script_member_page)
                    logging.debug(f"[{project.identifier}]<{script_file_path}>::{member.name} -> {member_file_path}")

        return True


    @staticmethod
    def wiki_page_create_index(file_path:str, settings:AppSettings, papyrus:PapyrusContext) -> Page:
        page:Page = PageIndex.create(file_path, settings, papyrus)
        try:
            page.write_compose()
        except Exception as exception:
            logging.error(f"Failed to write projects index: {str(exception)}")
        return page


    @staticmethod
    def wiki_page_create_script(file_path:str, papyrus:PapyrusContext, project:PapyrusProject, script:Script) -> Page:
        page:Page = PageScript.create(file_path, papyrus, project, script)
        try:
            page.write_compose()
        except Exception as exception:
            logging.error(f"Failed to write projects index: {str(exception)}")
        return page


    @staticmethod
    def wiki_page_create_script_member(file_path:str, project:PapyrusProject, script:Script, member:Member) -> Page:
        page:Page = PageMember.create(file_path, project, script, member)
        try:
            page.write_compose()
        except Exception as exception:
            logging.error(f"Failed to write projects index: {str(exception)}")
        return page



    @staticmethod
    def wiki_template_script_object_summary(papyrus:PapyrusContext, project:PapyrusProject, script:Script, game_version:str) -> Template:
        raise NotImplementedError("The `wiki_template_script_object_summary` method is not implemented yet.")
        template:Template = Template()
        template.file_path = "file_path"
        template.title = "Script_Object_Summary"
        template.content = []
        template.categories = [Wiki.CATEGORY_TEMPLATES_INFOBOX]

        content:str = Script_Object_Summary.script_object_summary(papyrus, project, script, game_version)
        template.content.append(content)

        return template
