"""
Unit tests for View class Sheet.
"""


import pytest   # type: ignore[import]

from factsheet.abc_types import abc_sheet as ASHEET
from factsheet.control import sheet as CSHEET
from factsheet.view import sheet as VSHEET

import gi   # type: ignore[import]
gi.require_version('Gtk', '3.0')
from gi.repository import GObject as GO  # type: ignore[import] # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class TestSheet:
    """Unit tests for View class Sheet."""

    def test_init(self, patch_factsheet, capfd):
        """Confirm initialization.
        Case: visual elements
        """
        # Setup
        factsheet = patch_factsheet()
        # Test
        target = VSHEET.Sheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

        assert target._control is None
        assert isinstance(target._window, Gtk.ApplicationWindow)
        assert target._window.get_application() is factsheet

        assert target._window.lookup_action('show_about_app') is not None
        assert target._window.lookup_action('show_help_app') is not None
        assert target._window.lookup_action('show_intro_app') is not None

    def test_init_signals(self, patch_factsheet, capfd):
        """Confirm initialization.
        Case: signals
        """
        # Setup
        factsheet = patch_factsheet()
        window_gtype = GO.type_from_name(GO.type_name(Gtk.ApplicationWindow))
        delete_signal = GO.signal_lookup('delete-event', window_gtype)
        # Test
        target = VSHEET.Sheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        assert target._window.get_application() is factsheet

        delete_id = GO.signal_handler_find(
            target._window, GO.SignalMatchType.ID, delete_signal,
            0, None, None, None)
        assert 0 != delete_id

    @pytest.mark.skip(reason='Pending implementation')
    def test_detach(self, patch_factsheet, capfd):
        """Confirm view detaches from control and closes."""
        # Setup
        # Test

    def test_on_close_view(self, patch_factsheet, capfd):
        """Confirm response to request to close view.
        Case: close allowed
        Case: close disallowed, user approves close
        Case: close disallowed, user cancels close
        """
        # Setup
        class PatchDetachViewSafe(CSHEET.Sheet):
            def __init__(self, p_result):
                super().__init__()
                self.n_calls = 0
                self.result = p_result

            def detach_view_safe(self, _view):
                self.n_calls += 1
                return self.result

        factsheet = patch_factsheet()

        target = VSHEET.Sheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

        control = PatchDetachViewSafe(ASHEET.ALLOWED)
        target._control = control
        N_CALLS = 1
        # Test -- stub
        assert target.on_close_view(None, None) is ASHEET.CONTINUE_GTK
        assert N_CALLS == control.n_calls

    @pytest.mark.skip(reason='Pending implementation')
    def test_on_delete_sheet(self):
        """Confirm response to request to delete factsheet.
        Case: deletion allowed
        Case: deletion disallowed, user approves delete
        Case: deletion disallowed, user cancels delete
        """
        # Setup
        # Test
        pass

    @pytest.mark.skip(reason='Pending implementation')
    def test_on_load_sheet(self):
        """Confirm response to request to load factsheet.
        Case: user cancels
        Case: user selects factsheet file
        Case: user selects file that is not a factsheet
        """
        # Setup
        # Test
        pass

    @pytest.mark.skip(reason='Pending implementation')
    def test_on_new_sheet(self):
        """Confirm response to request to create default factsheet."""
        # Setup
        # Test
        pass

    @pytest.mark.skip(reason='Pending implementation')
    def test_on_open_view(self):
        """Confirm response to request to open new view."""
        # Setup
        # Test
        pass

    @pytest.mark.parametrize('name_method', [
        'on_show_about_app',
        'on_show_help_app',
        'on_show_intro_app',
        ])
    def test_on_show_dialogs(
            self, patch_factsheet, capfd, name_method, monkeypatch):
        """Confirm running of dialogs.

        See manual tests for dialog content checks.
        """
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.Sheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        target_method = getattr(target, name_method)

        class DialogPatch:
            def __init__(self): self.called = False

            def run(self): self.called = True

        patch = DialogPatch()
        monkeypatch.setattr(Gtk.Dialog, 'run', patch.run)

        window = Gtk.ApplicationWindow()
        monkeypatch.setattr(
            Gtk.Application, 'get_windows', lambda *_args: [window])
        # Test
        target_method(None, None)
        assert patch.called

    @pytest.mark.skip(reason='Pending implementation')
    def test_open_factsheet(self):
        """Confirm factsheet creation from file."""
        # Setup
        # Test
        pass

    def test_new_factsheet(self, monkeypatch, patch_factsheet, capfd):
        """Confirm factsheet creation with default contents."""
        # Setup
        def patch_attach_view(self, px_view):
            self.view = px_view

        monkeypatch.setattr(
            CSHEET.Sheet, 'attach_view', patch_attach_view)
        factsheet = patch_factsheet()

        target = VSHEET.Sheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        # Test
        control = target.new_factsheet(target._window.get_application())
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        assert isinstance(control, CSHEET.Sheet)
        assert isinstance(control.view, VSHEET.Sheet)
        assert control.view._window.get_application() is factsheet
        assert control.view._control is control

    @pytest.mark.skip(reason='Pending implementation')
    def test_update_name(self):
        """Confirm window title update."""
        pass
