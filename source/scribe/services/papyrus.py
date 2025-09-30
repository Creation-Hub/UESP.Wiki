import logging
import json
import os
from typing import Any
from papyrus.client import PapyrusClient, PapyrusProject
from scribe.app.log import Log
from scribe.app.configuration import AppConfiguration
from scribe.assets.papyrus import PapyrusPackage, PapyrusTarget
from scribe.assets.papyrus import PapyrusPackage, PapyrusTarget

class PapyrusService:
    NAME:str = "Papyrus"
    """The name of this service."""


    def __init__(self) -> None:
        super().__init__()
        self.packages:dict[str, PapyrusPackage] = {}
        self.client:PapyrusClient = PapyrusClient()


    @staticmethod
    def create(configuration:AppConfiguration) -> 'PapyrusService':
        if not configuration.papyrus_file_path:
            raise Exception(f"No settings file found in the application configuration.")

        this:PapyrusService = PapyrusService()

        # Load settings from file.
        settings:PapyrusSettings = PapyrusSettings.load(configuration.papyrus_file_path)

        # Validate the loaded settings.
        logging.info(f" {PapyrusService.NAME} Settings ".center(Log.DIV_WIDTH, "-"))
        logging.info(f"Found {len(settings.packages)} packages in '{configuration.papyrus_file_path}'.")

        # Validate and add each package.
        for package_key in settings.packages:
            package:PapyrusPackage = settings.packages[package_key]

            # Skip any without target items.
            if not package.targets:
                logging.warning(f"[{package.identifier}] No Papyrus found for this resource. Skipping.")
                continue

            # Add resource to the publisher context.
            this.packages[package.identifier] = package

            # Add each package's targets to the Papyrus client.
            for target_key in package.targets:
                target:PapyrusTarget = package.targets[target_key]

                # Ensure the job root directory exists, else skip.
                if not target.root:
                    logging.warning(f"[{target.identifier}] Skipping this Papyrus target. The `root` directory was not specified.")
                    continue
                elif not os.path.exists(target.root):
                    logging.warning(f"[{target.identifier}] Skipping this Papyrus target. The `root` directory does not exist: '{target.root}'")
                    continue

                # Create a Papyrus project from this target.
                project:PapyrusProject = PapyrusService.to_project(target)

                # Add project to the Papyrus context.
                this.client.add(project)
                logging.info(f"[{project.identifier}] Added project from {package.identifier} package.")

        logging.info(f"Loaded {len(this.packages)} packages.")

        # Ensure that projects exist by loading each.
        logging.info(f" {PapyrusService.NAME} Client ".center(Log.DIV_WIDTH, "-"))
        logging.info(f"Loading client with {len(this.client.projects)} projects.")

        if not this.client.load():
            raise Exception("Failed to load one or more Papyrus projects.")
        return this


    @staticmethod
    def to_project(target:PapyrusTarget) -> PapyrusProject:
        project:PapyrusProject = PapyrusProject()
        project.identifier = target.identifier
        project.imports = target.imports
        project.root = target.root
        return project


class PapyrusSettings:
    JSON_ENCODING:str = "utf-8"

    def __init__(self) -> None:
        super().__init__()
        self.packages:dict[str, PapyrusPackage] = {}


    @staticmethod
    def load(file_path:str) -> 'PapyrusSettings':
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Settings file not found: {file_path}")
        with open(file_path, encoding=PapyrusSettings.JSON_ENCODING) as file:
            data:dict[str, Any] = json.load(file)
        return PapyrusSettings.decode(data)


    @staticmethod
    def decode(data:dict[str, Any]) -> 'PapyrusSettings':
        this:PapyrusSettings = PapyrusSettings()
        for key, value in data.items():
            package:PapyrusPackage = PapyrusPackage.decode(key, value)
            this.packages[package.identifier] = package
        return this


    @staticmethod
    def _decode_papyrus(data:dict[str, Any]) -> dict[str, PapyrusTarget]:
        targets:dict[str, PapyrusTarget] = {}
        for key in data:
            target:PapyrusTarget = PapyrusTarget.decode(data[key])
            targets[target.identifier] = target
        return targets
