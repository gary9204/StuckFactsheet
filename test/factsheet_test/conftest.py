"""
Test fixtures for Factsheet as a whole.
"""


import pytest   # type: ignore[import]


@pytest.fixture
def PatchLogger():
    """Return stub class for logging."""
    class Logger:
        T_CRITICAL = 'critical'
        T_DEBUG = 'debug'
        T_NONE = 'none'
        T_WARNING = 'warning'

        def __init__(self):
            self.called = False
            self.level = self.T_NONE
            self.message = "No log call"

        def debug(self, p_message, *_args, **_kwargs):
            self.called = True
            self.level = self.T_DEBUG
            self.message = p_message

        def warning(self, p_message, *_args, **_kwargs):
            self.called = True
            self.level = self.T_WARNING
            self.message = p_message

        def critical(self, p_message, *_args, **_kwargs):
            self.called = True
            self.level = self.T_CRITICAL
            self.message = p_message

    return Logger
