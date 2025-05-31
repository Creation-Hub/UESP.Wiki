import re
import papyrus.normalize

# Parser
#---------------------------------------------

def extract_script_documentation(lines, element_idx):
    """
    Extracts the documentation comment for a script or member.
    Supports:
    - Consecutive comment lines (;) immediately above the element (with blank lines allowed)
    - Or, a block docstring in curly braces { ... } immediately below the element (with blank lines allowed)
    Returns the doc string, or a default if none is found.
    """
    # 1. Check for doc comments above (Papyrus ;)
    desc_lines = []
    idx = element_idx - 1
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
    idx = element_idx + 1
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


def extract_script_extends(header_line):
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
    typ = papyrus.normalize.script_type(property_match.group("type"))
    name = papyrus.normalize.member_name(property_match.group("name"))
    # Strip comments from flags before splitting
    flags_raw = property_match.group("flags")
    flags_norm = papyrus.normalize.strip_comments(flags_raw)
    flags_norm = papyrus.normalize.script_flags(flags_norm.strip().split())
    doc = extract_script_documentation(lines, idx)
    if name not in seen_properties:
        seen_properties.add(name)
        return {
            "kind": "property",
            "type": typ,
            "name": name,
            "flags": flags_norm,
            "doc": doc
        }
    return None


def parse_script_member_function(function_match, lines, idx, property_names):
    fname = papyrus.normalize.member_name(function_match.group("name"))
    # Skip property accessor functions (Get<Property>, Set<Property>)
    for pname in property_names:
        if fname == f"Get{pname}" or fname == f"Set{pname}":
            return None
    rtype = function_match.group("rtype")
    params = papyrus.normalize.strip_comments(function_match.group("params").strip())
    # Strip comments from flags before splitting
    flags_raw = function_match.group("flags")
    norm_flags = papyrus.normalize.strip_comments(flags_raw)
    norm_flags = papyrus.normalize.script_flags(norm_flags.strip().split())
    param_list = parse_script_member_parameters(params)
    doc = extract_script_documentation(lines, idx)
    return {
        "kind": "function",
        "name": fname,
        "rtype": rtype,
        "params": param_list,
        "flags": norm_flags,
        "doc": doc
    }


def parse_script_member_event(event_match, lines, idx):
    name = papyrus.normalize.member_name(event_match.group("name"))
    params = event_match.group("params").strip()
    # Strip comments from flags before splitting
    flags_raw = event_match.group("flags")
    norm_flags = papyrus.normalize.strip_comments(flags_raw)
    norm_flags = papyrus.normalize.script_flags(norm_flags.strip().split())
    param_list = parse_script_member_parameters(params)
    doc = extract_script_documentation(lines, idx)
    return {
        "kind": "event",
        "name": name,
        "params": param_list,
        "flags": norm_flags,
        "doc": doc
    }


def parse_script_member_struct(struct_match, lines, idx):
    name = papyrus.normalize.member_name(struct_match.group("name"))
    doc = extract_script_documentation(lines, idx)
    return {
        "kind": "struct",
        "name": name,
        "doc": doc
    }


def parse_script_header(lines):
    """
    Finds the script header line, script name, and its line index.
    Returns (script_name, header_line, header_idx) or raises ValueError if not found.
    """
    for idx, line in enumerate(lines):
        # Skip empty lines and comments
        if line.strip() == "" or line.strip().startswith(";"):
            continue
        line = papyrus.normalize.strip_comments(line)
        match = re.match(r'^\s*scriptname\s+([^\s]+.*)$', line, re.IGNORECASE)
        if match:
            header_line = line.strip()
            script_name = match.group(1).split()[0]
            return idx, script_name, header_line
    raise ValueError("ScriptName not found")


# Parse
#---------------------------------------------

def parse_script(script_path):
    with open(script_path, encoding="utf-8") as f:
        lines = f.readlines()

    header_idx, script_name, header_line = parse_script_header(lines)
    documentation = extract_script_documentation(lines, header_idx)

    members = []
    seen_properties = set()
    property_names = set()

    # Regular expressions for matching members
    FUNC_PATTERN = re.compile(r'^\s*(?P<rtype>\w+(?:\[\])?)?\s*function\s+(?P<name>\w+)\s*\((?P<params>[^\)]*)\)\s*(?P<flags>.*)$', re.IGNORECASE)
    EVENT_PATTERN = re.compile(r'^\s*event\s+(?P<name>\w+)\s*\((?P<params>[^\)]*)\)\s*(?P<flags>.*)$', re.IGNORECASE)
    PROPERTY_PATTERN = re.compile(r'^\s*(?P<type>\w+(?:\[\])?)\s+property\s+(?P<name>\w+)\s*(?P<flags>.*)$', re.IGNORECASE)
    STRUCT_PATTERN = re.compile(r'^\s*struct\s+(?P<name>\w+)', re.IGNORECASE)
    ENDPROPERTY_PATTERN = re.compile(r'^\s*endproperty\b', re.IGNORECASE)

    # First pass: collect all property names (CamelCase)
    for idx, line in enumerate(lines[header_idx+1:], start=header_idx+1):
        property_match = PROPERTY_PATTERN.match(line)
        if property_match:
            pname = papyrus.normalize.member_name(property_match.group("name"))
            property_names.add(pname)

    # Second pass: collect members, skipping property accessors and property block contents
    inside_property_block = False
    for idx, line in enumerate(lines[header_idx+1:], start=header_idx+1):

        # Property: Detect start of a property block
        property_match = PROPERTY_PATTERN.match(line)
        if property_match:
            member = parse_script_member_property(property_match, lines, idx, seen_properties)
            if member:
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
            member = parse_script_member_function(function_match, lines, idx, property_names)
            if member:
                members.append(member)
            continue

        # Event
        event_match = EVENT_PATTERN.match(line)
        if event_match:
            member = parse_script_member_event(event_match, lines, idx)
            if member:
                members.append(member)
            continue

        # Struct
        struct_match = STRUCT_PATTERN.match(line)
        if struct_match:
            member = parse_script_member_struct(struct_match, lines, idx)
            if member:
                members.append(member)
            continue

    return script_name, papyrus.normalize.script_header(header_line), documentation, members
