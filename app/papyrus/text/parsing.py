import logging
from re import Match
from app.common.mutable import MutableBool
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
from app.papyrus.text import normalize
from app.papyrus.text import regex
from app.papyrus.text.parser import TextReader


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
        text = normalize.strip_comments(text)
        tokens:list[str] = text.split()
        for token in tokens:
            token = token.strip()
            if not token: continue
            else: flags.append(normalize.flag(token))
    return flags


def parse_initializer(text:str) -> str:
    if text:
        return normalize.symbol(text)
    return ""


# Header
#---------------------------------------------

def parse_header(header_match:Match[str], lines:list[str], line_index:int) -> Header:
    header:Header = Header()
    header.index = line_index
    header.index_end = line_index
    header.definition = normalize.definition(lines[line_index])
    header.documentation = parse_documentation(lines, line_index)
    header.name = ScriptName(header_match.group("name"))
    header.extends = ScriptName(header_match.group("extends"))
    header.flags = parse_flags(header_match.group("flags"))
    return header


# Members
#---------------------------------------------

def parse_variable(variable_match:Match[str], lines:list[str], line_index:int) -> Variable:
    variable:Variable = Variable()
    variable.name = normalize.member_name_upper(variable_match.group("name"))
    variable.index = line_index
    variable.index_end = line_index
    variable.definition = normalize.definition(lines[line_index])
    variable.documentation = parse_documentation(lines, line_index)
    variable.type = normalize.script_type(variable_match.group("type"))
    variable.flags = parse_flags(variable_match.group("flags"))
    variable.value = parse_initializer(variable_match.group("value"))
    return variable


def parse_parameters(parameters_line:str) -> list[Variable]:
    """Parse a Papyrus parameter string into a list of normalized parameter strings."""
    parameters:list[Variable] = []
    if parameters_line:
        parameters_line = normalize.strip_comments(parameters_line)
        tokens:list[str] = parameters_line.split(",")
        for token in tokens:
            token = token.strip()
            if not token:
                continue
            parameter_match = regex.PARAMETERS_PATTERN.match(token)
            if parameter_match:
                parameter:Variable = Variable()
                parameter.type = normalize.script_type(parameter_match.group("type"))
                parameter.name = normalize.member_name(parameter_match.group("name"))

                # TODO: Handle non-primitive default values.
                parameter.value = normalize.primitive_value(parameter_match.group("value"))
                parameters.append(parameter)
            else:
                logging.warning(f"Invalid parameter format: '{token}'")

    # Return the list of parsed parameters
    return parameters


# Block
def parse_property(property_match:Match[str], lines:list[str], line_index:int) -> Property:
    property:Property = Property()
    property.index = line_index
    property.index_end = line_index
    property.definition = normalize.definition(lines[line_index])
    property.documentation = parse_documentation(lines, line_index)
    property.name = normalize.member_name_upper(property_match.group("name"))
    property.flags = parse_flags(property_match.group("flags"))
    property.type = normalize.script_type(property_match.group("type"))
    property.value = parse_initializer(property_match.group("value"))

    if "Auto" in property.flags or "AutoReadOnly" in property.flags:
        return property

    line_index += 1
    while line_index < len(lines):
        line:str = lines[line_index]

        # Terminate this loop if we reach the block end.
        if regex.STRUCT_END_PATTERN.match(line):
            property.index_end = line_index
            break

        # Advance to next index.
        line_index += 1

    # Warn on unincremented block indexes.
    if property.index == property.index_end:
        logging.warning(f"Property '{property.name}' at line {property.index} has an unincremented block index.")

    logging.debug(f"'{property.name}'@{line_index}: Found {property.index_end - property.index} lines until end of block.")
    return property


# Block
def parse_structure(struct_match:Match[str], lines:list[str], line_index:int) -> Structure:
    structure:Structure = Structure()
    structure.index = line_index
    structure.index_end = line_index
    structure.definition = normalize.definition(lines[line_index])
    structure.documentation = parse_documentation(lines, line_index)
    structure.name = normalize.member_name_upper(struct_match.group("name"))

    line_index += 1
    while line_index < len(lines):
        line:str = lines[line_index]
        # Terminate this loop if we reach the block end.
        if regex.STRUCT_END_PATTERN.match(line):
            structure.index_end = line_index
            break

        # Match any variable definitions inside this structure.
        variable_match = regex.VARIABLE_PATTERN.match(line)
        if variable_match:
            variable:Variable = parse_variable(variable_match, lines, line_index)
            structure.variables[variable.name] = variable

        # Advance to next index.
        line_index += 1

    # Warn on unincremented block indexes.
    if structure.index == structure.index_end:
        logging.warning(f"Structure '{structure.name}' at line {structure.index} has an unincremented block index.")

    logging.debug(f"'{structure.name}'@{line_index}: Found {structure.index_end - structure.index} lines until end of block.")
    return structure


