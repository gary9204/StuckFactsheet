"""
Unit tests for class to display Factsheet document.  See
:mod:`.view_sheet`.

.. include:: /test/refs_include_pytest.txt
"""
import logging
# import math
# from pathlib import Path
import pytest   # type: ignore[import]

# from factsheet.abc_types import abc_outline as ABC_OUTLINE
# from factsheet.abc_types import abc_sheet as ABC_SHEET
# from factsheet.adapt_gtk import adapt_outline as AOUTLINE
# from factsheet.adapt_gtk import adapt_sheet as ASHEET
# from factsheet.content.note import spec_note as XSPEC_NOTE
# from factsheet.control import pool as CPOOL
import factsheet.control.control_sheet as CSHEET
# import factsheet.model.sheet as MSHEET
import factsheet.model.sheet as MSHEET
# from factsheet.model import topic as MTOPIC
# from factsheet.view import query_place as QPLACE
# from factsheet.view import query_template as QTEMPLATE
# import factsheet.view.view_idcore as VIDCORE
import factsheet.view.view_sheet as VSHEET
# from factsheet.view import scenes as VSCENES
# from factsheet.view import form_topic as VTOPIC
# from factsheet.view import types_view as VTYPES
# from factsheet.view import ui as UI
# from factsheet.view import view_infoid as VINFOID

import gi   # type: ignore[import]
gi.require_version('Gtk', '3.0')
# from gi.repository import Gdk   # type: ignore[import]    # noqa: E402
from gi.repository import GObject as GO  # type: ignore[import] # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402
# from gi.repository import Pango  # type: ignore[import]    # noqa: E402


# class PatchCall:
#     def __init__(self, p_response):
#         self.response = p_response
#         self.called = False
#
#     def __call__(self):
#         self.called = True
#         return self.response


@pytest.fixture
def gtk_app_window():
    """Fixture with teardown: return `GTK.ApplicationWindow <gtk_app_window_>`_.

    .. _gtk_app_window: https://lazka.github.io/pgi-docs/
       #Gtk-3.0/classes/ApplicationWindow.html#Gtk.ApplicationWindow
    """
    gtk_window = Gtk.ApplicationWindow()
    yield gtk_window
    gtk_window.destroy()


class PatchSetApp:
    """Basis for patches of
    `Gtk.ApplicationWindow.set_application <set_application_>`_ locally.

    .. _set_application: https://lazka.github.io/pgi-docs/
       #Gtk-3.0/classes/Window.html#Gtk.Window.set_application
    """
    def __init__(self):
        """Initially, mark patch as not called."""
        self.called = False
        self.apps = []

    def set_application(self, p_app):
        """Mark patch as called and record application argument."""
        self.called = True
        self.apps.append(p_app)


@pytest.fixture(autouse=True)
def patch_set_app(monkeypatch):
    patch = PatchSetApp()
    monkeypatch.setattr(
        Gtk.Window, 'set_application', patch.set_application)
    return patch


@pytest.fixture
def patch_is_stale(monkeypatch, request):
    """Pytest fixture: patch :meth:`.Sheet.is_stale` to return mark value."""
    class PatchIsStale:
        def __init__(self, p_is_stale):
            self.called = False
            self._is_stale = p_is_stale

        def is_stale(self):
            self.called = True
            return self._is_stale

    marker = request.node.get_closest_marker("is_stale")
    is_stale = False
    if marker is not None:
        try:
            is_stale = marker.kwargs['is_stale']
        except KeyError:
            pass

    patch = PatchIsStale(p_is_stale=is_stale)
    monkeypatch.setattr(MSHEET.Sheet, 'is_stale', patch.is_stale)
    return patch


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


@pytest.fixture(autouse=True)
def patch_g_control_app():
    """Pytest fixture with teardown: Reset :data:`.g_control_app`."""
    CSHEET.g_control_app = CSHEET.ControlApp()
    yield CSHEET.g_control_app
    control_app = CSHEET.g_control_app
    for sheet in control_app._roster_sheets.values():
        for view in sheet._roster_views.values():
            view._window.destroy()
        sheet._roster_views.clear()
    control_app._roster_sheets.clear()
    CSHEET.g_control_app = CSHEET.ControlApp()


class TestAppFactsheet:
    """Unit tests for :class:`~.view_sheet.AppFactsheet`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        app_id = 'com.novafolks.factsheet'
        # Test
        target = VSHEET.AppFactsheet()
        assert isinstance(target, Gtk.Application)
        assert app_id == target.get_application_id()
        assert not target.get_windows()

    def test_do_activate(self, monkeypatch):
        """| Confirm activation with initial window.
        | Case: activation succeeds

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        class PatchOnNew:
            def __init__(self): self.called = False

            def on_new_sheet(self, _a, _t): self.called = True

        patch_on_new = PatchOnNew()
        monkeypatch.setattr(
            VSHEET.ViewSheet, 'on_new_sheet', patch_on_new.on_new_sheet)
        target = VSHEET.AppFactsheet()
        # Test
        target.do_activate()
        assert patch_on_new.called

    def test_do_open(self):
        """| Confirm factsheet open with initial window.
        | Case: open succeeds
        """
        # Setup
        # Test
        pytest.xfail(reason='Pending implementation of file open')

    def test_do_open_warn(self):
        """| Confirm factsheet open with initial window.
        | Case: open fails
        """
        # Setup
        # Test
        pytest.xfail(reason='Pending implementation of file open')

    def test_do_shutdown(self, monkeypatch, caplog):
        """Confirm application teardown.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param caplog: built-in fixture `Pytest caplog`_.
        """
        # Setup
        # Bare call to superclass do_shutdown causes segmentation fault
        class PatchAppDoShutdown:
            def __init__(self): self.called = False

            def do_shutdown(self, _app): self.called = True

        patch = PatchAppDoShutdown()
        monkeypatch.setattr(
            Gtk.Application, 'do_shutdown', patch.do_shutdown)

        caplog.set_level(logging.INFO)
        N_LOGS = 1
        LAST = -1
        log_message = 'AppFactsheet application shutdown.'
        target = VSHEET.AppFactsheet()
        # Test
        target.do_shutdown()
        assert patch.called
        assert N_LOGS == len(caplog.records)
        record = caplog.records[LAST]
        assert log_message == record.message
        assert 'INFO' == record.levelname

    def test_do_startup(self, monkeypatch, caplog):
        """Confirm application setup.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param caplog: built-in fixture `Pytest caplog`_.
        """
        # Setup
        # Bare call to superclass do_startup causes segmentation fault
        class PatchAppDoStartup:
            def __init__(self): self.called = False

            def do_startup(self, _app): self.called = True

        patch = PatchAppDoStartup()
        monkeypatch.setattr(
            Gtk.Application, 'do_startup', patch.do_startup)

        caplog.set_level(logging.INFO)
        N_LOGS = 1
        LAST = -1
        log_message = 'AppFactsheet application startup.'
        target = VSHEET.AppFactsheet()
        # Test
        target.do_startup()
        assert patch.called
        assert N_LOGS == len(caplog.records)
        record = caplog.records[LAST]
        assert log_message == record.message
        assert 'INFO' == record.levelname


class TestNewDialogWarn:
    """Unit tests for :func:`.new_dialog_warn_loss`."""

    def test_new_dialog_warn(self, gtk_app_window):
        """Confirm data loss warning dialog construction.

        :param gtk_app_window: fixture :func:`.gtk_app_window`.
        """
        # Setup
        PARENT = gtk_app_window
        NAME = '<b>Parrot Sketch</b>'
        WARN = ('Factsheet {} contains unsaved changes.  All unsaved'
                ' changes will be discarded if you erase.').format(NAME)
        I_DIALOG = 0
        I_WARN = 0
        I_CANCEL = 0
        TEXT_CANCEL = 'Cancel'
        I_APPLY = 1
        TEXT_APPLY = 'Discard'
        # Test
        target = VSHEET.new_dialog_warn_loss(p_parent=PARENT, p_name=NAME)
        assert isinstance(target, Gtk.Dialog)
        assert target.get_transient_for() is PARENT
        assert target.get_destroy_with_parent()
        box_content = target.get_content_area()
        box_warn = box_content.get_children()[I_DIALOG]
        label_warn = box_warn.get_children()[I_WARN]
        assert isinstance(label_warn, Gtk.Label)
        assert WARN == label_warn.get_label()
        header_bar = target.get_header_bar()
        assert isinstance(header_bar, Gtk.HeaderBar)
        buttons = header_bar.get_children()
        button_cancel = buttons[I_CANCEL]
        assert TEXT_CANCEL == button_cancel.get_label()
        assert target.get_widget_for_response(
            Gtk.ResponseType.CANCEL) is button_cancel
        assert button_cancel.get_style_context(
            ).has_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)
        button_apply = buttons[I_APPLY]
        assert TEXT_APPLY == button_apply.get_label()
        assert target.get_widget_for_response(
            Gtk.ResponseType.APPLY) is button_apply
        assert button_apply.get_style_context(
            ).has_class(Gtk.STYLE_CLASS_DESTRUCTIVE_ACTION)


class TestUiItems:
    """Unit tests for user interface constants and shared objects."""


