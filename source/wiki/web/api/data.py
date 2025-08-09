"""
https://www.mediawiki.org/wiki/API:Data_formats
"""
from enum import Enum


class DataBoolean(str, Enum):
    """
    Boolean parameters work like HTML checkboxes.
    If the parameter is specified, regardless of value, it is considered true.

    For a false value, omit the parameter entirely.

    - https://www.mediawiki.org/wiki/API:Data_formats#Boolean_parameters
    - https://www.mediawiki.org/w/api.php?action=help&modules=main#main/datatype/boolean
    """
    TRUE  = "true"


#
class DataFormat(str, Enum):
    """
    - https://www.mediawiki.org/wiki/API:Data_formats#Output
    """
    JSON = "json"
    JSON_FM = "jsonfm" # recommended
    NONE = "none"
    PHP  = "php" # deprecated
    PHP_FM = "phpfm"
    XML  = "xml" # deprecated
    XML_FM = "xmlfm"
    TEXT = "txt" # removed in 1.27
    RAW_FM = "rawfm"
