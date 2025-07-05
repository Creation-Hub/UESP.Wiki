import re
from re import Pattern


# Regular Expressions
#---------------------------------------------

# TODO: Consolidate and optimize these regex patterns.

# Regular Patterns
#---------------------------------------------

HEADER_PATTERN:Pattern[str] = re.compile(
    r'^'                            # Start of sequence match
    r'\s*'                          # Whitespace optional (0+)
    # Name (Required)
    r'scriptname'                   # Papyrus keyword 'scriptname' and at least one space
    r'\s+'                          # Whitespace required (1+)
    r'(?P<name>[^\s]+)'             # Capture required `name`, non-whitespace
    # Extends (Optional)
    r'(?:\s+extends\s+'             # Papyrus keyword 'extends' and parent name
    r'(?P<extends>[^\s]+))?'        # Capture parent script name (non-whitespace)
    # Flags (Optional)
    r'\s*'                          # Whitespace optional (0+)
    r'(?P<flags>(?:\s+\w+)*)'       # Capture optional flags (zero or more flag words)
    r'$',                           # End of sequence match
    re.IGNORECASE
)

#-------------------------

# TODO: This does not match lines correctly
VARIABLE_PATTERN:Pattern[str] = re.compile(
    r'^'                            # Start of sequence match
    r'\s*'                          # Whitespace optional (0+)
    # Type (Required)
    r'(?P<type>\w+(?:\[\])?)'       # Capture required `type` (with optional array brackets)
    r'\s+'                          # Whitespace required (1+)
    # Name (Required)
    r'(?P<name>\w+)'                # Capture required `name`
    # Initializer (Optional)
    r'(?:'                          # Start optional group for initializer (non-capturing)
    r'\s*'                          # Whitespace optional (0+)
    r'='                            # Papyrus equals sign
    r'\s*'                          # Whitespace optional (0+)
    r'(?P<initializer>[^\s;]+)'     # Capture optional `initializer` (non-whitespace, non-semicolon)
    r')?'                           # End optional initializer group
    # Flags (Optional)
    r'\s*'                          # Whitespace optional (0+)
    r'(?P<flags>.*)'                # Capture optional `flags` (rest of line)
    r'$',                           # End of sequence match
    re.IGNORECASE
)

PARAMETERS_PATTERN:Pattern[str] = re.compile(
    r'^'                               # Start of sequence match
    r'\s*'                             # Whitespace optional (0+)
    # Type (Required)
    r'(?P<type>\w+(?::\w+)?(?:\[\])?)' # Parameter type (with optional namespace and array brackets)
    r'\s+'                             # Whitespace required (1+)
    # Name (Required)
    r'(?P<name>\w+)'                   # Parameter name
    # Initializer (Optional)
    r'(?:\s*=\s*(?P<value>.+))?'       # Optional default value with equals sign
    r'$',                              # End of sequence match
    re.IGNORECASE
)

#-------------------------

STRUCT_PATTERN:Pattern[str] = re.compile(
    r'^'                            # Start of sequence match
    r'\s*'                          # Whitespace optional (0+)
    # Name (Required)
    r'struct'                       # Papyrus keyword 'struct'
    r'\s+'                          # Whitespace required (1+)
    r'(?P<name>\w+)',               # Capture required `name`
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
    # Name (Required)
    r'group'                        # Papyrus keyword 'group'
    r'\s+'                          # Whitespace required (1+)
    r'(?P<name>\w+)'                # Capture required `name`
    # Flags (Optional)
    r'(?P<flags>.*)'                # Capture optional `flags`
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

PROPERTY_PATTERN:Pattern[str] = re.compile(
    r'^'                            # Start of sequence match
    r'\s*'                          # Whitespace optional (0+)
    # Property (Required)
    r'(?P<type>\w+(?:\[\])?)'       # Capture required `type`
    r'\s+'                          # Whitespace required (1+)
    r'property'                     # Papyrus keyword 'property'
    r'\s+'                          # Whitespace required (1+)
    r'(?P<name>\w+)'                # Capture required `name`
    # Initializer (Optional)
    r'(?:'                          # Capture-Start with discard
    r'\s*'                          # Whitespace optional (0+)
    r'='                            # Equals sign for initializer
    r'\s*'                          # Whitespace optional (0+)
    r'(?P<initializer>[^\s]+)'      # Capture optional `initializer`
    r')?'                           # Capture-End as optional
    # Flags (Optional)
    r'\s*'                          # Whitespace optional (0+)
    r'(?P<flags>.*)'                # Capture optional `flags`
    r'$',                           # End of sequence match
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

STATE_PATTERN:Pattern[str] = re.compile(
    r'^'                            # Start of sequence match
    r'\s*'                          # Whitespace optional (0+)
    # Flag Auto (Optional)
    r'(?P<flag_auto>auto\s+)?'      # Capture optional 'auto' flag
    # Name (Required)
    r'state'                        # Papyrus keyword 'state'
    r'\s+'                          # Whitespace required (1+)
    r'(?P<name>\w+)'                # Capture required `name`
    # Flags (Optional)
    r'\s*'                          # Whitespace optional (0+)
    r'(?P<flags>.*)'                # Capture optional `flags`
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

EVENT_PATTERN:Pattern[str] = re.compile(
    r'^'                            # Start of sequence match
    r'\s*'                          # Whitespace optional (0+)
    # Name (Required)
    r'event'                        # Papyrus keyword 'event'
    r'\s+'                          # Whitespace required (1+)
    r'(?P<name>\w+)'                # Event name
    r'\s*'                          # Whitespace optional (0+)
    # Parameters (Required)
    r'\('                           # Opening parenthesis
    r'(?P<params>[^\)]*)'           # Parameters
    r'\)'                           # Closing parenthesis
    # Flags (Optional)
    r'\s*'                          # Whitespace optional (0+)
    r'(?P<flags>.*)'                # Optional flags
    r'$',                           # End of sequence match
    re.IGNORECASE
)

FUNCTION_PATTERN:Pattern[str] = re.compile(
    r'^'                            # Start of sequence match
    r'\s*'                          # Whitespace optional (0+)
    # Type (Optional)
    r'(?P<rtype>\w+(?:\[\])?)?'     # Optional return type (with optional [])
    r'\s*'                          # Whitespace optional (0+)
    # Name (Required)
    r'function'                     # Papyrus keyword 'function'
    r'\s+'                          # Whitespace required (1+)
    r'(?P<name>\w+)'                # Function name
    r'\s*'                          # Whitespace optional (0+)
    # Parameters (Required)
    r'\('                           # Opening parenthesis
    r'(?P<params>[^\)]*)'           # Parameters (anything except ')' character)
    r'\)'                           # Closing parenthesis
    # Flags (Optional)
    r'\s*'                          # Whitespace optional (0+)
    r'(?P<flags>.*)'                # Optional flags (rest of line)
    r'$',                           # End of sequence match
    re.IGNORECASE
)
