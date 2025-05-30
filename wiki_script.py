import os
import re
import datetime

# Settings
#---------------------------------------------

# Settings file path
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.txt")

def parse_bool(val, default=False):
    """Parse a string as a boolean value. Accepts 1/0, true/false, yes/no, on/off (case-insensitive)."""
    if isinstance(val, bool):
        return val
    if not isinstance(val, str):
        return default
    val = val.strip().lower()
    if val in ("1", "true", "yes", "on"):
        return True
    if val in ("0", "false", "no", "off"):
        return False
    return default

# Read settings from file
def read_settings(settings_path):
    script_path = None
    output_path = None
    wiki_debug = "0"  # Default to off
    if os.path.exists(settings_path):
        with open(settings_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("WIKI_DEBUG="):
                    wiki_debug = line.split("=", 1)[1].strip()
                elif line.startswith("SCRIPT_PATH="):
                    script_path = line.split("=", 1)[1].strip()
                elif line.startswith("OUTPUT_PATH="):
                    output_path = line.split("=", 1)[1].strip()
    # Use the common parse_bool function
    wiki_debug_bool = parse_bool(wiki_debug, default=False)
    return wiki_debug_bool, script_path, output_path

WIKI_DEBUG, SCRIPT_PATH, OUTPUT_PATH = read_settings(SETTINGS_FILE)


# Normalize
#---------------------------------------------

def normalize_keyword(word):
    """Normalize Papyrus keywords and flags to CamelCase."""
    mapping = {
        # Keywords
        "scriptname": "ScriptName",
        "extends": "Extends",
        "function": "Function",
        "event": "Event",
        "property": "Property",
        "struct": "Struct",
        # Flags
        "native": "Native",
        "const": "Const",
        "hidden": "Hidden",
        "conditional": "Conditional",
        "default": "Default",
        "selfonly": "SelfOnly",
        "private": "Private",
        "protected": "Protected",
        "global": "Global",
        "auto": "Auto",
        "mandatory": "Mandatory",
        "readonly": "ReadOnly",
        "debugonly": "DebugOnly",
        "betaonly": "BetaOnly"
    }
    return mapping.get(word.lower(), word)


def normalize_type(type_str):
    """Papyrus primitive types are lowercase, object types are CamelCase. Handles arrays and 'none'."""
    if not type_str:
        return ""
    t = type_str.strip()
    is_array = False
    if t.endswith("[]"):
        is_array = True
        t = t[:-2]
    primitives = {"int", "float", "bool", "string", "var", "none"}
    if t.lower() in primitives:
        base = t.lower()
    else:
        base = t[:1].upper() + t[1:]
    return f"{base}[]" if is_array else base


def normalize_member_name(name):
    """Ensure member names are CamelCase."""
    if not name:
        return ""
    return name[0].upper() + name[1:]


def normalize_header(header_line):
    """Ensure Papyrus header keywords and flags are CamelCase."""
    tokens = header_line.strip().split()
    return " ".join(normalize_keyword(token) for token in tokens)


def normalize_flags(flag_tokens):
    """Normalize member flags to CamelCase."""
    return [normalize_keyword(f) for f in flag_tokens]


def normalize_default_value(default_val):
    """Normalize primitive default values (none, true, false, numbers)."""
    if not default_val:
        return ""
    val = default_val.strip()
    if val.startswith("="):
        val = val[1:].strip()
    primitives = {"none", "true", "false"}
    if val.lower() in primitives:
        return "= " + val.lower()
    try:
        float(val)
        return "= " + val
    except ValueError:
        pass
    return "= " + val


def normalize_strip_comments(line):
    """
    Strips this line of any Papyrus comments. ex (;), (;/.../;)
    Only removes comments, not string literals.
    """
    # Remove block comments: ;/ ... /;
    line = re.sub(r';/.*?/;', '', line)
    # Remove line comments: ; ...
    line = re.split(r';', line, maxsplit=1)[0]
    return line.rstrip()


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
    clean_line = normalize_strip_comments(header_line)
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


# Parser
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
                norm_default = normalize_default_value(default)
                param_str_piece = f"{normalize_type(ptype)} {pname}{(' ' + norm_default) if norm_default else ''}".strip()
                param_list.append(param_str_piece)
            else:
                param_list.append(p)
    return param_list


def parse_script_member_property(property_match, lines, idx, seen_properties):
    typ = normalize_type(property_match.group("type"))
    name = normalize_member_name(property_match.group("name"))
    # Strip comments from flags before splitting
    flags_raw = property_match.group("flags")
    flags_norm = normalize_strip_comments(flags_raw)
    flags_norm = normalize_flags(flags_norm.strip().split())
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
    fname = normalize_member_name(function_match.group("name"))
    # Skip property accessor functions (Get<Property>, Set<Property>)
    for pname in property_names:
        if fname == f"Get{pname}" or fname == f"Set{pname}":
            return None
    rtype = function_match.group("rtype")
    params = normalize_strip_comments(function_match.group("params").strip())
    # Strip comments from flags before splitting
    flags_raw = function_match.group("flags")
    norm_flags = normalize_strip_comments(flags_raw)
    norm_flags = normalize_flags(norm_flags.strip().split())
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
    name = normalize_member_name(event_match.group("name"))
    params = event_match.group("params").strip()
    # Strip comments from flags before splitting
    flags_raw = event_match.group("flags")
    norm_flags = normalize_strip_comments(flags_raw)
    norm_flags = normalize_flags(norm_flags.strip().split())
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
    name = normalize_member_name(struct_match.group("name"))
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
        line = normalize_strip_comments(line)
        match = re.match(r'^\s*scriptname\s+([^\s]+.*)$', line, re.IGNORECASE)
        if match:
            header_line = line.strip()
            script_name = match.group(1).split()[0]
            return idx, script_name, header_line
    raise ValueError("ScriptName not found")


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
            pname = normalize_member_name(property_match.group("name"))
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

    return script_name, normalize_header(header_line), documentation, members


# MediaWiki
#---------------------------------------------

def wiki_link_script(script_name):
    """Return a MediaWiki link for script objects."""
    return f"[[SFM:Script-{script_name}|{script_name}]]"


def wiki_link_script_member(script_name, member_name):
    """Return a MediaWiki link for a script member."""
    return f"[[SFM:Script-{script_name}/{member_name}|{member_name}]]"


def wiki_script_object_summary(title, script_name, extends_name, script_namespace=None, script_flags=None, game_version="v0.0.0+"):
    """
    Return the 'Script_Object_Summary' wiki template as a string.
    https://starfieldwiki.net/wiki/Template:Script_Object_Summary
    """
    return (
        "{{Script_Object_Summary\n"
        f"| title = {title}\n"
        f"| script = {wiki_link_script(script_name)}\n"
        f"| namespace = {script_namespace}\n"
        f"| extends = {wiki_link_script(extends_name)}\n"
        f"| flags = {script_flags}\n"
        f"| game_version = {game_version}\n"
        "}}\n"
    )


def wiki_script_object_member_summary(title, script_name, member_name, member_kind, member_return, member_flags, member_parameters, documentation, game_version="v0.0.0+"):
    """
    Return the 'Script_Object_Member_Summary' wiki template as a string.
    See https://starfieldwiki.net/wiki/Template:Script_Object_Member_Summary
    """
    return (
        "{{Script_Object_Member_Summary\n"
        f"| title = {title}\n"
        f"| script = {wiki_link_script(script_name)}\n"
        f"| name = {wiki_link_script_member(script_name, member_name)}\n"
        f"| kind = {member_kind}\n"
        f"| flags = {member_flags}\n"
        f"| returns = {member_return}\n"
        f"| parameters = {member_parameters}\n"
        f"| documentation = {documentation}\n"
        f"| game_version = {game_version}\n"
        "}}\n"
    )


# Not implemented yet, for standalone member pages
def wiki_script_member_summary(title, script_name, member_name, member_kind, member_return, member_flags, member_parameters, documentation, game_version="v0.0.0+"):
    """
    Return the 'Script_Member_Summary' wiki template as a string.
    https://starfieldwiki.net/wiki/Template:Script_Member_Summary
    """
    return (
        "{{Script_Member_Summary\n"
        f"| title = {title}\n"
        f"| script = {wiki_link_script(script_name)}\n"
        f"| name = {wiki_link_script_member(script_name, member_name)}\n"
        f"| kind = {member_kind}\n"
        f"| flags = {member_flags}\n"
        f"| returns = {member_return}\n"
        f"| parameters = {member_parameters}\n"
        f"| documentation = {game_version}\n"
        f"| game_version = {documentation}\n"
        "}}\n"
    )


# Debug
def wiki_generation_date():
    """Make a generation date string in the format YYYY/MM/DD hh:mm:ss AM/PM."""
    dt = datetime.datetime.now()
    pretty_date = dt.strftime("%Y/%m/%d %I:%M:%S %p")
    return f"* GENERATED: {pretty_date}"


# Debug
def wiki_script_date_modified(script_path):
    """Make a last modified date string for the script file in the format YYYY/MM/DD hh:mm:ss AM/PM."""
    mod_time = os.path.getmtime(script_path)
    dt = datetime.datetime.fromtimestamp(mod_time)
    pretty_date = dt.strftime("%Y/%m/%d %I:%M:%S %p")
    return f"* PAPYRUS:   {pretty_date}"


# Unused
def wiki_script_member(script_name, member):
    """
    Generate a MediaWiki formatted string for a script member.
    Returns a list of lines that can be written to a wiki page.

    Example:
        for line in wiki_script_member(script_name, member):
            f.write(f"{line}\n")
    """
    kind = member["kind"]
    lines = []

    if kind == "function":
        link = wiki_link_script_member(script_name, member["name"])
        flag_str = f" {' '.join(member['flags'])}" if member.get("flags") else ""
        param_str = ", ".join(member["params"])
        rtype = normalize_type(member["rtype"]) if member.get("rtype") else ""
        if rtype:
            lines.append(f"* {rtype} {normalize_keyword('function')} {link}({param_str}){flag_str}")
        else:
            lines.append(f"* {normalize_keyword('function')} {link}({param_str}){flag_str}")
        if member.get("doc"):
            lines.append(f"** {member['doc']}")

    elif kind == "event":
        link = wiki_link_script_member(script_name, member["name"])
        flag_str = f" {' '.join(member['flags'])}" if member.get("flags") else ""
        param_str = ", ".join(member["params"])
        lines.append(f"* {normalize_keyword('event')} {link}({param_str}){flag_str}")
        if member.get("doc"):
            lines.append(f"** {member['doc']}")

    elif kind == "property":
        link = wiki_link_script_member(script_name, member["name"])
        flag_str = f" {' '.join(member['flags'])}" if member.get("flags") else ""
        lines.append(f"* {member['type']} {normalize_keyword('property')} {link}{flag_str}")
        if member.get("doc"):
            lines.append(f"** {member['doc']}")

    elif kind == "struct":
        link = wiki_link_script_member(script_name, member["name"])
        lines.append(f"* {normalize_keyword('struct')} {link}")
        if member.get("doc"):
            lines.append(f"** {member['doc']}")

    return lines


# Writer
#---------------------------------------------

def wiki_write_page(script_path, output_path):
    """Generates a MediaWiki page for a given Papyrus script source file."""
    # Collect script information
    script_name, header_line, documentation, members = parse_script(script_path)
    extends_value = extract_script_extends(header_line)

    # Write the wiki page text content
    with open(output_path, "w", encoding="utf-8") as f:
        # DEBUG
        if WIKI_DEBUG:
            f.write(wiki_generation_date())
            f.write("\n")
            f.write(wiki_script_date_modified(script_path))
            f.write("\n\n")

        # Script Summary Template
        f.write(wiki_script_object_summary(script_name, script_name, extends_value))
        f.write("\n\n")

        # Script Definition
        f.write("== Definition ==\n")
        f.write(f"The <code>{script_name}.psc</code> source file header definition for this script.\n\n")
        f.write("<source lang=\"papyrus\">\n")
        f.write(f"{normalize_strip_comments(header_line)}\n")
        f.write("</source>\n\n\n")

        # Script Documentation
        f.write("== Documentation ==\n")
        f.write(f"The <code>{script_name}.psc</code> source file documentation comments for this script.\n\n")
        f.write("<source>\n")
        f.write(f"{documentation}\n")
        f.write("</source>\n\n\n")

        # Script Members
        f.write("== Members ==\n")
        f.write("The members that belong to this script.\n\n")
        for member in members:
            title = member["name"]
            member_name = member["name"]
            member_kind = member["kind"]
            member_rtype = member.get("rtype", "")
            member_flags = member.get("flags", [])
            member_params = member.get("params", [])
            member_doc = member.get("doc", "")
            f.write(
                wiki_script_object_member_summary(
                    title,
                    script_name,
                    member_name,
                    normalize_keyword(member_kind),
                    member_rtype,
                    " ".join(member_flags) if isinstance(member_flags, list) else member_flags,
                    ", ".join(member_params) if isinstance(member_params, list) else member_params,
                    member_doc,
                    "v0.0.0+"
                )
            )
            f.write("\n")

        # Page Categories
        f.write("\n\n")
        f.write("[[Category:Starfield_Mod-Papyrus]]\n")


# Main
#---------------------------------------------
if __name__ == "__main__":
    if not os.path.exists(SCRIPT_PATH):
        print(f"Script file does not exist: {SCRIPT_PATH}")
        exit(1)
    wiki_write_page(SCRIPT_PATH, OUTPUT_PATH)
    print(f"- Reading: {SCRIPT_PATH}")
    print(f"- Writing: {OUTPUT_PATH}")
