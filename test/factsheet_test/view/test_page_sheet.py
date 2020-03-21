"""
Unit tests for class to display Factsheet document.

See :mod:`.page_sheet`.
"""
from pathlib import Path
import pytest   # type: ignore[import]

from factsheet.abc_types import abc_sheet as ABC_SHEET
from factsheet.control import pool as CPOOL
from factsheet.control import sheet as CSHEET
from factsheet.model import sheet as MSHEET
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
        def __init__(self, p_effect, pm_sheets_active):
            super().__init__(pm_sheets_active)
            self.n_delete_force = 0
            self.n_delete_safe = 0
            self.n_detach_force = 0
            self.n_detach_safe = 0
            self.effect = p_effect

        def delete_force(self):
            self.n_delete_force += 1
            return self.effect

        def delete_safe(self):
            self.n_delete_safe += 1
            return self.effect

        def detach_page_force(self, _view):
            self.n_detach_force += 1
            return self.effect

        def detach_page_safe(self, _view):
            self.n_detach_safe += 1
            return self.effect

    return PatchSafe


@pytest.fixture
def patch_dialog_choose():
    class PatchDialog:
        def __init__(self, p_response, p_filename):
            self.called_hide = False
            self.called_get_filename = False
            self.called_run = False
            self.called_set_current_name = False
            self.called_set_filename = False
            self.response = p_response
            self.filename = p_filename

        def hide(self):
            self.called_hide = True

        def get_filename(self):
            self.called_get_filename = True
            return self.filename

        def run(self):
            self.called_run = True
            return self.response

        def set_current_name(self, _n):
            self.called_set_current_name = True

        def set_filename(self, _fn):
            self.called_set_filename = True

    return PatchDialog


@pytest.fixture
def patch_dialog_run():
    class PatchDialog:
        def __init__(self, p_response):
            self.called = False
            self.response = p_response

        def run(self):
            self.called = True
            return self.response

    return PatchDialog


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
#         sheets_active = CPOOL.PoolSheets()
        # Test
        target = PatchPageSheet(px_app=factsheet)
#             px_app=factsheet, pm_sheets_active=sheets_active)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

        assert target._control is None
        assert isinstance(target._window, Gtk.ApplicationWindow)
        assert target._window.get_application() is factsheet
        assert isinstance(target._dialog_data_loss, Gtk.Dialog)
        assert isinstance(target._warning_data_loss, Gtk.Label)
        assert isinstance(target._infoid, VINFOID.ViewInfoId)
        assert TEST_TITLE_UI == target._infoid.title

        # Application Title
        assert target._window.lookup_action('open-sheet') is not None
        assert target._window.lookup_action('new-sheet') is not None
        assert target._window.lookup_action('save-sheet') is not None
        assert target._window.lookup_action('save-as-sheet') is not None

        # Application Menu
        assert target._window.lookup_action('show-intro-app') is not None
        assert target._window.lookup_action('show-help-app') is not None
        assert target._window.lookup_action('show-about-app') is not None

        # Factsheet Menu
        assert target._window.lookup_action('show-help-sheet') is not None

        # Factsheet Display Menu
        assert target._window.lookup_action('open-page-sheet') is not None
        assert target._window.lookup_action('close-page-sheet') is not None
        assert target._window.lookup_action(
            'show-help-sheet-display') is not None

        # Factsheet File Menu
        assert target._window.lookup_action('delete-sheet') is not None
        assert target._window.lookup_action(
            'show-help-sheet-file') is not None

        assert not target._close_window
        assert target._window.is_visible()
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_init_signals(self, patch_factsheet, capfd):
        """Confirm initialization.
        Case: signals
        """
        # Setup
        factsheet = patch_factsheet()
#         sheets_active = CPOOL.PoolSheets()
        window_gtype = GO.type_from_name(GO.type_name(Gtk.ApplicationWindow))
        delete_signal = GO.signal_lookup('delete-event', window_gtype)
        # Test
        target = VSHEET.PageSheet(px_app=factsheet)
