import logging
from sharp.collections import KeyedCollection
from scribe.app.configuration import AppConfiguration
from scribe.publisher.configuration import PublishPapyrus, PublishSettings

class PublisherService:
    def __init__(self) -> None:
        super().__init__()
        self.settings:PublishSettings = PublishSettings()


    @staticmethod
    def create(configuration:AppConfiguration) -> 'PublisherService':
        if not configuration.generator_file_path:
            raise Exception(f"No settings file found in the application configuration.")

        this:PublisherService = PublisherService()
        this.settings = PublishSettings.load(configuration.generator_file_path)
        return this


    def get_papyrus(self) -> KeyedCollection[str, PublishPapyrus]:
        targets:KeyedCollection[str, PublishPapyrus] = KeyedCollection[str, PublishPapyrus](key_extract=lambda item: item.identifier)
        for resource in self.settings.resources.values():
            if not resource.papyrus:
                logging.warning(f"[{resource.identifier}] No Papyrus found for this resource. Skipping.")
                continue
            for job in resource.papyrus.values():
                targets.add(job)
        return targets
