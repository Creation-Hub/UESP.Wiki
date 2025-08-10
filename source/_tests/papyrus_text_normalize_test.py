# source/_tests/papyrus_text_normalize_test.py
import unittest
from papyrus.text.normalize import Normalize

class TestPapyrusNormalize(unittest.TestCase):

    # Test: Normalize.whitespace()
    #---------------------------------------------

    def test_whitespace(self) -> None:
        """Test whitespace normalization."""

        # Empty string
        self.assertEqual(Normalize.whitespace(""), "")

        # Only whitespace
        self.assertEqual(Normalize.whitespace("   \t\n   "), "")

        # Already normalized
        self.assertEqual(Normalize.whitespace("hello world"), "hello world")

        # Single word with whitespace
        self.assertEqual(Normalize.whitespace("  hello  "), "hello")

        # Multiple spaces to single space
        self.assertEqual(Normalize.whitespace("  hello    world  "), "hello world")

        # Tabs and spaces mixed
        self.assertEqual(Normalize.whitespace("\t\thello\t\tworld\t\t"), "hello world")

        # Newlines and mixed whitespace
        self.assertEqual(Normalize.whitespace("hello\n\n\tworld"), "hello world")

        # Leading/trailing whitespace removal
        self.assertEqual(Normalize.whitespace("   hello world   "), "hello world")


    # Test: Normalize.strip_comments()
    #---------------------------------------------

    def test_strip_comments(self) -> None:
        """Test comment stripping."""

        # Empty string
        self.assertEqual(Normalize.strip_comments(""), "")

        # No comments
        self.assertEqual(Normalize.strip_comments("Function MyFunc()"), "Function MyFunc()")

        # Only line comment
        self.assertEqual(Normalize.strip_comments("; just a comment"), "")

        # Only block comment
        self.assertEqual(Normalize.strip_comments(";/just a block comment/;"), "")

        # Semicolon without comment (at end of line)
        self.assertEqual(Normalize.strip_comments("text;"), "text")

        # Incomplete block comment (missing closing)
        self.assertEqual(Normalize.strip_comments("text ;/incomplete comment"), "text")



    def test_strip_comments_line(self) -> None:
        """Test removal of line comments (;...)."""

        # Basic line comment
        self.assertEqual(
            Normalize.strip_comments("Function MyFunc() ; This is a comment"),
            "Function MyFunc()"
        )

        # Comment with no leading space
        self.assertEqual(
            Normalize.strip_comments("int myVar;comment here"),
            "int myVar"
        )

        # Multiple semicolons (only first starts comment)
        self.assertEqual(
            Normalize.strip_comments("text ; comment ; more comment"),
            "text"
        )

        # Trailing whitespace after comment removal
        self.assertEqual(
            Normalize.strip_comments("Function MyFunc()   ; comment"),
            "Function MyFunc()"
        )



    def test_strip_comments_block(self) -> None:
        """Test removal of block comments (;/.../;)."""

        # Basic block comment
        self.assertEqual(
            Normalize.strip_comments("Function Foo(int ;/This is a comment/; x = 5)"),
            "Function Foo(int  x = 5)"
        )

        # Block comment at start
        # The leading whitespace is preserved (tab+space).
        self.assertEqual(
            Normalize.strip_comments(";/comment/; 	Function MyFunc()"),
            " 	Function MyFunc()"
        )

        # Block comment at end
        # The ending (right side) whitespace IS stripped.
        self.assertEqual(
            Normalize.strip_comments("Function MyFunc() ;/comment/;"),
            "Function MyFunc()"
        )

        # Multiple block comments
        self.assertEqual(
            Normalize.strip_comments("text ;/comment1/; middle ;/comment2/; end"),
            "text  middle  end"
        )



    def test_strip_comments_mixed(self) -> None:
        """Test removal of both block and line comments."""

        # Block comment followed by line comment
        self.assertEqual(
            Normalize.strip_comments("Function ;/block/; MyFunc() ; line comment"),
            "Function  MyFunc()"
        )

        # Line comment with semicolon in block comment (block should be removed first)
        self.assertEqual(
            Normalize.strip_comments("text ;/comment with ; inside/; more text"),
            "text  more text"
        )



    def test_strip_comments_samples(self) -> None:
        """Test with Papyrus code samples."""

        # Property with comment
        self.assertEqual(
            Normalize.strip_comments("int Property MyProperty Auto ; Getter/setter property"),
            "int Property MyProperty Auto"
        )

        # Function with parameter comment
        self.assertEqual(
            Normalize.strip_comments("Function DoSomething(int param = 5 ;/default value/;)"),
            "Function DoSomething(int param = 5 )"
        )

        # Event with trailing comment
        self.assertEqual(
            Normalize.strip_comments("Event OnActivate(ObjectReference akActionRef) ; Player activated"),
            "Event OnActivate(ObjectReference akActionRef)"
        )

        # Variable declaration with inline comment
        self.assertEqual(
            Normalize.strip_comments("bool isReady = true ;/initially ready/; Hidden"),
            "bool isReady = true  Hidden"
        )


    # Test: Normalize.symbol()
    #---------------------------------------------

    def test_symbol_normalization(self) -> None:
        """Test symbol normalization using `ChainMap` lookup."""

        # Empty string
        self.assertEqual(Normalize.symbol(""), "")

        # Unknown tokens (passthrough)
        self.assertEqual(Normalize.symbol("MyCustomType"), "MyCustomType")
        self.assertEqual(Normalize.symbol("someVariable"), "someVariable")

        # Keywords
        self.assertEqual(Normalize.symbol("ScRiPtNaMe"), "ScriptName")
        self.assertEqual(Normalize.symbol("FUNCTION"), "Function")
        self.assertEqual(Normalize.symbol("function"), "Function")

        # Flags
        self.assertEqual(Normalize.symbol("NATIVE"), "Native")
        self.assertEqual(Normalize.symbol("native"), "Native")

        # Primitive types
        self.assertEqual(Normalize.symbol("INT"), "int")
        self.assertEqual(Normalize.symbol("bool"), "bool")

        # Primitive values
        self.assertEqual(Normalize.symbol("TRUE"), "true")
        self.assertEqual(Normalize.symbol("false"), "false")


    # Test: Normalize.definition()
    #---------------------------------------------

    def test_definition_normalization(self) -> None:
        """Test complete definition line normalization."""

        # Function definition
        self.assertEqual(
            Normalize.definition("  FUNCTION   myFunc(  INT  param  )  NATIVE  ; comment"),
            "Function myFunc( int param ) Native"
        )

        # Property definition
        self.assertEqual(
            Normalize.definition("INT property myProp auto HIDDEN ;/comment/;"),
            "int Property myProp Auto Hidden"
        )

        # Event definition
        self.assertEqual(
            Normalize.definition("  event  onActivate(  )  "),
            "Event onActivate( )"
        )

        # Mixed case keywords
        self.assertEqual(
            Normalize.definition("ScriptName MyScript Extends ParentScript Native"),
            "ScriptName MyScript Extends ParentScript Native"
        )



# Unit Test Runner
#---------------------------------------------

if __name__ == "__main__":
    _ = unittest.main()
