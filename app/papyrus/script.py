class Header:
    index:int = -1
    definition:str = ""
    name:str = ""
    namespace:list[str] = []
    extends:str = ""
    flags:list[str] = []
    documentation:str = ""
    game_version:str = ""

class Member:
    index:int = -1
    definition:str = ""
    state:str = ""
    name:str = ""
    kind:str = ""
    type:str = ""
    parameters:list[str] = []
    flags:list[str] = []
    documentation:str = ""
    game_version:str = ""

class Script:
    header:Header = Header()
    members:list[Member] = []
