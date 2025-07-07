class Position:
    """
    Represents a zero-based positional index in text.
    """
    def __init__(self, line:int, column:int = 0):
        self.line = line
        self.column = column


class Parser:
    """
    Represents a cursor position in text and encapsulates parsing state with line-by-line navigation.
    """
    def __init__(self, lines:list[str]):
        self.lines:list[str] = lines
        self.cursor:Position = Position(0, 0)

    @property
    def line(self) -> str:
        """Returns the current line of text at the cursor position."""
        return self.lines[self.cursor.line]

    def peek(self, offset:int = 1) -> str:
        """Returns the next line of text without advancing the cursor."""
        line_index:int = self.cursor.line + offset
        if line_index < len(self.lines):
            return self.lines[line_index]
        return ""
