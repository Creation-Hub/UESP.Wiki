import re
from re import Match
from app import papyrus
from app.papyrus.code import Header, Member, Script, ScriptName


# Documentation
#---------------------------------------------

# TODO: This function is too greedy with check-1. It should stop at the first non-comment line.
# TODO: Ensire the function returns the result of both the comment and the block docstring.
def parse_script_documentation(lines:list[str], line_index:int):
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

# UNUSED: This function is not used in the current codebase.
def extract_header_extends(header_line:str) -> str:
    """
    Extracts the Extends value from the script header.
    Returns:
      - The script name after 'Extends' if present (may be namespaced).
      - 'Nothing' if this is ScriptObject itself.
      - 'ScriptObject' if no Extends is present.
    """
    clean_line = papyrus.normalize.strip_comments(header_line)
    tokens = clean_line.strip().split()
    script_name = None
    extends_name = None

    for i, token in enumerate(tokens):
        if token.lower() == "scriptname" and i + 1 < len(tokens):
            script_name = tokens[i + 1]
        if token.lower() == "extends" and i + 1 < len(tokens):
            extends_name = tokens[i + 1]

    if extends_name:
        return extends_name
    elif script_name and script_name.endswith("ScriptObject"):
        return "Nothing"
    else:
        return "ScriptObject"


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

        header_match = re.match(
            r'^\s*scriptname\s+(?P<name>[^\s]+)'     # Required name
            r'(?:\s+extends\s+(?P<extends>[^\s]+))?' # Optional extends
            r'(?P<flags>(?:\s+\w+)*)\s*$',           # Optional flags
            line,
            re.IGNORECASE
        )
        if header_match:
            header:Header = Header()
            header.index = line_index
            header.definition = papyrus.normalize.script_definition(line)
            header.documentation = parse_script_documentation(lines, line_index)
            #----------
            header.name = ScriptName(header_match.group("name"))
            header.extends = ScriptName(header_match.group("extends"))
            #----------
            # TODO:
            # header.flags = header_match.group("flags").strip().split() if header_match.group("flags") else []
            #----------
            flags:str = header_match.group("flags")
            flags = papyrus.normalize.strip_comments(flags)
            header.flags = papyrus.normalize.script_flags(flags.split())
            #----------
            return header
    raise ValueError("ScriptName not found")


# Members
#---------------------------------------------

def parse_script_member_parameters(parameters_match:Match[str]) -> list[str]:
    """Parse a Papyrus parameter string into a list of normalized parameter strings."""
    parameters = []
    if parameters_match:
        for element in parameters_match.split(","):
            element = element.strip()
            if not element:
                continue
            param_match = re.match(r'^(\w+(?:\[\])?)\s+(\w+)(\s*=\s*.+)?$', element)
            if param_match:
                ptype = param_match.group(1)
                pname = param_match.group(2)
                default = param_match.group(3) or ""
                default_norm = papyrus.normalize.default_value(default)
                param_str_piece = f"{papyrus.normalize.script_type(ptype)} {pname}{(' ' + default_norm) if default_norm else ''}".strip()
                parameters.append(param_str_piece)
            else:
                parameters.append(element)
    return parameters


def parse_script_member_property(property_match:Match[str], lines:list[str], line_index:int, seen_properties:list[str]) -> Member | None:
    key:str = papyrus.normalize.member_name(property_match.group("name"))
    #----------
    if key in seen_properties: return None
    else: seen_properties.add(key)
    #----------
    member:Member = Member()
    member.name = key
    member.index = line_index
    member.definition = lines[line_index]
    member.documentation = parse_script_documentation(lines, line_index)
    member.state = ""
    member.kind = "Property"
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


def parse_script_member_function(function_match:Match[str], lines:list[str], line_index:int, property_names:list[str]) -> Member | None:
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
    member.documentation = parse_script_documentation(lines, line_index)
    member.state = ""
    member.kind = "Function"
    #----------
    member.type = function_match.group("rtype")
    #----------
    flags:str = function_match.group("flags")
    flags = papyrus.normalize.strip_comments(flags)
    member.flags = papyrus.normalize.script_flags(flags.split())
    #----------
    parameters:str = papyrus.normalize.strip_comments(function_match.group("params"))
    member.parameters = parse_script_member_parameters(parameters)
    #----------
    return member


