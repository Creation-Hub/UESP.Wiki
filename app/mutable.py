class MutableBool:
    """
    A mutable boolean wrapper for tracking state across function calls.
    """
    def __init__(self, value:bool = False):
        self.value = value
