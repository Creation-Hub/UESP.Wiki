import re
from re import Match
from app.common.mutable import MutableBool
from app import papyrus
from app.papyrus.code import Event
from app.papyrus.code import Function
from app.papyrus.code import Header
from app.papyrus.code import Property
from app.papyrus.code import PropertyGroup
from app.papyrus.code import Script
from app.papyrus.code import ScriptName
from app.papyrus.code import State
from app.papyrus.code import Structure
from app.papyrus.code import Variable

# Regular Expressions
#---------------------------------------------

# Regular Patterns
#---------------------------------------------

HEADER_PATTERN = re.compile(
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
VARIABLE_PATTERN = re.compile(
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

PARAMETERS_PATTERN = re.compile(
    r'^'                            # Start of sequence match
    r'\s*'                          # Whitespace optional (0+)
    # Type (Required)
    r'(?P<type>\w+(?:\[\])?)'       # Parameter type
    r'\s+'                          # Whitespace required (1+)
    # Name (Required)
    r'(?P<name>\w+)'                # Parameter name
    # Initializer (Optional)
    r'(\s*=\s*.+)?'                 # Optional default value
    r'$',                           # End of sequence match
    re.IGNORECASE
)

#-------------------------

STRUCT_PATTERN = re.compile(
    r'^'                            # Start of sequence match
    r'\s*'                          # Whitespace optional (0+)
    # Name (Required)
    r'struct'                       # Papyrus keyword 'struct'
    r'\s+'                          # Whitespace required (1+)
    r'(?P<name>\w+)',               # Capture required `name`
    re.IGNORECASE
)

STRUCT_END_PATTERN = re.compile(
    r'^'                            # Start of sequence match
    r'\s*'                          # Whitespace optional (0+)
    r'endstruct'                    # Papyrus keyword 'endstruct'
    r'\b',                          # Word boundary
    re.IGNORECASE
)

#-------------------------

GROUP_PATTERN = re.compile(
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

GROUP_END_PATTERN = re.compile(
    r'^'                            # Start of sequence match
    r'\s*'                          # Whitespace optional (0+)
    r'endgroup'                     # Papyrus keyword 'endgroup'
    r'\s*'                          # Whitespace optional (0+)
    r'$',                           # End of sequence match
    re.IGNORECASE
)

PROPERTY_PATTERN = re.compile(
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

PROPERTY_END_PATTERN = re.compile(
    r'^'                            # Start of sequence match
    r'\s*'                          # Whitespace optional (0+)
    r'endproperty'                  # Papyrus keyword 'endproperty'
    r'\b',                          # Word boundary
    re.IGNORECASE
)

#-------------------------

STATE_PATTERN = re.compile(
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

STATE_END_PATTERN = re.compile(
    r'^'                            # Start of sequence match
    r'\s*'                          # Whitespace optional (0+)
    r'endstate'                     # Papyrus keyword 'endstate'
    r'\s*'                          # Whitespace optional (0+)
    r'$',                           # End of sequence match
    re.IGNORECASE
)

EVENT_PATTERN = re.compile(
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

FUNCTION_PATTERN = re.compile(
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


# Documentation
#---------------------------------------------

def collect_braced_docstring(lines:list[str], line_index:int) -> str:
    """
    Collects a braced docstring { ... } immediately below the code element at line_index.
    Allows blank lines between the element and the docstring, but nothing else.
    Returns the docstring content or an empty string if not found.
    """
    search_index:int = line_index + 1

    # Skip blank lines
    while search_index < len(lines) and lines[search_index].strip() == "":
        search_index += 1

    # Check for opening brace
    if search_index < len(lines) and lines[search_index].lstrip().startswith("{"):
        brace_line:str = lines[search_index].lstrip()
        doc_lines:list[str] = []

        # If the opening brace is on a line by itself, skip it
        if brace_line.strip() == "{":
            search_index += 1
            # Collect until closing brace
            while search_index < len(lines):
                line:str = lines[search_index]
                closing_brace_pos:int = line.find("}")
                if closing_brace_pos != -1:
                    doc_lines.append(line[:closing_brace_pos])
                    break
                doc_lines.append(line.rstrip())
                search_index += 1
        else:
            # Opening brace and content are on the same line
            after_brace:str = brace_line[1:]
            closing_brace_pos:int = after_brace.find("}")
            if closing_brace_pos != -1:
                # Both braces on the same line
                doc_lines.append(after_brace[:closing_brace_pos])
                return "\n".join(doc_lines).strip()
            else:
                # No closing brace on this line, collect as before
                doc_lines.append(after_brace.rstrip())
                search_index += 1
                while search_index < len(lines):
                    line:str = lines[search_index]
                    closing_brace_pos:int = line.find("}")
                    if closing_brace_pos != -1:
                        doc_lines.append(line[:closing_brace_pos])
                        break
                    doc_lines.append(line.rstrip())
                    search_index += 1

        return "\n".join(doc_lines).strip()
    return ""


def collect_contiguous_comments(lines:list[str], line_index:int) -> str:
    """
    Collects contiguous line/block comments immediately above the code element at line_index.
    Stops at the first blank or non-comment line.
    Returns the comments as a single string (joined by newlines), or an empty string if none found.
    """
    comment_lines:list[str] = []
    search_index:int = line_index - 1
    while search_index >= 0:
        line:str = lines[search_index]
        if line.strip() == "":
            break  # Blank line breaks the comment block
        stripped:str = line.lstrip()
        if stripped.startswith(";") or stripped.startswith(";/"):
            comment_lines.append(stripped)
            search_index -= 1
        else:
            break  # Non-comment line breaks the comment block
    if comment_lines:
        # Comments are collected in reverse order, so reverse them
        comments:list[str] = [l for l in reversed(comment_lines)]
        # Optionally, strip leading ';' and whitespace for a cleaner doc
        comments = [l.lstrip(";").strip() for l in comments]
        return "\n".join(comments)
    return ""


def parse_documentation(lines:list[str], line_index:int) -> str:
    """
    Collects Papyrus documentation for a code element at line_index.
    - Collects braced docstring below (with blank lines allowed, but nothing else in between).
    - Collects contiguous line/block comments above (no blank lines allowed).
    - If both exist, combines them (docstring first, then comments).
    """
    docstring:str = collect_braced_docstring(lines, line_index)
    comments:str = collect_contiguous_comments(lines, line_index)
    if docstring and comments:
        return f"{docstring}\n{comments}"
    elif docstring:
        return docstring
    elif comments:
        return comments
    else:
        return ""


# Elements
#---------------------------------------------

def parse_flags(text:str) -> list[str]:
    """Parse a Papyrus flags string into a list of normalized flag strings."""
    flags:list[str] = []
    if text:
        text = papyrus.normalize.strip_comments(text)
        tokens:list[str] = text.split()
        for flag in tokens:
            flag = flag.strip()
            if not flag: continue
            else: flags.append(papyrus.normalize.symbol(flag))
    return flags


def parse_initializer(initializer_text:str) -> str:
    if initializer_text:
        return papyrus.normalize.symbol(initializer_text)
    return ""


def parse_parameters(parameters_line:str) -> list[str]:
    """Parse a Papyrus parameter string into a list of normalized parameter strings."""
    parameters:list[str] = []
    if parameters_line:
        parameters_line = papyrus.normalize.strip_comments(parameters_line)
        tokens:list[str] = parameters_line.split(",")
        for token in tokens:
            token = token.strip()
            if not token:
                continue
            parameter_match = PARAMETERS_PATTERN.match(token)
            if parameter_match:
                type:str = parameter_match.group(1)
                name:str = parameter_match.group(2)
                initial:str = parameter_match.group(3) or ""
                if initial:
                    initial = papyrus.normalize.default_value(initial)
                parameter:str = f"{papyrus.normalize.script_type(type)} {name}{(' ' + initial) if initial else ''}".strip()
                parameters.append(parameter)
            else:
                parameters.append(token)
    return parameters


# Header
#---------------------------------------------

def skip(inside_comment_block:MutableBool, line:str) -> bool:
    """
    Determines if a line should be skipped based on whitespace and comment conditions.
    """
    line = line.strip()
    if line == "":
        # If the line is empty, skip it
        return True
    elif line.startswith(";/") and line.endswith("/;"):
        # This is a single-line block comment, skip it
        return True
    elif line.startswith(";/"):
        # This is the start of a multi-line block comment, skip it
        inside_comment_block.value = True
        return True
    elif line.endswith("/;"):
        # This is the end of a multi-line block comment, skip it
        inside_comment_block.value = False
        return True
    elif line.startswith(";"):
        # This is a single-line comment, skip it
        return True
    elif inside_comment_block.value:
        # If we are in a multi-line block comment, skip it
        return True
    else:
        return False


def parse_header(lines:list[str]) -> Header:
    """
    Finds the script header line information.
    Returns values or raises ValueError if `ScriptName` is not found.
    """
    inside_comment_block:MutableBool = MutableBool()
    for line_index, line in enumerate(lines):

        # Skip lines that are inside a comment block
        if skip(inside_comment_block, line): continue

        # Normalize the line by stripping comments and whitespace
        line = papyrus.normalize.strip_comments(line)
        line = papyrus.normalize.whitespace(line)

        # Check if this line matches the header pattern
        header_match = HEADER_PATTERN.match(line)
        if header_match:
            header:Header = Header()
            header.index = line_index
            header.index_end = line_index
            header.definition = papyrus.normalize.script_definition(line)
            header.documentation = parse_documentation(lines, line_index)
            header.name = ScriptName(header_match.group("name"))
            header.extends = ScriptName(header_match.group("extends"))
            header.flags = parse_flags(header_match.group("flags"))
            return header
    raise ValueError("ScriptName not found")


# Members
#---------------------------------------------

def parse_variable(variable_match:Match[str], lines:list[str], line_index:int) -> Variable:
    variable:Variable = Variable()
    variable.name = papyrus.normalize.member_name(variable_match.group("name"))
    variable.index = line_index
    variable.index_end = line_index
    variable.definition = lines[line_index]
    variable.documentation = parse_documentation(lines, line_index)
    variable.type = papyrus.normalize.script_type(variable_match.group("type"))
    variable.flags = parse_flags(variable_match.group("flags"))
    variable.value_auto = parse_initializer(variable_match.group("initializer"))
    return variable


def parse_structure(struct_match:Match[str], lines:list[str], line_index:int) -> Structure:
    structure:Structure = Structure()
    structure.name = papyrus.normalize.member_name(struct_match.group("name"))
    structure.index = line_index
    structure.index_end = line_index
    structure.definition = lines[line_index]
    structure.documentation = parse_documentation(lines, line_index)

    line_index += 1
    while line_index < len(lines):
        line:str = lines[line_index]

        # Terminate this loop if we reach the block end.
        if STRUCT_END_PATTERN.match(line):
            break

        variable_match = VARIABLE_PATTERN.match(line)
        if variable_match:
            variable:Variable = parse_variable(variable_match, lines, line_index)
            structure.variables[variable.name] = variable

        line_index += 1

    # The last visited `line_index` will be the `index_end` of this structure block.
    structure.index_end = line_index
    return structure


def parse_property(property_match:Match[str], lines:list[str], line_index:int) -> Property:
    property:Property = Property()
    property.index = line_index
    property.index_end = line_index
    property.definition = lines[line_index]
    property.documentation = parse_documentation(lines, line_index)
    property.name = papyrus.normalize.member_name(property_match.group("name"))
    property.flags = parse_flags(property_match.group("flags"))
    property.type = papyrus.normalize.script_type(property_match.group("type"))
    property.value_auto = parse_initializer(property_match.group("initializer"))
    return property


def parse_function(function_match:Match[str], lines:list[str], line_index:int) -> Function:
    function:Function = Function()
    function.name = papyrus.normalize.member_name(function_match.group("name"))
    function.index = line_index
    function.index_end = line_index
    function.definition = lines[line_index]
    function.documentation = parse_documentation(lines, line_index)
    function.type = papyrus.normalize.script_type(function_match.group("rtype"))
    function.flags = parse_flags(function_match.group("flags"))
    function.parameters = parse_parameters(function_match.group("params"))
    return function


def parse_event(event_match:Match[str], lines:list[str], line_index:int) -> Event:
    event:Event = Event()
    event.name = papyrus.normalize.member_name(event_match.group("name"))
    event.index = line_index
    event.index_end = line_index
    event.definition = lines[line_index]
    event.documentation = parse_documentation(lines, line_index)
    event.flags = parse_flags(event_match.group("flags"))
    event.parameters = parse_parameters(event_match.group("params"))
    return event


# Blocks
#---------------------------------------------

def parse_property_group(group_match:Match[str], lines:list[str], line_index:int) -> PropertyGroup:
    group:PropertyGroup = PropertyGroup()
    group.index = line_index
    group.index_end = line_index
    group.definition = lines[line_index]
    group.documentation = parse_documentation(lines, line_index)
    group.name = group_match.group("name")
    group.flags = parse_flags(group_match.group("flags"))

    line_index += 1
    while line_index < len(lines):
        line:str = lines[line_index]

        # Terminate this loop if we reach the block end.
        if GROUP_END_PATTERN.match(line):
            break

        # Parse members inside the group
        property_match = PROPERTY_PATTERN.match(line)
        if property_match:
            property:Property = parse_property(property_match, lines, line_index)
            if property:
                group.properties[property.name] = property

        line_index += 1

    # The last visited `line_index` will be the `index_end` of this group block.
    group.index_end = line_index
    return group


def parse_state(state_match:Match[str], lines:list[str], line_index:int) -> State:
    state:State = State()
    state.index = line_index
    state.index_end = line_index
    state.definition = lines[line_index]
    state.documentation = parse_documentation(lines, line_index)
    state.name = papyrus.normalize.member_name(state_match.group("name"))
    state.flags = parse_flags(state_match.group("flags"))

    line_index += 1
    while line_index < len(lines):
        line:str = lines[line_index]

        # Terminate this loop if we reach the block end.
        if STATE_END_PATTERN.match(line):
            break

        # Parse any function methods inside this state.
        function_match = FUNCTION_PATTERN.match(line)
        if function_match:
            function:Function = parse_function(function_match, lines, line_index)
            if function:
                state.methods[function.name] = function
            line_index += 1
            continue

        # Parse any event methods inside this state.
        event_match = EVENT_PATTERN.match(line)
        if event_match:
            event:Event = parse_event(event_match, lines, line_index)
            if event:
                state.methods[event.name] = event
            line_index += 1
            continue

        line_index += 1

    # The last visited `line_index` will be the `index_end` of this state block.
    state.index_end = line_index
    return state


# Parse
#---------------------------------------------

def parse(script_file_path:str) -> Script:
    with open(script_file_path, encoding="utf-8") as file:
        lines:list[str] = file.readlines()

    script:Script = Script()
    script.header = parse_header(lines)

    line_index:int = script.header.index + 1
    while line_index < len(lines):
        line:str = lines[line_index]

        # Group Block
        group_match = GROUP_PATTERN.match(line)
        if group_match:
            group:PropertyGroup = parse_property_group(group_match, lines, line_index)
            script.members[group.name] = group
            line_index = group.index_end + 1
            continue

        # State Block
        state_match = STATE_PATTERN.match(line)
        if state_match:
            state:State = parse_state(state_match, lines, line_index)
            script.members[state.name] = state
            line_index = state.index_end + 1
            continue

        # Property
        property_match = PROPERTY_PATTERN.match(line)
        if property_match:
            property:Property = parse_property(property_match, lines, line_index)
            if property:
                script.members[property.name] = property
            line_index += 1
            continue

        # Function
        function_match = FUNCTION_PATTERN.match(line)
        if function_match:
            function:Function = parse_function(function_match, lines, line_index)
            if function:
                script.members[function.name] = function
            line_index += 1
            continue

        # Event
        event_match = EVENT_PATTERN.match(line)
        if event_match:
            event:Event = parse_event(event_match, lines, line_index)
            if event:
                script.members[event.name] = event
            line_index += 1
            continue

        # Struct
        struct_match = STRUCT_PATTERN.match(line)
        if struct_match:
            structure:Structure = parse_structure(struct_match, lines, line_index)
            if structure:
                script.members[structure.name] = structure
            line_index += 1
            continue

        # Variable
        # TODO: This does not match lines correctly, it is disabled for now.
        if False:
            variable_match = VARIABLE_PATTERN.match(line)
            if variable_match:
                variable:Variable = parse_variable(variable_match, lines, line_index)
                if variable:
                    script.members[variable.name] = variable
                line_index += 1
                continue

        # Skip other lines
        line_index += 1

    return script
