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
    r'^'                                   # Start of line
    r'\s*'                                 # Optional leading whitespace
    r'(?P<type>\w+(?:\[\])?)'              # Property type
    r'\s+property\s+'                      # 'property' keyword
    r'(?P<name>\w+)'                       # Property name
    r'(?:\s*=\s*(?P<initializer>[^\s]+))?' # Optional initializer (e.g., = False)
    r'\s*'                                 # Optional whitespace
    r'(?P<flags>.*)'                       # Optional flags
    r'$',                                  # End of line
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

STATE_PATTERN = re.compile(
    r'^'                            # Start of line
    r'\s*(?P<flags>auto\s+)?'       # Optional 'auto' flag
    r'state\s+'                     # 'state' keyword
    r'(?P<name>\w+)'                # State name
    r'\s*$',                        # Optional trailing whitespace, end of line
    re.IGNORECASE
)

STATE_END_PATTERN = re.compile(
    r'^\s*endstate\s*$',            # 'endstate' keyword, optional whitespace
    re.IGNORECASE
)

GROUP_PATTERN = re.compile(
    r'^'                            # Start of line
    r'\s*group\s+'                  # 'group' keyword
    r'(?P<name>\w+)'                # Group name
    r'(?P<flags>.*)'                # Optional flags
    r'$',                           # End of line
    re.IGNORECASE
)

GROUP_END_PATTERN = re.compile(
    r'^\s*endgroup\s*$',            # 'endgroup' keyword, optional whitespace
    re.IGNORECASE
)


# Documentation
#---------------------------------------------

def collect_braced_docstring(lines: list[str], line_index: int) -> str:
    """
    Collects a braced docstring { ... } immediately below the code element at line_index.
    Allows blank lines between the element and the docstring, but nothing else.
    Returns the docstring content or an empty string if not found.
    """
    search_index = line_index + 1
    # Skip blank lines
    while search_index < len(lines) and lines[search_index].strip() == "":
        search_index += 1
    # Check for opening brace
    if search_index < len(lines) and lines[search_index].lstrip().startswith("{"):
        brace_line = lines[search_index].lstrip()
        doc_lines = []
        # If the opening brace is on a line by itself, skip it
        if brace_line.strip() == "{":
            search_index += 1
        else:
            doc_lines.append(brace_line.lstrip()[1:].rstrip())
            search_index += 1
        # Collect until closing brace
        while search_index < len(lines):
            line = lines[search_index]
            closing_brace_pos = line.find("}")
            if closing_brace_pos != -1:
                doc_lines.append(line[:closing_brace_pos])
                break
            doc_lines.append(line.rstrip())
            search_index += 1
        return "\n".join(doc_lines).strip()
    return ""


def collect_contiguous_comments(lines: list[str], line_index: int) -> str:
    """
    Collects contiguous line/block comments immediately above the code element at line_index.
    Stops at the first blank or non-comment line.
    Returns the comments as a single string (joined by newlines), or an empty string if none found.
    """
    comment_lines = []
    search_index = line_index - 1
    while search_index >= 0:
        line = lines[search_index]
        if line.strip() == "":
            break  # Blank line breaks the comment block
        stripped = line.lstrip()
        if stripped.startswith(";") or stripped.startswith(";/"):
            comment_lines.append(stripped)
            search_index -= 1
        else:
            break  # Non-comment line breaks the comment block
    if comment_lines:
        # Comments are collected in reverse order, so reverse them
        comments = [l for l in reversed(comment_lines)]
        # Optionally, strip leading ';' and whitespace for a cleaner doc
        comments = [l.lstrip(";").strip() for l in comments]
        return "\n".join(comments)
    return ""


def parse_documentation(lines: list[str], line_index: int) -> str:
    """
    Collects Papyrus documentation for a code element at line_index.
    - Collects braced docstring below (with blank lines allowed, but nothing else in between).
    - Collects contiguous line/block comments above (no blank lines allowed).
    - If both exist, combines them (docstring first, then comments).
    """
    docstring = collect_braced_docstring(lines, line_index)
    comments = collect_contiguous_comments(lines, line_index)
    if docstring and comments:
        return f"{docstring}\n{comments}"
    elif docstring:
        return docstring
    elif comments:
        return comments
    else:
        return ""


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


