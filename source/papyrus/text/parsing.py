"""
Provides functionality to parse Papyrus script text into structured objects.
The main loop acts as a "coarse parser" that advances through the file, while the block parsers handle their internal content independently.
"""
import logging
from re import Match
from ..code import Event
from ..code import Function
from ..code import Header
from ..code import Property
from ..code import PropertyGroup
from ..code import Script
from ..code import ScriptName
from ..code import State
from ..code import Structure
from ..code import Variable
from .normalize import Normalize
from .regex import RegEx
from .reader import LineReader


# Messages
#---------------------------------------------

class ParseMessage:

    @staticmethod
    def element_success(name:str, start_index:int, end_index:int) -> str:
        """Format a block parsing debug message."""
        line_count = (end_index - start_index) + 1
        return f"'{name}' - @index({start_index}-{end_index}, count={line_count})"


    @staticmethod
    def block_warning(name:str, start_index:int) -> str:
        """Format a block validation warning message."""
        return f"'{name}' - @index({start_index}) - Has an unincremented block index."


# Documentation
#---------------------------------------------

class ParseDocumentation:

    @staticmethod
    def collect_braced_docstring(reader:LineReader) -> str:
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


    @staticmethod
    def collect_contiguous_comments(reader:LineReader) -> str:
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
    @staticmethod
    def parse_documentation(reader:LineReader) -> str:
        """
        Collects Papyrus documentation for a code element at line_index.
        - Collects braced docstring below (with blank lines allowed, but nothing else in between).
        - Collects contiguous line/block comments above (no blank lines allowed).
        - If both exist, combines them (docstring first, then comments).
        """
        docstring:str = ParseDocumentation.collect_braced_docstring(reader)
        comments:str = ParseDocumentation.collect_contiguous_comments(reader)
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

