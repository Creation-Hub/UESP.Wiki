import logging
import os
from sharp.collections import KeyedCollection
from papyrus.client import PapyrusClient, PapyrusProject
from scribe.publisher.configuration import PublishPapyrus
from scribe.services.publisher import PublisherService

class PapyrusService:

    DIV_WIDTH:int = 50
    """The width of divider lines in the log output."""


    def __init__(self) -> None:
        super().__init__()
        self.client:PapyrusClient = PapyrusClient()


    @staticmethod
    def create(publisher:PublisherService) -> 'PapyrusService':
        """
        Start the Papyrus context and load all projects.
        """
        this:PapyrusService = PapyrusService()
        jobs:KeyedCollection[str, PublishPapyrus] = publisher.get_papyrus()

        # Load each configuration.
        logging.info(" Configurations ".center(PapyrusService.DIV_WIDTH, "-"))
        logging.info(f"Found {len(jobs)} configurations.")
        for job in jobs.values():
            # Ensure the job root directory exists, else skip.
            if not job.root:
                logging.warning(f"[{job.identifier}] Skipping this job. The path values were not set in the job options.")
                continue
            elif not os.path.exists(job.root):
                logging.warning(f"[{job.identifier}] Skipping this job. The job `root` directory does not exist: '{job.root}'")
                continue

            # Create a Papyrus project for this configuration.
            project:PapyrusProject = PapyrusProject()
            project.identifier = job.identifier
            project.imports = job.imports
            project.root = job.root

            # Add project to the Papyrus context.
            this.client.add(project)
            logging.info(f"[{project.identifier}] Loaded project from configuration.")

        # Ensure that projects exist by loading each.
        logging.info(" Papyrus ".center(PapyrusService.DIV_WIDTH, "-"))
        logging.info(f"Loading {len(this.client.projects)} projects.")
        if not this.client.load():
            raise Exception("Failed to load one or more Papyrus projects.")

        return this