def parse_script_member_event(event_match:Match[str], lines:list[str], line_index:int) -> Member | None:
    key:str = papyrus.normalize.member_name(event_match.group("name"))
    member:Member = Member()
    member.name = key
    member.index = line_index
    member.definition = lines[line_index]
    member.documentation = parse_script_documentation(lines, line_index)
    member.state = ""
    member.kind = "Event"
    #----------
    flags:str = event_match.group("flags")
    flags = papyrus.normalize.strip_comments(flags)
    member.flags = papyrus.normalize.script_flags(flags.split())
    #----------
    parameters:str = papyrus.normalize.strip_comments(event_match.group("params"))
    member.parameters = parse_script_member_parameters(parameters)
    #----------
    return member


def parse_script_member_struct(struct_match:Match[str], lines:list[str], line_index:int) -> Member | None:
    key:str = papyrus.normalize.member_name(struct_match.group("name"))
    member:Member = Member()
    member.name = key
    member.index = line_index
    member.definition = lines[line_index]
    member.documentation = parse_script_documentation(lines, line_index)
    member.state = ""
    member.kind = "Struct"
    return member


# Parse
#---------------------------------------------

def parse(script_file_path:str) -> Script:
    with open(script_file_path, encoding="utf-8") as file:
        lines:list[str] = file.readlines()

    script:Script = Script()
    script.source_file = script_file_path
    script.header = parse_header(lines)

    # Initialize loop variables
    seen_properties = set()
    property_names = set()

    # Regular expressions for matching members
    FUNC_PATTERN = re.compile(r'^\s*(?P<rtype>\w+(?:\[\])?)?\s*function\s+(?P<name>\w+)\s*\((?P<params>[^\)]*)\)\s*(?P<flags>.*)$', re.IGNORECASE)
    EVENT_PATTERN = re.compile(r'^\s*event\s+(?P<name>\w+)\s*\((?P<params>[^\)]*)\)\s*(?P<flags>.*)$', re.IGNORECASE)
    PROPERTY_PATTERN = re.compile(r'^\s*(?P<type>\w+(?:\[\])?)\s+property\s+(?P<name>\w+)\s*(?P<flags>.*)$', re.IGNORECASE)
    STRUCT_PATTERN = re.compile(r'^\s*struct\s+(?P<name>\w+)', re.IGNORECASE)
    ENDPROPERTY_PATTERN = re.compile(r'^\s*endproperty\b', re.IGNORECASE)

    # First pass: collect all property names
    for line_index, line in enumerate(lines[script.header.index+1:], start=script.header.index+1):
        property_match = PROPERTY_PATTERN.match(line)
        if property_match:
            pname = papyrus.normalize.member_name(property_match.group("name"))
            property_names.add(pname)

    # Second pass: collect members, skipping property accessors and property block contents
    inside_property_block = False
    for line_index, line in enumerate(lines[script.header.index+1:], start=script.header.index+1):

        # Property: Detect start of a property block
        property_match = PROPERTY_PATTERN.match(line)
        if property_match:
            member = parse_script_member_property(property_match, lines, line_index, seen_properties)
            if member:
                member.kind = papyrus.normalize.symbol(member.kind)
                script.members.append(member)
            # Check if this is a block property (not auto)
            if not line.strip().lower().endswith("auto") and not line.strip().lower().endswith("auto const") and not line.strip().lower().endswith("auto readonly"):
                inside_property_block = True
            continue

        # Property: Detect end of a property block
        if inside_property_block:
            if ENDPROPERTY_PATTERN.match(line):
                inside_property_block = False
            continue  # Skip everything inside property blocks

        # Function
        function_match = FUNC_PATTERN.match(line)
        if function_match:
            member = parse_script_member_function(function_match, lines, line_index, property_names)
            if member:
                member.kind = papyrus.normalize.symbol(member.kind)
                script.members.append(member)
            continue

        # Event
        event_match = EVENT_PATTERN.match(line)
        if event_match:
            member = parse_script_member_event(event_match, lines, line_index)
            if member:
                member.kind = papyrus.normalize.symbol(member.kind)
                script.members.append(member)
            continue

        # Struct
        struct_match = STRUCT_PATTERN.match(line)
        if struct_match:
            member = parse_script_member_struct(struct_match, lines, line_index)
            if member:
                member.kind = papyrus.normalize.symbol(member.kind)
                script.members.append(member)
            continue

    return script
