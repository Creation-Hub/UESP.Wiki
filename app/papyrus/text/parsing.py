"""
Provides functionality to parse Papyrus script text into structured objects.
The main loop acts as a "coarse parser" that advances through the file, while the block parsers handle their internal content independently.
"""
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
from app.papyrus.text.reader import TextReader


# Messages
#---------------------------------------------

def message_block_warning(name:str, start_index:int) -> str:
    """Format a block validation warning message."""
    return f"'{name}' at line {start_index} has an unincremented block index."


def message_block_success(name:str, start_index:int, end_index:int) -> str:
    """Format a block parsing debug message."""
    line_count = end_index - start_index
    return f"'{name}' @({start_index}-{end_index}) with {line_count} lines."


# Documentation
#---------------------------------------------

def collect_braced_docstring(reader:TextReader) -> str:
    """
    Collects a braced docstring { ... } immediately below the code element at line_index.
    Allows blank lines between the element and the docstring, but nothing else.
    Returns the docstring content or an empty string if not found.
    """
    search_index:int = reader.cursor + 1

    # Skip blank lines
    while search_index < len(reader) and reader[search_index].strip() == "":
        search_index += 1

    # Check for opening brace
    if search_index < len(reader) and reader[search_index].lstrip().startswith("{"):
        brace_line:str = reader[search_index].lstrip()
        doc_lines:list[str] = []

        # If the opening brace is on a line by itself, skip it
        if brace_line.strip() == "{":
            search_index += 1
            # Collect until closing brace
            while search_index < len(reader):
                line:str = reader[search_index]
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
                while search_index < len(reader):
                    line:str = reader[search_index]
                    closing_brace_pos:int = line.find("}")
                    if closing_brace_pos != -1:
                        doc_lines.append(line[:closing_brace_pos])
                        break
                    doc_lines.append(line.rstrip())
                    search_index += 1

        return "\n".join(doc_lines).strip()
    return ""


def collect_contiguous_comments(reader:TextReader) -> str:
    """
    Collects contiguous line/block comments immediately above the code element at line_index.
    Stops at the first blank or non-comment line.
    Returns the comments as a single string (joined by newlines), or an empty string if none found.
    """
    comment_lines:list[str] = []
    search_index:int = reader.cursor - 1
    while search_index >= 0:
        line:str = reader[search_index]
        if line.strip() == "":
            break # Blank line ends the comment block
        stripped:str = line.lstrip()
        if stripped.startswith(";") or stripped.startswith(";/"):
            comment_lines.append(stripped)
            search_index -= 1
        else:
            break # Non-comment line ends the comment block
    if comment_lines:
        # Comments are collected in reverse order, so reverse them
        comments:list[str] = [l for l in reversed(comment_lines)]
        # Optionally, strip leading ';' and whitespace for a cleaner doc
        comments = [l.lstrip(";").strip() for l in comments]
        return "\n".join(comments)
    return ""


# TODO: The line squashing logic (line continuations) in the main parsing loop breaks line comments.
def parse_documentation(reader:TextReader) -> str:
    """
    Collects Papyrus documentation for a code element at line_index.
    - Collects braced docstring below (with blank lines allowed, but nothing else in between).
    - Collects contiguous line/block comments above (no blank lines allowed).
    - If both exist, combines them (docstring first, then comments).
    """
    docstring:str = collect_braced_docstring(reader)
    comments:str = collect_contiguous_comments(reader)
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

def parse_header(reader:TextReader, header_match:Match[str]) -> Header:
    header:Header = Header()
    header.index = reader.cursor
    header.index_end = reader.cursor
    header.definition = normalize.definition(reader.line())
    header.documentation = parse_documentation(reader)
    header.name = ScriptName(header_match.group("name"))
    header.extends = ScriptName(header_match.group("extends"))
    header.flags = parse_flags(header_match.group("flags"))
    return header


# Members
#---------------------------------------------

def parse_variable(reader:TextReader, variable_match:Match[str]) -> Variable:
    variable:Variable = Variable()
    variable.name = normalize.member_name_upper(variable_match.group("name"))
    variable.index = reader.cursor
    variable.index_end = reader.cursor
    variable.definition = normalize.definition(reader.line())
    variable.documentation = parse_documentation(reader)
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
def parse_property(reader:TextReader, property_match:Match[str]) -> Property:
    property:Property = Property()
    property.index = reader.cursor
    property.index_end = reader.cursor
    property.definition = normalize.definition(reader.line())
    property.documentation = parse_documentation(reader)
    property.name = normalize.member_name_upper(property_match.group("name"))
    property.flags = parse_flags(property_match.group("flags"))
    property.type = normalize.script_type(property_match.group("type"))
    property.value = parse_initializer(property_match.group("value"))

    if "Auto" in property.flags or "AutoReadOnly" in property.flags:
        return property

    while reader.has_next():
        line:str = reader.move()

        # Terminate this loop if we reach the block end.
        if regex.PROPERTY_END_PATTERN.match(line):
            property.index_end = reader.cursor
            break

        # Function Block
        function_match:Match[str]|None = regex.FUNCTION_PATTERN.match(line)
        if function_match:
            function:Function = parse_function(reader, function_match)
            if function.name == "Get":
                property.getter = function
            elif function.name == "Set":
                property.setter = function
            else:
                logging.warning(f"Property '{property.name}' has a function '{function.name}' that is neither a getter nor a setter.")
            continue

    # Warn on unincremented block indexes.
    if property.index == property.index_end:
        logging.warning(message_block_warning(property.name, property.index))

    logging.debug(message_block_success(property.name, property.index, property.index_end))
    return property


