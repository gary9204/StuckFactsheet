"""
factsheet_test.test_app - unit tests for Factsheet applicaton entry.
"""

import gi   # type: ignore[import]
import pytest   # type: ignore[import]

import factsheet.app as APP
# from factsheet.view import sheet as VSHEET

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class TestFactsheet:
    """Unit tests for application class Factsheet."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        app_id = 'com.novafolks.g2alpha'
        # Test
        target = APP.Factsheet()
        assert isinstance(target, Gtk.Application)
        assert app_id == target.get_application_id()
        assert not target.get_windows()

    def test_do_activate(self, capfd):
        """Confirm creation of initial window.."""
        # Setup
        target = APP.Factsheet()
        # Test
        target.do_activate()
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

    def test_do_shutdown(self, monkeypatch, capfd):
        """Confirm application teardown."""
        # Setup
        # Bare call to superclass do_startup causes segmentation fault
        class PatchAppDoShutdown:
            def __init__(self): self.called = False

            def do_shutdown(self, _app): self.called = True

        patch = PatchAppDoShutdown()
        monkeypatch.setattr(
            Gtk.Application, 'do_shutdown', patch.do_shutdown)

        target = APP.Factsheet()
        # Test
        target.do_shutdown()
        assert patch.called
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert 'Factsheet application shutdown.' in snapshot.out

    def test_do_startup(self, monkeypatch, capfd):
        """Confirm application setup."""
        # Setup
        # Bare call to superclass do_startup causes segmentation fault
        class PatchAppDoStartup:
            def __init__(self): self.called = False

            def do_startup(self, _app): self.called = True

        patch = PatchAppDoStartup()
        monkeypatch.setattr(
            Gtk.Application, 'do_startup', patch.do_startup)

        target = APP.Factsheet()
        # Test
        target.do_startup()
        assert patch.called
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert 'Factsheet application startup.' in snapshot.out


class TestApp:
    """Unit tests for Factsheet application entry."""

    def test_run_app(self, monkeypatch):
        """Confirm application starts GTK."""
        # Setup
        class PatchRun:
            def __init__(self): self.called = False

            def run(self, _argv): self.called = True

        patch = PatchRun()
        monkeypatch.setattr(APP.Factsheet, 'run', patch.run)
        # Test
        APP.run_app()
        assert patch.called