class Parse:
    """
    Parsing functions that convert matched regex groups into structured objects.

    Takes regex matches and LineReader context to build typed representations of Papyrus code elements.
    """

    @staticmethod
    def flags(text:str) -> list[str]:
        """Parse a Papyrus flags string into a list of normalized flag strings."""
        flags:list[str] = []
        if text:
            text = Normalize.strip_comments(text)
            tokens:list[str] = text.split()
            for token in tokens:
                token = token.strip()
                if not token: continue
                else: flags.append(Normalize.flag(token))
        return flags


    @staticmethod
    def initializer(text:str) -> str:
        if text:
            return Normalize.symbol(text)
        return ""


    # Header
    #---------------------------------------------

    @staticmethod
    def header(reader:LineReader, header_match:Match[str]) -> Header:
        header:Header = Header()
        header.index = reader.cursor
        header.index_end = reader.cursor
        header.definition = Normalize.definition(reader.line())
        header.documentation = ParseDocumentation.parse_documentation(reader)
        header.name = ScriptName(header_match.group("name"))
        header.extends = ScriptName(header_match.group("extends"))
        header.flags = Parse.flags(header_match.group("flags"))
        logging.debug(ParseMessage.element_success(header.name.key, header.index, header.index_end))
        return header


    # Members
    #---------------------------------------------

    @staticmethod
    def variable(reader:LineReader, variable_match:Match[str]) -> Variable:
        variable:Variable = Variable()
        variable.name = Normalize.member_name_upper(variable_match.group("name"))
        variable.index = reader.cursor
        variable.index_end = reader.cursor
        variable.definition = Normalize.definition(reader.line())
        variable.documentation = ParseDocumentation.parse_documentation(reader)
        variable.type = Normalize.script_type(variable_match.group("type"))
        variable.flags = Parse.flags(variable_match.group("flags"))
        variable.value = Parse.initializer(variable_match.group("value"))
        logging.debug(ParseMessage.element_success(variable.name, variable.index, variable.index_end))
        return variable


    @staticmethod
    def parameters(parameters_line:str) -> list[Variable]:
        """Parse a Papyrus parameter string into a list of normalized parameter strings."""
        parameters:list[Variable] = []
        if parameters_line:
            parameters_line = Normalize.strip_comments(parameters_line)
            tokens:list[str] = parameters_line.split(",")
            for token in tokens:
                token = token.strip()
                if not token:
                    continue
                parameter_match = RegEx.PARAMETERS_PATTERN.match(token)
                if parameter_match:
                    parameter:Variable = Variable()
                    parameter.type = Normalize.script_type(parameter_match.group("type"))
                    parameter.name = Normalize.member_name(parameter_match.group("name"))

                    # TODO: Handle non-primitive default values.
                    parameter.value = Normalize.primitive_value(parameter_match.group("value"))
                    parameters.append(parameter)
                else:
                    logging.warning(f"Invalid parameter format: '{token}'")

        # Return the list of parsed parameters
        return parameters


    # Block
    @staticmethod
    def property(reader:LineReader, property_match:Match[str]) -> Property:
        property:Property = Property()
        property.index = reader.cursor
        property.index_end = reader.cursor
        property.definition = Normalize.definition(reader.line())
        property.documentation = ParseDocumentation.parse_documentation(reader)
        property.name = Normalize.member_name_upper(property_match.group("name"))
        property.flags = Parse.flags(property_match.group("flags"))
        property.type = Normalize.script_type(property_match.group("type"))
        property.value = Parse.initializer(property_match.group("value"))

        if "Auto" in property.flags or "AutoReadOnly" in property.flags:
            logging.debug(ParseMessage.element_success(property.name, property.index, property.index_end))
            return property

        while reader.has_next():
            line:str = reader.move()

            # Terminate this loop if we reach the block end.
            if RegEx.PROPERTY_END_PATTERN.match(line):
                property.index_end = reader.cursor
                break

            # Function Block
            function_match:Match[str]|None = RegEx.FUNCTION_PATTERN.match(line)
            if function_match:
                function:Function = Parse.function(reader, function_match)
                if function.name == "Get":
                    property.getter = function
                elif function.name == "Set":
                    property.setter = function
                else:
                    logging.warning(f"Property '{property.name}' has a function '{function.name}' that is neither a getter nor a setter.")
                continue

        # Warn on unincremented block indexes.
        if property.index == property.index_end:
            logging.warning(ParseMessage.block_warning(property.name, property.index))

        logging.debug(ParseMessage.element_success(property.name, property.index, property.index_end))
        return property


    # Block
    @staticmethod
    def structure(reader:LineReader, struct_match:Match[str]) -> Structure:
        structure:Structure = Structure()
        structure.index = reader.cursor
        structure.index_end = reader.cursor
        structure.definition = Normalize.definition(reader.line())
        structure.documentation = ParseDocumentation.parse_documentation(reader)
        structure.name = Normalize.member_name_upper(struct_match.group("name"))

        while reader.has_next():
            line:str = reader.move()

            # Terminate this loop if we reach the block end.
            if RegEx.STRUCT_END_PATTERN.match(line):
                structure.index_end = reader.cursor
                break

            # Match any variable definitions inside this structure.
            variable_match = RegEx.VARIABLE_PATTERN.match(line)
            if variable_match:
                variable:Variable = Parse.variable(reader, variable_match)
                structure.variables[variable.name] = variable

        # Warn on unincremented block indexes.
        if structure.index == structure.index_end:
            logging.warning(ParseMessage.block_warning(structure.name, structure.index))

        logging.debug(ParseMessage.element_success(structure.name, structure.index, structure.index_end))
        return structure


    # Block
    @staticmethod
    def event(reader:LineReader, event_match:Match[str]) -> Event:
        event:Event = Event()

        name:str = event_match.group("name")
        remote:str = event_match.group("remote")
        if remote:
            name = Normalize.member_name_upper(name) + Normalize.member_name_upper(remote)
        else:
            name = Normalize.member_name_upper(name)

        event.name = name
        event.index = reader.cursor
        event.index_end = reader.cursor
        event.definition = Normalize.definition(reader.line())
        event.documentation = ParseDocumentation.parse_documentation(reader)
        event.flags = Parse.flags(event_match.group("flags"))
        event.parameters = Parse.parameters(event_match.group("params"))

        if "Native" in event.flags:
            return event

        while reader.has_next():
            line:str = reader.move()

            # Terminate this loop if we reach the block end.
            if RegEx.EVENT_END_PATTERN.match(line):
                event.index_end = reader.cursor
                break

        # Warn on unincremented block indexes.
        if event.index == event.index_end:
            logging.warning(ParseMessage.block_warning(event.name, event.index))

        logging.debug(ParseMessage.element_success(event.name, event.index, event.index_end))
        return event


    # Block
    @staticmethod
    def function(reader:LineReader, function_match:Match[str]) -> Function:
        function:Function = Function()
        function.name = Normalize.member_name_upper(function_match.group("name"))
        function.index = reader.cursor
        function.index_end = reader.cursor
        function.definition = Normalize.definition(reader.line())
        function.documentation = ParseDocumentation.parse_documentation(reader)
        function.type = Normalize.script_type(function_match.group("type"))
        function.flags = Parse.flags(function_match.group("flags"))
        function.parameters = Parse.parameters(function_match.group("params"))

        if "Native" in function.flags:
            logging.debug(ParseMessage.element_success(function.name, function.index, function.index_end))
            return function

        while reader.has_next():
            line:str = reader.move()

            # Terminate this loop if we reach the block end.
            if RegEx.FUNCTION_END_PATTERN.match(line):
                function.index_end = reader.cursor
                break

        # Warn on unincremented block indexes.
        if function.index == function.index_end:
            logging.warning(ParseMessage.block_warning(function.name, function.index))

        logging.debug(ParseMessage.element_success(function.name, function.index, function.index_end))
        return function


    # Blocks
    #---------------------------------------------

    @staticmethod
    def property_group(reader:LineReader, group_match:Match[str]) -> PropertyGroup:
        group:PropertyGroup = PropertyGroup()
        group.index = reader.cursor
        group.index_end = reader.cursor
        group.definition = Normalize.definition(reader.line())
        group.documentation = ParseDocumentation.parse_documentation(reader)
        group.name = group_match.group("name")
        group.flags = Parse.flags(group_match.group("flags"))

        while reader.has_next():
            line:str = reader.move()

            # Terminate this loop if we reach the block end.
            if RegEx.GROUP_END_PATTERN.match(line):
                group.index_end = reader.cursor
                break

            # Parse members inside the group
            property_match:Match[str]|None = RegEx.PROPERTY_PATTERN.match(line)
            if property_match:
                property:Property = Parse.property(reader, property_match)
                if property:
                    group.properties[property.name] = property

        # Warn on unincremented block indexes.
        if group.index == group.index_end:
            logging.warning(ParseMessage.block_warning(group.name, group.index))

        logging.debug(ParseMessage.element_success(group.name, group.index, group.index_end))
        return group


    @staticmethod
    def state(reader:LineReader, state_match:Match[str]) -> State:
        state:State = State()
        state.index = reader.cursor
        state.index_end = reader.cursor
        state.definition = Normalize.definition(reader.line())
        state.documentation = ParseDocumentation.parse_documentation(reader)
        state.name = Normalize.member_name_upper(state_match.group("name"))
        state.flags = Parse.flags(state_match.group("flags"))

        while reader.has_next():
            line:str = reader.move()

            # Terminate this loop if we reach the block end.
            if RegEx.STATE_END_PATTERN.match(line):
                state.index_end = reader.cursor
                break

            # Parse any event methods inside this state.
            event_match:Match[str]|None = RegEx.EVENT_PATTERN.match(line)
            if event_match:
                event:Event = Parse.event(reader, event_match)
                state.methods[event.name] = event
                continue

            # Parse any function methods inside this state.
            function_match:Match[str]|None = RegEx.FUNCTION_PATTERN.match(line)
            if function_match:
                function:Function = Parse.function(reader, function_match)
                state.methods[function.name] = function
                continue

        # Warn on unincremented block indexes.
        if state.index == state.index_end:
            logging.warning(ParseMessage.block_warning(state.name, state.index))

        logging.debug(ParseMessage.element_success(state.name, state.index, state.index_end))
        return state


    # Parsing
    #---------------------------------------------

    @staticmethod
    def squash_continuation(reader:LineReader) -> str:
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
        reader.cursor = index
        return line


