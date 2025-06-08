import logging
import re
from re import Match
from app import papyrus
from app.papyrus.code import Header, Member, Script, ScriptName


# Regular Expressions
#---------------------------------------------

HEADER_PATTERN = re.compile(
    r'^'                            # Start of line
    r'\s*'                          # Optional leading whitespace
    r'scriptname\s+'                # 'scriptname' keyword and at least one space
    r'(?P<name>[^\s]+)'             # Script name (non-whitespace)
    r'(?:\s+extends\s+'             # Optional: 'extends' keyword and parent name
    r'(?P<extends>[^\s]+))?'        # Parent script name (non-whitespace)
    r'(?P<flags>(?:\s+\w+)*)'       # Optional flags (zero or more flag words)
    r'\s*'                          # Optional trailing whitespace
    r'$',                           # End of line
    re.IGNORECASE
)

FUNCTION_PATTERN = re.compile(
    r'^'                            # Start of line
    r'\s*'                          # Optional leading whitespace
    r'(?P<rtype>\w+(?:\[\])?)?'     # Optional return type (with optional [])
    r'\s*function\s+'               # 'function' keyword
    r'(?P<name>\w+)'                # Function name
    r'\s*\('                        # Opening parenthesis
    r'(?P<params>[^\)]*)'           # Parameters (anything except ')')
    r'\)\s*'                        # Closing parenthesis
    r'(?P<flags>.*)'                # Optional flags (rest of line)
    r'$',                           # End of line
    re.IGNORECASE
)

EVENT_PATTERN = re.compile(
    r'^'                            # Start of line
    r'\s*event\s+'                  # 'event' keyword
    r'(?P<name>\w+)'                # Event name
    r'\s*\('                        # Opening parenthesis
    r'(?P<params>[^\)]*)'           # Parameters
    r'\)\s*'                        # Closing parenthesis
    r'(?P<flags>.*)'                # Optional flags
    r'$',                           # End of line
    re.IGNORECASE
)

PROPERTY_PATTERN = re.compile(
    r'^'                            # Start of line
    r'\s*'                          # Optional leading whitespace
    r'(?P<type>\w+(?:\[\])?)'       # Property type
    r'\s+property\s+'               # 'property' keyword
    r'(?P<name>\w+)'                # Property name
    r'\s*'                          # Optional whitespace
    r'(?P<flags>.*)'                # Optional flags
    r'$',                           # End of line
    re.IGNORECASE
)

PROPERTY_END_PATTERN = re.compile(
    r'^'                            # Start of line
    r'\s*'                          # Optional leading whitespace
    r'endproperty\b',               # 'endproperty' keyword
    re.IGNORECASE
)

STRUCT_PATTERN = re.compile(
    r'^'                            # Start of line
    r'\s*struct\s+'                 # 'struct' keyword
    r'(?P<name>\w+)',               # Struct name
    re.IGNORECASE
)

PARAMETERS_PATTERN = re.compile(
    r'^'                            # Start of line
    r'\s*(?P<type>\w+(?:\[\])?)'    # Parameter type
    r'\s+(?P<name>\w+)'             # Parameter name
    r'(\s*=\s*.+)?'                 # Optional default value
    r'$',                           # End of line
    re.IGNORECASE
)


# Documentation
#---------------------------------------------

# TODO: This function is too greedy with check-1. It should stop at the first non-comment line.
# TODO: Ensire the function returns the result of both the comment and the block docstring.
def parse_documentation(lines:list[str], line_index:int):
    """
    Extracts the documentation comment for a script or member.
    Supports:
    - Consecutive comment lines (;) immediately above the element (with blank lines allowed)
    - Or, a block docstring in curly braces { ... } immediately below the element (with blank lines allowed)
    Returns the doc string, or a default if none is found.
    """
    # 1. Check for doc comments above (Papyrus ;)
    desc_lines = []
    idx = line_index - 1
    while idx >= 0:
        line = lines[idx].rstrip()
        if line.lstrip().startswith(";"):
            desc_lines.insert(0, line.lstrip(";").strip())
            idx -= 1
        elif line.strip() == "":
            idx -= 1
        else:
            break
    description = "\n".join(desc_lines).strip()
    if description:
        return description

    # 2. Check for curly-brace doc block immediately below (allow blank lines)
    idx = line_index + 1
    # Skip blank lines
    while idx < len(lines) and lines[idx].strip() == "":
        idx += 1
    if idx < len(lines) and lines[idx].lstrip().startswith("{"):
        doc_block = []
        line = lines[idx].lstrip()
        # If the opening brace is on a line by itself, skip it
        if line.strip() == "{":
            idx += 1
        else:
            # If there's text after the opening brace, include it (minus the brace)
            doc_block.append(line.lstrip("{").rstrip())
            idx += 1
        # Collect until closing brace
        while idx < len(lines):
            line = lines[idx]
            if "}" in line:
                # If there's text before the closing brace, include it (minus the brace)
                before, _, _ = line.partition("}")
                doc_block.append(before.rstrip())
                break
            doc_block.append(line.rstrip())
            idx += 1
        documentation = "\n".join([l.rstrip() for l in doc_block]).strip()
        if documentation:
            return documentation

    # 3. Fallback default
    return "No documentation provided."


