from typing import override


class LineReader:
    """
    Represents a cursor position in text and encapsulates parsing state with line-by-line navigation.
    The cursor starts at index `-1`, before the first line.
    The underlying line buffer is immutable.
    """

    def __init__(self, lines:list[str]) -> None:
        super().__init__()
        self._lines:list[str] = lines.copy()
        self._cursor:int = -1


    def __len__(self) -> int:
        """Provides the number of lines in this collection."""
        return len(self._lines)


    def __getitem__(self, index:int) -> str:
        """Provides access to lines by index using array sub-script notation."""
        return self._lines[index]


    @override
    def __str__(self) -> str:
        """Provides a string representation of this object."""
        return f"TextReader(cursor={self._cursor}, lines={len(self)})"


    # Cursor Boundaries
    #---------------------------------------------

    @property
    def min(self) -> int:
        """Returns the minimum index for this collection."""
        return 0

    @property
    def max(self) -> int:
        """Returns the maximum index for this collection."""
        return len(self) - 1

    def valid_min(self, index:int) -> bool:
        """Determines if the given `index` satisfies the valid minimum range of lines."""
        return index >= self.min

    def valid_max(self, index:int) -> bool:
        """Determines if the given `index` satisfies the valid maximum range of lines."""
        return index <= self.max

    def valid(self, index:int) -> bool:
        """Determines if the given `index` is within the valid range of lines."""
        return self.valid_min(index) and self.valid_max(index)


    # Cursor
    #---------------------------------------------

    @property
    def cursor(self) -> int:
        """An index for the current line in this collection."""
        return self._cursor

    @cursor.setter
    def cursor(self, index:int) -> None:
        if self.valid(index):
            self._cursor = index
        else:
            raise IndexError(
                f"Cannot set cursor @'{self._cursor}' to index '{index}'. " +
                f"The index is out of bounds ({self.min} - {self.max})."
            )


    # Line
    #---------------------------------------------

    def line(self) -> str:
        """Gets the current line of text at the cursor position."""
        if self.valid(self.cursor):
            return self._lines[self.cursor]
        else:
            raise IndexError(
                f"Cannot get line at cursor index '{self.cursor}'. " +
                f"The index is out of bounds ({self.min} - {self.max})."
            )


    # Cursor Navigation
    #---------------------------------------------

    def has_line(self) -> bool:
        """Check if there is a line at the current cursor position."""
        return self.valid(self.cursor)

    def has_next(self) -> bool:
        """Check if a line exists after the current cursor position."""
        return self.valid_max(self.cursor + 1)

    def has_end(self) -> bool:
        """Check if cursor is beyond the last line."""
        return not self.valid_max(self.cursor)


    # Cursor Positioning
    #---------------------------------------------

    def move(self, offset:int = 1) -> str:
        """Advances the cursor by `offset` lines and returns the new current line."""
        self.cursor = self.cursor + offset
        return self.line()