class FileReader:
    def __init__(self, path:str) -> None:
        super().__init__()
        self._path:str = path


    @property
    def path(self) -> str:
        return self._path


    def load(self) -> list[str]:
        with open(self.path, encoding="utf-8") as file:
            lines:list[str] = file.readlines()
            file_size:str = str(file.tell()) if hasattr(file, 'tell') else 'unknown'
        logging.debug(f"Loaded '{self.path}': {len(lines)} lines, {file_size} bytes")
        return lines


    def read(self) -> Script:
        """Parses a Papyrus script file and returns a Script object."""
        reader:LineReader = LineReader(self.load())
        script:Script = Script()
        while reader.has_next():
            line:str = reader.move()

            # Squash any line continuations.
            # TODO: Line squashing may affect documentation parsing.
            #  The documentation parser searches above and below the definition line.
            line = Parse.squash_continuation(reader)

            # Normalize the line by stripping comments and extra whitespace.
            line = Normalize.strip_comments(line)
            line = Normalize.whitespace(line)

            # Header
            #---------------------------------------------

            if not script.header.name.key:
                # Check if this line matches the header pattern.
                header_match:Match[str]|None = RegEx.HEADER_PATTERN.match(line)
                if header_match:
                    header:Header = Parse.header(reader, header_match)
                    script.header = header
                continue # Skip any lines before the header.

            # Types
            #---------------------------------------------

            # Group Block
            group_match:Match[str]|None = RegEx.GROUP_PATTERN.match(line)
            if group_match:
                group:PropertyGroup = Parse.property_group(reader, group_match)
                script.members[group.name] = group
                for property in group.properties.values():
                    script.members[property.name] = property
                continue

            # State Block
            state_match:Match[str]|None = RegEx.STATE_PATTERN.match(line)
            if state_match:
                state:State = Parse.state(reader, state_match)
                script.members[state.name] = state
                for method in state.methods.values():
                    script.members[method.name] = method
                continue

            # Property Block
            property_match:Match[str]|None = RegEx.PROPERTY_PATTERN.match(line)
            if property_match:
                property:Property = Parse.property(reader, property_match)
                script.members[property.name] = property
                continue

            # Function Block
            function_match:Match[str]|None = RegEx.FUNCTION_PATTERN.match(line)
            if function_match:
                function:Function = Parse.function(reader, function_match)
                script.members[function.name] = function
                continue

            # Event Block
            event_match:Match[str]|None = RegEx.EVENT_PATTERN.match(line)
            if event_match:
                event:Event = Parse.event(reader, event_match)
                script.members[event.name] = event
                continue

            # Struct Block
            struct_match:Match[str]|None = RegEx.STRUCT_PATTERN.match(line)
            if struct_match:
                structure:Structure = Parse.structure(reader, struct_match)
                script.members[structure.name] = structure
                continue

            # CustomEvent
            event_custom_match:Match[str]|None = RegEx.CUSTOM_EVENT_PATTERN.match(line)
            if event_custom_match:
                logging.debug(f"'{self.path}'@{reader.cursor}: Skipped custom event: '{line.strip()}'")
                continue

            # Guard
            guard_match:Match[str]|None = RegEx.GUARD_PATTERN.match(line)
            if guard_match:
                logging.debug(f"'{self.path}'@{reader.cursor}: Skipped guard: '{line.strip()}'")
                continue

            # Variable
            variable_match:Match[str]|None = RegEx.VARIABLE_PATTERN.match(line)
            if variable_match:
                # TODO: Fix variable parsing comment issue
                # TODO: Fix variable parsing context issue
                # Variables inside function/event/property blocks are incorrectly parsed as class-level fields
                # when the main loop advances past block parsers. Need context-aware variable parsing that
                # distinguishes between class fields and local/parameter variables based on current scope.
                # Consider implementing scope tracking or updating block parsers to handle their own variables.
                if False:
                    variable:Variable = Parse.variable(reader, variable_match)
                    script.members[variable.name] = variable
                else:
                    logging.debug(f"'{self.path}'@{reader.cursor}: Skipped variable: '{line.strip()}'")
                    continue


        # Raise an error if no header was found.
        if not script.header:
            raise ValueError(
                f"File: '{self.path}'\n" +
                "The `ScriptName` element was not found in the source file. " +
                "Check for missing or malformed header in the script file. " +
                "Ensure the first non-comment line contains a valid `ScriptName` declaration."
            )

        if not script.header.name.key:
            raise ValueError(
                f"File: '{self.path}'\n" +
                "The `ScriptName` element was found but could not be parsed. " +
                "Check for missing or malformed header in the script file. " +
                "Ensure the first non-comment line contains a valid `ScriptName` declaration."
            )

        return script