class TestViewSheet:
    """Unit tests for :class:`.ViewSheet`.

    The following manual tests are needed to confirm placement,
    appearance, and behavior of :class:`.ViewSheet` components.

    * :doc:`../test_manual/test_cases/case_sheet_name` for Factsheet name
    * :doc:`../test_manual/test_cases/case_sheet_open_view` for new
      Factsheet window.
    * :doc:`../test_manual/test_cases/case_sheet_summary` for Factsheet summary
    * :doc:`../test_manual/test_cases/case_sheet_title` for Factsheet title
    """

    @pytest.mark.parametrize('NAME, TYPE', [
        ('NAME_FILE_SHEET_UI', str),
        ('NAME_FILE_DIALOG_DATA_LOSS_UI', str),
        # ('CANCEL_CLOSE', bool),
        # ('CONTINUE_CLOSE', bool),
        ])
    def test_class_constants(self, NAME, TYPE):
        """Confirm class defines constants."""
        # Setup
        item = getattr(VSHEET.ViewSheet, NAME)
        assert isinstance(item, TYPE)

    def test_init(self, patch_set_app):
        # def test_init(self, patch_appfactsheet, capfd):
        """| Confirm initialization.
        | Case: visual elements.
        """
        # Setup
        patch = patch_set_app
        control = CSHEET.g_control_app.open_factsheet(p_path=None)
        # Test
        target = VSHEET.ViewSheet(p_control=control)
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)

        assert not VSHEET.ViewSheet.ALLOW_CLOSE
        assert VSHEET.ViewSheet.DENY_CLOSE
        assert target._control is control
        assert control._roster_views[CSHEET.id_view_sheet(target)] is target
        assert isinstance(target._window, Gtk.ApplicationWindow)
        assert patch.called
        assert patch.apps.pop() is VSHEET.g_app

        headerbar = target._window.get_titlebar()
        title_window = headerbar.get_custom_title()
        assert isinstance(title_window, Gtk.Label)
        title_window_str = title_window.get_label()
        assert target._control.model.name == title_window_str

        # Components
        # assert isinstance(target._context_name, Gtk.Popover)
        # assert isinstance(target._context_summary, Gtk.Expander)
        # assert isinstance(target._flip_summary, Gtk.CheckButton)
        # assert isinstance(
        #     target._view_topics, ABC_OUTLINE.AbstractViewOutline)
        # assert target._view_topics.scope_search is ~ASHEET.FieldsTopic.VOID
        # assert target._view_topics.gtk_view.get_reorderable()
        # assert target._view_topics.gtk_view.get_parent() is not None
        # assert isinstance(target._cursor_topics, Gtk.TreeSelection)
        # assert isinstance(target._scenes_topic, VSCENES.Scenes)
        # assert isinstance(target._dialog_data_loss, Gtk.Dialog)
        # assert target._query_place is None
        # assert target._query_template is None
        # assert target._name_former is None
        # assert isinstance(target._warning_data_loss, Gtk.Label)
        #
        # # Identification Information
        # assert isinstance(target._infoid, VINFOID.ViewInfoId)
        # assert target._infoid.name is not None
        # assert target._infoid.summary is not None
        # assert target._infoid.title is not None
        #
        # # Application Title
        # assert target._window.lookup_action('open-sheet') is not None
        assert target._window.lookup_action('new-sheet') is not None
        # assert target._window.lookup_action('save-sheet') is not None
        # assert target._window.lookup_action('save-as-sheet') is not None
        #
        # # Factsheet Menu
        # assert target._window.lookup_action('show-help-sheet') is not None
        #
        # # Factsheet Display Menu
        # assert target._window.lookup_action('flip-summary') is not None
        assert target._window.lookup_action('open-view-sheet') is not None
        # assert target._window.lookup_action('erase-view-sheet') is not None
        # assert target._window.lookup_action(
        #     'show-help-sheet-display') is not None
        #
        # # Factsheet File Menu
        assert target._window.lookup_action('delete-sheet') is not None
        # assert target._window.lookup_action(
        #     'show-help-sheet-file') is not None
        #
        # # Topics Outline Toolbar and Menu
        # assert target._view_topics.gtk_view.get_search_entry() is not None
        # assert target._window.lookup_action('new-topic') is not None
        # assert target._window.lookup_action('go-first-topic') is not None
        # assert target._window.lookup_action('go-last-topic') is not None
        # assert target._window.lookup_action('delete-topic') is not None
        # assert target._window.lookup_action('clear-topics') is not None
        # assert target._window.lookup_action('show-help-topics') is not None
        #
        # assert not target._close_window
        assert target._window.is_visible()

    @pytest.mark.parametrize('HELPER, EDITOR, SITE', [
        ('_init_name_sheet', 'Name', 'ui_site_name_sheet'),
        ('_init_title_sheet', 'Title', 'ui_site_title_sheet'),
        ])
    def test_init_helper_editor(self, monkeypatch, HELPER, EDITOR, SITE):
        """Confirm helper creates editor fields in view.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        class PatchGetObject:
            def __init__(self):
                self.called = False
                self.site_ui = ''

            def get_object(self, p_site_ui):
                self.called = True
                self.site_ui = p_site_ui
                return Gtk.Box()

        patch_get_object = PatchGetObject()

        class PatchEditorMarkup:
            def __init__(self):
                self.called = False
                self.view_active = 'Oops'
                self.view_passive = None
                self.text = ''

            def init(self, p_view_passive, p_view_active, p_text):
                self.called = True
                self.view_active = p_view_active
                self.view_passive = p_view_passive
                self.text = p_text

            def view_editor(self):
                pass

        patch_editor = PatchEditorMarkup()
        monkeypatch.setattr(
            VSHEET.VIDCORE.EditorMarkup, '__init__', patch_editor.init)
        monkeypatch.setattr(VSHEET.VIDCORE.EditorMarkup, 'view_editor',
                            patch_editor.view_editor)

        class PatchSite:
            def __init__(self):
                self.called = False
                self.view_editor = None
                self.expand_okay = None
                self.fill_okay = None
                self.n_padding = 0

            def pack_start(
                    self, p_editor, p_exapnd_okay, p_fill_okay, p_n_padding):
                self.called = True
                self.view_editor = p_editor
                self.expand_okay = p_exapnd_okay
                self.fill_okay = p_fill_okay
                self.n_padding = p_n_padding

        patch_site = PatchSite()
        monkeypatch.setattr(Gtk.Box, 'pack_start', patch_site.pack_start)

        EXPAND_OKAY = True
        FILL_OKAY = True
        N_PADDING = 6
        control = CSHEET.g_control_app.open_factsheet(p_path=None)
        # Test
        target = VSHEET.ViewSheet(p_control=control)
        helper = getattr(target, HELPER)
        helper(patch_get_object.get_object)
        assert patch_editor.called
        assert isinstance(patch_editor.view_active, Gtk.Entry)
        assert isinstance(patch_editor.view_passive, Gtk.Label)
        assert EDITOR == patch_editor.text
        assert patch_get_object.called
        assert SITE == patch_get_object.site_ui
        assert patch_site.called
        assert patch_editor.view_editor == patch_site.view_editor
        assert EXPAND_OKAY == patch_site.expand_okay
        assert FILL_OKAY == patch_site.fill_okay
        assert N_PADDING == patch_site.n_padding

    def test_init_helper_summary(self, monkeypatch):
        """Confirm helper creates summary field in view.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        class PatchGetObject:
            def __init__(self):
                self.called = False
                self.ui = list()

            def get_object(self, p_ui):
                self.called = True
                self.ui.append(p_ui)
                return Gtk.Box()

        patch_get_object = PatchGetObject()

        class PatchBind:
            def __init__(self):
                self.called = False
                self.prop_source = 'Oops!'
                self.target = None
                self.prop_target = 'Oops!'
                self.flags = None

            def bind_property(
                    self, p_prop_source, p_target, p_prop_target, p_flags):
                self.called = True
                self.prop_source = p_prop_source
                self.target = p_target
                self.prop_target = p_prop_target
                self.flags = p_flags

        patch_bind = PatchBind()
        monkeypatch.setattr(Gtk.Box, 'bind_property', patch_bind.bind_property)

        class PatchSite:
            def __init__(self):
                self.called = False
                self.view = None

            def add(self, p_view):
                self.called = True
                self.view = p_view

        patch_site = PatchSite()
        monkeypatch.setattr(Gtk.Box, 'add', patch_site.add)

        SITE_UI = 'ui_site_summary_sheet'
        BUTTON_SHOW_UI = 'ui_button_show_summary_sheet'
        PROP_BUTTON_SHOW = 'active'
        EXPANDER_UI = 'ui_expander_summary_sheet'
        PROP_EXPANDER = 'visible'
        FLAGS = GO.BindingFlags.BIDIRECTIONAL | GO.BindingFlags.SYNC_CREATE
        control = CSHEET.g_control_app.open_factsheet(p_path=None)
        target = VSHEET.ViewSheet(p_control=control)
        # Test
        target._init_summary_sheet(patch_get_object.get_object)
        assert patch_get_object.called
        assert SITE_UI in patch_get_object.ui
        assert patch_site.called
        assert isinstance(patch_site.view, Gtk.TextView)
        assert BUTTON_SHOW_UI in patch_get_object.ui
        assert EXPANDER_UI in patch_get_object.ui
        assert PROP_BUTTON_SHOW == patch_bind.prop_source
        assert isinstance(patch_bind.target, Gtk.Box)
        assert PROP_EXPANDER == patch_bind.prop_target
        assert FLAGS == patch_bind.flags

    @pytest.mark.parametrize(
        'NAME_SIGNAL, NAME_ATTRIBUTE, ORIGIN, N_DEFAULT', [
            # ('closed', '_context_name', Gtk.Popover, 0),
            ('delete-event', '_window', Gtk.ApplicationWindow, 0),
            # ('changed', '_cursor_topics', Gtk.TreeSelection, 0),
            ])
    def test_init_signals(self, NAME_SIGNAL, NAME_ATTRIBUTE, ORIGIN,
                          N_DEFAULT, gtk_app_window):
        """| Confirm initialization.
        | Case: signal connections

        :param NAME_SIGNAL: name of signal.
        :param NAME_ATTRIBTE: name of attribute connected to signal.
        :param ORIGIN: GTK class of connected attribute.
        :param N_DEFAULT: number of default handlers
        :param gtk_app_window: fixture :func:`.gtk_app_window`.
        """
        # Setup
        origin_gtype = GO.type_from_name(GO.type_name(ORIGIN))
        signal = GO.signal_lookup(NAME_SIGNAL, origin_gtype)
        control = CSHEET.g_control_app.open_factsheet(p_path=None)
        target = VSHEET.ViewSheet(p_control=control)
        # Test
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(gtk_app_window)

        attribute = getattr(target, NAME_ATTRIBUTE)
        n_handlers = 0
        while True:
            id_signal = GO.signal_handler_find(
                attribute, GO.SignalMatchType.ID, signal,
                0, None, None, None)
            if 0 == id_signal:
                break

            n_handlers += 1
            GO.signal_handler_disconnect(attribute, id_signal)

        assert N_DEFAULT + 1 == n_handlers

    @pytest.mark.skip
    def test_init_activate(self, patch_factsheet, capfd):
        """Confirm initialization of name view activation signal.

        :param capfd: built-in fixture `Pytest capfd`_.
        """
        # # Setup
        # factsheet = patch_factsheet()
        # entry_gtype = GO.type_from_name(GO.type_name(Gtk.Entry))
        # delete_signal = GO.signal_lookup('activate', entry_gtype)
        # # Test
        # target = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)
        #
        # entry = target._infoid.get_view_name()
        # activate_id = GO.signal_handler_find(
        #     entry, GO.SignalMatchType.ID, delete_signal,
        #     0, None, None, None)
        # assert 0 != activate_id
        # # Teardown
        # target._window.destroy()
        # del target._window
        # del factsheet

    @pytest.mark.parametrize('ACTION', [
        'show-about-app',
        'show-help-app',
        'show-intro-app',
        ])
    def test_init_app_menu(self, ACTION):
        """| Confirm initialization.
        | Case: definition fo app menu actions

        :param ACTION: name of action for menu item.
        """
        # Setup
        control = CSHEET.g_control_app.open_factsheet(p_path=None)
        target = VSHEET.ViewSheet(p_control=control)
        # Test
        assert target._window.lookup_action(ACTION) is not None

    @pytest.mark.parametrize('ACTION', [
        'show-help-sheet',
        ])
    def test_init_factsheet_menu(self, ACTION):
        """| Confirm initialization.
        | Case: definition fo app menu actions

        :param ACTION: name of action for menu item.
        """
        # Setup
        control = CSHEET.g_control_app.open_factsheet(p_path=None)
        target = VSHEET.ViewSheet(p_control=control)
        # Test
        assert target._window.lookup_action(ACTION) is not None

    @pytest.mark.parametrize('RESPONSE, RETURN', [
        (Gtk.ResponseType.APPLY, VSHEET.ViewSheet.ALLOW_CLOSE),
        (Gtk.ResponseType.CANCEL, VSHEET.ViewSheet.DENY_CLOSE)
        ])
    def test_confirm_close(self, monkeypatch, RESPONSE, RETURN):
        """Confirm translation of GTK response types.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        monkeypatch.setattr(Gtk.Dialog, 'run', lambda _s: RESPONSE)
        control = CSHEET.g_control_app.open_factsheet(p_path=None)
        target = VSHEET.ViewSheet(p_control=control)
        # Test
        assert RETURN == target.confirm_close()

    def test_erases(self, monkeypatch):
        """Confirm view destroys its visual element."""
        # Setup
        class PatchDestroy:
            def __init__(self): self.called = False

            def destroy(self): self.called = True

        patch_destroy = PatchDestroy()
        monkeypatch.setattr(Gtk.Window, 'destroy', patch_destroy.destroy)

        control = CSHEET.g_control_app.open_factsheet(p_path=None)
        target = VSHEET.ViewSheet(p_control=control)
        # Test
        target.erase()
        assert not target._window.get_visible()
        assert patch_destroy.called

    @pytest.mark.skip
    def test_close_topic(self, patch_factsheet, capfd, new_outline_topics):
        """Confirm topic form removed from scenes and closed.

        :param capfd: built-in fixture `Pytest capfd`_.
        """
        # # Setup
        # factsheet = patch_factsheet()
        # target = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)
        # sheets_active = CPOOL.PoolSheets()
        # control = CSHEET.ControlSheet.new(sheets_active)
        # target.link_factsheet(target, control)
        #
        # outline_topics = new_outline_topics()
        # topics = outline_topics._gtk_model
        # view = target._view_topics.gtk_view
        # view.set_model(topics)
        # for index in outline_topics.indices():
        #     topic = outline_topics.get_item(index)
        #     control = target._control._add_new_control_topic(topic)
        #     form = VTOPIC.FormTopic(p_control=control)
        #     target._scenes_topic.add_scene(
        #         form.gtk_pane, hex(topic.tag))
        #
        # target._cursor_topics.unselect_all()
        # PATH_CURRENT = '0:0:0'
        # i_remove = topics.get_iter_from_string(PATH_CURRENT)
        # topic_remove = AOUTLINE.get_item_gtk(topics, i_remove)
        # id_remove = topic_remove.tag
        # NAME_DEFAULT = 'Default'
        # # Test
        # target.close_topic(id_remove)
        # is_scene = target._scenes_topic.show_scene(hex(id_remove))
        # assert NAME_DEFAULT == is_scene
        # # Teardown
        # target._window.destroy()
        # del target._window
        # del factsheet

    @pytest.mark.skip
    def test_get_infoid(self, patch_factsheet, capfd):
        """Confirm returns InfoId attribute.

        :param capfd: built-in fixture `Pytest capfd`_.
        """
        # # Setup
        # factsheet = patch_factsheet()
        # target = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)
        # # Test
        # assert target._infoid is target.get_infoid()
        # # Teardown
        # target._window.destroy()
        # del target._window
        # del factsheet

    @pytest.mark.skip
    def test_get_view_topics(self, patch_factsheet, capfd):
        """Confirm returns view of topics outline.

        :param capfd: built-in fixture `Pytest capfd`_.
        """
        # # Setup
        # factsheet = patch_factsheet()
        # target = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)
        # # Test
        # assert target._view_topics is target.get_view_topics()
        # # Teardown
        # target._window.destroy()
        # del target._window
        # del factsheet

    @pytest.mark.skip
    def test_link_factsheet(self, patch_factsheet, capfd):
        """Confirm creation of factsheet links.

        :param capfd: built-in fixture `Pytest capfd`_.
        """
        # # Setup
        # factsheet = patch_factsheet()
        # sheets_active = CPOOL.PoolSheets()
        # control = CSHEET.ControlSheet.new(sheets_active)
        # page = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # page._window.set_skip_pager_hint(True)
        # page._window.set_skip_taskbar_hint(True)
        # # Test
        # VSHEET.ViewSheet.link_factsheet(page, control)
        # assert page._control is control
        # model = page._view_topics.gtk_view.get_model()
        # assert model is not None
        # assert page._query_place is not None
        # assert isinstance(page._query_place, QPLACE.QueryPlace)
        # query_view_topics = page._query_place._view_topics
        # assert query_view_topics.gtk_view.get_model() is model
        # assert isinstance(page._query_template, QTEMPLATE.QueryTemplate)
        # # Teardown
        # page._window.destroy()
        # del page._window
        # del factsheet

    @pytest.mark.skip
    @pytest.mark.parametrize('ACTION, LABEL', [
        # (Gtk.FileChooserAction.SAVE, 'Save'),
        # (Gtk.FileChooserAction.OPEN, 'Open'),
        ])
    def test_make_dialog_file(
            self, patch_factsheet, capfd, ACTION, LABEL):
        """Confirm construction of dialog for file save.

        :param capfd: built-in fixture `Pytest capfd`_.
        """
        # # Setup
        # factsheet = patch_factsheet()
        # source = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # source._window.set_skip_pager_hint(True)
        # source._window.set_skip_taskbar_hint(True)
        # FILTERS = set(['Factsheet', 'Any'])
        # # Test
        # target = source._make_dialog_file(ACTION)
        # assert isinstance(target, Gtk.FileChooserDialog)
        # assert target.get_action() is ACTION
        # assert target.get_transient_for() is source._window
        # assert target.get_destroy_with_parent()
        # if ACTION is Gtk.FileChooserAction.SAVE:
        #     assert target.get_do_overwrite_confirmation()
        #
        # button = target.get_widget_for_response(Gtk.ResponseType.CANCEL)
        # assert 'Cancel' == button.get_label()
        #
        # button = target.get_widget_for_response(Gtk.ResponseType.APPLY)
        # assert LABEL == button.get_label()
        # style = button.get_style_context()
        # assert style.has_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)
        #
        # assert FILTERS == {f.get_name() for f in target.list_filters()}
        # # Teardown
        # source._window.destroy()
        # del source._window
        # del factsheet

    @pytest.mark.skip
    def test_new_factsheet(self, patch_factsheet, capfd):
        """Confirm factsheet creation with default contents.

        :param capfd: built-in fixture `Pytest capfd`_.
        """
        # # Setup
        # factsheet = patch_factsheet()
        # sheets_active = CPOOL.PoolSheets()
        # # Test
        # target = VSHEET.ViewSheet.new_factsheet(factsheet, sheets_active)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)
        # assert isinstance(target, VSHEET.ViewSheet)
        # assert target._window.get_application() is factsheet
        # control = target._control
        # assert isinstance(control, CSHEET.ControlSheet)
        # # Teardown
        # target._window.destroy()
        # del target._window
        # del factsheet

    # def test_new_view_topics(self, patch_factsheet, capfd):
    #     """ """
    #     # Setup
    #     factsheet = patch_factsheet()
    #     target = VSHEET.ViewSheet(px_app=factsheet)
    #     snapshot = capfd.readouterr()   # Resets the internal buffer
    #     assert not snapshot.out
    #     assert 'Gtk-CRITICAL' in snapshot.err
    #     assert 'GApplication::startup signal' in snapshot.err
    #     # target._window.set_skip_pager_hint(True)
    #     # target._window.set_skip_taskbar_hint(True)
    #     target._window.set_transient_for(WINDOW_ANCHOR)
    #     sheets_active = CPOOL.PoolSheets()
    #     control = CSHEET.ControlSheet.new(sheets_active)
    #     target.link_factsheet(target, control)

    #     # Test
    #     view_new = target.new_view_topics()
    #     assert isinstance(view_new, VTYPES.ViewOutlineTopics)
    #     model = target._view_topics.gtk_view.get_model()
    #     assert view_new.gtk_view.get_model() is model
    #     # Teardown

    @pytest.mark.skip
    def test_on_changed_cursor(
            self, patch_factsheet, capfd, new_outline_topics):
        """| Confirm updates when current topic changes.
        | Case: change to topic with scene.

        :param capfd: built-in fixture `Pytest capfd`_.
        """
        # # Setup
        # factsheet = patch_factsheet()
        # target = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)
        # sheets_active = CPOOL.PoolSheets()
        # control = CSHEET.ControlSheet.new(sheets_active)
        # target.link_factsheet(target, control)
        #
        # outline_topics = new_outline_topics()
        # topics = outline_topics._gtk_model
        # view = target._view_topics.gtk_view
        # view.set_model(topics)
        # for index in outline_topics.indices():
        #     topic = outline_topics.get_item(index)
        #     control = target._control._add_new_control_topic(topic)
        #     form = VTOPIC.FormTopic(p_control=control)
        #     target._scenes_topic.add_scene(
        #         form.gtk_pane, hex(topic.tag))
        #
        # view.expand_all()
        # PATH_CURRENT = '0:0:0'
        # i_current = topics.get_iter_from_string(PATH_CURRENT)
        # topic_current = AOUTLINE.get_item_gtk(topics, i_current)
        # # Test
        # target._cursor_topics.select_iter(i_current)
        # id_visible = target._scenes_topic.get_scene_visible()
        # assert id_visible == hex(topic_current.tag)
        # # Teardown
        # target._window.destroy()
        # del target._window
        # del factsheet

    @pytest.mark.skip
    def test_on_changed_cursor_new(
            self, patch_factsheet, capfd, new_outline_topics):
        """| Confirm updates when current topic changes.
        | Case: change to topic without scene.

        :param capfd: built-in fixture `Pytest capfd`_.
        """
        # # Setup
        # factsheet = patch_factsheet()
        # target = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)
        # sheets_active = CPOOL.PoolSheets()
        # control = CSHEET.ControlSheet.new(sheets_active)
        # target.link_factsheet(target, control)
        #
        # outline_topics = new_outline_topics()
        # topics = outline_topics._gtk_model
        # view = target._view_topics.gtk_view
        # view.set_model(topics)
        # for index in outline_topics.indices():
        #     topic = outline_topics.get_item(index)
        #     control = target._control._add_new_control_topic(topic)
        #     form = VTOPIC.FormTopic(p_control=control)
        #     target._scenes_topic.add_scene(
        #         form.gtk_pane, hex(topic.tag))
        #
        # view.expand_all()
        # PATH_CURRENT = '0:0:0'
        # i_current = topics.get_iter_from_string(PATH_CURRENT)
        # topic_current = AOUTLINE.get_item_gtk(topics, i_current)
        # target._scenes_topic.remove_scene(hex(topic_current.tag))
        # # Test
        # target._cursor_topics.select_iter(i_current)
        # topic_visible = target._scenes_topic.get_scene_visible()
        # assert topic_visible == hex(topic_current.tag)
        # # Teardown
        # target._window.destroy()
        # del target._window
        # del factsheet

    @pytest.mark.skip
    def test_on_changed_cursor_no_control(
            self, patch_factsheet, capfd, new_outline_topics, monkeypatch):
        """| Confirm updates when current topic changes.
        | Case: change to topic without scene.

        :param capfd: built-in fixture `Pytest capfd`_.
        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # # Setup
        # factsheet = patch_factsheet()
        # target = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)
        # sheets_active = CPOOL.PoolSheets()
        # control = CSHEET.ControlSheet.new(sheets_active)
        # target.link_factsheet(target, control)
        #
        # outline_topics = new_outline_topics()
        # topics = outline_topics._gtk_model
        # view = target._view_topics.gtk_view
        # view.set_model(topics)
        # for index in outline_topics.indices():
        #     topic = outline_topics.get_item(index)
        #     control = target._control._add_new_control_topic(topic)
        #     form = VTOPIC.FormTopic(p_control=control)
        #     target._scenes_topic.add_scene(
        #         form.gtk_pane, hex(topic.tag))
        #
        # monkeypatch.setattr(
        #     CSHEET.ControlSheet, 'get_control_topic', lambda _s, _t: None)
        #
        # view.expand_all()
        # PATH_INIT = '0'
        # i_init = topics.get_iter_from_string(PATH_INIT)
        # target._cursor_topics.select_iter(i_init)
        #
        # PATH_CURRENT = '0:0:0'
        # i_current = topics.get_iter_from_string(PATH_CURRENT)
        # topic_current = AOUTLINE.get_item_gtk(topics, i_current)
        # target._scenes_topic.remove_scene(hex(topic_current.tag))
        # NAME_DEFAULT = 'Default'
        # # Test
        # target._cursor_topics.select_iter(i_current)
        # topic_visible = target._scenes_topic.get_scene_visible()
        # assert NAME_DEFAULT == topic_visible
        # # Teardown
        # target._window.destroy()
        # del target._window
        # del factsheet

    @pytest.mark.skip
    def test_on_changed_cursor_to_none(
            self, patch_factsheet, capfd, new_outline_topics):
        """| Confirm updates when current topic changes.
        | Case: change to no current topic.

        :param capfd: built-in fixture `Pytest capfd`_.
        """
        # # Setup
        # factsheet = patch_factsheet()
        # target = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)
        # sheets_active = CPOOL.PoolSheets()
        # control = CSHEET.ControlSheet.new(sheets_active)
        # target.link_factsheet(target, control)
        #
        # outline_topics = new_outline_topics()
        # topics = outline_topics._gtk_model
        # view = target._view_topics.gtk_view
        # view.set_model(topics)
        # for index in outline_topics.indices():
        #     topic = outline_topics.get_item(index)
        #     control = target._control._add_new_control_topic(topic)
        #     form = VTOPIC.FormTopic(p_control=control)
        #     target._scenes_topic.add_scene(
        #         form.gtk_pane, hex(topic.tag))
        #
        # # pane_none = Gtk.Label(label='No form')
        # # target._scenes_topic.add_scene(
        # #     pane_none, target._scenes_topic.ID_NONE)
        #
        # target._cursor_topics.unselect_all()
        # NAME_DEFAULT = 'Default'
        # # Test
        # target.on_changed_cursor(target._cursor_topics)
        # id_visible = target._scenes_topic.get_scene_visible()
        # assert NAME_DEFAULT == id_visible
        # # Teardown
        # target._window.destroy()
        # del target._window
        # del factsheet

    @pytest.mark.skip
    def test_on_changed_cursor_no_topic(
            self, patch_factsheet, capfd, new_outline_topics):
        """| Confirm updates when current topic changes.
        | Case: change to a topic is that is None.

        :param capfd: built-in fixture `Pytest capfd`_.
        """
        # # Setup
        # factsheet = patch_factsheet()
        # target = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)
        # sheets_active = CPOOL.PoolSheets()
        # control = CSHEET.ControlSheet.new(sheets_active)
        # target.link_factsheet(target, control)
        #
        # outline_topics = new_outline_topics()
        # topics = outline_topics._gtk_model
        # view = target._view_topics.gtk_view
        # view.set_model(topics)
        # for index in outline_topics.indices():
        #     topic = outline_topics.get_item(index)
        #     control = target._control._add_new_control_topic(topic)
        #     form = VTOPIC.FormTopic(p_control=control)
        #     target._scenes_topic.add_scene(
        #         form.gtk_pane, hex(topic.tag))
        #
        # view.expand_all()
        # PATH_CURRENT = '0:0:0'
        # i_current = topics.get_iter_from_string(PATH_CURRENT)
        # target._cursor_topics.select_iter(i_current)
        # topics[i_current][AOUTLINE.AdaptTreeStore.N_COLUMN_ITEM] = None
        # NAME_DEFAULT = 'Default'
        # # Test
        # target.on_changed_cursor(target._cursor_topics)
        # id_visible = target._scenes_topic.get_scene_visible()
        # assert NAME_DEFAULT == id_visible
        # # Teardown
        # target._window.destroy()
        # del target._window
        # del factsheet

    @pytest.mark.skip
    def test_on_close_page_force(self, patch_factsheet, capfd):
        """| Confirm response to request to erase page.
        | Case: unconditional erase.

        :param capfd: built-in fixture `Pytest capfd`_.
        """
        # # Setup
        # factsheet = patch_factsheet()
        # target = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)
        #
        # sheets_active = CPOOL.PoolSheets()
        # control = PatchSafe(ABC_SHEET.EffectSafe.COMPLETED, sheets_active)
        # target._control = control
        # target._close_window = True
        # N_CALLS_SAFE = 0
        # N_CALLS_FORCE = 0
        # # Test
        # assert target.on_close_page(None, None) is UI.CLOSE_GTK
        # assert N_CALLS_SAFE == control.n_detach_safe
        # assert N_CALLS_FORCE == control.n_detach_force
        # # Teardown
        # target._window.destroy()
        # del target._window
        # del factsheet

    @pytest.mark.skip
    def test_on_close_page_safe(self, patch_factsheet, capfd):
        """| Confirm response to request to erase page.
        | Case: safe to erase.

        :param capfd: built-in fixture `Pytest capfd`_.
        """
        # # Setup
        # factsheet = patch_factsheet()
        # target = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)
        #
        # sheets_active = CPOOL.PoolSheets()
        # control = PatchSafe(ABC_SHEET.EffectSafe.COMPLETED, sheets_active)
        # target._control = control
        # N_CALLS_SAFE = 1
        # N_CALLS_FORCE = 0
        # # Test
        # assert target.on_close_page(None, None) is UI.CLOSE_GTK
        # assert N_CALLS_SAFE == control.n_detach_safe
        # assert N_CALLS_FORCE == control.n_detach_force
        # # Teardown
        # target._window.destroy()
        # del target._window
        # del factsheet

    @pytest.mark.skip
    def test_on_close_page_cancel(
            self, patch_factsheet, capfd, monkeypatch):
        """| Confirm response to request to erase page.
        | Case: not safe to erase, user cancels erase.

        :param capfd: built-in fixture `Pytest capfd`_.
        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # # Setup
        # factsheet = patch_factsheet()
        # target = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)
        #
        # monkeypatch.setattr(
        #     Gtk.Dialog, 'run', lambda _self: Gtk.ResponseType.CANCEL)
        # target._dialog_data_loss.set_visible(True)
        # monkeypatch.setattr(
        #     Gtk.Dialog, 'hide', lambda self: self.set_visible(False))
        #
        # sheets_active = CPOOL.PoolSheets()
        # control = PatchSafe(ABC_SHEET.EffectSafe.NO_EFFECT, sheets_active)
        # target._control = control
        # N_CALLS_SAFE = 1
        # N_CALLS_FORCE = 0
        # # Test
        # assert target.on_close_page(None, None) is UI.CANCEL_GTK
        # assert not target._dialog_data_loss.get_visible()
        # assert N_CALLS_SAFE == control.n_detach_safe
        # assert N_CALLS_FORCE == control.n_detach_force
        # # Teardown
        # target._window.destroy()
        # del target._window
        # del factsheet

    @pytest.mark.skip
    def test_on_close_page_discard(
            self, patch_factsheet, capfd, monkeypatch):
        """| Confirm response to request to erase page.
        | Case: not safe to erase, user approves erase.

        :param capfd: built-in fixture `Pytest capfd`_.
        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # # Setup
        # factsheet = patch_factsheet()
        # target = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)
        #
        # monkeypatch.setattr(
        #     Gtk.Dialog, 'run', lambda _self: Gtk.ResponseType.APPLY)
        # target._dialog_data_loss.set_visible(True)
        # monkeypatch.setattr(
        #     Gtk.Dialog, 'hide', lambda self: self.set_visible(False))
        #
        # sheets_active = CPOOL.PoolSheets()
        # control = PatchSafe(ABC_SHEET.EffectSafe.NO_EFFECT, sheets_active)
        # target._control = control
        # N_CALLS_SAFE = 1
        # N_CALLS_FORCE = 1
        # # Test
        # assert target.on_close_page(None, None) is UI.CLOSE_GTK
        # assert not target._dialog_data_loss.get_visible()
        # assert N_CALLS_SAFE == control.n_detach_safe
        # assert N_CALLS_FORCE == control.n_detach_force
        # # Teardown
        # target._window.destroy()
        # del target._window
        # del factsheet

    # @pytest.mark.skip
    # def test_on_delete_sheet_safe(
    #         self, patch_factsheet, capfd, patch_dialog_run, monkeypatch):
    #     """| Confirm response to request to delete factsheet.
    #     | Case: no unsaved changes.
    #
    #     :param capfd: built-in fixture `Pytest capfd`_.
    #     :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
    #     """
    #     # # Setup
    #     # factsheet = patch_factsheet()
    #     # target = VSHEET.ViewSheet(px_app=factsheet)
    #     # snapshot = capfd.readouterr()   # Resets the internal buffer
    #     # assert not snapshot.out
    #     # assert 'Gtk-CRITICAL' in snapshot.err
    #     # assert 'GApplication::startup signal' in snapshot.err
    #     # # target._window.set_skip_pager_hint(True)
    #     # # target._window.set_skip_taskbar_hint(True)
    #     # target._window.set_transient_for(WINDOW_ANCHOR)
    #     #
    #     # patch_dialog = patch_dialog_run(Gtk.ResponseType.CANCEL)
    #     # monkeypatch.setattr(Gtk.Dialog, 'run', patch_dialog.run)
    #     #
    #     # sheets_active = CPOOL.PoolSheets()
    #     # control = PatchSafe(ABC_SHEET.EffectSafe.COMPLETED, sheets_active)
    #     # control._model = MSHEET.Sheet()
    #     # VSHEET.ViewSheet.link_factsheet(target, control)
    #     # N_CALLS_SAFE = 1
    #     # N_CALLS_FORCE = 0
    #     # # Test
    #     # target.on_delete_sheet(None, None)
    #     # assert not patch_dialog.called
    #     # assert N_CALLS_SAFE == control.n_delete_safe
    #     # assert N_CALLS_FORCE == control.n_delete_force
    #     # # Teardown
    #     # target._window.destroy()
    #     # del target._window
    #     # del factsheet
    #
    # @pytest.mark.skip
    # def test_on_delete_sheet_cancel(
    #         self, patch_factsheet, capfd, patch_dialog_run, monkeypatch):
    #     """| Confirm response to request to delete factsheet.
    #     | Case: unsaved chagnes, user cancels delete.
    #
    #     :param capfd: built-in fixture `Pytest capfd`_.
    #     :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
    #     """
    #     # # Setup
    #     # factsheet = patch_factsheet()
    #     # target = VSHEET.ViewSheet(px_app=factsheet)
    #     # snapshot = capfd.readouterr()   # Resets the internal buffer
    #     # assert not snapshot.out
    #     # assert 'Gtk-CRITICAL' in snapshot.err
    #     # assert 'GApplication::startup signal' in snapshot.err
    #     # # target._window.set_skip_pager_hint(True)
    #     # # target._window.set_skip_taskbar_hint(True)
    #     # target._window.set_transient_for(WINDOW_ANCHOR)
    #     #
    #     # patch_dialog = patch_dialog_run(Gtk.ResponseType.CANCEL)
    #     # monkeypatch.setattr(Gtk.Dialog, 'run', patch_dialog.run)
    #     # target._dialog_data_loss.set_visible(True)
    #     # monkeypatch.setattr(
    #     #     Gtk.Dialog, 'hide', lambda self: self.set_visible(False))
    #     #
    #     # sheets_active = CPOOL.PoolSheets()
    #     # control = PatchSafe(ABC_SHEET.EffectSafe.NO_EFFECT, sheets_active)
    #     # control._model = MSHEET.Sheet()
    #     # VSHEET.ViewSheet.link_factsheet(target, control)
    #     # N_CALLS_SAFE = 1
    #     # N_CALLS_FORCE = 0
    #     # # Test
    #     # target.on_delete_sheet(None, None)
    #     # assert patch_dialog.called
    #     # assert not target._dialog_data_loss.get_visible()
    #     # assert N_CALLS_SAFE == control.n_delete_safe
    #     # assert N_CALLS_FORCE == control.n_delete_force
    #     # # Teardown
    #     # target._window.destroy()
    #     # del target._window
    #     # del factsheet
    #
    # @pytest.mark.skip
    # def test_on_delete_sheet_discard(
    #         self, patch_factsheet, capfd, patch_dialog_run, monkeypatch):
    #     """| Confirm response to request to delete factsheet.
    #     | Case: unsaved changes, user approves delete.
    #
    #     :param capfd: built-in fixture `Pytest capfd`_.
    #     :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
    #     """
    #     # # Setup
    #     # factsheet = patch_factsheet()
    #     # target = VSHEET.ViewSheet(px_app=factsheet)
    #     # snapshot = capfd.readouterr()   # Resets the internal buffer
    #     # assert not snapshot.out
    #     # assert 'Gtk-CRITICAL' in snapshot.err
    #     # assert 'GApplication::startup signal' in snapshot.err
    #     # # target._window.set_skip_pager_hint(True)
    #     # # target._window.set_skip_taskbar_hint(True)
    #     # target._window.set_transient_for(WINDOW_ANCHOR)
    #     #
    #     # patch_dialog = patch_dialog_run(Gtk.ResponseType.APPLY)
    #     # monkeypatch.setattr(Gtk.Dialog, 'run', patch_dialog.run)
    #     # target._dialog_data_loss.set_visible(True)
    #     # monkeypatch.setattr(
    #     #     Gtk.Dialog, 'hide', lambda self: self.set_visible(False))
    #     #
    #     # sheets_active = CPOOL.PoolSheets()
    #     # control = PatchSafe(ABC_SHEET.EffectSafe.NO_EFFECT, sheets_active)
    #     # control._model = MSHEET.Sheet()
    #     # VSHEET.ViewSheet.link_factsheet(target, control)
    #     # N_CALLS_SAFE = 1
    #     # N_CALLS_FORCE = 1
    #     # # Test
    #     # target.on_delete_sheet(None, None)
    #     # assert patch_dialog.called
    #     # assert not target._dialog_data_loss.get_visible()
    #     # assert N_CALLS_SAFE == control.n_delete_safe
    #     # assert N_CALLS_FORCE == control.n_delete_force
    #     # # Teardown
    #     # target._window.destroy()
    #     # del target._window
    #     # del factsheet

    @pytest.mark.skip
    def test_on_delete_topic(
            self, monkeypatch, patch_factsheet, capfd, new_outline_topics):
        """| Confirm topic removal.
        | Case: Topic selected.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param capfd: built-in fixture `Pytest capfd`_.
        """
        # # Setup
        # class PatchExtract:
        #     def __init__(self):
        #         self.called = False
        #         self.index = None
        #
        #     def extract_topic(self, p_index):
        #         self.called = True
        #         self.index = p_index
        #
        # patch_extract = PatchExtract()
        # monkeypatch.setattr(
        #     CSHEET.ControlSheet, 'extract_topic',
        #     patch_extract.extract_topic)
        #
        # factsheet = patch_factsheet()
        # target = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)
        #
        # sheets_active = CPOOL.PoolSheets()
        # control = CSHEET.ControlSheet.new(sheets_active)
        # target.link_factsheet(target, control)
        #
        # outline_topics = new_outline_topics()
        # topics = outline_topics._gtk_model
        # i_first = topics.get_iter_first()
        # path_first = topics.get_string_from_iter(i_first)
        # view = target._view_topics.gtk_view
        # view.set_model(topics)
        # view.expand_all()
        # cursor = view.get_selection()
        # cursor.select_iter(i_first)
        # # Test
        # target.on_delete_topic(None, None)
        # assert patch_extract.called
        # path_target = topics.get_string_from_iter(patch_extract.index)
        # assert path_first == path_target
        # # Teardown
        # target._window.destroy()
        # del target._window
        # del factsheet

    @pytest.mark.skip
    def test_on_delete_topic_none(
            self, monkeypatch, patch_factsheet, capfd):
        """| Confirm topic removal.
        | Case: No topic selected.s

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param capfd: built-in fixture `Pytest capfd`_.
        """
        # # Setup
        # class PatchExtract:
        #     def __init__(self): self.called = False
        #
        #     def extract_topic(self, _index): self.called = True
        #
        # patch_extract = PatchExtract()
        # monkeypatch.setattr(
        #     CSHEET.ControlSheet, 'extract_topic',
        #     patch_extract.extract_topic)
        # factsheet = patch_factsheet()
        # target = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)
        #
        # sheets_active = CPOOL.PoolSheets()
        # control = CSHEET.ControlSheet.new(sheets_active)
        # target.link_factsheet(target, control)
        # # Test
        # target.on_delete_topic(None, None)
        # assert not patch_extract.called
        # # Teardown
        # target._window.destroy()
        # del target._window
        # del factsheet

    @pytest.mark.skip
    def test_on_clear_topics(
            self, monkeypatch, patch_factsheet, capfd):
        """TBD

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param capfd: built-in fixture `Pytest capfd`_.
        """
        # # Setup
        # class PatchClear:
        #     def __init__(self): self.called = False
        #
        #     def clear(self): self.called = True
        #
        # patch_clear = PatchClear()
        # monkeypatch.setattr(
        #     CSHEET.ControlSheet, 'clear', patch_clear.clear)
        # factsheet = patch_factsheet()
        # target = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)
        #
        # sheets_active = CPOOL.PoolSheets()
        # control = CSHEET.ControlSheet.new(sheets_active)
        # target.link_factsheet(target, control)
        # # Test
        # target.on_clear_topics(None, None)
        # assert patch_clear.called
        # # Teardown
        # target._window.destroy()
        # del target._window
        # del factsheet

    def test_on_close_view_sheet_safe(self, monkeypatch):
        """| Confirm attempt to erase view.
        | Case: no loss of unsaved changes

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        class PatchIsSafe:
            def __init__(self, p_is_safe):
                self.called = False
                self.is_safe = p_is_safe

            def remove_view_is_safe(self):
                self.called = True
                return self.is_safe

        patch_safe = PatchIsSafe(p_is_safe=True)
        monkeypatch.setattr(CSHEET.ControlSheet, 'remove_view_is_safe',
                            patch_safe.remove_view_is_safe)

        control = CSHEET.g_control_app.open_factsheet(p_path=None)
        target = VSHEET.ViewSheet(p_control=control)
        id_target = CSHEET.id_view_sheet(p_view_sheet=target)
        _view_new = VSHEET.ViewSheet(p_control=control)
        roster_views = control._roster_views
        N_VIEWS = 1
        # Test
        result = target.on_close_view_sheet(None, None)
        assert patch_safe.called
        assert VSHEET.ViewSheet.ALLOW_CLOSE == result
        assert N_VIEWS == len(roster_views)
        assert id_target not in roster_views

    def test_on_close_view_sheet_unsafe_allow(self, monkeypatch):
        """| Confirm attempt to erase view.
        | Case: user allows loss of unsaved changes

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        class PatchIsSafe:
            def __init__(self, p_is_safe):
                self.called = False
                self.is_safe = p_is_safe

            def remove_view_is_safe(self):
                self.called = True
                return self.is_safe

        patch_unsafe = PatchIsSafe(p_is_safe=False)
        monkeypatch.setattr(CSHEET.ControlSheet, 'remove_view_is_safe',
                            patch_unsafe.remove_view_is_safe)
        monkeypatch.setattr(
            Gtk.Dialog, 'run', lambda _s: Gtk.ResponseType.APPLY)

        control = CSHEET.g_control_app.open_factsheet(p_path=None)
        target = VSHEET.ViewSheet(p_control=control)
        id_target = CSHEET.id_view_sheet(p_view_sheet=target)
        _view_new = VSHEET.ViewSheet(p_control=control)
        roster_views = control._roster_views
        N_VIEWS = 1
        # Test
        result = target.on_close_view_sheet(None, None)
        assert patch_unsafe.called
        assert VSHEET.ViewSheet.ALLOW_CLOSE == result
        assert N_VIEWS == len(roster_views)
        assert id_target not in roster_views

    def test_on_close_view_sheet_unsafe_deny(self, monkeypatch):
        """| Confirm attempt to erase view.
        | Case: user denies loss of unsaved changes

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        class PatchIsSafe:
            def __init__(self, p_is_safe):
                self.called = False
                self.is_safe = p_is_safe

            def remove_view_is_safe(self):
                self.called = True
                return self.is_safe

        patch_unsafe = PatchIsSafe(p_is_safe=False)
        monkeypatch.setattr(CSHEET.ControlSheet, 'remove_view_is_safe',
                            patch_unsafe.remove_view_is_safe)
        monkeypatch.setattr(
            Gtk.Dialog, 'run', lambda _s: Gtk.ResponseType.CANCEL)

        control = CSHEET.g_control_app.open_factsheet(p_path=None)
        target = VSHEET.ViewSheet(p_control=control)
        view_new = VSHEET.ViewSheet(p_control=control)
        id_view_new = CSHEET.id_view_sheet(p_view_sheet=view_new)
        roster_views = control._roster_views
        N_VIEWS = 2
        # Test
        result = target.on_close_view_sheet(None, None)
        assert patch_unsafe.called
        assert VSHEET.ViewSheet.DENY_CLOSE == result
        assert N_VIEWS == len(roster_views)
        assert id_view_new in roster_views

    @pytest.mark.skip
    def test_on_flip_summary(self, patch_factsheet, capfd):
        """Confirm flip of facthseet summary visibility.

        #. Case: hide
        #. Case: show

        :param capfd: built-in fixture `Pytest capfd`_.
        """
        # # Setup
        # factsheet = patch_factsheet()
        # target = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)
        #
        # target._context_summary.set_visible(True)
        # assert target._context_summary.get_visible()
        # assert target._flip_summary.get_active()
        # # Test: hide
        # # Call clicked to invoke target.on_flip_summary.  Method clicked
        # # has the side effect of setting active state of _flip_summary.
        # target._flip_summary.clicked()
        # assert not target._context_summary.get_visible()
        # assert not target._flip_summary.get_active()
        # # Test: show
        # # As in case hide.
        # target._flip_summary.clicked()
        # assert target._context_summary.get_visible()
        # assert target._flip_summary.get_active()
        # # Teardown
        # target._window.destroy()
        # del target._window
        # del factsheet

    @pytest.mark.skip
    def test_on_go_first_topic(
            self, patch_factsheet, capfd, new_outline_topics):
        """| Confirm first topic selection.
        | Case: Topic outline is not empty.

        :param capfd: built-in fixture `Pytest capfd`_.
        """
        # # Setup
        # factsheet = patch_factsheet()
        # target = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)
        # sheets_active = CPOOL.PoolSheets()
        # control = CSHEET.ControlSheet.new(sheets_active)
        # target.link_factsheet(target, control)
        #
        # outline_topics = new_outline_topics()
        # topics = outline_topics._gtk_model
        # i_first = topics.get_iter_first()
        # path_first = topics.get_path(i_first)
        # item_first = AOUTLINE.get_item_gtk(topics, i_first)
        # view = target._view_topics.gtk_view
        # view.set_model(topics)
        # cursor = view.get_selection()
        # cursor.unselect_all()
        # # Test
        # target.on_go_first_topic(None, None)
        # model, index = cursor.get_selected()
        # assert model is topics
        # path_target = model.get_path(index)
        # assert path_first == path_target
        # item_target = AOUTLINE.get_item_gtk(model, index)
        # assert item_target is item_first
        # # Teardown
        # target._window.destroy()
        # del target._window
        # del factsheet

    @pytest.mark.skip
    def test_on_go_first_topic_none(
            self, monkeypatch, patch_factsheet, capfd):
        """| Confirm first topic selection.
        | Case: topic outline is empty.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param capfd: built-in fixture `Pytest capfd`_.
        """
        # # Setup
        # class PatchSelect:
        #     def __init__(self): self.called = False
        #
        #     def select_iter(self, _index):
        #         self.called = True
        #
        # patch_select = PatchSelect()
        # monkeypatch.setattr(
        #     Gtk.TreeSelection, 'select_iter', patch_select.select_iter)
        #
        # factsheet = patch_factsheet()
        # target = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)
        #
        # sheets_active = CPOOL.PoolSheets()
        # control = CSHEET.ControlSheet.new(sheets_active)
        # target.link_factsheet(target, control)
        # # Test
        # target.on_go_first_topic(None, None)
        # assert not patch_select.called
        # # Teardown
        # target._window.destroy()
        # del target._window
        # del factsheet

    @pytest.mark.skip
    def test_on_go_last_topic(
            self, patch_factsheet, capfd, new_outline_topics):
        """| Confirm last topic selection.
        | Case: Topic outline is not empty; last topic is not top level.

        :param capfd: built-in fixture `Pytest capfd`_.
        """
        # # Setup
        # factsheet = patch_factsheet()
        # target = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)
        #
        # sheets_active = CPOOL.PoolSheets()
        # control = CSHEET.ControlSheet.new(sheets_active)
        # target.link_factsheet(target, control)
        #
        # outline_topics = new_outline_topics()
        # topics = outline_topics._gtk_model
        # PATH_LAST = '1:1:2'
        # i_last = topics.get_iter(PATH_LAST)
        # item_last = AOUTLINE.get_item_gtk(topics, i_last)
        # view = target._view_topics.gtk_view
        # view.set_model(topics)
        # cursor = view.get_selection()
        # cursor.unselect_all()
        # # Test
        # target.on_go_last_topic(None, None)
        # model, index = cursor.get_selected()
        # assert model is topics
        # path_target = model.get_string_from_iter(index)
        # assert PATH_LAST == path_target
        # item_target = AOUTLINE.get_item_gtk(model, index)
        # assert item_target is item_last
        # # Teardown
        # target._window.destroy()
        # del target._window
        # del factsheet

    @pytest.mark.skip
    def test_on_go_last_topic_none(
            self, monkeypatch, patch_factsheet, capfd):
        """| Confirm last topic selection.
        | Case: topic outline is empty.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param capfd: built-in fixture `Pytest capfd`_.
        """
        # # Setup
        # class PatchSelect:
        #     def __init__(self): self.called = False
        #
        #     def select_iter(self, _index):
        #         self.called = True
        #
        # patch_select = PatchSelect()
        # monkeypatch.setattr(
        #     Gtk.TreeSelection, 'select_iter', patch_select.select_iter)
        #
        # factsheet = patch_factsheet()
        # target = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)
        #
        # sheets_active = CPOOL.PoolSheets()
        # control = CSHEET.ControlSheet.new(sheets_active)
        # target.link_factsheet(target, control)
        # # Test
        # target.on_go_last_topic(None, None)
        # assert not patch_select.called
        # # Teardown
        # target._window.destroy()
        # del target._window
        # del factsheet

    @pytest.mark.skip
    def test_on_go_last_topic_top(
            self, patch_factsheet, capfd, new_outline_topics):
        """| Confirm last topic selection.
        | Case: Topic outline is not empty; last topic is top level.

        :param capfd: built-in fixture `Pytest capfd`_.
        """
        # # Setup
        # factsheet = patch_factsheet()
        # target = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)
        #
        # sheets_active = CPOOL.PoolSheets()
        # control = CSHEET.ControlSheet.new(sheets_active)
        # target.link_factsheet(target, control)
        #
        # outline_topics = new_outline_topics()
        # topics = outline_topics._gtk_model
        # PATH_LAST = '1'
        # i_last = topics.get_iter(PATH_LAST)
        # i_prune = topics.iter_children(i_last)
        # while i_prune:
        #     is_valid = topics.remove(i_prune)
        #     if not is_valid:
        #         i_prune = None
        # item_last = AOUTLINE.get_item_gtk(topics, i_last)
        # view = target._view_topics.gtk_view
        # view.set_model(topics)
        # cursor = view.get_selection()
        # cursor.unselect_all()
        # # Test
        # target.on_go_last_topic(None, None)
        # model, index = cursor.get_selected()
        # assert model is topics
        # path_target = model.get_string_from_iter(index)
        # assert PATH_LAST == path_target
        # item_target = AOUTLINE.get_item_gtk(model, index)
        # assert item_target is item_last
        # # Teardown
        # target._window.destroy()
        # del target._window
        # del factsheet

    @pytest.mark.skip(resson='pending deleteion')
    def old_test_on_new_sheet(self, monkeypatch):
        """Confirm response to request to create default factsheet.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param capfd: built-in fixture `Pytest capfd`_.
        """
        # Setup
        control = CSHEET.g_control_app.open_factsheet(p_path=None)
        target = VSHEET.ViewSheet(p_control=control)
        # class PatchNew:
        #     def __init__(self): self.called = False
        #
        #     def new_factsheet(self, px_app, pm_sheets_active):
        #         _ = px_app
        #         _ = pm_sheets_active
        #         self.called = True
        #
        # patch_new = PatchNew()
        # monkeypatch.setattr(
        #     VSHEET.ViewSheet, 'new_factsheet', patch_new.new_factsheet)
        #
        # factsheet = patch_factsheet()
        # target = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)
        #
        # sheets_active = CPOOL.PoolSheets()
        # control = CSHEET.ControlSheet.new(sheets_active)
        # target.link_factsheet(target, control)
        # # Test
        # target.on_new_sheet(None, None)
        # assert patch_new.called
        # # Teardown
        # target._window.destroy()
        # del target._window
        # del factsheet

    def test_on_new_sheet(self, monkeypatch):
        """| Confirm factsheet creation with initial window.
        | Case: creation succeeds

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        patch_app = PatchSetApp()
        monkeypatch.setattr(
            Gtk.Window, 'set_application', patch_app.set_application)
        monkeypatch.setattr(
            Gtk.Window, 'show_all', lambda _s: None)
        control_app = CSHEET.g_control_app
        N_SHEETS = 1
        N_VIEWS = 1
        # Test
        VSHEET.ViewSheet.on_new_sheet(None, None)
        assert N_SHEETS == len(control_app._roster_sheets)
        _key, control_sheet = control_app._roster_sheets.popitem()
        assert N_VIEWS == len(control_sheet._roster_views)
        _key, view = control_sheet._roster_views.popitem()
        assert view._control is control_sheet

    def test_on_new_sheet_warn(self, monkeypatch, caplog):
        """| Confirm factsheet creation with initial window.
        | Case: creation fails

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param caplog: built-in fixture `Pytest caplog`_.
        """
        # Setup
        monkeypatch.setattr(
            CSHEET.ControlApp, 'open_factsheet', lambda _c, **_kw: None)
        log_message = (
            'Failed to create new factsheet (ViewSheet.on_new_sheet)')
        N_LOGS = 1
        LAST = -1
        # Test
        VSHEET.ViewSheet.on_new_sheet(None, None)
        assert N_LOGS == len(caplog.records)
        record = caplog.records[LAST]
        assert log_message == record.message
        assert 'CRITICAL' == record.levelname

    @pytest.mark.skip
    def test_on_new_topic(self, patch_factsheet, capfd, monkeypatch):
        """| Confirm response to request to specify topic.
        | Case: user completes placement, template selection, and topic
          specification.

        :param capfd: built-in fixture `Pytest capfd`_.
        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # # Setup
        # factsheet = patch_factsheet()
        # target = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)
        #
        # sheets_active = CPOOL.PoolSheets()
        # control = CSHEET.ControlSheet.new(sheets_active)
        # target.link_factsheet(target, control)
        # gtk_model = target._view_topics.gtk_view.get_model()
        # NAME = 'Parrot'
        # SUMMARY = 'A sketch about customer service.'
        # TITLE = 'The Parrot Sketch'
        # topic = MTOPIC.Topic(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
        # index_0 = gtk_model.append(None, [topic])
        #
        # PATH_EXPECT = '0:0'
        # placement = QPLACE.Placement(index_0, QPLACE.Order.CHILD)
        # patch_place = PatchCall(placement)
        # monkeypatch.setattr(
        #     QPLACE.QueryPlace, '__call__', patch_place.__call__)
        #
        # query_template = target._query_template
        # outline = query_template._outline
        # model = outline.gtk_view.get_model()
        # i_first = model.get_iter_first()
        # template = AOUTLINE.get_item_gtk(model, i_first)
        # patch_query_template = PatchCall(template)
        # monkeypatch.setattr(QTEMPLATE.QueryTemplate, '__call__',
        #                     patch_query_template.__call__)
        #
        # patch_template = PatchCall(topic)
        # monkeypatch.setattr(
        #     XSPEC_NOTE.SpecNote, '__call__', patch_template.__call__)
        # # Test
        # target.on_new_topic(None, None)
        # assert patch_place.called
        # assert patch_query_template.called
        # assert patch_template.called
        # id_visible = target._scenes_topic.show_scene(hex(topic.tag))
        # assert id_visible == hex(topic.tag)
        # topics, i_new = target._cursor_topics.get_selected()
        # assert PATH_EXPECT == gtk_model.get_string_from_iter(i_new)
        # topic_new = AOUTLINE.get_item_gtk(topics, i_new)
        # assert topic_new is topic
        # # Teardown
        # target._window.destroy()
        # del target._window
        # del factsheet

    @pytest.mark.skip
    def test_on_new_topic_cancel_place(
            self, patch_factsheet, capfd, monkeypatch):
        """| Confirm response to request to specify topic.
        | Case: user cancels placement.

        :param capfd: built-in fixture `Pytest capfd`_.
        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # # Setup
        # factsheet = patch_factsheet()
        # target = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)
        #
        # sheets_active = CPOOL.PoolSheets()
        # control = CSHEET.ControlSheet.new(sheets_active)
        # target.link_factsheet(target, control)
        # gtk_model = target._view_topics.gtk_view.get_model()
        # _index = gtk_model.append(None)
        #
        # patch_place = PatchCall(None)
        # monkeypatch.setattr(
        #     QPLACE.QueryPlace, '__call__', patch_place.__call__)
        #
        # patch_query_template = PatchCall(None)
        # monkeypatch.setattr(QTEMPLATE.QueryTemplate, '__call__',
        #                     patch_query_template.__call__)
        #
        # class PatchInsert:
        #     def __init__(self): self.called = False
        #
        #     def insert_topic_child(self, _t, _a): self.called = True
        #
        # patch_insert = PatchInsert()
        # monkeypatch.setattr(CSHEET.ControlSheet, 'insert_topic_child',
        #                     patch_insert.insert_topic_child)
        # # Test
        # target.on_new_topic(None, None)
        # assert not patch_query_template.called
        # # Teardown
        # target._window.destroy()
        # del target._window
        # del factsheet

    @pytest.mark.skip
    def test_on_new_topic_cancel_template(
            self, patch_factsheet, capfd, monkeypatch):
        """| Confirm response to request to specify topic.
        | Case: user cancels template selection.

        :param capfd: built-in fixture `Pytest capfd`_.
        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.

        """
        # # Setup
        # factsheet = patch_factsheet()
        # target = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)
        #
        # sheets_active = CPOOL.PoolSheets()
        # control = CSHEET.ControlSheet.new(sheets_active)
        # target.link_factsheet(target, control)
        #
        # patch_query_template = PatchCall(None)
        # monkeypatch.setattr(QTEMPLATE.QueryTemplate, '__call__',
        #                     patch_query_template.__call__)
        # # Test
        # target.on_new_topic(None, None)
        # # Return from call shows guard against template = None
        # # Teardown
        # target._window.destroy()
        # del target._window
        # del factsheet

    @pytest.mark.skip
    def test_on_new_topic_cancel_topic(
            self, patch_factsheet, capfd, monkeypatch):
        """| Confirm response to request to specify topic.
        | Case: user cancels topic specification.

        :param capfd: built-in fixture `Pytest capfd`_.
        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # # Setup
        # factsheet = patch_factsheet()
        # target = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)
        #
        # sheets_active = CPOOL.PoolSheets()
        # control = CSHEET.ControlSheet.new(sheets_active)
        # target.link_factsheet(target, control)
        #
        # query_template = target._query_template
        # outline = query_template._outline
        # model = outline.gtk_view.get_model()
        # i_first = model.get_iter_first()
        # template = AOUTLINE.get_item_gtk(model, i_first)
        #
        # patch_query_template = PatchCall(template)
        # monkeypatch.setattr(QTEMPLATE.QueryTemplate, '__call__',
        #                     patch_query_template.__call__)
        #
        # patch_template = PatchCall(None)
        # monkeypatch.setattr(
        #     XSPEC_NOTE.SpecNote, '__call__', patch_template.__call__)
        #
        # class PatchInsert:
        #     def __init__(self): self.called = False
        #
        #     def insert_topic_child(self, _t, _a): self.called = True
        #
        # patch_insert = PatchInsert()
        # monkeypatch.setattr(CSHEET.ControlSheet, 'insert_topic_child',
        #                     patch_insert.insert_topic_child)
        # # Test
        # target.on_new_topic(None, None)
        # assert not patch_insert.called
        # # Teardown
        # target._window.destroy()
        # del target._window
        # del factsheet

    @pytest.mark.skip
    def test_on_open_sheet_apply(self, tmp_path, patch_dialog_choose,
                                 monkeypatch, patch_factsheet, capfd):
        """Confirm open from file.
        Case: apply open.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param capfd: built-in fixture `Pytest capfd`_.
        """
        # # Setup
        # PATH = Path(tmp_path / 'factsheet.fsg')
        # patch_dialog = patch_dialog_choose(
        #     Gtk.ResponseType.APPLY, str(PATH))
        # monkeypatch.setattr(
        #     Gtk.FileChooserDialog, 'get_filename', patch_dialog.get_filename)
        # monkeypatch.setattr(
        #     Gtk.FileChooserDialog, 'hide', patch_dialog.hide)
        # monkeypatch.setattr(
        #     Gtk.FileChooserDialog, 'run', patch_dialog.run)
        #
        # class PatchPageSheet:
        #     def __init__(self):
        #         self.called = False
        #         self.app = None
        #         self.path = None
        #
        #     def open_factsheet(self, p_app, p_pool, p_path):
        #         self.called = True
        #         self.app = p_app
        #         self.path = p_path
        #         return CSHEET.ControlSheet(p_pool)
        #
        # patch_page = PatchPageSheet()
        # monkeypatch.setattr(
        #     VSHEET.ViewSheet, 'open_factsheet', patch_page.open_factsheet)
        #
        # factsheet = patch_factsheet()
        # target = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)
        #
        # sheets_active = CPOOL.PoolSheets()
        # control = CSHEET.ControlSheet.new(sheets_active)
        # target.link_factsheet(target, control)
        # # Test
        # target.on_open_sheet(None, None)
        # assert patch_dialog.called_run
        # assert patch_dialog.called_hide
        # assert patch_page.called
        # assert factsheet == patch_page.app
        # assert PATH == patch_page.path
        # # Teardown
        # target._window.destroy()
        # del target._window
        # del factsheet

    @pytest.mark.skip
    def test_on_open_sheet_cancel(self, tmp_path, patch_dialog_choose,
                                  monkeypatch, patch_factsheet, capfd):
        """Confirm open from file.
        Case: cancel open.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param capfd: built-in fixture `Pytest capfd`_.
        """
        # # Setup
        # PATH = Path(tmp_path / 'factsheet.fsg')
        # patch_dialog = patch_dialog_choose(
        #     Gtk.ResponseType.CANCEL, str(PATH))
        # monkeypatch.setattr(
        #     Gtk.FileChooserDialog, 'hide', patch_dialog.hide)
        # monkeypatch.setattr(
        #     Gtk.FileChooserDialog, 'run', patch_dialog.run)
        #
        # class PatchPageSheet:
        #     def __init__(self):
        #         self.called = False
        #         self.app = None
        #         self.path = None
        #
        #     def open_factsheet(self, p_app, p_path):
        #         self.called = True
        #         self.app = p_app
        #         self.path = p_path
        #         return CSHEET.ControlSheet()
        #
        # patch_page = PatchPageSheet()
        # monkeypatch.setattr(
        #     VSHEET.ViewSheet, 'open_factsheet', patch_page.open_factsheet)
        #
        # factsheet = patch_factsheet()
        # target = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)
        # # Test
        # target.on_open_sheet(None, None)
        # assert patch_dialog.called_run
        # assert patch_dialog.called_hide
        # assert not patch_page.called
        # # Teardown
        # target._window.destroy()
        # del target._window
        # del factsheet

    def test_on_open_view_sheet(self):
        """Confirm view created and added to control."""
        # Setup
        control = CSHEET.g_control_app.open_factsheet(p_path=None)
        target = VSHEET.ViewSheet(p_control=control)
        roster_views = control._roster_views
        N_VIEWS = 2
        # Test
        target.on_open_view_sheet(None, None)
        assert N_VIEWS == len(roster_views)
        _ = roster_views.pop(CSHEET.id_view_sheet(p_view_sheet=target))
        key_new, view_new = roster_views.popitem()
        assert key_new == CSHEET.id_view_sheet(view_new)
        assert isinstance(view_new, VSHEET.ViewSheet)
        assert view_new._control is control

    @pytest.mark.skip
    def test_on_save_sheet(self, patch_factsheet, capfd, tmp_path):
        """Confirm save to file.
        Case: file path defined.

        :param capfd: built-in fixture `Pytest capfd`_.
        """
        # # Setup
        # factsheet = patch_factsheet()
        # target = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)
        #
        # sheets_active = CPOOL.PoolSheets()
        # control = CSHEET.ControlSheet.new(sheets_active)
        # target.link_factsheet(target, control)
        # PATH = Path(tmp_path / 'saved_factsheet.fsg')
        # control._path = PATH
        # assert not control._path.exists()
        # # Test
        # target.on_save_sheet(None, None)
        # assert control._path.exists()
        # # Teardown
        # target._window.destroy()
        # del target._window
        # del factsheet

    @pytest.mark.skip
    def test_on_save_sheet_none(self, monkeypatch, patch_factsheet, capfd):
        """Confirm save to file.
        Case: file path undefined.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param capfd: built-in fixture `Pytest capfd`_.
        """
        # # Setup
        # class PatchSaveAs:
        #     def __init__(self): self.called = False
        #
        #     def on_save_as_sheet(self, *_a): self.called = True
        #
        # patch_save_as = PatchSaveAs()
        # monkeypatch.setattr(VSHEET.ViewSheet, 'on_save_as_sheet',
        #                     patch_save_as.on_save_as_sheet)
        #
        # factsheet = patch_factsheet()
        # target = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)
        #
        # sheets_active = CPOOL.PoolSheets()
        # control = CSHEET.ControlSheet.new(sheets_active)
        # target.link_factsheet(target, control)
        # control._path = None
        # # Test
        # target.on_save_sheet(None, None)
        # assert patch_save_as.called
        # # Teardown
        # target._window.destroy()
        # del target._window
        # del factsheet

    @pytest.mark.skip
    def test_on_save_as_sheet_apply(self, tmp_path, patch_dialog_choose,
                                    monkeypatch, patch_factsheet, capfd):
        """Confirm save to file with path set.
        Case: apply save.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param capfd: built-in fixture `Pytest capfd`_.
        """
        # # Setup
        # PATH_NEW = Path(tmp_path / 'new_factsheet.fsg')
        # patch_dialog = patch_dialog_choose(
        #     Gtk.ResponseType.APPLY, str(PATH_NEW))
        # monkeypatch.setattr(
        #     Gtk.FileChooserDialog, 'hide', patch_dialog.hide)
        # monkeypatch.setattr(
        #     Gtk.FileChooserDialog, 'get_filename', patch_dialog.get_filename)
        # monkeypatch.setattr(
        #     Gtk.FileChooserDialog, 'run', patch_dialog.run)
        # monkeypatch.setattr(
        #     Gtk.FileChooserDialog, 'set_current_name',
        #     patch_dialog.set_current_name)
        # monkeypatch.setattr(Gtk.FileChooserDialog, 'set_filename',
        #                     patch_dialog.set_filename)
        #
        # factsheet = patch_factsheet()
        # target = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)
        #
        # sheets_active = CPOOL.PoolSheets()
        # control = CSHEET.ControlSheet.new(sheets_active)
        # target.link_factsheet(target, control)
        # PATH_OLD = Path(tmp_path / 'old_factsheet.fsg')
        # control._path = PATH_OLD
        # # Test
        # target.on_save_as_sheet(None, None)
        # assert patch_dialog.called_set_filename
        # assert not patch_dialog.called_set_current_name
        # assert patch_dialog.called_run
        # assert patch_dialog.called_hide
        # assert patch_dialog.called_get_filename
        # assert PATH_NEW == target._control.path
        # assert control._path.exists()
        # # Teardown
        # target._window.destroy()
        # del target._window
        # del factsheet

    @pytest.mark.skip
    def test_on_save_as_sheet_cancel(self, tmp_path, patch_dialog_choose,
                                     monkeypatch, patch_factsheet, capfd):
        """Confirm save to file with path set.
        Case: cancel save.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param capfd: built-in fixture `Pytest capfd`_.
        """
        # # Setup
        # PATH = Path(tmp_path / 'save_as_factsheet.fsg')
        # patch_dialog = patch_dialog_choose(
        #     Gtk.ResponseType.CANCEL, str(PATH))
        # monkeypatch.setattr(
        #     Gtk.FileChooserDialog, 'hide', patch_dialog.hide)
        # monkeypatch.setattr(
        #     Gtk.FileChooserDialog, 'get_filename', patch_dialog.get_filename)
        # monkeypatch.setattr(
        #     Gtk.FileChooserDialog, 'run', patch_dialog.run)
        # monkeypatch.setattr(
        #     Gtk.FileChooserDialog, 'set_current_name',
        #     patch_dialog.set_current_name)
        # monkeypatch.setattr(Gtk.FileChooserDialog, 'set_filename',
        #                     patch_dialog.set_filename)
        #
        # factsheet = patch_factsheet()
        # target = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)
        # target._window.hide()
        #
        # sheets_active = CPOOL.PoolSheets()
        # control = CSHEET.ControlSheet.new(sheets_active)
        # target.link_factsheet(target, control)
        # control._path = None
        # # Test
        # target.on_save_as_sheet(None, None)
        # assert not patch_dialog.called_set_filename
        # assert patch_dialog.called_set_current_name
        # assert patch_dialog.called_run
        # assert patch_dialog.called_hide
        # assert not patch_dialog.called_get_filename
        # assert target._control.path is None
        # # Teardown
        # target._window.destroy()
        # del target._window
        # del factsheet

    def test_on_show_dialog(self, monkeypatch, gtk_app_window):
        """Confirm handler displays dialog.

        See manual tests for dialog content checks.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param gtk_app_window: fixture :func:`.gtk_app_window`.
        """
        # Setup
        control = CSHEET.g_control_app.open_factsheet(p_path=None)
        target = VSHEET.ViewSheet(p_control=control)
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)

        class PatchRun:
            def __init__(self): self.called = False

            def run(self): self.called = True

        patch = PatchRun()
        monkeypatch.setattr(Gtk.Dialog, 'run', patch.run)

        dialog = Gtk.Dialog()
        parent = gtk_app_window
        dialog.set_transient_for(parent)
        dialog.set_visible(True)
        # Test
        target.on_show_dialog(None, None, dialog)
        assert dialog.get_transient_for() is None
        assert patch.called
        assert not dialog.is_visible()

    @pytest.mark.skip
    def test_on_toggle_search_field_inactive(self, patch_factsheet, capfd):
        """| Confirm search field set.
        | Case: button inactive.

        :param capfd: built-in fixture `Pytest capfd`_.
        """
        # # Setup
        # factsheet = patch_factsheet()
        # target_page = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target_page._window.set_skip_pager_hint(True)
        # target_page._window.set_skip_taskbar_hint(True)
        #
        # target = target_page._view_topics
        # SEARCH_ALL = ~ASHEET.FieldsTopic.VOID
        # target.scope_search = SEARCH_ALL
        # button = Gtk.ToggleButton(active=False)
        # # Test
        # target_page.on_toggle_search_field(button, ASHEET.FieldsTopic.NAME)
        # assert not target.scope_search & ASHEET.FieldsTopic.NAME
        # assert target.scope_search & ASHEET.FieldsTopic.TITLE
        # # Teardown
        # target_page._window.destroy()
        # del target_page._window
        # del factsheet

    @pytest.mark.skip
    def test_on_toggle_search_field_active(self, patch_factsheet, capfd):
        """| Confirm search field set.
        | Case: button inactive.

        :param capfd: built-in fixture `Pytest capfd`_.
        """
        # # Setup
        # factsheet = patch_factsheet()
        # target_page = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target_page._window.set_skip_pager_hint(True)
        # target_page._window.set_skip_taskbar_hint(True)
        #
        # target = target_page._view_topics
        # SEARCH_NONE = ASHEET.FieldsTopic.VOID
        # target.scope_search = SEARCH_NONE
        # button = Gtk.ToggleButton(active=True)
        # # Test - not active
        # target_page.on_toggle_search_field(button, ASHEET.FieldsTopic.TITLE)
        # assert target.scope_search & ASHEET.FieldsTopic.TITLE
        # assert not target.scope_search & ASHEET.FieldsTopic.NAME
        # # Teardown
        # target_page._window.destroy()
        # del target_page._window
        # del factsheet

    @pytest.mark.skip
    def test_open_factsheet(
            self, monkeypatch, patch_factsheet, capfd, tmp_path):
        """Confirm factsheet creation from file.
        Case: factsheet is not open.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param capfd: built-in fixture `Pytest capfd`_.
        """
        # # Setup
        # def patch_open(p_pool, p_path):
        #     sheets_active = CPOOL.PoolSheets()
        #     control = CSHEET.ControlSheet(sheets_active)
        #     control._model = MSHEET.Sheet()
        #     control._path = p_path
        #     control._sheets_active = p_pool
        #     return control
        #
        # monkeypatch.setattr(CSHEET.ControlSheet, 'open', patch_open)
        # factsheet = patch_factsheet()
        #
        # PATH = Path(tmp_path / 'factsheet.fsg')
        # sheets_active = CPOOL.PoolSheets()
        # # Test
        # target = VSHEET.ViewSheet.open_factsheet(
        #     factsheet, sheets_active, PATH)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)
        #
        # assert isinstance(target, VSHEET.ViewSheet)
        # assert target._window.get_application() is factsheet
        # control = target._control
        # assert isinstance(control, CSHEET.ControlSheet)
        # # Teardown
        # target._window.destroy()
        # del target._window
        # del factsheet

    @pytest.mark.skip
    def test_open_factsheet_active(
            self, monkeypatch, patch_factsheet, capfd, tmp_path):
        """Confirm factsheet creation from file.
        Case: factsheet is open.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param capfd: built-in fixture `Pytest capfd`_.
        """
        # # Setup
        # class PatchPresentFactsheet:
        #     def __init__(self): self.called = False
        #
        #     def present_factsheet(self, _time): self.called = True
        #
        # patch_present = PatchPresentFactsheet()
        # monkeypatch.setattr(CSHEET.ControlSheet, 'present_factsheet',
        #                     patch_present.present_factsheet)
        #
        # PATH_MISS = Path(tmp_path / 'miss.fsg')
        # PATH_NONE = None
        # PATH_HIT = Path(tmp_path / 'hit.fsg')
        # paths = [PATH_MISS, PATH_NONE, PATH_HIT]
        #
        # sheets_active = CPOOL.PoolSheets()
        # for path in paths:
        #     control = CSHEET.ControlSheet.new(sheets_active)
        #     control._path = path
        #
        # factsheet = patch_factsheet()
        # # Test
        # target = VSHEET.ViewSheet.open_factsheet(
        #     factsheet, sheets_active, PATH_HIT)
        # assert target is None
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert not snapshot.err
        # assert patch_present.called
        # # Teardown
        # # None - no window created

    @pytest.mark.skip
    def test_present(self, patch_factsheet, capfd):
        """Confirm page becomes visible.

        :param capfd: built-in fixture `Pytest capfd`_.
        """
        # # Setup
        # factsheet = patch_factsheet()
        # target = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)
        #
        # sheets_active = CPOOL.PoolSheets()
        # control = CSHEET.ControlSheet.new(sheets_active)
        # target.link_factsheet(target, control)
        # target._window.hide()
        # # Test
        # target.present(Gdk.CURRENT_TIME)
        # assert target._window.get_visible()
        # # Teardown
        # target._window.destroy()
        # del target._window
        # del factsheet

    @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
        ['_window', 'window'],
        ])
    def test_property(self, NAME_ATTR, NAME_PROP):
        """Confirm properties are get-only.

        #. Case: get
        #. Case: no set
        #. Case: no delete

        :param NAME_ATTR: name of attribute.
        :param NAME_PROP: name of property.
        """
        # Setup
        control = CSHEET.g_control_app.open_factsheet(p_path=None)
        target = VSHEET.ViewSheet(p_control=control)
        value_attr = getattr(target, NAME_ATTR)
        target_prop = getattr(VSHEET.ViewSheet, NAME_PROP)
        value_prop = getattr(target, NAME_PROP)
        # Test: read
        assert target_prop.fget is not None
        assert value_attr is value_prop
        # Test: no replace
        assert target_prop.fset is None
        # Test: no delete
        assert target_prop.fdel is None

    @pytest.mark.skip
    def test_set_title(self, patch_factsheet, capfd):
        """Confirm window title update.

        :param capfd: built-in fixture `Pytest capfd`_.
        """
        # # Setup
        # factsheet = patch_factsheet()
        # target = VSHEET.ViewSheet(px_app=factsheet)
        # snapshot = capfd.readouterr()   # Resets the internal buffer
        # assert not snapshot.out
        # assert 'Gtk-CRITICAL' in snapshot.err
        # assert 'GApplication::startup signal' in snapshot.err
        # # target._window.set_skip_pager_hint(True)
        # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(WINDOW_ANCHOR)
        #
        # TITLE = 'The Larch'
        # entry_name = target._infoid.get_view_name()
        # entry_name.set_text(TITLE)
        # SUBTITLE = 'larch.fsg (ABE:123)'
        # # Test
        # target.set_titles(SUBTITLE)
        # headerbar = target._window.get_titlebar()
        # assert TITLE == headerbar.get_title()
        # assert SUBTITLE == headerbar.get_subtitle()
        # # Teardown
        # target._window.destroy()
        # del target._window
        # del factsheet

    @pytest.mark.is_stale(is_stale=False)
    def test_on_delete_sheet_safe(self, patch_is_stale):
        """| Confirm attempt to erase factsheetsheet.
        | Case: no loss of unsaved changes

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        control = CSHEET.g_control_app.open_factsheet(p_path=None)
        id_control = CSHEET.id_factsheet(p_control_sheet=control)
        target = VSHEET.ViewSheet(p_control=control)
        # Test
        target.on_delete_sheet(None, None)
        assert patch_is_stale.called
        assert not control._roster_views
        assert id_control not in CSHEET.g_control_app._roster_sheets

    @pytest.mark.is_stale(is_stale=True)
    def test_on_delete_sheet_unsafe_allow(self, patch_is_stale, monkeypatch):
        """| Confirm attempt to close factsheet.
        | Case: user allows loss of unsaved changes

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        monkeypatch.setattr(
            Gtk.Dialog, 'run', lambda _s: Gtk.ResponseType.APPLY)
        control = CSHEET.g_control_app.open_factsheet(p_path=None)
        id_control = CSHEET.id_factsheet(p_control_sheet=control)
        target = VSHEET.ViewSheet(p_control=control)
        # Test
        target.on_delete_sheet(None, None)
        assert patch_is_stale.called
        assert not control._roster_views
        assert id_control not in CSHEET.g_control_app._roster_sheets

    @pytest.mark.is_stale(is_stale=True)
    def test_on_delete_sheet_unsafe_deny(self, patch_is_stale, monkeypatch):
        """| Confirm attempt to close factsheet.
        | Case: user denies loss of unsaved changes

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        monkeypatch.setattr(
            Gtk.Dialog, 'run', lambda _s: Gtk.ResponseType.CANCEL)
        control = CSHEET.g_control_app.open_factsheet(p_path=None)
        id_control = CSHEET.id_factsheet(p_control_sheet=control)
        target = VSHEET.ViewSheet(p_control=control)
        id_target = CSHEET.id_view_sheet(p_view_sheet=target)
        # Test
        target.on_delete_sheet(None, None)
        assert patch_is_stale.called
        assert control._roster_views[id_target] is target
        assert CSHEET.g_control_app._roster_sheets[id_control] is control
