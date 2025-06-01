import re
import papyrus.normalize

# Documentation
#---------------------------------------------

# TODO: This function is too greedy with check-1. It should stop at the first non-comment line.
# TODO: Ensire the function returns the result of both the comment and the block docstring.
def extract_script_documentation(lines, line_index):
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

def parse_header(lines):
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

        header_match = re.match(r'^\s*scriptname\s+([^\s]+.*)$', line, re.IGNORECASE)
        if header_match:
            script_header = papyrus.normalize.script_header(line)
            script_name = header_match.group(1).split()[0]
            script_namespace = script_name.split(":")
            script_extends = extract_header_extends(script_header)
            script_doc = extract_script_documentation(lines, line_index)
            return {
                "line_index": line_index,
                "header": script_header,
                "name": script_name,
                "namespace": None,
                "extends": script_extends,
                "doc": script_doc
            }
    raise ValueError("ScriptName not found")


def extract_header_extends(header_line):
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


# Members
#---------------------------------------------

def parse_script_member_parameters(parameter_match):
    """Parse a Papyrus parameter string into a list of normalized parameter strings."""
    param_list = []
    if parameter_match:
        for p in parameter_match.split(","):
            p = p.strip()
            if not p:
                continue
            param_match = re.match(r'^(\w+(?:\[\])?)\s+(\w+)(\s*=\s*.+)?$', p)
            if param_match:
                ptype = param_match.group(1)
                pname = param_match.group(2)
                default = param_match.group(3) or ""
                norm_default = papyrus.normalize.default_value(default)
                param_str_piece = f"{papyrus.normalize.script_type(ptype)} {pname}{(' ' + norm_default) if norm_default else ''}".strip()
                param_list.append(param_str_piece)
            else:
                param_list.append(p)
    return param_list


def parse_script_member_property(property_match, lines, idx, seen_properties):
    member_type = papyrus.normalize.script_type(property_match.group("type"))
    member_name = papyrus.normalize.member_name(property_match.group("name"))
    flags = property_match.group("flags")
    member_flags = papyrus.normalize.strip_comments(flags)
    member_flags = papyrus.normalize.script_flags(member_flags.strip().split())
    member_doc = extract_script_documentation(lines, idx)
    # If this property has already been seen, skip it.
    if member_name not in seen_properties:
        seen_properties.add(member_name)
        return {
            "kind": "Property",
            "type": member_type,
            "name": member_name,
            "flags": member_flags,
            "doc": member_doc
        }
    return None


def parse_script_member_function(function_match, lines, idx, property_names):
    member_name = papyrus.normalize.member_name(function_match.group("name"))
    # Skip property accessor functions (Get<Property>, Set<Property>)
    # This is a workaround to avoid parsing them as functions.
    # TODO: This is not a correct naming for property accessors, they should not include the property name.
    #   Property accessors are just named "Get" or "Set" without the property name.
    for property_name in property_names:
        if member_name == f"Get{property_name}" or member_name == f"Set{property_name}":
            return None
    # Get the member details.
    member_returns = function_match.group("rtype")
    member_params = papyrus.normalize.strip_comments(function_match.group("params").strip())
    member_param_list = parse_script_member_parameters(member_params)
    flags = function_match.group("flags")
    member_flags = papyrus.normalize.strip_comments(flags)
    member_flags = papyrus.normalize.script_flags(member_flags.strip().split())
    member_doc = extract_script_documentation(lines, idx)
    return {
        "kind": "Function",
        "name": member_name,
        "rtype": member_returns,
        "params": member_param_list,
        "flags": member_flags,
        "doc": member_doc
    }


def parse_script_member_event(event_match, lines, idx):
    member_name = papyrus.normalize.member_name(event_match.group("name"))
    params = event_match.group("params").strip()
    member_params = parse_script_member_parameters(params)
    flags = event_match.group("flags")
    member_flags = papyrus.normalize.strip_comments(flags)
    member_flags = papyrus.normalize.script_flags(member_flags.strip().split())
    member_doc = extract_script_documentation(lines, idx)
    return {
        "kind": "Event",
        "name": member_name,
        "params": member_params,
        "flags": member_flags,
        "doc": member_doc
    }


def parse_script_member_struct(struct_match, lines, idx):
    member_name = papyrus.normalize.member_name(struct_match.group("name"))
    member_doc = extract_script_documentation(lines, idx)
    return {
        "kind": "Struct",
        "name": member_name,
        "doc": member_doc
    }


# Parse
#---------------------------------------------

def parse(script_path):
    with open(script_path, encoding="utf-8") as file:
        lines = file.readlines()

    # Parse the script header
    header = parse_header(lines)
    header_idx = header["line_index"]

    # Initialize member variables
    members = []
    seen_properties = set()
    property_names = set()

    # Regular expressions for matching members
    FUNC_PATTERN = re.compile(r'^\s*(?P<rtype>\w+(?:\[\])?)?\s*function\s+(?P<name>\w+)\s*\((?P<params>[^\)]*)\)\s*(?P<flags>.*)$', re.IGNORECASE)
    EVENT_PATTERN = re.compile(r'^\s*event\s+(?P<name>\w+)\s*\((?P<params>[^\)]*)\)\s*(?P<flags>.*)$', re.IGNORECASE)
    PROPERTY_PATTERN = re.compile(r'^\s*(?P<type>\w+(?:\[\])?)\s+property\s+(?P<name>\w+)\s*(?P<flags>.*)$', re.IGNORECASE)
    STRUCT_PATTERN = re.compile(r'^\s*struct\s+(?P<name>\w+)', re.IGNORECASE)
    ENDPROPERTY_PATTERN = re.compile(r'^\s*endproperty\b', re.IGNORECASE)

    # First pass: collect all property names
    for line_index, line in enumerate(lines[header_idx+1:], start=header_idx+1):
        property_match = PROPERTY_PATTERN.match(line)
        if property_match:
            pname = papyrus.normalize.member_name(property_match.group("name"))
            property_names.add(pname)

    # Second pass: collect members, skipping property accessors and property block contents
    inside_property_block = False
    for line_index, line in enumerate(lines[header_idx+1:], start=header_idx+1):

        # Property: Detect start of a property block
        property_match = PROPERTY_PATTERN.match(line)
        if property_match:
            member = parse_script_member_property(property_match, lines, line_index, seen_properties)
            if member:
                member["kind"] = papyrus.normalize.script_keyword(member["kind"])
                members.append(member)
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
                member["kind"] = papyrus.normalize.script_keyword(member["kind"])
                members.append(member)
            continue

        # Event
        event_match = EVENT_PATTERN.match(line)
        if event_match:
            member = parse_script_member_event(event_match, lines, line_index)
            if member:
                member["kind"] = papyrus.normalize.script_keyword(member["kind"])
                members.append(member)
            continue

        # Struct
        struct_match = STRUCT_PATTERN.match(line)
        if struct_match:
            member = parse_script_member_struct(struct_match, lines, line_index)
            if member:
                member["kind"] = papyrus.normalize.script_keyword(member["kind"])
                members.append(member)
            continue

    return header, members
