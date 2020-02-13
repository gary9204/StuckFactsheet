"""
factsheet_test.test_app - unit tests for Factsheet applicaton entry.
"""

# import pytest   # type: ignore[import]

import factsheet.app as APP

import gi   # type: ignore[import]
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class TestApp:
    """Unit tests for Factsheet application entry."""

    def test_run_app(self, monkeypatch):
        """Confirm application starts GTK."""
        # Setup
        class PatchGtk:
            def __init__(self): self.called = False

            def main(self): self.called = True

        patch = PatchGtk()
        monkeypatch.setattr(Gtk, 'main', patch.main)
        # Test
        APP.run_app()
        assert patch.called
