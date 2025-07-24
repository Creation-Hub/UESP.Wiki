"""
https://www.mediawiki.org/w/api.php?action=help
"""
from enum import Enum


class LoginStatus(str, Enum):
    PASS     = "PASS"
    FAIL     = "FAIL"
    RESTART  = "RESTART"
    CONTINUE = "CONTINUE"


class EditResult(str, Enum):
    SUCCESS = "Success"
    FAILURE = "Failure"


# https://www.mediawiki.org/wiki/API:Data_formats#Output
class DataFormat(str, Enum):
    JSON = "json" # recommended
    PHP  = "php" # deprecated
    XML  = "xml" # deprecated
    TEXT = "txt" # removed in 1.27
    NONE = "none"


# https://www.mediawiki.org/wiki/API:Errors_and_warnings#Errors
class ErrorFormat(str, Enum):
    HTML = "html"
    WIKI = "wikitext"
    TEXT = "plaintext"
    RAW  = "raw"
    NONE = "none"
