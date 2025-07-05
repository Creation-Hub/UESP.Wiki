import re
from re import Pattern


# Regular Expressions
#---------------------------------------------
SCRIPT_NAME:str = r'(?P<name>[^\s]+)'
SCRIPT_FLAGS:str = r'(?P<flags>(?:\s+\w+)*)'
#-------------------------
NAME:str = r'(?P<name>\w+)'
FLAGS:str = r'(?P<flags>.*)'
PARAMETERS:str = r'(?P<params>[^\)]*)'
#-------------------------
ARRAY_BRACKETS:str = r'(?:\[\])'
NAMESPACE:str      = r'(?::\w+)?'
#-------------------------
TYPE_RETURN:str    = r'(?P<type>\w+'             + ARRAY_BRACKETS + r'?)?'
TYPE_VARIABLE:str  = r'(?P<type>\w+'             + ARRAY_BRACKETS + r'?)'
TYPE_PARAMETER:str = r'(?P<type>\w+' + NAMESPACE + ARRAY_BRACKETS + r'?)'
#-------------------------
PARAMETER_INITIALIZER:str = r'(?:\s*=\s*(?P<value>.+))?'
VARIABLE_INITIALIZER:str  = r'(?:\s*=\s*(?P<value>[^\s;]+))?'
PROPERTY_INITIALIZER:str  = r'(?:\s*=\s*(?P<value>[^\s]+))?'


# Regular Patterns
#---------------------------------------------

HEADER_PATTERN:Pattern[str] = re.compile(
    r'^'                            # Start of sequence match
    r'\s*'                          # Whitespace optional (0+)
    # Name (Required)
    r'scriptname'                   # Papyrus keyword 'scriptname' and at least one space
    r'\s+'                          # Whitespace required (1+)
    f'{SCRIPT_NAME}'                # Capture required `name`, non-whitespace
    # Extends (Optional)
    r'(?:\s+extends\s+'             # Papyrus keyword 'extends' and parent name
    r'(?P<extends>[^\s]+))?'        # Capture parent script name (non-whitespace)
    # Flags (Optional)
    r'\s*'                          # Whitespace optional (0+)
    f'{SCRIPT_FLAGS}'               # Capture optional flags (zero or more flag words)
    r'$',                           # End of sequence match
    re.IGNORECASE
)

#-------------------------

# TODO: This does not match lines correctly
VARIABLE_PATTERN:Pattern[str] = re.compile(
    r'^'                           # Start of sequence match
    r'\s*'                         # Whitespace optional (0+)
    f'{TYPE_VARIABLE}'             # Capture required `type` (with optional array brackets)
    r'\s+'                         # Whitespace required (1+)
    f'{NAME}'                      # Capture required `name`
    f'{VARIABLE_INITIALIZER}'      # Optional default value with equals sign
    r'\s*'                         # Whitespace optional (0+)
    f'{FLAGS}'                     # Capture optional `flags` (rest of line)
    r'$',                          # End of sequence match
    re.IGNORECASE
)

PARAMETERS_PATTERN:Pattern[str] = re.compile(
    r'^'                           # Start of sequence match
    r'\s*'                         # Whitespace optional (0+)
    f'{TYPE_PARAMETER}'            # Parameter type (with optional namespace and array brackets)
    r'\s+'                         # Whitespace required (1+)
    f'{NAME}'                      # Parameter name
    f'{PARAMETER_INITIALIZER}'     # Optional default value with equals sign
    r'$',                          # End of sequence match
    re.IGNORECASE
)

#-------------------------

PROPERTY_PATTERN:Pattern[str] = re.compile(
    r'^'                           # Start of sequence match
    r'\s*'                         # Whitespace optional (0+)
    f'{TYPE_VARIABLE}'             # Capture required `type`
    r'\s+'                         # Whitespace required (1+)
    r'property'                    # Papyrus keyword 'property'
    r'\s+'                         # Whitespace required (1+)
    f'{NAME}'                      # Capture required `name`
    f'{PROPERTY_INITIALIZER}'
    r'\s*'                         # Whitespace optional (0+)
    f'{FLAGS}'                     # Capture optional `flags`
    r'$',                          # End of sequence match
    re.IGNORECASE
)