def parse_member_property(property_match:Match[str], lines:list[str], line_index:int) -> Member | None:
    member:Member = Member()
    member.name = papyrus.normalize.member_name(property_match.group("name"))
    member.index = line_index
    member.definition = lines[line_index]
    member.documentation = parse_documentation(lines, line_index)
    member.state = ""
    member.kind = papyrus.normalize.symbol("Property")
    #----------
    member.type = papyrus.normalize.script_type(property_match.group("type"))
    #----------
    # Get initializer if present and store in parameters as a single-element list
    initializer = property_match.group("initializer")
    if initializer:
        initializer = papyrus.normalize.symbol(initializer)
        member.parameters = [initializer] if initializer is not None else []
    #----------
    flags:str = property_match.group("flags")
    flags = papyrus.normalize.strip_comments(flags)
    member.flags = papyrus.normalize.script_flags(flags.split())
    #----------
    return member


def parse_member_function(function_match:Match[str], lines:list[str], line_index:int) -> Member | None:
    member:Member = Member()
    member.name = papyrus.normalize.member_name(function_match.group("name"))
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

def parse_state_block(lines, start_index, state_name):
    """Parse a state block, returning members and the index after the block."""
    members = []
    line_index = start_index
    while line_index < len(lines):
        line = lines[line_index]

        # End of state block
        if STATE_END_PATTERN.match(line):
            return members, line_index

        # Parse members inside the state
        function_match = FUNCTION_PATTERN.match(line)
        if function_match:
            member = parse_member_function(function_match, lines, line_index)
            if member:
                member.state = state_name
                members.append(member)
            line_index += 1
            continue

        event_match = EVENT_PATTERN.match(line)
        if event_match:
            member = parse_member_event(event_match, lines, line_index)
            if member:
                member.state = state_name
                members.append(member)
            line_index += 1
            continue

        # Skip other lines (structs, properties, etc. are not allowed in states)
        line_index += 1
    return members, line_index


def parse_group_block(lines, start_index, group_name, group_flags):
    """Parse a group block, returning properties and the index after the block."""
    members = []
    line_index = start_index
    while line_index < len(lines):
        line = lines[line_index]

        # End of group block
        if GROUP_END_PATTERN.match(line):
            return members, line_index

        # Parse members inside the group
        property_match = PROPERTY_PATTERN.match(line)
        if property_match:
            member = parse_member_property(property_match, lines, line_index)
            if member:
                member.group = group_name
                member.group_flags = group_flags.strip()
                members.append(member)

        line_index += 1
    return members, line_index


# TODO: Detect property groups for properties.
# TODO: Detect get/set capabilities for non-auto properties.
# TODO: Detect states for events and functions.
# TODO: Support line continuations.
# TODO: Support guards and guard flags on properties.
def parse(script_file_path: str) -> Script:
    with open(script_file_path, encoding="utf-8") as file:
        lines = file.readlines()

    script = Script()
    script.header = parse_header(lines)
    script.members = []

    line_index = script.header.index + 1
    while line_index < len(lines):
        line = lines[line_index]

        # State block
        state_match = STATE_PATTERN.match(line)
        if state_match:
            state_name = state_match.group("name")
            state_members, state_end_index = parse_state_block(lines, line_index + 1, state_name)
            script.members.extend(state_members)
            line_index = state_end_index + 1
            continue

        # Group block
        group_match = GROUP_PATTERN.match(line)
        if group_match:
            group_name = group_match.group("name")
            group_flags = group_match.group("flags")
            group_members, group_end_index = parse_group_block(lines, line_index + 1, group_name, group_flags)
            script.members.extend(group_members)
            line_index = group_end_index + 1
            continue

        # Property
        property_match = PROPERTY_PATTERN.match(line)
        if property_match:
            member = parse_member_property(property_match, lines, line_index)
            if member:
                script.members.append(member)
            line_index += 1
            continue

        # Function
        function_match = FUNCTION_PATTERN.match(line)
        if function_match:
            member = parse_member_function(function_match, lines, line_index)
            if member:
                member.state = ""  # Empty state
                script.members.append(member)
            line_index += 1
            continue

        # Event (in empty state)
        event_match = EVENT_PATTERN.match(line)
        if event_match:
            member = parse_member_event(event_match, lines, line_index)
            if member:
                member.state = ""  # Empty state
                script.members.append(member)
            line_index += 1
            continue

        # Struct
        struct_match = STRUCT_PATTERN.match(line)
        if struct_match:
            member = parse_member_struct(struct_match, lines, line_index)
            if member:
                script.members.append(member)
            line_index += 1
            continue

        # Skip other lines
        line_index += 1

    return script
