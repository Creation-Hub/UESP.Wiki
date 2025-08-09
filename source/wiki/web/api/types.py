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
