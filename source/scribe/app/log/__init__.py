"""
Logging configuration and utilities for the application.
"""
from .level import LogLevel

__all__ = [
    "LogLevel"
]


class Log:
    DIV_WIDTH:int = 50
    """The width of divider lines in the log output."""