# Header
#---------------------------------------------

def parse_header(lines:list[str]) -> Header:
    """
    Finds the script header line information.
    Returns values or raises ValueError if `ScriptName` is not found.
    """
    inside_comment_block = False
    for line_index, line in enumerate(lines):
        # Skip empty lines and comments
        line = line.strip()
        if line == "":
            # If the line is empty, skip it
            continue
        elif line.startswith(";/") and line.endswith("/;"):
            # This is a single-line block comment, skip it
            continue
        elif line.startswith(";/"):
            # This is the start of a multi-line block comment, skip it
            inside_comment_block = True
            continue
        elif line.endswith("/;"):
            # This is the end of a multi-line block comment, skip it
            inside_comment_block = False
            continue
        elif line.startswith(";"):
            # This is a single-line comment, skip it
            continue
        elif inside_comment_block:
            # If we are in a multi-line block comment, skip it
            continue

        line = papyrus.normalize.strip_comments(line)
        line = papyrus.normalize.whitespace(line)

        header_match = HEADER_PATTERN.match(line)
        if header_match:
            header:Header = Header()
            header.index = line_index
            header.definition = papyrus.normalize.script_definition(line)
            header.documentation = parse_documentation(lines, line_index)
            header.name = ScriptName(header_match.group("name"))
            header.extends = ScriptName(header_match.group("extends"))
            #----------
            flags:str = header_match.group("flags")
            flags = papyrus.normalize.strip_comments(flags)
            header.flags = papyrus.normalize.script_flags(flags.split())
            #----------
            return header
    raise ValueError("ScriptName not found")


# Members
#---------------------------------------------

#TODO: Fix parameter type Match[str] to str. Expects regex match group but is passed a string.
def parse_member_parameters(parameters_line:str) -> list[str]:
    """Parse a Papyrus parameter string into a list of normalized parameter strings."""
    parameters = []
    if parameters_line:
        parameters_line = papyrus.normalize.strip_comments(parameters_line)
        for element in parameters_line.split(","):
            element = element.strip()
            if not element:
                continue
            param_match = PARAMETERS_PATTERN.match(element)
            if param_match:
                ptype = param_match.group(1)
                pname = param_match.group(2)
                default = param_match.group(3) or ""
                default_norm = papyrus.normalize.default_value(default)
                param_str_piece = f"{papyrus.normalize.script_type(ptype)} {pname}{(' ' + default_norm) if default_norm else ''}".strip()
                parameters.append(param_str_piece)
            else:
                parameters.append(element)
    else:
        logging.warning("parse_member_parameters: No parameters found in line.")
    return parameters


def parse_member_property(property_match:Match[str], lines:list[str], line_index:int, seen_properties:list[str]) -> Member | None:
    key:str = papyrus.normalize.member_name(property_match.group("name"))
    #----------
    if key in seen_properties: return None
    else: seen_properties.add(key)
    #----------
    member:Member = Member()
    member.name = key
    member.index = line_index
    member.definition = lines[line_index]
    member.documentation = parse_documentation(lines, line_index)
    member.state = ""
    member.kind = papyrus.normalize.symbol("Property")
    #----------
    member.type = papyrus.normalize.script_type(property_match.group("type"))
    #----------
    flags:str = property_match.group("flags")
    flags = papyrus.normalize.strip_comments(flags)
    member.flags = papyrus.normalize.script_flags(flags.split())
    #----------
    member.parameters = []
    #----------
    return member


