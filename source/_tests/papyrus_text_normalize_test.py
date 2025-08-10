# source/_tests/papyrus_text_normalize_test.py
import unittest
from papyrus.text import normalize

class TestPapyrusNormalize(unittest.TestCase):

    # Test: normalize.whitespace()
    #---------------------------------------------

    def test_whitespace(self) -> None:
        """Test whitespace normalization."""

        # Empty string
        self.assertEqual(normalize.whitespace(""), "")

        # Only whitespace
        self.assertEqual(normalize.whitespace("   \t\n   "), "")

        # Already normalized
        self.assertEqual(normalize.whitespace("hello world"), "hello world")

        # Single word with whitespace
        self.assertEqual(normalize.whitespace("  hello  "), "hello")

        # Multiple spaces to single space
        self.assertEqual(normalize.whitespace("  hello    world  "), "hello world")

        # Tabs and spaces mixed
        self.assertEqual(normalize.whitespace("\t\thello\t\tworld\t\t"), "hello world")

        # Newlines and mixed whitespace
        self.assertEqual(normalize.whitespace("hello\n\n\tworld"), "hello world")

        # Leading/trailing whitespace removal
        self.assertEqual(normalize.whitespace("   hello world   "), "hello world")


    # Test: normalize.strip_comments()
    #---------------------------------------------

    def test_strip_comments(self) -> None:
        """Test comment stripping."""

        # Empty string
        self.assertEqual(normalize.strip_comments(""), "")

        # No comments
        self.assertEqual(normalize.strip_comments("Function MyFunc()"), "Function MyFunc()")

        # Only line comment
        self.assertEqual(normalize.strip_comments("; just a comment"), "")

        # Only block comment
        self.assertEqual(normalize.strip_comments(";/just a block comment/;"), "")

        # Semicolon without comment (at end of line)
        self.assertEqual(normalize.strip_comments("text;"), "text")

        # Incomplete block comment (missing closing)
        self.assertEqual(normalize.strip_comments("text ;/incomplete comment"), "text")



    def test_strip_comments_line(self) -> None:
        """Test removal of line comments (;...)."""

        # Basic line comment
        self.assertEqual(
            normalize.strip_comments("Function MyFunc() ; This is a comment"),
            "Function MyFunc()"
        )

        # Comment with no leading space
        self.assertEqual(
            normalize.strip_comments("int myVar;comment here"),
            "int myVar"
        )

        # Multiple semicolons (only first starts comment)
        self.assertEqual(
            normalize.strip_comments("text ; comment ; more comment"),
            "text"
        )

        # Trailing whitespace after comment removal
        self.assertEqual(
            normalize.strip_comments("Function MyFunc()   ; comment"),
            "Function MyFunc()"
        )



    def test_strip_comments_block(self) -> None:
        """Test removal of block comments (;/.../;)."""

        # Basic block comment
        self.assertEqual(
            normalize.strip_comments("Function Foo(int ;/This is a comment/; x = 5)"),
            "Function Foo(int  x = 5)"
        )

        # Block comment at start
        # The leading whitespace is preserved (tab+space).
        self.assertEqual(
            normalize.strip_comments(";/comment/; 	Function MyFunc()"),
            " 	Function MyFunc()"
        )

        # Block comment at end
        # The ending (right side) whitespace IS stripped.
        self.assertEqual(
            normalize.strip_comments("Function MyFunc() ;/comment/;"),
            "Function MyFunc()"
        )

        # Multiple block comments
        self.assertEqual(
            normalize.strip_comments("text ;/comment1/; middle ;/comment2/; end"),
            "text  middle  end"
        )



    def test_strip_comments_mixed(self) -> None:
        """Test removal of both block and line comments."""

        # Block comment followed by line comment
        self.assertEqual(
            normalize.strip_comments("Function ;/block/; MyFunc() ; line comment"),
            "Function  MyFunc()"
        )

        # Line comment with semicolon in block comment (block should be removed first)
        self.assertEqual(
            normalize.strip_comments("text ;/comment with ; inside/; more text"),
            "text  more text"
        )



    def test_strip_comments_samples(self) -> None:
        """Test with Papyrus code samples."""

        # Property with comment
        self.assertEqual(
            normalize.strip_comments("int Property MyProperty Auto ; Getter/setter property"),
            "int Property MyProperty Auto"
        )

        # Function with parameter comment
        self.assertEqual(
            normalize.strip_comments("Function DoSomething(int param = 5 ;/default value/;)"),
            "Function DoSomething(int param = 5 )"
        )

        # Event with trailing comment
        self.assertEqual(
            normalize.strip_comments("Event OnActivate(ObjectReference akActionRef) ; Player activated"),
            "Event OnActivate(ObjectReference akActionRef)"
        )

        # Variable declaration with inline comment
        self.assertEqual(
            normalize.strip_comments("bool isReady = true ;/initially ready/; Hidden"),
            "bool isReady = true  Hidden"
        )


    # Test: normalize.symbol()
    #---------------------------------------------

    def test_symbol_normalization(self) -> None:
        """Test symbol normalization using `ChainMap` lookup."""

        # Empty string
        self.assertEqual(normalize.symbol(""), "")

        # Unknown tokens (passthrough)
        self.assertEqual(normalize.symbol("MyCustomType"), "MyCustomType")
        self.assertEqual(normalize.symbol("someVariable"), "someVariable")

        # Keywords
        self.assertEqual(normalize.symbol("ScRiPtNaMe"), "ScriptName")
        self.assertEqual(normalize.symbol("FUNCTION"), "Function")
        self.assertEqual(normalize.symbol("function"), "Function")

        # Flags
        self.assertEqual(normalize.symbol("NATIVE"), "Native")
        self.assertEqual(normalize.symbol("native"), "Native")

        # Primitive types
        self.assertEqual(normalize.symbol("INT"), "int")
        self.assertEqual(normalize.symbol("bool"), "bool")

        # Primitive values
        self.assertEqual(normalize.symbol("TRUE"), "true")
        self.assertEqual(normalize.symbol("false"), "false")


    # Test: normalize.definition()
    #---------------------------------------------

    def test_definition_normalization(self) -> None:
        """Test complete definition line normalization."""

        # Function definition
        self.assertEqual(
            normalize.definition("  FUNCTION   myFunc(  INT  param  )  NATIVE  ; comment"),
            "Function myFunc( int param ) Native"
        )

        # Property definition
        self.assertEqual(
            normalize.definition("INT property myProp auto HIDDEN ;/comment/;"),
            "int Property myProp Auto Hidden"
        )

        # Event definition
        self.assertEqual(
            normalize.definition("  event  onActivate(  )  "),
            "Event onActivate( )"
        )

        # Mixed case keywords
        self.assertEqual(
            normalize.definition("ScriptName MyScript Extends ParentScript Native"),
            "ScriptName MyScript Extends ParentScript Native"
        )
