# source/_tests/papyrus_text_regex_test.py
import unittest
from re import Match
from papyrus.text import regex

class TestPapyrusRegex(unittest.TestCase):



    def test_header_pattern(self) -> None:
        """Test script header pattern matching."""
        # Valid headers
        valid_cases:list[str] = [
            "ScriptName MyScript",
            "ScriptName MyScript Extends MyParent",
            "ScriptName My:Namespaced:Script Extends MyParent Native",
            "  ScriptName  MyScript  Extends  MyParent  Native  Hidden  "
        ]

        for case in valid_cases:
            with self.subTest(case=case):
                match:Match[str]|None = regex.HEADER_PATTERN.match(case)
                self.assertIsNotNone(match, f"Failed to match: {case}")
                if match:
                    self.assertIsNotNone(match.group("name"))
                else:
                    self.fail(f"Match unexpectedly None for case: {case}")



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
                GROUP_PARAMS: None,
                GROUP_FLAGS: None
            },
            "bool Function MyFunc() Native":
            {
                GROUP_NAME: "MyFunc",
                GROUP_TYPE: "bool",
                GROUP_PARAMS: None,
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
                GROUP_FLAGS: None
            },
            "bool Function MyFunc() Native":
            {
                GROUP_NAME: "MyFunc",
                GROUP_TYPE: "bool",
                GROUP_PARAMS: None,
                GROUP_FLAGS: "Native"
            }
        }

        # Compare each case line against the expected group matches.
        for line, expected in cases.items():
            with self.subTest(line=line):
                match:Match[str]|None = regex.FUNCTION_PATTERN.match(line)
                self.assertIsNotNone(match)
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