# Block
def parse_event(event_match:Match[str], lines:list[str], line_index:int) -> Event:
    event:Event = Event()
    event.name = normalize.member_name_upper(event_match.group("name"))
    event.index = line_index
    event.index_end = line_index
    event.definition = normalize.definition(lines[line_index])
    event.documentation = parse_documentation(lines, line_index)
    event.flags = parse_flags(event_match.group("flags"))
    event.parameters = parse_parameters(event_match.group("params"))

    if "Native" in event.flags:
        return event

    line_index += 1
    while line_index < len(lines):
        line:str = lines[line_index]

        # Terminate this loop if we reach the block end.
        if regex.EVENT_END_PATTERN.match(line):
            event.index_end = line_index
            break

        # Advance to next index.
        line_index += 1

    # Warn on unincremented block indexes.
    if event.index == event.index_end:
        logging.warning(f"Event '{event.name}' at line {event.index} has an unincremented block index.")

    logging.debug(f"'{event.name}'@{line_index}: Found {event.index_end - event.index} lines until end of block.")
    return event


# Block
def parse_function(function_match:Match[str], lines:list[str], line_index:int) -> Function:
    function:Function = Function()
    function.name = normalize.member_name_upper(function_match.group("name"))
    function.index = line_index
    function.index_end = line_index
    function.definition = normalize.definition(lines[line_index])
    function.documentation = parse_documentation(lines, line_index)
    function.type = normalize.script_type(function_match.group("type"))
    function.flags = parse_flags(function_match.group("flags"))
    function.parameters = parse_parameters(function_match.group("params"))

    if "Native" in function.flags:
        return function

    line_index += 1
    while line_index < len(lines):
        line:str = lines[line_index]

        # Terminate this loop if we reach the block end.
        if regex.FUNCTION_END_PATTERN.match(line):
            function.index_end = line_index
            break

        # Advance to next index.
        line_index += 1

    # Warn on unincremented block indexes.
    if function.index == function.index_end:
        logging.warning(f"Function '{function.name}' at line {function.index} has an unincremented block index.")

    logging.debug(f"'{function.name}'@{line_index}: Found {function.index_end - function.index} lines until end of block.")
    return function


# Blocks
#---------------------------------------------

def parse_property_group(group_match:Match[str], lines:list[str], line_index:int) -> PropertyGroup:
    group:PropertyGroup = PropertyGroup()
    group.index = line_index
    group.index_end = line_index
    group.definition = normalize.definition(lines[line_index])
    group.documentation = parse_documentation(lines, line_index)
    group.name = group_match.group("name")
    group.flags = parse_flags(group_match.group("flags"))

    line_index += 1
    while line_index < len(lines):
        line:str = lines[line_index]

        # Terminate this loop if we reach the block end.
        if regex.GROUP_END_PATTERN.match(line):
            group.index_end = line_index
            break

        # Parse members inside the group
        property_match = regex.PROPERTY_PATTERN.match(line)
        if property_match:
            property:Property = parse_property(property_match, lines, line_index)
            if property:
                group.properties[property.name] = property

        # Advance to next index.
        line_index += 1

    # Warn on unincremented block indexes.
    if group.index == group.index_end:
        logging.warning(f"Group '{group.name}' at line {group.index} has an unincremented block index.")

    logging.debug(f"'{group.name}'@{line_index}: Found {group.index_end - group.index} lines until end of block.")
    return group


def parse_state(state_match:Match[str], lines:list[str], line_index:int) -> State:
    state:State = State()
    state.index = line_index
    state.index_end = line_index
    state.definition = normalize.definition(lines[line_index])
    state.documentation = parse_documentation(lines, line_index)
    state.name = normalize.member_name_upper(state_match.group("name"))
    state.flags = parse_flags(state_match.group("flags"))

    line_index += 1
    while line_index < len(lines):
        line:str = lines[line_index]

        # Terminate this loop if we reach the block end.
        if regex.STATE_END_PATTERN.match(line):
            state.index_end = line_index
            break

        # Parse any function methods inside this state.
        function_match = regex.FUNCTION_PATTERN.match(line)
        if function_match:
            function:Function = parse_function(function_match, lines, line_index)
            if function:
                state.methods[function.name] = function
            line_index += 1
            continue

        # Parse any event methods inside this state.
        event_match = regex.EVENT_PATTERN.match(line)
        if event_match:
            event:Event = parse_event(event_match, lines, line_index)
            if event:
                state.methods[event.name] = event
            line_index += 1
            continue

        line_index += 1

    # Warn on unincremented block indexes.
    if state.index == state.index_end:
        logging.warning(f"State '{state.name}' at line {state.index} has an unincremented block index.")

    logging.debug(f"'{state.name}'@{line_index}: Found {state.index_end - state.index} lines until end of block.")
    return state


# Parse
#---------------------------------------------

def load(script_file_path:str) -> list[str]:
    with open(script_file_path, encoding="utf-8") as file:
        lines:list[str] = file.readlines()
        logging.debug(f"'{script_file_path}': Read with {len(lines)} lines.")
    return lines


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


