
class Position(object):
    """
    Represents a zero-based positional index in text.
    """
    def __init__(self, line:int, column:int):
        self.line = line
        self.column = column


class Cursor(object):
    """
    Represents a cursor position in text.
    """
    def __init__(self, lines:list[str]):
        self.lines:list[str] = lines
        self.position:Position = Position(0, 0)