# Block
def parse_structure(reader:TextReader, struct_match:Match[str]) -> Structure:
    structure:Structure = Structure()
    structure.index = reader.cursor
    structure.index_end = reader.cursor
    structure.definition = normalize.definition(reader.line())
    structure.documentation = parse_documentation(reader)
    structure.name = normalize.member_name_upper(struct_match.group("name"))

    while reader.has_next():
        line:str = reader.move()

        # Terminate this loop if we reach the block end.
        if regex.STRUCT_END_PATTERN.match(line):
            structure.index_end = reader.cursor
            break

        # Match any variable definitions inside this structure.
        # TODO: Disabled for now due to context issues.
        if False:
            variable_match = regex.VARIABLE_PATTERN.match(line)
            if variable_match:
                variable:Variable = parse_variable(reader, variable_match)
                structure.variables[variable.name] = variable

    # Warn on unincremented block indexes.
    if structure.index == structure.index_end:
        logging.warning(message_block_warning(structure.name, structure.index))

    logging.debug(message_block_success(structure.name, structure.index, structure.index_end))
    return structure


# Block
def parse_event(reader:TextReader, event_match:Match[str]) -> Event:
    event:Event = Event()

    name:str = ""
    g_name:str = event_match.group("name")
    g_remote:str = event_match.group("remote")
    if g_remote:
        name = g_name + g_remote
    else:
        name = g_name

    event.name = normalize.member_name_upper(name)
    event.index = reader.cursor
    event.index_end = reader.cursor
    event.definition = normalize.definition(reader.line())
    event.documentation = parse_documentation(reader)
    event.flags = parse_flags(event_match.group("flags"))
    event.parameters = parse_parameters(event_match.group("params"))

    if "Native" in event.flags:
        return event

    while reader.has_next():
        line:str = reader.move()

        # Terminate this loop if we reach the block end.
        if regex.EVENT_END_PATTERN.match(line):
            event.index_end = reader.cursor
            break

    # Warn on unincremented block indexes.
    if event.index == event.index_end:
        logging.warning(message_block_warning(event.name, event.index))

    logging.debug(message_block_success(event.name, event.index, event.index_end))
    return event


# Block
def parse_function(reader:TextReader, function_match:Match[str]) -> Function:
    function:Function = Function()
    function.name = normalize.member_name_upper(function_match.group("name"))
    function.index = reader.cursor
    function.index_end = reader.cursor
    function.definition = normalize.definition(reader.line())
    function.documentation = parse_documentation(reader)
    function.type = normalize.script_type(function_match.group("type"))
    function.flags = parse_flags(function_match.group("flags"))
    function.parameters = parse_parameters(function_match.group("params"))

    if "Native" in function.flags:
        return function

    while reader.has_next():
        line:str = reader.move()

        # Terminate this loop if we reach the block end.
        if regex.FUNCTION_END_PATTERN.match(line):
            function.index_end = reader.cursor
            break

    # Warn on unincremented block indexes.
    if function.index == function.index_end:
        logging.warning(message_block_warning(function.name, function.index))

    logging.debug(message_block_success(function.name, function.index, function.index_end))
    return function


# Blocks
#---------------------------------------------

def parse_property_group(reader:TextReader, group_match:Match[str]) -> PropertyGroup:
    group:PropertyGroup = PropertyGroup()
    group.index = reader.cursor
    group.index_end = reader.cursor
    group.definition = normalize.definition(reader.line())
    group.documentation = parse_documentation(reader)
    group.name = group_match.group("name")
    group.flags = parse_flags(group_match.group("flags"))

    while reader.has_next():
        line:str = reader.move()

        # Terminate this loop if we reach the block end.
        if regex.GROUP_END_PATTERN.match(line):
            group.index_end = reader.cursor
            break

        # Parse members inside the group
        property_match = regex.PROPERTY_PATTERN.match(line)
        if property_match:
            property:Property = parse_property(reader, property_match)
            if property:
                group.properties[property.name] = property

    # Warn on unincremented block indexes.
    if group.index == group.index_end:
        logging.warning(message_block_warning(group.name, group.index))

    logging.debug(message_block_success(group.name, group.index, group.index_end))
    return group