def squash_continuation(lines:list[str], line_index:int) -> tuple[str, int]:
    """
    Collects any Papyrus line continuations by squashing them into a single line.
    Example:
        Papyrus line continuations are indicated by a trailing backslash `\\` and newline.
    Returns:
        If the line is a continuation, returns a merged line and the index of the last line that was merged.
        If the line is not a continuation, returns the original line and the current index.
    """
    index:int = line_index
    line:str = lines[line_index]
    while index < len(lines) and line.rstrip().endswith("\\"):
        line = line.rstrip()
        line = line.rstrip("\\")
        index += 1 # move to the next line
        if index >= len(lines):
            raise IndexError(f"Missing next line continuation: Next index at {index} is out of bounds for {len(lines)} length.")
        # Append the next line to the current line.
        line += lines[index].strip()
    return line, index


# Parsing
#---------------------------------------------

def parse(script_file_path:str) -> Script:
    """Parses a Papyrus script file and returns a Script object."""
    reader:TextReader = TextReader(load(script_file_path))
    script:Script = Script()

    # Header Parsing Loop
    #---------------------------------------------
    inside_comment_block:MutableBool = MutableBool()
    while reader.has_next():
        line:str = reader.move_next()
        line_index:int = reader.cursor

        # Skip lines that are inside any comment blocks.
        if skip(inside_comment_block, line):
            continue

        # Normalize the line by stripping comments and whitespace.
        line = normalize.strip_comments(line)
        line = normalize.whitespace(line)

        # Check if this line matches the header pattern.
        header_match:Match[str]|None = regex.HEADER_PATTERN.match(line)
        if header_match:
            header:Header = parse_header(header_match, reader.lines, line_index)
            script.header = header
            break

    # Raise an error if no header was found.
    if not script.header:
        message:str = (
            f"File: '{script_file_path}'\n"
            "The `ScriptName` element was not found in the source file. "
            "Check for missing or malformed header in the script file. "
            "Ensure the first non-comment line contains a valid `ScriptName` declaration."
        )
        raise ValueError(message)


    # Main Parsing Loop
    #---------------------------------------------
    logging.debug(f"'{script.header.name.file_path()}'@{reader.cursor}: Parsing...")
    while reader.has_next():
        line:str = reader.move_next()
        line_index:int = reader.cursor

        # Squash any line continuations.
        # TODO: Line squashing may affect documentation parsing because it searches above and below the definition line.
        (line_squashed, line_squashed_end) = squash_continuation(reader.lines, reader.cursor)

        # Update the line and cursor position after squashing.
        line = line_squashed
        reader.cursor = line_squashed_end

        # Types
        #---------------------------------------------

        # Group Block
        group_match:Match[str]|None = regex.GROUP_PATTERN.match(line)
        if group_match:
            group:PropertyGroup = parse_property_group(group_match, reader.lines, reader.cursor)
            script.members[group.name] = group
            continue

        # State Block
        state_match:Match[str]|None = regex.STATE_PATTERN.match(line)
        if state_match:
            state:State = parse_state(state_match, reader.lines, reader.cursor)
            script.members[state.name] = state
            continue

        # Property Block
        property_match:Match[str]|None = regex.PROPERTY_PATTERN.match(line)
        if property_match:
            property:Property = parse_property(property_match, reader.lines, reader.cursor)
            script.members[property.name] = property
            continue

        # Function Block
        function_match:Match[str]|None = regex.FUNCTION_PATTERN.match(line)
        if function_match:
            function:Function = parse_function(function_match, reader.lines, reader.cursor)
            script.members[function.name] = function
            continue

        # Event Block
        event_match:Match[str]|None = regex.EVENT_PATTERN.match(line)
        if event_match:
            event:Event = parse_event(event_match, reader.lines, reader.cursor)
            script.members[event.name] = event
            continue

        # Struct Block
        struct_match:Match[str]|None = regex.STRUCT_PATTERN.match(line)
        if struct_match:
            structure:Structure = parse_structure(struct_match, reader.lines, reader.cursor)
            script.members[structure.name] = structure
            continue

        # CustomEvent
        event_custom_match:Match[str]|None = regex.CUSTOM_EVENT_PATTERN.match(line)
        if event_custom_match:
            logging.debug(f"'{script_file_path}'@{reader.cursor}: Skipped custom event: '{line.strip()}'")
            continue

        # Guard
        guard_match:Match[str]|None = regex.GUARD_PATTERN.match(line)
        if guard_match:
            logging.debug(f"'{script_file_path}'@{reader.cursor}: Skipped guard: '{line.strip()}'")
            continue

        # Variable
        variable_match:Match[str]|None = regex.VARIABLE_PATTERN.match(line)
        if variable_match:
            # TODO: This does not match lines correctly, it is disabled for now.
            if False:
                variable:Variable = parse_variable(variable_match, reader.lines, reader.cursor)
                script.members[variable.name] = variable
            else:
                logging.debug(f"'{script_file_path}'@{reader.cursor}: Skipped variable: '{line.strip()}'")
                continue

    return script