def parse_member_function(function_match:Match[str], lines:list[str], line_index:int, property_names:list[str]) -> Member | None:
    key:str = papyrus.normalize.member_name(function_match.group("name"))
    #----------
    # Skip property accessor functions (Get<Property>, Set<Property>)
    # This is a workaround to avoid parsing them as functions.
    # TODO: This is not a correct naming for property accessors, they should not include the property name.
    #   Property accessors are just named "Get" or "Set" without the property name.
    for property_name in property_names:
        if key == f"Get{property_name}" or key == f"Set{property_name}":
            return None
    #----------
    member:Member = Member()
    member.name = key
    member.index = line_index
    member.definition = lines[line_index]
    member.documentation = parse_documentation(lines, line_index)
    member.state = ""
    member.kind = papyrus.normalize.symbol("Function")
    #----------
    member.type = function_match.group("rtype")
    #----------
    flags:str = function_match.group("flags")
    flags = papyrus.normalize.strip_comments(flags)
    member.flags = papyrus.normalize.script_flags(flags.split())
    #----------
    parameters:str = function_match.group("params")
    member.parameters = parse_member_parameters(parameters)
    #----------
    return member


def parse_member_event(event_match:Match[str], lines:list[str], line_index:int) -> Member | None:
    key:str = papyrus.normalize.member_name(event_match.group("name"))
    member:Member = Member()
    member.name = key
    member.index = line_index
    member.definition = lines[line_index]
    member.documentation = parse_documentation(lines, line_index)
    member.state = ""
    member.kind = papyrus.normalize.symbol("Event")
    #----------
    flags:str = event_match.group("flags")
    flags = papyrus.normalize.strip_comments(flags)
    member.flags = papyrus.normalize.script_flags(flags.split())
    #----------
    parameters:str = event_match.group("params")
    member.parameters = parse_member_parameters(parameters)
    #----------
    return member


def parse_member_struct(struct_match:Match[str], lines:list[str], line_index:int) -> Member | None:
    key:str = papyrus.normalize.member_name(struct_match.group("name"))
    member:Member = Member()
    member.name = key
    member.index = line_index
    member.definition = lines[line_index]
    member.documentation = parse_documentation(lines, line_index)
    member.state = ""
    member.kind = papyrus.normalize.symbol("Struct")
    return member


# Parse
#---------------------------------------------

# TODO: Detect property groups for properties.
# TODO: Detect get/set capabilities for non-auto properties.
# TODO: Detect states for events and functions.
# TODO: Support line continuations.
def parse(script_file_path:str) -> Script:
    with open(script_file_path, encoding="utf-8") as file:
        lines:list[str] = file.readlines()

    script:Script = Script()
    # script.source_file = script_file_path

    # Pass 0: find and parse the script header
    #---------------------------------------------
    script.header = parse_header(lines)

    # Initialize loop variables
    #---------------------------------------------
    seen_properties = set()
    property_names = set()

    # Pass 1: collect all property names
    #---------------------------------------------
    for line_index, line in enumerate(lines[script.header.index+1:], start=script.header.index+1):
        property_match = PROPERTY_PATTERN.match(line)
        if property_match:
            pname = papyrus.normalize.member_name(property_match.group("name"))
            property_names.add(pname)

    # Pass 2: collect members, skipping property accessors and property block contents
    #---------------------------------------------
    inside_property_block = False
    for line_index, line in enumerate(lines[script.header.index+1:], start=script.header.index+1):

        #---------------------------------------------
        # Property: Detect start of a property block
        property_match = PROPERTY_PATTERN.match(line)
        if property_match:
            member = parse_member_property(property_match, lines, line_index, seen_properties)
            if member:
                script.members.append(member)

            # Check if this is a block property (not auto)
            line_strip = line.strip().lower()
            if not line_strip.endswith("auto") \
                and not line_strip.endswith("auto const") \
                and not line_strip.endswith("auto readonly"):
                inside_property_block = True
            continue

        # Property: Detect end of a property block
        if inside_property_block:
            if PROPERTY_END_PATTERN.match(line):
                inside_property_block = False
            continue  # Skip everything inside property blocks
        #---------------------------------------------

        # Function
        function_match = FUNCTION_PATTERN.match(line)
        if function_match:
            member = parse_member_function(function_match, lines, line_index, property_names)
            if member:
                script.members.append(member)
            continue

        # Event
        event_match = EVENT_PATTERN.match(line)
        if event_match:
            member = parse_member_event(event_match, lines, line_index)
            if member:
                script.members.append(member)
            continue

        # Struct
        struct_match = STRUCT_PATTERN.match(line)
        if struct_match:
            member = parse_member_struct(struct_match, lines, line_index)
            if member:
                script.members.append(member)
            continue

    return script
