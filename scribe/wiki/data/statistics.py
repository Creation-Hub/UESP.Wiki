from collections import Counter
from scribe.papyrus.code import Member
from scribe.papyrus.project import PapyrusProject

class PapyrusStatistics:
    def __init__(self) -> None:
        self.project_imports_count:int = 0
        self.project_scripts_count:int = 0
        self.script_extends_counter:Counter[str] = Counter()
        self.script_member_kind_counter:Counter[str] = Counter()


    @staticmethod
    def create(project:PapyrusProject) -> 'PapyrusStatistics':
        statistics:PapyrusStatistics = PapyrusStatistics()
        statistics.project_imports_count = len(project.imports)
        statistics.project_scripts_count = len(project.scripts)

        # Iterate through each script to count each use of extends
        for script in project.scripts:
            script_name:str = script.header.extends.key
            if not script_name: script_name = "ScriptObject"
            statistics.script_extends_counter[script_name] += 1

            # Iterate through each member in the script to count their kinds
            for member_key in script.members:
                member:Member = script.members[member_key]
                statistics.script_member_kind_counter[member.kind] += 1

        return statistics
