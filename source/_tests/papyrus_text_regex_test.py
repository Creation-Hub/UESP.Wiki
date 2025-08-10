"""
Unit tests for `papyrus.text.regex` module.


This module tests regex patterns designed to parse valid Papyrus source code with "standard variance" in formatting.

The patterns are intentionally tolerant of:
- Reasonable whitespace variations (extra spaces, leading/trailing whitespace)
- Case insensitivity for Papyrus keywords (ScriptName, SCRIPTNAME, scriptname)
- Common formatting inconsistencies found in real-world scripts


The regex patterns assume valid, compilable Papyrus source as input.

Patterns are NOT designed to handle:
- Malformed or invalid syntax that wouldn't compile
- Extreme edge cases or unusual formatting
- Complex normalization (handled by separate parsing layers)


Each test verifies that regex capture groups extract raw text faithfully,
preserving original formatting including whitespace. Text normalization and
cleanup are the responsibility of upstream & downstream parsing functions, maintaining
clear separation of concerns between pattern matching and data processing.

Test cases focus on realistic patterns encountered in actual Papyrus scripts
rather than theoretical edge cases, ensuring the regex patterns work reliably
with standard development practices while remaining maintainable and performant.
"""
import unittest
from re import Match
from papyrus.text import regex

class TestPapyrusRegex(unittest.TestCase):


    def test_header_pattern(self) -> None:
        """Test script header pattern matching."""

        GROUP_NAME:str = "name" # Required
        GROUP_EXTENDS:str = "extends" # Optional
        GROUP_FLAGS:str = "flags" # Optional

        # Valid headers
        # Test each `key` line with the expected group match values.
        cases:dict[str, dict[str, str|None]] = {
            "ScriptName MyScript1":
            {
                GROUP_NAME: "MyScript1",
                GROUP_EXTENDS: None,
                GROUP_FLAGS: ""
            },
            "ScriptName MyScript2 Extends MyParent":
            {
                GROUP_NAME: "MyScript2",
                GROUP_EXTENDS: "MyParent",
                GROUP_FLAGS: ""
            },
            "ScriptName MyScript3 Extends MyParent Native":
            {
                GROUP_NAME: "MyScript3",
                GROUP_EXTENDS: "MyParent",
                GROUP_FLAGS: " Native"
            },
            "ScriptName MyScript4 Extends MyParent Native Hidden":
            {
                GROUP_NAME: "MyScript4",
                GROUP_EXTENDS: "MyParent",
                GROUP_FLAGS: " Native Hidden"
            },
            "  ScriptName  MyScript5  Extends  MyParent  Native  Hidden  ":
            {
                GROUP_NAME: "MyScript5",
                GROUP_EXTENDS: "MyParent",
                GROUP_FLAGS: " Native  Hidden"
            },
            "ScriptName My:Namespaced:MyScript6 Extends MyParent Native":
            {
                GROUP_NAME: "My:Namespaced:MyScript6",
                GROUP_EXTENDS: "MyParent",
                GROUP_FLAGS: " Native"
            }
        }

        # Compare each case line against the expected group matches.
        for line, expected in cases.items():
            with self.subTest(line=line):
                match:Match[str]|None = regex.HEADER_PATTERN.match(line)
                self.assertIsNotNone(match, f"Failed to match: {line}")
                if match:
                    self.assertEqual(match.group(GROUP_NAME), expected[GROUP_NAME], f"The `{GROUP_NAME}` match group had an unexpected value.")
                    self.assertEqual(match.group(GROUP_EXTENDS), expected[GROUP_EXTENDS], f"The `{GROUP_EXTENDS}` match group had an unexpected value.")
                    self.assertEqual(match.group(GROUP_FLAGS), expected[GROUP_FLAGS], f"The `{GROUP_FLAGS}` match group had an unexpected value.")
                else:
                    self.fail(f"Match unexpectedly None for case: {line}")



    def test_function_pattern(self) -> None:
        """Test function pattern matching."""

        GROUP_NAME:str = "name" # Required
        GROUP_TYPE:str = "type" # Optional
        GROUP_PARAMS:str = "params" # Optional
        GROUP_FLAGS:str = "flags" # Optional

        # Test each `key` line with the expected group match values.
        cases:dict[str, dict[str, str|None]] = {
            "Function MyFunc()":
            {
                GROUP_NAME: "MyFunc",
                GROUP_TYPE: None,
                GROUP_PARAMS: "",
                GROUP_FLAGS: ""
            },
            "bool Function MyFunc() Native":
            {
                GROUP_NAME: "MyFunc",
                GROUP_TYPE: "bool",
                GROUP_PARAMS: "",
                GROUP_FLAGS: "Native"
            },
            "Function MyFunc(string param1) Native":
            {
                GROUP_NAME: "MyFunc",
                GROUP_TYPE: None,
                GROUP_PARAMS: "string param1",
                GROUP_FLAGS: "Native"
            },
            "int Function MyFunc(string param1)":
            {
                GROUP_NAME: "MyFunc",
                GROUP_TYPE: "int",
                GROUP_PARAMS: "string param1",
                GROUP_FLAGS: ""
            },
            "bool Function MyFunc() Native":
            {
                GROUP_NAME: "MyFunc",
                GROUP_TYPE: "bool",
                GROUP_PARAMS: "",
                GROUP_FLAGS: "Native"
            }
        }

        # Compare each case line against the expected group matches.
        for line, expected in cases.items():
            with self.subTest(line=line):
                match:Match[str]|None = regex.FUNCTION_PATTERN.match(line)
                self.assertIsNotNone(match, f"Failed to match: {line}")
                if match:
                    self.assertEqual(match.group(GROUP_NAME), expected[GROUP_NAME], f"The `{GROUP_NAME}` match group had an unexpected value.")
                    self.assertEqual(match.group(GROUP_TYPE), expected[GROUP_TYPE], f"The `{GROUP_TYPE}` match group had an unexpected value.")
                    self.assertEqual(match.group(GROUP_PARAMS), expected[GROUP_PARAMS], f"The `{GROUP_PARAMS}` match group had an unexpected value.")
                    self.assertEqual(match.group(GROUP_FLAGS), expected[GROUP_FLAGS], f"The `{GROUP_FLAGS}` match group had an unexpected value.")
                else:
                    self.fail(f"`Match` unexpectedly `None` for line: {line}")




    def test_variable_pattern(self) -> None:
        """Test variable declaration pattern matching."""
        cases:list[str] = [
            "int myVar",
            "string myString = \"default\"",
            "bool myBool = true",
            "float[] myArray"
        ]

        for case in cases:
            with self.subTest(case=case):
                match:Match[str]|None = regex.VARIABLE_PATTERN.match(case)
                self.assertIsNotNone(match, f"Failed to match variable: {case}")
