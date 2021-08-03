"""
Unit tests for :class:`~.app.AppFactsheet` and entry point.
"""
import gi   # type: ignore[import]

import factsheet.app as APP

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class TestApp:
    """Unit tests for AppFactsheet application entry point."""

    def test_run_app(self, monkeypatch):
        """Confirm application invoked."""
        # Setup
        class PatchRun:
            def __init__(self): self.called = False

            def run(self, _argv): self.called = True

        patch = PatchRun()
        monkeypatch.setattr(APP.AppFactsheet, 'run', patch.run)
        # Test
        APP.run_app()
        assert patch.called