#             px_app=factsheet, pm_sheets_active=sheets_active)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        assert target._window.get_application() is factsheet

        delete_id = GO.signal_handler_find(
            target._window, GO.SignalMatchType.ID, delete_signal,
            0, None, None, None)
        assert 0 != delete_id
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_close_page(self, monkeypatch, patch_factsheet, capfd):
        """Confirm view detaches from control and closes."""
        # Setup
        class PatchWindow:
            def __init__(self): self.called = False

            def close(self): self.called = True

        patch_window = PatchWindow()
        monkeypatch.setattr(
            Gtk.ApplicationWindow, 'close', patch_window.close)

        factsheet = patch_factsheet()
#         sheets_active = CPOOL.PoolSheets()
        target = VSHEET.PageSheet(px_app=factsheet)
#             px_app=factsheet, pm_sheets_active=sheets_active)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        target._window.set_visible(True)
        # Test
        target.close_page()
        assert not target._window.get_visible()
        assert target._close_window
        assert patch_window.called
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_get_infoid(self, patch_factsheet, capfd):
        """Confirm returns InfoId attribute."""
        # Setup
        factsheet = patch_factsheet()
#         sheets_active = CPOOL.PoolSheets()
        target = VSHEET.PageSheet(px_app=factsheet)
#             px_app=factsheet, pm_sheets_active=sheets_active)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        # Test
        assert target._infoid is target.get_infoid()
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_init_factsheet(self, monkeypatch, patch_factsheet, capfd):
        """Confirm creation of factsheet links."""
        # Setup
        def patch_attach_page(self, pm_view):
            self.test_view = pm_view

        monkeypatch.setattr(
            CSHEET.Sheet, 'attach_page', patch_attach_page)
        factsheet = patch_factsheet()
        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.Sheet(sheets_active)
        page = VSHEET.PageSheet(px_app=factsheet)
#             px_app=factsheet, pm_sheets_active=sheets_active)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        # Test
        VSHEET.PageSheet.link_factsheet(page, control)
        assert control.test_view is page
        assert page._control is control
#         assert sheets_active._controls[id(control)] is control
        # Teardown
        page._window.destroy()
        del page._window
        del factsheet

    @pytest.mark.parametrize('action, label', [
        (Gtk.FileChooserAction.SAVE, 'Save'),
        (Gtk.FileChooserAction.OPEN, 'Open'),
        ])
    def test_make_dialog_file_save(
            self, patch_factsheet, capfd, action, label):
        """Confirm construction of dialog for file save."""
        # Setup
        factsheet = patch_factsheet()
#         sheets_active = CPOOL.PoolSheets()
        source = VSHEET.PageSheet(px_app=factsheet)
#             px_app=factsheet, pm_sheets_active=sheets_active)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        FILTERS = set(['Factsheet', 'Any'])
        # Test
        target = source._make_dialog_file(action)
        assert isinstance(target, Gtk.FileChooserDialog)
        assert target.get_action() is action
        assert target.get_transient_for() is source._window
        assert target.get_destroy_with_parent()
        if action is Gtk.FileChooserAction.SAVE:
            assert target.get_do_overwrite_confirmation()

        button = target.get_widget_for_response(Gtk.ResponseType.CANCEL)
        assert 'Cancel' == button.get_label()

        button = target.get_widget_for_response(Gtk.ResponseType.APPLY)
        assert label == button.get_label()
        style = button.get_style_context()
        assert style.has_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)

        assert FILTERS == {f.get_name() for f in target.list_filters()}
        # Teardown
        source._window.destroy()
        del source._window
        del factsheet

    def test_new_factsheet(self, patch_factsheet, capfd):
        """Confirm factsheet creation with default contents."""
        # Setup
        factsheet = patch_factsheet()
        sheets_active = CPOOL.PoolSheets()
        # Test
        target = VSHEET.PageSheet.new_factsheet(factsheet, sheets_active)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        assert isinstance(target, VSHEET.PageSheet)
        assert target._window.get_application() is factsheet
        control = target._control
        assert isinstance(control, CSHEET.Sheet)
