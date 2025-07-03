from app.project import PapyrusProject
from app.publishing import PublishOption

class Configuration:
    def __init__(self):
        self.identifier:str = ""
        self.project:PapyrusProject = PapyrusProject()
        self.publish:PublishOption = PublishOption()
