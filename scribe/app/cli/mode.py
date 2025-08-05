from enum import Enum

class AppMode(str, Enum):
    NONE = ""
    GENERATE = "generate"
    UPLOAD = "upload"