#         assert sheets_active._controls[id(control)] is control
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_on_close_page_force(
            self, patch_factsheet, capfd, patch_control_safe):
        """Confirm response to request to close page.
        Case: unconditional close
        """
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
#             px_app=factsheet, pm_sheets_active=sheets_active)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

        sheets_active = CPOOL.PoolSheets()
        control = patch_control_safe(
            ABC_SHEET.EffectSafe.COMPLETED, sheets_active)
        target._control = control
        target._close_window = True
        N_CALLS_SAFE = 0
        N_CALLS_FORCE = 0
        # Test
        assert target.on_close_page(None, None) is UI.CLOSE_GTK
        assert N_CALLS_SAFE == control.n_detach_safe
        assert N_CALLS_FORCE == control.n_detach_force
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_on_close_page_safe(
            self, patch_factsheet, capfd, patch_control_safe):
        """Confirm response to request to close page.
        Case: safe to close
        """
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
#             px_app=factsheet, pm_sheets_active=sheets_active)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

        sheets_active = CPOOL.PoolSheets()
        control = patch_control_safe(
            ABC_SHEET.EffectSafe.COMPLETED, sheets_active)
        target._control = control
        N_CALLS_SAFE = 1
        N_CALLS_FORCE = 0
        # Test
        assert target.on_close_page(None, None) is UI.CLOSE_GTK
        assert N_CALLS_SAFE == control.n_detach_safe
        assert N_CALLS_FORCE == control.n_detach_force
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_on_close_page_cancel(
            self, patch_factsheet, capfd, monkeypatch, patch_control_safe):
        """Confirm response to request to close page.
        Case: not safe to close, user cancels close
        """
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
#             px_app=factsheet, pm_sheets_active=sheets_active)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

        monkeypatch.setattr(
            Gtk.Dialog, 'run', lambda _self: Gtk.ResponseType.CANCEL)
        target._dialog_data_loss.set_visible(True)
        monkeypatch.setattr(
            Gtk.Dialog, 'hide', lambda self: self.set_visible(False))

        sheets_active = CPOOL.PoolSheets()
        control = patch_control_safe(
            ABC_SHEET.EffectSafe.NO_EFFECT, sheets_active)
        target._control = control
        N_CALLS_SAFE = 1
        N_CALLS_FORCE = 0
        # Test
        assert target.on_close_page(None, None) is UI.CANCEL_GTK
        assert not target._dialog_data_loss.get_visible()
        assert N_CALLS_SAFE == control.n_detach_safe
        assert N_CALLS_FORCE == control.n_detach_force
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_on_close_page_discard(
            self, patch_factsheet, capfd, monkeypatch, patch_control_safe):
        """Confirm response to request to close page.
        Case: not safe to close, user approves close
        """
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
#             px_app=factsheet, pm_sheets_active=sheets_active)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

        monkeypatch.setattr(
            Gtk.Dialog, 'run', lambda _self: Gtk.ResponseType.APPLY)
        target._dialog_data_loss.set_visible(True)
        monkeypatch.setattr(
            Gtk.Dialog, 'hide', lambda self: self.set_visible(False))

        sheets_active = CPOOL.PoolSheets()
        control = patch_control_safe(
            ABC_SHEET.EffectSafe.NO_EFFECT, sheets_active)
        target._control = control
        N_CALLS_SAFE = 1
        N_CALLS_FORCE = 1
        # Test
        assert target.on_close_page(None, None) is UI.CLOSE_GTK
        assert not target._dialog_data_loss.get_visible()
        assert N_CALLS_SAFE == control.n_detach_safe
        assert N_CALLS_FORCE == control.n_detach_force
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_on_delete_sheet_safe(
            self, patch_factsheet, capfd, patch_dialog_run,
            monkeypatch, patch_control_safe):
        """Confirm response to request to delete factsheet.
        Case: no unsaved changes
        """
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
#             px_app=factsheet, pm_sheets_active=sheets_active)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

        patch_dialog = patch_dialog_run(Gtk.ResponseType.CANCEL)
        monkeypatch.setattr(Gtk.Dialog, 'run', patch_dialog.run)

        sheets_active = CPOOL.PoolSheets()
        control = patch_control_safe(
            ABC_SHEET.EffectSafe.COMPLETED, sheets_active)
        control._model = MSHEET.Sheet()
        VSHEET.PageSheet.link_factsheet(target, control)
#         assert sheets_active._controls[id(control)] is control
        N_CALLS_SAFE = 1
        N_CALLS_FORCE = 0
        # Test
        target.on_delete_sheet(None, None)
