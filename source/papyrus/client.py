import logging
from .project import PapyrusProject

class PapyrusClient:
    """
    The Papyrus context for script analysis.
    """
    def __init__(self) -> None:
        super().__init__()

        self.projects:dict[str, PapyrusProject] = {}
        """The list of Papyrus projects in this context."""


    def add(self, project:PapyrusProject) -> None:
        """Adds a project to the Papyrus context."""
        self.projects[project.identifier] = project


    def _valid_imports(self, project:PapyrusProject) -> bool:
        for imported in project.imports:
            if imported not in self.projects:
                logging.error(f"[{project.identifier}] The imported '{imported}' project dependency does not exist.")
                return False
        return True


    def load(self) -> bool:
        if not self.projects:
            logging.warning("No projects found in this Papyrus context.")
            return False

        for project in self.projects.values():
            if not self._valid_imports(project):
                logging.error(f"[{project.identifier}] There was a problem with one or more imported projects.")
                return False

            if not project.load():
                logging.error(f"[{project.identifier}] Failed to load project scripts.")

        return True
