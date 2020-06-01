"""
Unit tests for class to display Factsheet document.

See :mod:`.page_sheet`.
"""
from pathlib import Path
import pytest   # type: ignore[import]

from factsheet.abc_types import abc_outline as ABC_OUTLINE
from factsheet.abc_types import abc_sheet as ABC_SHEET
from factsheet.adapt_gtk import adapt_outline as AOUTLINE
from factsheet.adapt_gtk import adapt_sheet as ASHEET
from factsheet.content.outline import template as XSECTION
from factsheet.content.outline import topic as XTOPIC
from factsheet.control import pool as CPOOL
from factsheet.control import sheet as CSHEET
from factsheet.model import sheet as MSHEET
from factsheet.view import query_place as QPLACE
from factsheet.view import query_template as QTEMPLATE
from factsheet.view import page_sheet as VSHEET
from factsheet.view import ui as UI
from factsheet.view import view_infoid as VINFOID

import gi   # type: ignore[import]
gi.require_version('Gtk', '3.0')
from gi.repository import Gdk   # type: ignore[import]    # noqa: E402
from gi.repository import GObject as GO  # type: ignore[import] # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class PatchCall:
    def __init__(self, p_response):
        self.response = p_response
        self.called = False

    def __call__(self):
        self.called = True
        return self.response


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


@pytest.fixture
def patch_dialog_choose():
    """Pytest fixture returns stub
    `GtkFileChooserDialog <GtkFileChooserDialog_>`_.

    .. _GtkFileChooserDialog: https://lazka.github.io/pgi-docs/
       #Gtk-3.0/classes/FileChooserDialog.html
    """
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