def parse_state(reader:TextReader, state_match:Match[str]) -> State:
    state:State = State()
    state.index = reader.cursor
    state.index_end = reader.cursor
    state.definition = normalize.definition(reader.line())
    state.documentation = parse_documentation(reader)
    state.name = normalize.member_name_upper(state_match.group("name"))
    state.flags = parse_flags(state_match.group("flags"))

    while reader.has_next():
        line:str = reader.move()

        # Terminate this loop if we reach the block end.
        if regex.STATE_END_PATTERN.match(line):
            state.index_end = reader.cursor
            break

        # Parse any event methods inside this state.
        event_match = regex.EVENT_PATTERN.match(line)
        if event_match:
            event:Event = parse_event(reader, event_match)
            state.methods[event.name] = event
            continue

        # Parse any function methods inside this state.
        function_match = regex.FUNCTION_PATTERN.match(line)
        if function_match:
            function:Function = parse_function(reader, function_match)
            state.methods[function.name] = function
            continue

    # Warn on unincremented block indexes.
    if state.index == state.index_end:
        logging.warning(message_block_warning(state.name, state.index))

    logging.debug(message_block_success(state.name, state.index, state.index_end))
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


def squash_continuation(reader:TextReader) -> tuple[str, int]:
    """
    Collects any Papyrus line continuations by squashing them into a single line.
    Example:
        Papyrus line continuations are indicated by a trailing backslash `\\` and newline.
    Returns:
        If the line is a continuation, returns a merged line and the index of the last line that was merged.
        If the line is not a continuation, returns the original line and the current index.
    """
    index:int = reader.cursor
    line:str = reader.line()
    while index < len(reader) and line.rstrip().endswith("\\"):
        line = line.rstrip()
        line = line.rstrip("\\")
        index += 1 # move to the next line
        if index >= len(reader):
            raise IndexError(f"Missing next line continuation: Next index at {index} is out of bounds for {len(reader)} length.")
        # Append the next line to the current line.
        line += reader[index].strip()
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
        line:str = reader.move()

        # Skip lines that are inside any comment blocks.
        if skip(inside_comment_block, line):
            continue

        # Normalize the line by stripping comments and whitespace.
        line = normalize.strip_comments(line)
        line = normalize.whitespace(line)

        # Check if this line matches the header pattern.
        header_match:Match[str]|None = regex.HEADER_PATTERN.match(line)
        if header_match:
            header:Header = parse_header(reader, header_match)
            script.header = header
            break

    # Raise an error if no header was found.
    if not script.header:
        raise ValueError(
            f"File: '{script_file_path}'\n"
            "The `ScriptName` element was not found in the source file. "
            "Check for missing or malformed header in the script file. "
            "Ensure the first non-comment line contains a valid `ScriptName` declaration."
        )


    # Main Parsing Loop
    #---------------------------------------------
    logging.debug(f"'{script.header.name.file_path()}'@{reader.cursor}: Parsing...")
    while reader.has_next():
        line:str = reader.move()

        # Squash any line continuations.
        # TODO: Line squashing may affect documentation parsing because it searches above and below the definition line.
        (line_squashed, line_squashed_end) = squash_continuation(reader)

        # Update the line and cursor position after squashing.
        line = line_squashed
        reader.cursor = line_squashed_end

        # Types
        #---------------------------------------------

        # Group Block
        group_match:Match[str]|None = regex.GROUP_PATTERN.match(line)
        if group_match:
            group:PropertyGroup = parse_property_group(reader, group_match)
            script.members[group.name] = group
            for property in group.properties.values():
                script.members[property.name] = property
            continue

        # State Block
        state_match:Match[str]|None = regex.STATE_PATTERN.match(line)
        if state_match:
            state:State = parse_state(reader, state_match)
            script.members[state.name] = state
            for method in state.methods.values():
                script.members[method.name] = method
            continue

        # Property Block
        property_match:Match[str]|None = regex.PROPERTY_PATTERN.match(line)
        if property_match:
            property:Property = parse_property(reader, property_match)
            script.members[property.name] = property
            continue

        # Function Block
        function_match:Match[str]|None = regex.FUNCTION_PATTERN.match(line)
        if function_match:
            function:Function = parse_function(reader, function_match)
            script.members[function.name] = function
            continue

        # Event Block
        event_match:Match[str]|None = regex.EVENT_PATTERN.match(line)
        if event_match:
            event:Event = parse_event(reader, event_match)
            script.members[event.name] = event
            continue

        # Struct Block
        struct_match:Match[str]|None = regex.STRUCT_PATTERN.match(line)
        if struct_match:
            structure:Structure = parse_structure(reader, struct_match)
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
            # TODO: Fix variable parsing context issue
            # Variables inside function/event/property blocks are incorrectly parsed as class-level fields
            # when the main loop advances past block parsers. Need context-aware variable parsing that
            # distinguishes between class fields and local/parameter variables based on current scope.
            # Consider implementing scope tracking or updating block parsers to handle their own variables.
            if False:
                variable:Variable = parse_variable(reader, variable_match)
                script.members[variable.name] = variable
            else:
                logging.debug(f"'{script_file_path}'@{reader.cursor}: Skipped variable: '{line.strip()}'")
                continue

    return script
