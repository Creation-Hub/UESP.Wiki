class TextReader:
    """
    Represents a cursor position in text and encapsulates parsing state with line-by-line navigation.
    """
    def __init__(self, lines:list[str]):
        self.lines:list[str] = lines
        self.cursor:int = -1


    # Python Collections
    #---------------------------------------------

    def __len__(self) -> int:
        """Provides the number of lines in this collection."""
        return len(self.lines)


    def __getitem__(self, index:int) -> str:
        """Provides access to lines by index using array sub-script notation."""
        return self.lines[index]


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
        """Determines if the given `index` is within the valid minimum range of lines."""
        return index >= self.min

    def valid_max(self, index:int) -> bool:
        """Determines if the given `index` is within the valid maximum range of lines."""
        return index <= self.max

    def valid(self, index:int) -> bool:
        """Determines if the given `index` is within the valid range of lines."""
        return self.valid_min(index) and self.valid_max(index)


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

    def move(self, offset:int = 1) -> None:
        index:int = self.cursor + offset
        if self.valid(index):
            self.cursor = index
        else:
            message:str = (
                f"Cannot move cursor from index '{self.cursor}' to index '{index}'. "
                f"Destination index is out of bounds ({self.min} - {self.max})."
            )
            raise IndexError(message)


    def get_line(self) -> str:
        """Gets the current line of text at the cursor position."""
        if self.valid(self.cursor):
            return self.lines[self.cursor]
        else:
            message:str = (
                f"Cannot get line at cursor index '{self.cursor}'. "
                f"The index is out of bounds ({self.min} - {self.max})."
            )
            raise IndexError(message)


    def move_next(self) -> str:
        """Gets the current line and advances the cursor to the next line."""
        self.move()
        return self.get_line()
