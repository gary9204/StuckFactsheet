"""
Unit tests for class to display Factsheet document.

See :mod:`.page_sheet`.
"""
from pathlib import Path
import pytest   # type: ignore[import]

from factsheet.abc_types import abc_sheet as ABC_SHEET
from factsheet.control import sheet as CSHEET
from factsheet.view import page_sheet as VSHEET
from factsheet.view import ui as UI
from factsheet.view import view_infoid as VINFOID

import gi   # type: ignore[import]
gi.require_version('Gtk', '3.0')
from gi.repository import GObject as GO  # type: ignore[import] # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


@pytest.fixture
def patch_control_safe():
    class PatchSafe(CSHEET.Sheet):
        def __init__(self, p_effect):
            super().__init__()
            self.n_delete_force = 0
            self.n_delete_safe = 0
            self.n_detach_force = 0
            self.n_detach_safe = 0
            self.effect = p_effect

        def delete_force(self, _view):
            self.n_delete_force += 1
            return self.effect

        def delete_safe(self, _view):
            self.n_delete_safe += 1
            return self.effect

        def detach_page_force(self, _view):
            self.n_detach_force += 1
            return self.effect

        def detach_page_safe(self, _view):
            self.n_detach_safe += 1
            return self.effect

    return PatchSafe


class TestSheet:
    """Unit tests for View class Sheet."""

    PATH_DIR_UI_TEST = Path(__file__).parent
    NAME_FILE_UI_TEST = str(PATH_DIR_UI_TEST / 'test_page_sheet.ui')

    def test_init(self, patch_factsheet, capfd):
        """Confirm initialization.
        Case: visual elements
        """
        # Setup
        PatchPageSheet = VSHEET.PageSheet
        PatchPageSheet.NAME_FILE_SHEET_UI = self.NAME_FILE_UI_TEST
        TEST_TITLE_UI = 'Sheet title'

        factsheet = patch_factsheet()
        # Test
        target = PatchPageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

        assert target._control is None
        assert isinstance(target._window, Gtk.ApplicationWindow)
        assert target._window.get_application() is factsheet
        assert isinstance(target._infoid, VINFOID.ViewInfoId)
        assert TEST_TITLE_UI == target._infoid.title

        assert isinstance(target._dialog_warn, Gtk.Dialog)

        assert target._window.lookup_action('close_page_sheet') is not None
        assert target._window.lookup_action('new_sheet') is not None
        assert target._window.lookup_action('open_page_sheet') is not None

        assert target._window.lookup_action('show_about_app') is not None
        assert target._window.lookup_action('show_help_app') is not None
        assert target._window.lookup_action('show_intro_app') is not None

        assert target._window.lookup_action('show_help_sheet') is not None
        assert target._window.lookup_action(
            'show_help_sheet_display') is not None

        assert target._window.is_visible()

    def test_init_signals(self, patch_factsheet, capfd):
        """Confirm initialization.
        Case: signals
        """
        # Setup
        factsheet = patch_factsheet()
        window_gtype = GO.type_from_name(GO.type_name(Gtk.ApplicationWindow))
        delete_signal = GO.signal_lookup('delete-event', window_gtype)
        # Test
        target = VSHEET.PageSheet(px_app=factsheet)
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

    def test_get_infoid(self, patch_factsheet, capfd):
        """Confirm returns InfoId attribute."""
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        # Test
        assert target._infoid is target.get_infoid()

    def test_on_close_page_safe(
            self, patch_factsheet, capfd, patch_control_safe):
        """Confirm response to request to close page.
        Case: safe to close
        """
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

        control = patch_control_safe(ABC_SHEET.EffectSafe.COMPLETED)
        target._control = control
        N_CALLS_SAFE = 1
        N_CALLS_FORCE = 0
        # Test
        assert target.on_close_page(None, None) is UI.CLOSE_GTK
        assert N_CALLS_SAFE == control.n_detach_safe
        assert N_CALLS_FORCE == control.n_delete_force

    def test_on_close_page_cancel(
            self, patch_factsheet, capfd, monkeypatch, patch_control_safe):
        """Confirm response to request to close page.
        Case: not safe to close, user cancels close
        """
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

        monkeypatch.setattr(
            Gtk.Dialog, 'run', lambda _self: Gtk.ResponseType.CANCEL)

        control = patch_control_safe(ABC_SHEET.EffectSafe.NO_EFFECT)
        target._control = control
        N_CALLS_SAFE = 1
        N_CALLS_FORCE = 0
        # Test -- stub
        assert target.on_close_page(None, None) is UI.CANCEL_GTK
        assert N_CALLS_SAFE == control.n_detach_safe
        assert N_CALLS_FORCE == control.n_detach_force

    def test_on_close_page_discard(
            self, patch_factsheet, capfd, monkeypatch, patch_control_safe):
        """Confirm response to request to close page.
        Case: not safe to close, user approves close
        """
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

        monkeypatch.setattr(
            Gtk.Dialog, 'run', lambda _self: Gtk.ResponseType.APPLY)

        control = patch_control_safe(ABC_SHEET.EffectSafe.NO_EFFECT)
        target._control = control
        N_CALLS_SAFE = 1
        N_CALLS_FORCE = 1
        # Test -- stub
        assert target.on_close_page(None, None) is UI.CLOSE_GTK
        assert N_CALLS_SAFE == control.n_detach_safe
        assert N_CALLS_FORCE == control.n_detach_force

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

    def test_on_new_sheet(self, monkeypatch, patch_factsheet, capfd):
        """Confirm response to request to create default factsheet."""
        # Setup
        class PatchNew:
            def __init__(self): self.called = False

            def new_factsheet(self, px_app):
                _ = px_app
                self.called = True

        patch_new = PatchNew()
        monkeypatch.setattr(
            VSHEET.PageSheet, 'new_factsheet', patch_new.new_factsheet)

        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        # Test
        target.on_new_sheet(None, None)
        assert patch_new.called

    def test_on_open_page(self, patch_factsheet, capfd):
        """Confirm response to request to open new view."""
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        control = CSHEET.Sheet.new()
        target._control = control
        # Test
        target.on_open_page(None, None)
        assert 1 == control._model.n_pages()

    def test_on_show_dialog(self, patch_factsheet, capfd, monkeypatch):
        """Confirm handler runs dialog.

        See manual tests for dialog content checks.
        """
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

        class DialogPatch:
            def __init__(self): self.called = False

            def run(self): self.called = True

        patch = DialogPatch()
        monkeypatch.setattr(Gtk.Dialog, 'run', patch.run)

        window = Gtk.ApplicationWindow()
        monkeypatch.setattr(
            Gtk.Application, 'get_windows', lambda *_args: [window])
        dialog = Gtk.Dialog()
        dialog.set_visible(True)
        # Test
        target.on_show_dialog(None, None, dialog)
        assert patch.called
        assert not dialog.is_visible()

    @pytest.mark.skip(reason='Pending implementation')
    def test_open_factsheet(self):
        """Confirm factsheet creation from file."""
        # Setup
        # Test
        pass

    def test_new_factsheet(self, monkeypatch, patch_factsheet, capfd):
        """Confirm factsheet creation with default contents."""
        # Setup
        def patch_attach_page(self, pm_view):
            self.view = pm_view

        monkeypatch.setattr(
            CSHEET.Sheet, 'attach_page', patch_attach_page)
        factsheet = patch_factsheet()

        target = VSHEET.PageSheet(px_app=factsheet)
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
        assert isinstance(control.view, VSHEET.PageSheet)
        assert control.view._window.get_application() is factsheet
        assert control.view._control is control

#     @pytest.mark.parametrize('name_attr, name_prop', [
#         ['_infoid', 'infoid'],
#         ])
#     def test_property(self, patch_factsheet, name_attr, name_prop, capfd):
#         """Confirm properties are get-only.
#
#         #. Case: read
#         #. Case: no replace
#         #. Case: no delete
#         """
#         # Setup
#         factsheet = patch_factsheet()
#         target = VSHEET.PageSheet(px_app=factsheet)
#         value_attr = getattr(target, name_attr)
#         target_prop = getattr(VSHEET.PageSheet, name_prop)
#         value_prop = getattr(target, name_prop)
#
#         snapshot = capfd.readouterr()   # Resets the internal buffer
#         assert not snapshot.out
#         assert 'Gtk-CRITICAL' in snapshot.err
#         assert 'GApplication::startup signal' in snapshot.err
#         # Test: read
#         assert target_prop.fget is not None
#         assert str(value_attr) == str(value_prop)
#         # Test: no replace
#         assert target_prop.fset is None
#         # Test: no delete
#         assert target_prop.fdel is None

    @pytest.mark.skip(reason='Pending implementation')
    def test_update_name(self):
        """Confirm window title update."""
        pass