#         assert id(control) not in sheets_active._controls.keys()
        assert not patch_dialog.called
        assert N_CALLS_SAFE == control.n_delete_safe
        assert N_CALLS_FORCE == control.n_delete_force
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_on_delete_sheet_cancel(
            self, patch_factsheet, capfd, patch_dialog_run,
            monkeypatch, patch_control_safe):
        """Confirm response to request to delete factsheet.
        Case: unsaved chagnes, user cancels delete
        """
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
#             px_app=factsheet, pm_sheets_active=sheets_active)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

        patch_dialog = patch_dialog_run(Gtk.ResponseType.CANCEL)
        monkeypatch.setattr(Gtk.Dialog, 'run', patch_dialog.run)
        target._dialog_data_loss.set_visible(True)
        monkeypatch.setattr(
            Gtk.Dialog, 'hide', lambda self: self.set_visible(False))

        sheets_active = CPOOL.PoolSheets()
        control = patch_control_safe(
            ABC_SHEET.EffectSafe.NO_EFFECT, sheets_active)
        control._model = MSHEET.Sheet()
        VSHEET.PageSheet.link_factsheet(target, control)
#         assert sheets_active._controls[id(control)] is control
        N_CALLS_SAFE = 1
        N_CALLS_FORCE = 0
        # Test
        target.on_delete_sheet(None, None)
#         assert sheets_active._controls[id(control)] is control
        assert patch_dialog.called
        assert not target._dialog_data_loss.get_visible()
        assert N_CALLS_SAFE == control.n_delete_safe
        assert N_CALLS_FORCE == control.n_delete_force
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_on_delete_sheet_discard(
            self, patch_factsheet, capfd, patch_dialog_run,
            monkeypatch, patch_control_safe):
        """Confirm response to request to delete factsheet.
        Case: unsaved changes, user approves delete
        """
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
#             px_app=factsheet, pm_sheets_active=sheets_active)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

        patch_dialog = patch_dialog_run(Gtk.ResponseType.APPLY)
        monkeypatch.setattr(Gtk.Dialog, 'run', patch_dialog.run)
        target._dialog_data_loss.set_visible(True)
        monkeypatch.setattr(
            Gtk.Dialog, 'hide', lambda self: self.set_visible(False))

        sheets_active = CPOOL.PoolSheets()
        control = patch_control_safe(
            ABC_SHEET.EffectSafe.NO_EFFECT, sheets_active)
        control._model = MSHEET.Sheet()
        VSHEET.PageSheet.link_factsheet(target, control)
#         assert sheets_active._controls[id(control)] is control
        N_CALLS_SAFE = 1
        N_CALLS_FORCE = 1
        # Test
        target.on_delete_sheet(None, None)
#         assert id(control) not in sheets_active._controls.keys()
        assert patch_dialog.called
        assert not target._dialog_data_loss.get_visible()
        assert N_CALLS_SAFE == control.n_delete_safe
        assert N_CALLS_FORCE == control.n_delete_force
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_on_new_sheet(self, monkeypatch, patch_factsheet, capfd):
        """Confirm response to request to create default factsheet."""
        # Setup
        class PatchNew:
            def __init__(self): self.called = False

            def new_factsheet(self, px_app, pm_sheets_active):
                _ = px_app
                _ = pm_sheets_active
                self.called = True

        patch_new = PatchNew()
        monkeypatch.setattr(
            VSHEET.PageSheet, 'new_factsheet', patch_new.new_factsheet)

        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
#             px_app=factsheet, pm_sheets_active=sheets_active)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.Sheet(sheets_active)
        target._control = control
        # Test
        target.on_new_sheet(None, None)
        assert patch_new.called
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_on_open_page(self, patch_factsheet, capfd):
        """Confirm response to request to open new view."""
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
#             px_app=factsheet, pm_sheets_active=sheets_active)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.Sheet.new(sheets_active)
        target._control = control
        # Test
        target.on_open_page(None, None)
        assert 1 == control._model.n_pages()
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_on_open_sheet_apply(self, tmp_path, patch_dialog_choose,
                                 monkeypatch, patch_factsheet, capfd):
        """Confirm open from file.
        Case: apply open
        """
        # Setup
        PATH = Path(tmp_path / 'factsheet.fsg')
        patch_dialog = patch_dialog_choose(
            Gtk.ResponseType.APPLY, str(PATH))
        monkeypatch.setattr(
            Gtk.FileChooserDialog, 'get_filename', patch_dialog.get_filename)
        monkeypatch.setattr(
            Gtk.FileChooserDialog, 'hide', patch_dialog.hide)
        monkeypatch.setattr(
            Gtk.FileChooserDialog, 'run', patch_dialog.run)

        class PatchPageSheet:
            def __init__(self):
                self.called = False
                self.app = None
                self.path = None

            def open_factsheet(self, p_app, p_pool, p_path):
                self.called = True
                self.app = p_app
                self.path = p_path
                return CSHEET.Sheet(p_pool)

        patch_page = PatchPageSheet()
        monkeypatch.setattr(
            VSHEET.PageSheet, 'open_factsheet', patch_page.open_factsheet)

        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