class TestPageSheet:
    """Unit tests for :class:`.PageSheet`."""

    def test_init(self, patch_factsheet, capfd):
        """Confirm initialization.
        Case: visual elements.
        """
        # Setup
        factsheet = patch_factsheet()
        # Test
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

        assert target._control is None
        assert isinstance(target._window, Gtk.ApplicationWindow)
        assert target._window.get_application() is factsheet

        # Components
        assert isinstance(target._context_name, Gtk.Popover)
        assert isinstance(target._context_summary, Gtk.Frame)
        assert isinstance(target._flip_summary, Gtk.CheckButton)
        assert isinstance(
            target._view_topics, ABC_OUTLINE.AbstractViewOutline)
        assert target._view_topics._search is ~ASHEET.FieldsTopic.VOID
        assert isinstance(target._cursor_topics, Gtk.TreeSelection)
        assert target._view_topics.gtk_view.get_parent() is not None
        assert isinstance(target._dialog_data_loss, Gtk.Dialog)
        assert target._query_place is None
        assert isinstance(target._query_template, QTEMPLATE.QueryTemplate)
        assert target._name_former is None
        assert isinstance(target._warning_data_loss, Gtk.Label)

        # Identification Information
        assert isinstance(target._infoid, VINFOID.ViewInfoId)
        assert target._infoid.name is not None
        assert target._infoid.summary is not None
        assert target._infoid.title is not None

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
        assert target._window.lookup_action('popup-name') is not None
        assert target._window.lookup_action('reset-name') is not None
        assert target._window.lookup_action('flip-summary') is not None
        assert target._window.lookup_action('open-page-sheet') is not None
        assert target._window.lookup_action('close-page-sheet') is not None
        assert target._window.lookup_action(
            'show-help-sheet-display') is not None

        # Factsheet File Menu
        assert target._window.lookup_action('delete-sheet') is not None
        assert target._window.lookup_action(
            'show-help-sheet-file') is not None

        # Topics Outline Toolbar and Menu
        assert target._view_topics.gtk_view.get_search_entry() is not None
        assert target._window.lookup_action('new-topic') is not None
        assert target._window.lookup_action('delete-topic') is not None
        assert target._window.lookup_action('show-help-topics') is not None

        assert not target._close_window
        assert target._window.is_visible()
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    @pytest.mark.parametrize(
        'name_signal, name_attribute, origin, n_default', [
            ('closed', '_context_name', Gtk.Popover, 0),
            ('delete-event', '_window', Gtk.ApplicationWindow, 0),
            ])
    def test_init_signals(self, name_signal, name_attribute, origin,
                          n_default, patch_factsheet, capfd):
        """Confirm initialization of signal connections."""
        # Setup
        origin_gtype = GO.type_from_name(GO.type_name(origin))
        signal = GO.signal_lookup(name_signal, origin_gtype)
        factsheet = patch_factsheet()
        # Test
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

        attribute = getattr(target, name_attribute)
        n_handlers = 0
        while True:
            id_signal = GO.signal_handler_find(
                attribute, GO.SignalMatchType.ID, signal,
                0, None, None, None)
            if 0 == id_signal:
                break

            n_handlers += 1
            GO.signal_handler_disconnect(attribute, id_signal)

        assert n_default + 1 == n_handlers
        # Cleanup
        target._window.destroy()
        del target._window
        del factsheet

    def test_init_activate(self, patch_factsheet, capfd):
        """Confirm initialization of name view activation signal."""
        # Setup
        factsheet = patch_factsheet()
        entry_gtype = GO.type_from_name(GO.type_name(Gtk.Entry))
        delete_signal = GO.signal_lookup('activate', entry_gtype)
        # Test
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

        entry = target._infoid.get_view_name()
        activate_id = GO.signal_handler_find(
            entry, GO.SignalMatchType.ID, delete_signal,
            0, None, None, None)
        assert 0 != activate_id
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
        target = VSHEET.PageSheet(px_app=factsheet)
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
        target = VSHEET.PageSheet(px_app=factsheet)
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

    def test_get_view_topics(self, patch_factsheet, capfd):
        """Confirm returns view of topics outline."""
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        # Test
        assert target._view_topics is target.get_view_topics()
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_link_factsheet(self, patch_factsheet, capfd):
        """Confirm creation of factsheet links."""
        # Setup
        factsheet = patch_factsheet()
        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.Sheet.new(sheets_active)
        page = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        # Test
        VSHEET.PageSheet.link_factsheet(page, control)
        assert page._control is control
        model = page._view_topics.gtk_view.get_model()
        assert model is not None
        assert page._query_place is not None
        query_view_topics = page._query_place._outline
        assert query_view_topics.gtk_view.get_model() is model
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
        source = VSHEET.PageSheet(px_app=factsheet)
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
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_on_close_page_force(self, patch_factsheet, capfd):
        """| Confirm response to request to close page.
        | Case: unconditional close.
        """
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

        sheets_active = CPOOL.PoolSheets()
        control = PatchSafe(ABC_SHEET.EffectSafe.COMPLETED, sheets_active)
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

    def test_on_close_page_safe(self, patch_factsheet, capfd):
        """| Confirm response to request to close page.
        | Case: safe to close.
        """
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

        sheets_active = CPOOL.PoolSheets()
        control = PatchSafe(ABC_SHEET.EffectSafe.COMPLETED, sheets_active)
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
            self, patch_factsheet, capfd, monkeypatch):
        """| Confirm response to request to close page.
        | Case: not safe to close, user cancels close.
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
        target._dialog_data_loss.set_visible(True)
        monkeypatch.setattr(
            Gtk.Dialog, 'hide', lambda self: self.set_visible(False))

        sheets_active = CPOOL.PoolSheets()
        control = PatchSafe(ABC_SHEET.EffectSafe.NO_EFFECT, sheets_active)
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
            self, patch_factsheet, capfd, monkeypatch):
        """| Confirm response to request to close page.
        | Case: not safe to close, user approves close.
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
        target._dialog_data_loss.set_visible(True)
        monkeypatch.setattr(
            Gtk.Dialog, 'hide', lambda self: self.set_visible(False))

        sheets_active = CPOOL.PoolSheets()
        control = PatchSafe(ABC_SHEET.EffectSafe.NO_EFFECT, sheets_active)
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
            self, patch_factsheet, capfd, patch_dialog_run, monkeypatch):
        """| Confirm response to request to delete factsheet.
        | Case: no unsaved changes.
        """
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

        patch_dialog = patch_dialog_run(Gtk.ResponseType.CANCEL)
        monkeypatch.setattr(Gtk.Dialog, 'run', patch_dialog.run)

        sheets_active = CPOOL.PoolSheets()
        control = PatchSafe(ABC_SHEET.EffectSafe.COMPLETED, sheets_active)
        control._model = MSHEET.Sheet()
        VSHEET.PageSheet.link_factsheet(target, control)
        N_CALLS_SAFE = 1
        N_CALLS_FORCE = 0
        # Test
        target.on_delete_sheet(None, None)
        assert not patch_dialog.called
        assert N_CALLS_SAFE == control.n_delete_safe
        assert N_CALLS_FORCE == control.n_delete_force
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_on_delete_sheet_cancel(
            self, patch_factsheet, capfd, patch_dialog_run, monkeypatch):
        """| Confirm response to request to delete factsheet.
        | Case: unsaved chagnes, user cancels delete.
        """
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
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
        control = PatchSafe(ABC_SHEET.EffectSafe.NO_EFFECT, sheets_active)
        control._model = MSHEET.Sheet()
        VSHEET.PageSheet.link_factsheet(target, control)
        N_CALLS_SAFE = 1
        N_CALLS_FORCE = 0
        # Test
        target.on_delete_sheet(None, None)
        assert patch_dialog.called
        assert not target._dialog_data_loss.get_visible()
        assert N_CALLS_SAFE == control.n_delete_safe
        assert N_CALLS_FORCE == control.n_delete_force
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_on_delete_sheet_discard(
            self, patch_factsheet, capfd, patch_dialog_run, monkeypatch):
        """| Confirm response to request to delete factsheet.
        | Case: unsaved changes, user approves delete.
        """
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
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
        control = PatchSafe(ABC_SHEET.EffectSafe.NO_EFFECT, sheets_active)
        control._model = MSHEET.Sheet()
        VSHEET.PageSheet.link_factsheet(target, control)
        N_CALLS_SAFE = 1
        N_CALLS_FORCE = 1
        # Test
        target.on_delete_sheet(None, None)
        assert patch_dialog.called
        assert not target._dialog_data_loss.get_visible()
        assert N_CALLS_SAFE == control.n_delete_safe
        assert N_CALLS_FORCE == control.n_delete_force
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    @pytest.mark.skip(reason='add guard against index of None')
    def test_on_delete_topic(self, monkeypatch, patch_factsheet, capfd):
        # Setup
        class PatchExtract:
            def __init__(self): self.called = False

            def extract_topic(self, _index): self.called = True

        patch_extract = PatchExtract()
        monkeypatch.setattr(
            CSHEET.Sheet, 'extract_topic', patch_extract.extract_topic)
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.Sheet(sheets_active)
        target._control = control
        # Test
        target.on_delete_topic(None, None)
        assert patch_extract.called

    def test_on_flip_summary(self, patch_factsheet, capfd):
        """Confirm flip of facthseet summary visibility.

        #. Case: hide
        #. Case: show
        """
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

        target._context_summary.set_visible(True)
        assert target._context_summary.get_visible()
        assert target._flip_summary.get_active()
        # Test: hide
        # Call clicked to invoke target.on_flip_summary.  Method clicked
        # has the side effect of setting active state of _flip_summary.
        target._flip_summary.clicked()
        assert not target._context_summary.get_visible()
        assert not target._flip_summary.get_active()
        # Test: show
        # As in case hide.
        target._flip_summary.clicked()
        assert target._context_summary.get_visible()
        assert target._flip_summary.get_active()

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

    def test_on_new_topic(self, patch_factsheet, capfd, monkeypatch):
        """| Confirm response to request to specify topic.
        | Case: user completes placement, template selection, and topic
          specification.
        """
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.Sheet.new(sheets_active)
        target.link_factsheet(target, control)
        gtk_model = target._view_topics.gtk_view.get_model()
        _index = gtk_model.append(None)

        placement = QPLACE.Placement(None, QPLACE.Order.CHILD)
        patch_place = PatchCall(placement)
        monkeypatch.setattr(
            QPLACE.QueryPlace, '__call__', patch_place.__call__)

        query_template = target._query_template
        outline = query_template._outline
        model = outline.gtk_view.get_model()
        i_first = model.get_iter_first()
        template = AOUTLINE.get_item_gtk(model, i_first)
        patch_query_template = PatchCall(template)
        monkeypatch.setattr(QTEMPLATE.QueryTemplate, '__call__',
                            patch_query_template.__call__)

        NAME = 'Parrot'
        SUMMARY = 'A sketch about customer service.'
        TITLE = 'Dead Parrot Sketch'
        topic = XTOPIC.Topic(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
        patch_template = PatchCall(topic)
        monkeypatch.setattr(
            XSECTION.Section, '__call__', patch_template.__call__)

        class PatchInsert:
            def __init__(self): self.called = False

            def insert_topic_child(self, _t, _a): self.called = True

        patch_insert = PatchInsert()
        monkeypatch.setattr(CSHEET.Sheet, 'insert_topic_child',
                            patch_insert.insert_topic_child)
        # Test
        target.on_new_topic(None, None)
        assert patch_place.called
        assert patch_query_template.called
        assert patch_template.called
        assert patch_insert.called

    def test_on_new_topic_cancel_place(
            self, patch_factsheet, capfd, monkeypatch):
        """| Confirm response to request to specify topic.
        | Case: user cancels placement.
        """
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.Sheet.new(sheets_active)
        target.link_factsheet(target, control)
        gtk_model = target._view_topics.gtk_view.get_model()
        _index = gtk_model.append(None)

        patch_place = PatchCall(None)
        monkeypatch.setattr(
            QPLACE.QueryPlace, '__call__', patch_place.__call__)

        patch_query_template = PatchCall(None)
        monkeypatch.setattr(QTEMPLATE.QueryTemplate, '__call__',
                            patch_query_template.__call__)

        class PatchInsert:
            def __init__(self): self.called = False

            def insert_topic_child(self, _t, _a): self.called = True

        patch_insert = PatchInsert()
        monkeypatch.setattr(CSHEET.Sheet, 'insert_topic_child',
                            patch_insert.insert_topic_child)
        # Test
        target.on_new_topic(None, None)
        assert not patch_query_template.called

    def test_on_new_topic_cancel_template(
            self, patch_factsheet, capfd, monkeypatch):
        """| Confirm response to request to specify topic.
        | Case: user cancels template selection.
        """
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.Sheet.new(sheets_active)
        target.link_factsheet(target, control)

        patch_query_template = PatchCall(None)
        monkeypatch.setattr(QTEMPLATE.QueryTemplate, '__call__',
                            patch_query_template.__call__)
        # Test
        target.on_new_topic(None, None)
        # Return from call shows guard against template = None

    def test_on_new_topic_cancel_topic(
            self, patch_factsheet, capfd, monkeypatch):
        """| Confirm response to request to specify topic.
        | Case: user cancels topic specification.
        """
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.Sheet.new(sheets_active)
        target.link_factsheet(target, control)

        query_template = target._query_template
        outline = query_template._outline
        model = outline.gtk_view.get_model()
        i_first = model.get_iter_first()
        template = AOUTLINE.get_item_gtk(model, i_first)

        patch_query_template = PatchCall(template)
        monkeypatch.setattr(QTEMPLATE.QueryTemplate, '__call__',
                            patch_query_template.__call__)

        patch_template = PatchCall(None)
        monkeypatch.setattr(
            XSECTION.Section, '__call__', patch_template.__call__)

        class PatchInsert:
            def __init__(self): self.called = False

            def insert_topic_child(self, _t, _a): self.called = True

        patch_insert = PatchInsert()
        monkeypatch.setattr(CSHEET.Sheet, 'insert_topic_child',
                            patch_insert.insert_topic_child)
        # Test
        target.on_new_topic(None, None)
        assert not patch_insert.called

    def test_on_open_page(self, patch_factsheet, capfd):
        """Confirm response to request to open new view."""
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
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
        Case: apply open.
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
        Case: cancel open.
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
        target = VSHEET.PageSheet(px_app=factsheet)
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

    def test_on_popdown_name(self, monkeypatch, patch_factsheet, capfd):
        """Confirm name popover becomes invisible.
        Case: name changed.
        """
        # Setup
        class PatchNewName:
            def __init__(self): self.called = False

            def new_name(self): self.called = True

        patch_new_name = PatchNewName()
        monkeypatch.setattr(
            CSHEET.Sheet, 'new_name', patch_new_name.new_name)

        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.Sheet.new(sheets_active)
        target._control = control
        target._infoid.get_view_name().set_text('The Confy Chair!')
        target._name_former = target._infoid.name + ' Oh no!'
        # Test
        target.on_popdown_name(None)
        assert target._name_former is None
        assert patch_new_name.called
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_on_popdown_name_static(
            self, monkeypatch, patch_factsheet, capfd):
        """Confirm name popover becomes invisible.
        Case: name did not change.
        """
        # Setup
        class PatchNewName:
            def __init__(self): self.called = False

            def new_name(self): self.called = True

        patch_new_name = PatchNewName()
        monkeypatch.setattr(
            CSHEET.Sheet, 'new_name', patch_new_name.new_name)

        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.Sheet.new(sheets_active)
        target._control = control
        target._infoid.get_view_name().set_text('The Confy Chair!')
        target._name_former = target._infoid.name
        # Test
        target.on_popdown_name(None)
        assert target._name_former is None
        assert not patch_new_name.called
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_on_popup_name(self, patch_factsheet, capfd):
        """Confirm name popover becomes visible."""
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

        target._context_name.set_visible(False)
        target._infoid.get_view_name().set_text('The Confy Chair!')
        # Test
        target.on_popup_name(None, None)
        assert target._context_name.get_visible()
        assert target._infoid.name == target._name_former
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_on_reset_name(self, patch_factsheet, capfd):
        """Confirm name reset."""
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

        name = target._infoid.get_view_name()
        name.set_text('The Spanish Inquisition!')
        target._name_former = 'Oh no!'
        # Test
        target.on_reset_name(None, None)
        assert target._name_former == name.get_text()
        # Target
        target._window.destroy()
        del target._window
        del factsheet

    def test_on_save_sheet(self, patch_factsheet, capfd, tmp_path):
        """Confirm save to file.
        Case: file path defined.
        """
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
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
        Case: file path undefined.
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
        Case: apply save.
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
        Case: cancel save.
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
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        target._window.hide()

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
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_on_toggle_search_field_inactive(self, patch_factsheet, capfd):
        """| Confirm search field set.
        | Case: button inactive.
        """
        # Setup
        factsheet = patch_factsheet()
        target_page = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

        target = target_page._view_topics
        SEARCH_ALL = ~ASHEET.FieldsTopic.VOID
        target._search = SEARCH_ALL
        button = Gtk.ToggleButton(active=False)
        # Test
        target_page.on_toggle_search_field(button, ASHEET.FieldsTopic.NAME)
        assert not target._search & ASHEET.FieldsTopic.NAME
        assert target._search & ASHEET.FieldsTopic.TITLE
        # Teardown
        target_page._window.destroy()
        del target_page._window
        del factsheet

    def test_on_toggle_search_field_active(self, patch_factsheet, capfd):
        """| Confirm search field set.
        | Case: button inactive.
        """
        # Setup
        factsheet = patch_factsheet()
        target_page = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

        target = target_page._view_topics
        SEARCH_NONE = ASHEET.FieldsTopic.VOID
        target._search = SEARCH_NONE
        button = Gtk.ToggleButton(active=True)
        # Test - not active
        target_page.on_toggle_search_field(button, ASHEET.FieldsTopic.TITLE)
        assert target._search & ASHEET.FieldsTopic.TITLE
        assert not target._search & ASHEET.FieldsTopic.NAME
        # Teardown
        target_page._window.destroy()
        del target_page._window
        del factsheet

    def test_open_factsheet(
            self, monkeypatch, patch_factsheet, capfd, tmp_path):
        """Confirm factsheet creation from file.
        Case: factsheet is not open.
        """
        # Setup
        def patch_open(p_pool, p_path):
            sheets_active = CPOOL.PoolSheets()
            control = CSHEET.Sheet(sheets_active)
            control._model = MSHEET.Sheet()
            control._path = p_path
            control._sheets_active = p_pool
            return control

        monkeypatch.setattr(CSHEET.Sheet, 'open', patch_open)
        factsheet = patch_factsheet()

        PATH = Path(tmp_path / 'factsheet.fsg')
        sheets_active = CPOOL.PoolSheets()
        # Test
        target = VSHEET.PageSheet.open_factsheet(
            factsheet, sheets_active, PATH)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

        assert isinstance(target, VSHEET.PageSheet)
        assert target._window.get_application() is factsheet
        control = target._control
        assert isinstance(control, CSHEET.Sheet)
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_open_factsheet_active(
            self, monkeypatch, patch_factsheet, capfd, tmp_path):
        """Confirm factsheet creation from file.
        Case: factsheet is open.
        """
        # Setup
        class PatchPresentFactsheet:
            def __init__(self): self.called = False

            def present_factsheet(self, _time): self.called = True

        patch_present = PatchPresentFactsheet()
        monkeypatch.setattr(CSHEET.Sheet, 'present_factsheet',
                            patch_present.present_factsheet)

        PATH_MISS = Path(tmp_path / 'miss.fsg')
        PATH_NONE = None
        PATH_HIT = Path(tmp_path / 'hit.fsg')
        paths = [PATH_MISS, PATH_NONE, PATH_HIT]

        sheets_active = CPOOL.PoolSheets()
        for path in paths:
            control = CSHEET.Sheet.new(sheets_active)
            control._path = path

        factsheet = patch_factsheet()
        # Test
        target = VSHEET.PageSheet.open_factsheet(
            factsheet, sheets_active, PATH_HIT)
        assert target is None
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert not snapshot.err
        assert patch_present.called

    def test_present(self, patch_factsheet, capfd):
        """Confirm page becomes visible."""
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.Sheet.new(sheets_active)
        target._control = control
        target._window.hide()
        # Test
        target.present(Gdk.CURRENT_TIME)
        assert target._window.get_visible()
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_set_title(self, patch_factsheet, capfd):
        """Confirm window title update."""
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err

        TITLE = 'The Larch'
        entry_name = target._infoid.get_view_name()
        entry_name.set_text(TITLE)
        SUBTITLE = 'larch.fsg (ABE:123)'
        # Test
        target.set_titles(SUBTITLE)
        headerbar = target._window.get_titlebar()
        assert TITLE == headerbar.get_title()
        assert SUBTITLE == headerbar.get_subtitle()
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet
