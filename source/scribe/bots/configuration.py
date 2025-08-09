import json
import os
from typing import Any
from scribe.bots.jobs import JobOwner
from scribe.bots.jobs import Job

class GenerateConfiguration:
    JSON_ENCODING:str = "utf-8"

    def __init__(self) -> None:
        super().__init__()

        self.providers:dict[str, JobOwner] = {}
        """The job providers loaded from the settings file."""

        self.papyrus:dict[str, Job] = {}


    @staticmethod
    def load(file_path:str) -> 'GenerateConfiguration':
        """Reads the given application settings file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Settings file not found: {file_path}")
        with open(file_path, encoding=GenerateConfiguration.JSON_ENCODING) as file:
            data:dict[str, Any] = json.load(file)
        return GenerateConfiguration.json_decode(data)


    @staticmethod
    def json_decode(data:dict[str, Any]) -> 'GenerateConfiguration':
        this:GenerateConfiguration = GenerateConfiguration()

        # Decode the `providers` element (list).
        data_providers:list[Any] = data.get("providers", [])
        for data_provider in data_providers:
            provider:JobOwner = JobOwner.json_decode(data_provider)
            this.providers[provider.identifier] = provider

        # Decode the `papyrus` element (dict).
        # TODO: This is not fully implemented yet.
        data_papyrus:dict[str, Any]|None = data.get("papyrus")
        if not data_papyrus: return this
        this.papyrus = GenerateConfiguration.json_decode_papyrus(data_papyrus)
        return this


    @staticmethod
    def json_decode_papyrus(data:dict[str, Any]) -> dict[str, Job]:
        jobs:dict[str, Job] = {}
        for key in data:
            job:Job = Job.json_decode(data[key])
            jobs[job.identifier] = job
        return jobs