#             px_app=factsheet, pm_sheets_active=sheets_active)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.Sheet(sheets_active)
        target._control = control
        # Test
        target.on_open_sheet(None, None)
        assert patch_dialog.called_run
        assert patch_dialog.called_hide
        assert patch_page.called
        assert factsheet == patch_page.app
        assert PATH == patch_page.path
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_on_open_sheet_cancel(self, tmp_path, patch_dialog_choose,
                                  monkeypatch, patch_factsheet, capfd):
        """Confirm open from file.
        Case: cancel open
        """
        # Setup
        PATH = Path(tmp_path / 'factsheet.fsg')
        patch_dialog = patch_dialog_choose(
            Gtk.ResponseType.CANCEL, str(PATH))
        monkeypatch.setattr(
            Gtk.FileChooserDialog, 'hide', patch_dialog.hide)
        monkeypatch.setattr(
            Gtk.FileChooserDialog, 'run', patch_dialog.run)

        class PatchPageSheet:
            def __init__(self):
                self.called = False
                self.app = None
                self.path = None

            def open_factsheet(self, p_app, p_path):
                self.called = True
                self.app = p_app
                self.path = p_path
                return CSHEET.Sheet()

        patch_page = PatchPageSheet()
        monkeypatch.setattr(
            VSHEET.PageSheet, 'open_factsheet', patch_page.open_factsheet)

        factsheet = patch_factsheet()
#         sheets_active = CPOOL.PoolSheets()
        target = VSHEET.PageSheet(px_app=factsheet)
#             px_app=factsheet, pm_sheets_active=sheets_active)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        # Test
        target.on_open_sheet(None, None)
        assert patch_dialog.called_run
        assert patch_dialog.called_hide
        assert not patch_page.called
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_on_save_sheet(self, patch_factsheet, capfd, tmp_path):
        """Confirm save to file.
        Case: file path defined
        """
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
#             px_app=factsheet, pm_sheets_active=sheets_active)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

        PATH = Path(tmp_path / 'saved_factsheet.fsg')
        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.Sheet.new(sheets_active)
        control._path = PATH
        assert not control._path.exists()
        target._control = control
        # Test
        target.on_save_sheet(None, None)
        assert control._path.exists()
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_on_save_sheet_none(self, monkeypatch, patch_factsheet, capfd):
        """Confirm save to file.
        Case: file path undefined
        """
        # Setup
        class PatchSaveAs:
            def __init__(self): self.called = False

            def on_save_as_sheet(self, *_a): self.called = True

        patch_save_as = PatchSaveAs()
        monkeypatch.setattr(VSHEET.PageSheet, 'on_save_as_sheet',
                            patch_save_as.on_save_as_sheet)

        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
#             px_app=factsheet, pm_sheets_active=sheets_active)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.Sheet.new(sheets_active)
        control._path = None
        target._control = control
        # Test
        target.on_save_sheet(None, None)
        assert patch_save_as.called
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_on_save_as_sheet_apply(self, tmp_path, patch_dialog_choose,
                                    monkeypatch, patch_factsheet, capfd):
        """Confirm save to file with path set.
        Case: apply save
        """
        # Setup
        PATH_NEW = Path(tmp_path / 'new_factsheet.fsg')
        patch_dialog = patch_dialog_choose(
            Gtk.ResponseType.APPLY, str(PATH_NEW))
        monkeypatch.setattr(
            Gtk.FileChooserDialog, 'hide', patch_dialog.hide)
        monkeypatch.setattr(
            Gtk.FileChooserDialog, 'get_filename', patch_dialog.get_filename)
        monkeypatch.setattr(
            Gtk.FileChooserDialog, 'run', patch_dialog.run)
        monkeypatch.setattr(
            Gtk.FileChooserDialog, 'set_current_name',
            patch_dialog.set_current_name)
        monkeypatch.setattr(Gtk.FileChooserDialog, 'set_filename',
                            patch_dialog.set_filename)

        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
