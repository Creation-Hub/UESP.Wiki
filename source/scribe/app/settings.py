"""
Provides features for application settings management.
"""
import os
import json
from typing import Any, override
from sharp.objects import Dump
from .log import LogLevel
from .cli.arguments import AppArguments

class AppSettings:
    """
    Represents the application settings.
    """

    # TODO: Have one default fallback path for settings.
    # JSON_FILENAME:str = "app.settings.json"

    JSON_ENCODING:str = "utf-8"


    def __init__(self) -> None:
        super().__init__()

        self.file_path:str|None = None
        """The json file path for these settings."""

        self._base_directory:str|None = None
        """The base directory of the settings file."""

        self._data:dict[str, Any]|None = {}
        """The raw JSON data for the settings."""


    @override
    def __str__(self) -> str:
        return Dump.get(self)


    @staticmethod
    def create(arguments:AppArguments) -> 'AppSettings':
        if not arguments.configuration_file:
            raise ValueError("No configuration file provided in arguments.")

        # Read the settings from the provided configuration file.
        this:AppSettings = AppSettings.json_load(arguments.configuration_file)
        return this


    @staticmethod
    def json_load(file_path:str) -> 'AppSettings':
        """
        Reads the given application settings file.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Settings file not found: {file_path}")
        with open(file_path, encoding=AppSettings.JSON_ENCODING) as file:
            data:dict[str, Any] = json.load(file)

        this:AppSettings = AppSettings()
        this._data = data
        this.file_path = os.path.abspath(file_path)
        this._base_directory = os.path.dirname(file_path)
        return this


    @property # Shared
    def export_directory(self) -> str|None:
        """The export directory for wiki pages."""
        if not self._data: return None
        return self._data.get("export.directory")


    @property # Log
    def log(self) -> dict[str, Any]|None:
        if not self._data: return None
        return self._data.get("log")


    @property # Log
    def log_date_format(self) -> str|None:
        """Date format for log messages."""
        if not self.log: return None
        return self.log.get("date_format")


    @property # Log
    def log_console_level(self) -> LogLevel|None:
        """The logging level for console output."""
        if not self.log: return None
        return LogLevel.json_decode(self.log, "console_level")


    @property # Log
    def log_file_level(self) -> LogLevel|None:
        """The logging level for file output."""
        if not self.log: return None
        return LogLevel.json_decode(self.log, "file_level")


    @property # Log
    def log_file_path(self) -> str|None:
        """The log file path to use."""
        if not self.log: return None
        return self.log.get("file_path")


    @property # Generator
    def papyrus_file_path(self) -> str|None:
        """The json file path for the generator configuration file."""
        if not self._data: return None
        return self._data.get("generator.file")


    @property # Uploader
    def uploader_file_path(self) -> str|None:
        """The json file path for the uploader configuration file."""
        if not self._data: return None
        return self._data.get("uploader.file")


    @property # Uploader
    def uploader_environment(self) -> str|None:
        """The environment to use for the uploader."""
        if not self._data: return None
        return self._data.get("uploader.environment")
