"""
Unit tests for :class:`~.app.AppFactsheet` and entry point.
"""
import gi   # type: ignore[import]

import factsheet.app as APP

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class TestFactsheet:
    """Unit tests for :class:`~.app.AppFactsheet`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        app_id = 'com.novafolks.g2alpha'
        # Test
        target = APP.AppFactsheet()
        assert isinstance(target, Gtk.Application)
        assert app_id == target.get_application_id()
        assert not target.get_windows()

    def test_do_activate(self, capfd):
        """Confirm creation of initial window.."""
        # Setup
        target = APP.AppFactsheet()
        # Test
        target.do_activate()
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

    def test_do_shutdown(self, monkeypatch, caplog):
        """Confirm application teardown."""
        # Setup
        # Bare call to superclass do_shutdown causes segmentation fault
        class PatchAppDoShutdown:
            def __init__(self): self.called = False

            def do_shutdown(self, _app): self.called = True

        patch = PatchAppDoShutdown()
        monkeypatch.setattr(
            Gtk.Application, 'do_shutdown', patch.do_shutdown)

        N_LOGS = 1
        target = APP.AppFactsheet()
        # Test
        target.do_shutdown()
        assert patch.called
        assert N_LOGS == len(caplog.records)
        assert 'AppFactsheet application shutdown.' in caplog.text

    def test_do_startup(self, monkeypatch, caplog):
        """Confirm application setup."""
        # Setup
        # Bare call to superclass do_startup causes segmentation fault
        class PatchAppDoStartup:
            def __init__(self): self.called = False

            def do_startup(self, _app): self.called = True

        patch = PatchAppDoStartup()
        monkeypatch.setattr(
            Gtk.Application, 'do_startup', patch.do_startup)

        N_LOGS = 1
        target = APP.AppFactsheet()
        # Test
        target.do_startup()
        assert patch.called
        assert N_LOGS == len(caplog.records)
        assert 'AppFactsheet application startup.' in caplog.text


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