#             px_app=factsheet, pm_sheets_active=sheets_active)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

        PATH_OLD = Path(tmp_path / 'old_factsheet.fsg')
        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.Sheet.new(sheets_active)
        control._path = PATH_OLD
        target._control = control
        # Test
        target.on_save_as_sheet(None, None)
        assert patch_dialog.called_set_filename
        assert not patch_dialog.called_set_current_name
        assert patch_dialog.called_run
        assert patch_dialog.called_hide
        assert patch_dialog.called_get_filename
        assert PATH_NEW == target._control.path
        assert control._path.exists()
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_on_save_as_sheet_cancel(self, tmp_path, patch_dialog_choose,
                                     monkeypatch, patch_factsheet, capfd):
        """Confirm save to file with path set.
        Case: cancel save
        """
        # Setup
        PATH = Path(tmp_path / 'save_as_factsheet.fsg')
        patch_dialog = patch_dialog_choose(
            Gtk.ResponseType.CANCEL, str(PATH))
        monkeypatch.setattr(
            Gtk.FileChooserDialog, 'hide', patch_dialog.hide)
        monkeypatch.setattr(
            Gtk.FileChooserDialog, 'get_filename', patch_dialog.get_filename)
        monkeypatch.setattr(
            Gtk.FileChooserDialog, 'run', patch_dialog.run)
        monkeypatch.setattr(
            Gtk.FileChooserDialog, 'set_current_name',
            patch_dialog.set_current_name)
        monkeypatch.setattr(Gtk.FileChooserDialog, 'set_filename',
                            patch_dialog.set_filename)

        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
#             px_app=factsheet, pm_sheets_active=sheets_active)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.Sheet.new(sheets_active)
        control._path = None
        target._control = control
        # Test
        target.on_save_as_sheet(None, None)
        assert not patch_dialog.called_set_filename
        assert patch_dialog.called_set_current_name
        assert patch_dialog.called_run
        assert patch_dialog.called_hide
        assert not patch_dialog.called_get_filename
        assert target._control.path is None
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_on_show_dialog(self, patch_factsheet, capfd, monkeypatch):
        """Confirm handler runs dialog.

        See manual tests for dialog content checks.
        """
        # Setup
        factsheet = patch_factsheet()
#         sheets_active = CPOOL.PoolSheets()
        target = VSHEET.PageSheet(px_app=factsheet)
#             px_app=factsheet, pm_sheets_active=sheets_active)
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
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_open_factsheet(
            self, monkeypatch, patch_factsheet, capfd, tmp_path):
        """Confirm factsheet creation from file."""
        # Setup
        def patch_open(p_pool, p_path):
            sheets_active = CPOOL.PoolSheets()
            control = CSHEET.Sheet(sheets_active)
            control._model = MSHEET.Sheet()
            control._path = p_path
            control._sheets_active = p_pool
            return control

#         def patch_attach_page(self, pm_view):
#             self.test_view = pm_view

        monkeypatch.setattr(CSHEET.Sheet, 'open', patch_open)
#         monkeypatch.setattr(CSHEET.Sheet, 'attach_page', patch_attach_page)
        factsheet = patch_factsheet()

#         source = VSHEET.PageSheet(
#             px_app=factsheet, pm_sheets_active=sheets_active)
#         snapshot = capfd.readouterr()   # Resets the internal buffer
#         assert not snapshot.out
#         assert 'Gtk-CRITICAL' in snapshot.err
#         assert 'GApplication::startup signal' in snapshot.err
        PATH = Path(tmp_path / 'factsheet.fsg')
        sheets_active = CPOOL.PoolSheets()
        # Test
        target = VSHEET.PageSheet.open_factsheet(
            factsheet, sheets_active, PATH)
#             factsheet, sheets_active, PATH)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

        assert isinstance(target, VSHEET.PageSheet)
        assert target._window.get_application() is factsheet
        control = target._control
        assert isinstance(control, CSHEET.Sheet)
#         assert sheets_active._controls[id(control)] is control
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    @pytest.mark.skip(reason='Pending implementation')
    def test_update_name(self):
        """Confirm window title update."""
        # Setup
        # Test
        # Teardown
#         target._window.destroy()
#         del target._window
#         del factsheet