PROPERTY_END_PATTERN:Pattern[str] = re.compile(
    r'^'                            # Start of sequence match
    r'\s*'                          # Whitespace optional (0+)
    r'endproperty'                  # Papyrus keyword 'endproperty'
    r'\b',                          # Word boundary
    re.IGNORECASE
)

#-------------------------

EVENT_PATTERN:Pattern[str] = re.compile(
    r'^'                            # Start of sequence match
    r'\s*'                          # Whitespace optional (0+)
    r'event'                        # Papyrus keyword 'event'
    r'\s+'                          # Whitespace required (1+)
    f'{NAME}'                       # Event name
    r'\s*'                          # Whitespace optional (0+)
    r'\('                           # Opening parenthesis
    f'{PARAMETERS}'                 # Parameters
    r'\)'                           # Closing parenthesis
    r'\s*'                          # Whitespace optional (0+)
    f'{FLAGS}'                      # Optional flags
    r'$',                           # End of sequence match
    re.IGNORECASE
)

FUNCTION_PATTERN:Pattern[str] = re.compile(
    r'^'                            # Start of sequence match
    r'\s*'                          # Whitespace optional (0+)
    f'{TYPE_RETURN}'                # Optional return type (with optional [])
    r'\s*'                          # Whitespace optional (0+)
    r'function'                     # Papyrus keyword 'function'
    r'\s+'                          # Whitespace required (1+)
    f'{NAME}'                       # Function name
    r'\s*'                          # Whitespace optional (0+)
    r'\('                           # Opening parenthesis
    f'{PARAMETERS}'                 # Parameters (anything except ')' character)
    r'\)'                           # Closing parenthesis
    r'\s*'                          # Whitespace optional (0+)
    f'{FLAGS}'                      # Optional flags (rest of line)
    r'$',                           # End of sequence match
    re.IGNORECASE
)

#-------------------------

STRUCT_PATTERN:Pattern[str] = re.compile(
    r'^'                            # Start of sequence match
    r'\s*'                          # Whitespace optional (0+)
    r'struct'                       # Papyrus keyword 'struct'
    r'\s+'                          # Whitespace required (1+)
    f'{NAME}',                      # Capture required `name`
    re.IGNORECASE
)

STRUCT_END_PATTERN:Pattern[str] = re.compile(
    r'^'                            # Start of sequence match
    r'\s*'                          # Whitespace optional (0+)
    r'endstruct'                    # Papyrus keyword 'endstruct'
    r'\b',                          # Word boundary
    re.IGNORECASE
)

#-------------------------

GROUP_PATTERN:Pattern[str] = re.compile(
    r'^'                            # Start of sequence match
    r'\s*'                          # Whitespace optional (0+)
    r'group'                        # Papyrus keyword 'group'
    r'\s+'                          # Whitespace required (1+)
    f'{NAME}'                       # Capture required `name`
    f'{FLAGS}'                      # Capture optional `flags`
    r'$',                           # End of sequence match
    re.IGNORECASE
)

GROUP_END_PATTERN:Pattern[str] = re.compile(
    r'^'                            # Start of sequence match
    r'\s*'                          # Whitespace optional (0+)
    r'endgroup'                     # Papyrus keyword 'endgroup'
    r'\s*'                          # Whitespace optional (0+)
    r'$',                           # End of sequence match
    re.IGNORECASE
)

#-------------------------

STATE_PATTERN:Pattern[str] = re.compile(
    r'^'                            # Start of sequence match
    r'\s*'                          # Whitespace optional (0+)
    r'(?P<flag_auto>auto\s+)?'      # Capture optional 'auto' flag
    r'state'                        # Papyrus keyword 'state'
    r'\s+'                          # Whitespace required (1+)
    f'{NAME}'                       # Capture required `name`
    r'\s*'                          # Whitespace optional (0+)
    f'{FLAGS}'                      # Capture optional `flags`
    r'$',                           # End of sequence match
    re.IGNORECASE
)

STATE_END_PATTERN:Pattern[str] = re.compile(
    r'^'                            # Start of sequence match
    r'\s*'                          # Whitespace optional (0+)
    r'endstate'                     # Papyrus keyword 'endstate'
    r'\s*'                          # Whitespace optional (0+)
    r'$',                           # End of sequence match
    re.IGNORECASE
)
