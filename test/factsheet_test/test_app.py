"""
Unit tests for :class:`~.app.AppFactsheet` and entry point.
"""
import runpy

import factsheet.view.view_sheet as VSHEET


class TestApp:
    """Unit tests for AppFactsheet application entry point."""

    def test_run_app(self, monkeypatch):
        """Confirm application invoked."""
        # Setup
        class PatchRun:
            def __init__(self): self.called = False

            def run(self, _argv): self.called = True

        patch = PatchRun()
        monkeypatch.setattr(VSHEET.AppFactsheet, 'run', patch.run)
        # Test
        runpy.run_module('factsheet.app', run_name='__main__')
        assert patch.called
