"""
Unit tests for class to display Factsheet document.  See
:mod:`.view_sheet`.

.. include:: /test/refs_include_pytest.txt
"""
import logging
# import math
from pathlib import Path
import pytest   # type: ignore[import]

import factsheet.bridge_ui as BUI
# from factsheet.content.note import spec_note as XSPEC_NOTE
import factsheet.control.control_sheet as CSHEET
# import factsheet.model.sheet as MSHEET
import factsheet.model.sheet as MSHEET
# from factsheet.model import topic as MTOPIC
# from factsheet.view import query_place as QPLACE
# from factsheet.view import query_template as QTEMPLATE
# import factsheet.view.view_markup as VMARKUP
import factsheet.view.view_sheet as VSHEET
# from factsheet.view import scenes as VSCENES
# from factsheet.view import form_topic as VTOPIC
# from factsheet.view import types_view as VTYPES
# from factsheet.view import ui as UI
# from factsheet.view import view_infoid as VINFOID

import gi
# gi.require_version('Gdk', '3.0')
# from gi.repository import Gdk   # noqa: E402
from gi.repository import GObject as GO  # noqa: E402
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # noqa: E402
# from gi.repository import Pango  # noqa: E402


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
    gtk_window.close()


@pytest.fixture
def patch_dialog_choose(monkeypatch, request):
    """Pytest fixture returns stub
    `GtkFileChooserDialog <GtkFileChooserDialog_>`_.

    :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
    :param request: built-in fixture `Pytest request`_.

    .. _GtkFileChooserDialog: https://lazka.github.io/pgi-docs/
       #Gtk-3.0/classes/FileChooserDialog.html
    """
    class PatchDialog:
        def __init__(self):
            marker = request.node.get_closest_marker('dialog_choose')
            suggest = None
            response = Gtk.ResponseType.NONE
            if marker is not None:
                try:
                    suggest = marker.kwargs['suggest']
                except KeyError:
                    pass
                try:
                    response = marker.kwargs['response']
                except KeyError:
                    pass

            self.called_get_filename = False
            self.called_hide = False
            self.called_run = False
            self.called_set_current_name = False
            self.called_set_filename = False
            self.filename = None
            self.path_suggest = suggest
            self.response = response

        def get_filename(self):
            self.called_get_filename = True
            return self.filename

        def hide(self):
            self.called_hide = True

        def run(self):
            self.called_run = True
            return self.response

        def set_current_name(self, _n):
            self.called_set_current_name = True

        def set_filename(self, p_filename):
            self.filename = p_filename
            self.called_set_filename = True

    dialog = PatchDialog()
    monkeypatch.setattr(
        Gtk.FileChooserDialog, 'get_filename', dialog.get_filename)
    monkeypatch.setattr(
        Gtk.FileChooserDialog, 'hide', dialog.hide)
    monkeypatch.setattr(
        Gtk.FileChooserDialog, 'run', dialog.run)
    monkeypatch.setattr(
        Gtk.FileChooserDialog, 'set_current_name', dialog.set_current_name)
    monkeypatch.setattr(
        Gtk.FileChooserDialog, 'set_filename', dialog.set_filename)

    return dialog


@pytest.fixture(autouse=True)
def patch_g_control_app():
    """Pytest fixture with teardown: Reset :data:`.g_control_app`."""
    CSHEET.g_control_app = CSHEET.ControlApp()
    yield CSHEET.g_control_app
    control_app = CSHEET.g_control_app
    for sheet in control_app._roster_sheets.values():
        for view in sheet._roster_views.values():
            view._window.close()
            del view._window
        sheet._roster_views.clear()
    control_app._roster_sheets.clear()
    CSHEET.g_control_app = CSHEET.ControlApp()


@pytest.fixture
def patch_get_path(request, monkeypatch, tmp_path):
    """Pytest fixture: patch :meth:`.ViewSheet.get_path` to return value
    set with pytest mark.

    :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
    :param request: built-in fixture `Pytest request`_.
    :param tmp_path: built-in fixture `Pytest tmp_path`_.
    """
    marker = request.node.get_closest_marker("get_path")
    cancel = True
    if marker is not None:
        try:
            cancel = marker.kwargs['cancel']
        except KeyError:
            pass

    if cancel:
        path = None
    else:
        path = Path(tmp_path / 'Parrot.fsg')
    monkeypatch.setattr(
        VSHEET.ViewSheet, 'get_path', lambda _s, _a, _p: path)
    return path


@pytest.fixture
def patch_is_stale(monkeypatch, request):
    """Pytest fixture: patch :meth:`.Sheet.is_stale` to return value set
    with pytest mark.

    :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
    :param request: built-in fixture `Pytest request`_.
    """
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


class PatchSetApp:
    """Patch for
    `Gtk.ApplicationWindow.set_application <set_application_>`_.

    Tests cannot complete `Gtk.Application`_ setup in the test
    environment.  This class and fixture :func:`patch_set_app` patch
    around the incomplete setup.

    .. _`Gtk.Application`: https://lazka.github.io/pgi-docs/
       #Gtk-3.0/classes/Application.html

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
    """Pytest fixture: prevents call to
    `Gtk.ApplicationWindow.set_application <set_application_>`_ in test
    environment.

    :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
    """
    patch = PatchSetApp()
    monkeypatch.setattr(Gtk.Window, 'set_application', patch.set_application)
    return patch


class TestAppFactsheet:
    """Unit tests for :class:`~.view_sheet.AppFactsheet`."""

    def test_do_activate(self, monkeypatch):
        """Confirm activation with initial window.

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
        """Confirm extension of application shutdown.

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
        """Confirm extension of application startup.

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

    def test_init(self):
        """Confirm initialization."""
        # Setup
        app_id = 'com.novafolks.factsheet'
        # Test
        target = VSHEET.AppFactsheet()
        assert isinstance(target, Gtk.Application)
        assert app_id == target.get_application_id()
        assert not target.get_windows()


class TestNewDialogWarn:
    """Unit tests for :func:`.new_dialog_warn_loss`."""

    def test_new_dialog_warn_loss(self, gtk_app_window):
        """Confirm data loss warning dialog construction.

        :param gtk_app_window: fixture :func:`.gtk_app_window`.
        """
        # Setup
        PARENT = gtk_app_window
        NAME = '<b>Parrot Sketch</b>'
        WARN = ('Factsheet {} contains unsaved changes.  All unsaved'
                ' changes will be discarded if you close.').format(NAME)
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
        """Confirm class defines constants.

        :param NAME: name of constant.
        :param TYPE: type of constant.
        """
        # Setup
        item = getattr(VSHEET.ViewSheet, NAME)
        assert isinstance(item, TYPE)

    def test_init(self, patch_set_app):
        """| Confirm initialization.
        | Case: visual elements.

        :param patch_set_app: fixture :func:`.patch_set_app`.
        """
        # Setup
        patch = patch_set_app
        control = CSHEET.g_control_app.open_factsheet(
            p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
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
        assert not title_window.get_selectable()
        title_window_str = title_window.get_label()
        target_name = target._control.name
        assert target_name == title_window_str

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
        assert target._window.lookup_action('open-sheet') is not None
        assert target._window.lookup_action('new-sheet') is not None
        assert target._window.lookup_action('save-sheet') is not None
        assert target._window.lookup_action('save-as-sheet') is not None
        #
        # # Factsheet Menu
        # assert target._window.lookup_action('show-help-sheet') is not None
        #
        # # Factsheet Display Menu
        # assert target._window.lookup_action('flip-summary') is not None
        assert target._window.lookup_action('open-view-sheet') is not None
        assert target._window.lookup_action('close-view-sheet') is not None
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
        # assert target._window.lookup_action('go-first') is not None
        # assert target._window.lookup_action('go-last') is not None
        # assert target._window.lookup_action('delete-topic') is not None
        # assert target._window.lookup_action('clear-topics') is not None
        # assert target._window.lookup_action('show-help-topics') is not None
        #
        # assert not target._close_window
        assert target._window.is_visible()

    @pytest.mark.parametrize('NAME_HELPER', [
        '_init_name_sheet',
        '_init_summary_sheet',
        '_init_title_sheet',
        '_init_topics',
        ])
    def test_init_helpers(self, NAME_HELPER, monkeypatch, patch_set_app):
        """| Confirm initialization.
        | Case: helper function calls.

        :param NAME_HELPER: name of helper under test.
        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param patch_set_app: fixture :func:`.patch_set_app`.
        """
        # Setup
        class PatchHelper:
            def __init__(self):
                self.called = False
                self.name_get = 'Oops'

            def helper(self, p_get_object):
                self.called = True
                self.name_get = p_get_object.__name__

        patch_helper = PatchHelper()
        monkeypatch.setattr(
            VSHEET.ViewSheet, NAME_HELPER, patch_helper.helper)

        patch = patch_set_app
        control = CSHEET.g_control_app.open_factsheet(
            p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
        NAME_GET = 'get_object'
        # Test
        _target = VSHEET.ViewSheet(p_control=control)
        assert patch.called
        assert patch_helper.called
        assert NAME_GET == patch_helper.name_get

    @pytest.mark.parametrize('ACTION', [
        'show-about-app',
        'show-help-app',
        'show-intro-app',
        ])
    def test_init_app_menu(self, ACTION):
        """| Confirm initialization.
        | Case: definition of app menu actions

        :param ACTION: name of action to show menu item.
        """
        # Setup
        control = CSHEET.g_control_app.open_factsheet(
            p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
        target = VSHEET.ViewSheet(p_control=control)
        # Test
        assert target._window.lookup_action(ACTION) is not None

    @pytest.mark.parametrize('ACTION', [
        'show-help-sheet',
        ])
    def test_init_factsheet_menu(self, ACTION):
        """| Confirm initialization.
        | Case: definition of factsheet menu actions

        :param ACTION: name of action to show menu item.
        """
        # Setup
        control = CSHEET.g_control_app.open_factsheet(
            p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
        target = VSHEET.ViewSheet(p_control=control)
        # Test
        assert target._window.lookup_action(ACTION) is not None

    def test_helper_init_topics(self, monkeypatch):
        """Confirm helper creates topics editor in sheet view.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        class PatchGetObject:
            def __init__(self):
                self.called = False
                self.ui = 'Oops'
                self.ui_view = Gtk.Box()

            def get_object(self, p_ui):
                self.called = True
                self.ui = p_ui
                return self.ui_view

        patch_get_object = PatchGetObject()

        class PatchSite:
            def __init__(self):
                self.clear()

            def clear(self):
                self.called = False
                self.ui_view = None
                self.expand_okay = None
                self.fill_okay = None
                self.n_padding = -1

            def pack_start(
                    self, p_view, p_exapnd_okay, p_fill_okay, p_n_padding):
                self.called = True
                self.ui_view = p_view
                self.expand_okay = p_exapnd_okay
                self.fill_okay = p_fill_okay
                self.n_padding = p_n_padding

        patch_site = PatchSite()
        monkeypatch.setattr(Gtk.Box, 'pack_start', patch_site.pack_start)

        SITE_UI = 'ui_site_topics'
        EXPAND_OKAY = True
        FILL_OKAY = True
        N_PADDING = 0
        control = CSHEET.g_control_app.open_factsheet(
            p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
        target = VSHEET.ViewSheet(p_control=control)
        patch_site.clear()
        # Test
        target._init_topics(patch_get_object.get_object)
        assert patch_get_object.called
        assert SITE_UI == patch_get_object.ui
        assert patch_site.called
        assert isinstance(patch_site.ui_view, Gtk.Frame)
        assert EXPAND_OKAY == patch_site.expand_okay
        assert FILL_OKAY == patch_site.fill_okay
        assert N_PADDING == patch_site.n_padding

    def test_helper_init_summary(self, monkeypatch):
        """Confirm helper creates summary field in sheet view.

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
        control = CSHEET.g_control_app.open_factsheet(
            p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
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

    @pytest.mark.parametrize('HELPER, CONTENT, SITE', [
        ('_init_name_sheet', 'Name', 'ui_site_name_sheet'),
        ('_init_title_sheet', 'Title', 'ui_site_title_sheet'),
        ])
    def test_helper_init_view(self, monkeypatch, HELPER, CONTENT, SITE):
        """Confirm helper creates name and title fields in sheet view.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param HELPER: initialization helper method under test.
        :param CONTENT: name of view type.
        :param SITE: expected locaton for new view.
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

        class PatchViewEditor:
            def __init__(self):
                self.called = False
                self.display = None
                self.editor = 'Oops'
                self.content = ''
                self.ui_view = Gtk.Box()

            def init(self, p_display, p_editor, p_type):
                self.called = True
                self.display = p_display
                self.editor = p_editor
                self.content = p_type

        patch_view = PatchViewEditor()
        monkeypatch.setattr(
            VSHEET.VMARKUP.ViewMarkup, '__init__', patch_view.init)
        monkeypatch.setattr(
            VSHEET.VMARKUP.ViewMarkup, 'ui_view', patch_view.ui_view)

        class PatchSite:
            def __init__(self):
                self.clear()

            def clear(self):
                self.called = False
                self.ui_view = None
                self.expand_okay = None
                self.fill_okay = None
                self.n_padding = 0

            def pack_start(
                    self, p_view, p_exapnd_okay, p_fill_okay, p_n_padding):
                self.called = True
                self.ui_view = p_view
                self.expand_okay = p_exapnd_okay
                self.fill_okay = p_fill_okay
                self.n_padding = p_n_padding

        patch_site = PatchSite()
        monkeypatch.setattr(Gtk.Box, 'pack_start', patch_site.pack_start)

        EXPAND_OKAY = True
        FILL_OKAY = True
        N_PADDING = 6
        control = CSHEET.g_control_app.open_factsheet(
            p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
        view_sheet = VSHEET.ViewSheet(p_control=control)
        patch_site.clear()
        # Test
        target = getattr(view_sheet, HELPER)
        target(patch_get_object.get_object)
        assert patch_view.called
        assert isinstance(patch_view.editor, Gtk.Entry)
        assert isinstance(patch_view.display, Gtk.Label)
        assert CONTENT == patch_view.content
        assert patch_get_object.called
        assert SITE == patch_get_object.site_ui
        assert patch_site.called
        assert patch_view.ui_view is patch_site.ui_view
        assert EXPAND_OKAY == patch_site.expand_okay
        assert FILL_OKAY == patch_site.fill_okay
        assert N_PADDING == patch_site.n_padding

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
        :param NAME_ATTRIBUTE: name of attribute connected to signal.
        :param ORIGIN: GTK class of connected attribute.
        :param N_DEFAULT: number of default handlers
        :param gtk_app_window: fixture :func:`.gtk_app_window`.
        """
        # Setup
        origin_gtype = GO.type_from_name(GO.type_name(ORIGIN))
        signal = GO.signal_lookup(NAME_SIGNAL, origin_gtype)
        control = CSHEET.g_control_app.open_factsheet(
            p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
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
        control = CSHEET.g_control_app.open_factsheet(
            p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
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

        control = CSHEET.g_control_app.open_factsheet(
            p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
        target = VSHEET.ViewSheet(p_control=control)
        # Test
        target.erase()
        assert not target._window.get_visible()
        assert patch_destroy.called

    @pytest.mark.parametrize(
        'NAME_ACT, IS_SET, GET_FILE, SET_CURRENT, SET_FILE', [
            (pytest.param('save', False, False, True, False)),
            (pytest.param('open', False, False, False, False)),
            (pytest.param('create', False, False, False, False)),
            (pytest.param('select', False, False, False, False)),
            (pytest.param('save', False, False, False, True,
                          marks=pytest.mark.dialog_choose(
                              suggest='saved.fsg', response=None))),
            (pytest.param('save', False, False, True, False,
                          marks=pytest.mark.dialog_choose(
                              suggest=None,
                              response=Gtk.ResponseType.CANCEL))),
            (pytest.param('save', True, True, False, True,
                          marks=pytest.mark.dialog_choose(
                              suggest="saved.fsg",
                              response=Gtk.ResponseType.APPLY))),
            ])
    def test_get_path(self, patch_dialog_choose, tmp_path,
                      NAME_ACT, IS_SET, GET_FILE, SET_CURRENT, SET_FILE):
        """| Confirm save to file.
        | Case: file path defined.

        :param patch_dialog_choose: fixture :func:`.patch_dialog_choose`.
        :param tmp_path: built-in fixture `Pytest tmp_path`_.
        :param NAME_ACT: name of dialog box action (Open, Save, etc.).
        :param IS_SET: True when return value should not be None.
        :param GET_FILE: True when method should use path from dialog.
        :param SET_CURRENT: True when method should suggest default file
            name.
        :param SET_FILE: True when method should suggest file name from
            parameter mark.
        """
        # Setup
        dialog = patch_dialog_choose
        path_suggest = None
        if dialog.path_suggest is not None:
            path_suggest = Path(tmp_path / dialog.path_suggest)
        control = CSHEET.g_control_app.open_factsheet(
            p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
        target = VSHEET.ViewSheet(p_control=control)
        ACTIONS = dict(
            save=Gtk.FileChooserAction.SAVE,
            open=Gtk.FileChooserAction.OPEN,
            create=Gtk.FileChooserAction.CREATE_FOLDER,
            select=Gtk.FileChooserAction.SELECT_FOLDER,
            )
        action = ACTIONS[NAME_ACT]
        # Test
        result = target.get_path(p_action=action, p_suggest=path_suggest)
        if IS_SET:
            assert str(path_suggest) == dialog.filename
        else:
            assert result is None
        assert dialog.called_get_filename is GET_FILE
        assert dialog.called_hide
        assert dialog.called_run
        assert dialog.called_set_current_name is SET_CURRENT
        assert dialog.called_set_filename is SET_FILE

    @pytest.mark.parametrize('ACTION', [
        Gtk.FileChooserAction.OPEN,
        Gtk.FileChooserAction.SAVE
        ])
    def test_get_path_action(self, monkeypatch, ACTION):
        """Confirm file chooser dialog consistent with action.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param ACTION: action for file chooser dialog.
        """
        # Setup
        class PatchDialog:
            def __init__(self):
                self.action = None

            def _make_file_chooser(self, p_action):
                self.action = p_action
                raise CSHEET.FactsheetError('Oops!')

        patch_dialog = PatchDialog()
        monkeypatch.setattr(VSHEET.ViewSheet, '_make_file_chooser',
                            patch_dialog._make_file_chooser)
        control = CSHEET.g_control_app.open_factsheet(
            p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
        target = VSHEET.ViewSheet(p_control=control)
        # Test
        with pytest.raises(CSHEET.FactsheetError):
            _path = target.get_path(p_action=ACTION)
        assert ACTION == patch_dialog.action

    @pytest.mark.parametrize('ACTION, LABEL', [
        (Gtk.FileChooserAction.SAVE, 'Save'),
        (Gtk.FileChooserAction.OPEN, 'Open'),
        (Gtk.FileChooserAction.SELECT_FOLDER, 'Select'),
        (Gtk.FileChooserAction.CREATE_FOLDER, 'Create'),
        ])
    def test_make_dialog_file(self, ACTION, LABEL):
        """Confirm construction of dialog for file save and open.

        :param ACTION: dialog box action (Open or Save)
        :param LABEL: response button label
        """
        # Setup
        control = CSHEET.g_control_app.open_factsheet(
            p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
        target = VSHEET.ViewSheet(p_control=control)
        target._window.set_skip_taskbar_hint(True)
        FILTERS = set(['Factsheet', 'Any'])
        # Test
        dialog = target._make_file_chooser(ACTION)
        assert isinstance(dialog, Gtk.FileChooserDialog)
        assert dialog.get_action() is ACTION
        assert dialog.get_transient_for() is target._window
        assert dialog.get_destroy_with_parent()
        if ACTION is Gtk.FileChooserAction.SAVE:
            assert dialog.get_do_overwrite_confirmation()

        button = dialog.get_widget_for_response(Gtk.ResponseType.CANCEL)
        assert 'Cancel' == button.get_label()

        button = dialog.get_widget_for_response(Gtk.ResponseType.APPLY)
        assert LABEL == button.get_label()
        style = button.get_style_context()
        assert style.has_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)

        assert FILTERS == {f.get_name() for f in dialog.list_filters()}

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

    def test_on_close_view_sheet_safe(self, monkeypatch):
        """| Confirm attempt to close view.
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

        control = CSHEET.g_control_app.open_factsheet(
            p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
        target = VSHEET.ViewSheet(p_control=control)
        id_target = CSHEET.id_view_sheet(p_view_sheet=target)
        view_new = VSHEET.ViewSheet(p_control=control)
        roster_views = control._roster_views
        N_VIEWS = 1
        # Test
        result = target.on_close_view_sheet(None, None)
        assert patch_safe.called
        assert VSHEET.ViewSheet.ALLOW_CLOSE == result
        assert N_VIEWS == len(roster_views)
        assert id_target not in roster_views
        # Teardown
        view_new._window.close()

    def test_on_close_view_sheet_unsafe_allow(self, monkeypatch):
        """| Confirm attempt to close view.
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

        control = CSHEET.g_control_app.open_factsheet(
            p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
        target = VSHEET.ViewSheet(p_control=control)
        id_target = CSHEET.id_view_sheet(p_view_sheet=target)
        view_new = VSHEET.ViewSheet(p_control=control)
        roster_views = control._roster_views
        N_VIEWS = 1
        # Test
        result = target.on_close_view_sheet(None, None)
        assert patch_unsafe.called
        assert VSHEET.ViewSheet.ALLOW_CLOSE == result
        assert N_VIEWS == len(roster_views)
        assert id_target not in roster_views
        # Teardown
        view_new._window.close()

    def test_on_close_view_sheet_unsafe_deny(self, monkeypatch):
        """| Confirm attempt to close view.
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

        control = CSHEET.g_control_app.open_factsheet(
            p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
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
        # Teardown
        view_new._window.close()

    @pytest.mark.is_stale(is_stale=False)
    def test_on_delete_sheet_safe(self, patch_is_stale):
        """| Confirm attempt to close factsheet.
        | Case: no loss of unsaved changes

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        control = CSHEET.g_control_app.open_factsheet(
            p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
        id_control = control.tag
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
        control = CSHEET.g_control_app.open_factsheet(
            p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
        id_control = control.tag
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
        control = CSHEET.g_control_app.open_factsheet(
            p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
        id_control = control.tag
        target = VSHEET.ViewSheet(p_control=control)
        id_target = CSHEET.id_view_sheet(p_view_sheet=target)
        # Test
        target.on_delete_sheet(None, None)
        assert patch_is_stale.called
        assert control._roster_views[id_target] is target
        assert CSHEET.g_control_app._roster_sheets[id_control] is control

    def test_on_new_sheet(self, monkeypatch):
        """| Confirm factsheet creation with initial window.
        | Case: creation succeeds

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        monkeypatch.setattr(Gtk.Window, 'show_all', lambda _s: None)
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

    def test_on_new_sheet_fail(self, monkeypatch, caplog):
        """| Confirm factsheet creation with initial window.
        | Case: creation fails.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param caplog: built-in fixture `Pytest caplog`_.
        """
        # Setup
        monkeypatch.setattr(Gtk.Window, 'show_all', lambda _s: None)
        monkeypatch.setattr(
            CSHEET.ControlApp, 'open_factsheet', lambda _c, **_kw: None)
        N_LOGS = 1
        LAST = -1
        log_message = 'Failed to create new factsheet (ViewSheet.on_new_sheet)'
        # Test
        VSHEET.ViewSheet.on_new_sheet(None, None)
        assert N_LOGS == len(caplog.records)
        record = caplog.records[LAST]
        assert log_message == record.message
        assert 'CRITICAL' == record.levelname

    @pytest.mark.get_path(cancel=False)
    def test_on_open_sheet(self, monkeypatch, patch_get_path):
        """| Confirm open from file.
        | Case: open file not in collection of open factsheets.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param patch_get_path: fixture :func:`.patch_get_path`.
        """
        # Setup
        class PatchOpenFactsheet:
            def __init__(self):
                self.called = False
                self.path = None
                self.time = None

            def open_factsheet(self, p_path, p_time):
                self.called = True
                self.time = p_time
                sheet = CSHEET.ControlSheet(p_path=p_path)
                self.id_sheet = sheet.tag
                CSHEET.g_control_app._roster_sheets[self.id_sheet] = sheet
                return sheet

        patch_open = PatchOpenFactsheet()
        monkeypatch.setattr(
            CSHEET.ControlApp, 'open_factsheet', patch_open.open_factsheet)
        control = CSHEET.ControlSheet(p_path=None)
        target = VSHEET.ViewSheet(p_control=control)
        N_VIEWS = 1
        # Test
        target.on_open_sheet(None, None)
        assert patch_open.called
        assert BUI.TIME_EVENT_CURRENT == patch_open.time
        sheet = CSHEET.g_control_app._roster_sheets[patch_open.id_sheet]
        assert sheet.path is patch_get_path
        assert N_VIEWS == len(sheet._roster_views)
        view = next(iter(sheet._roster_views.values()))
        assert isinstance(view, VSHEET.ViewSheet)

    @pytest.mark.get_path(cancel=True)
    def test_on_open_sheet_cancel(self, monkeypatch, patch_get_path):
        """| Confirm open from file.
        | Case: cancel open.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param patch_get_path: fixture :func:`.patch_get_path`.
        """
        # Setup
        class PatchOpenFactsheet:
            def __init__(self):
                self.called = False
                self.path = None
                self.time = None

            def open_factsheet(self, p_path, p_time):
                self.called = True
                self.time = p_time
                sheet = CSHEET.ControlSheet(p_path=p_path)
                # self.id_sheet = CSHEET.id_factsheet(sheet)
                self.id_sheet = sheet.tag
                CSHEET.g_control_app._roster_sheets[self.id_sheet] = sheet
                return sheet

        patch_open = PatchOpenFactsheet()
        monkeypatch.setattr(
            CSHEET.ControlApp, 'open_factsheet', patch_open.open_factsheet)
        control = CSHEET.ControlSheet(p_path=None)
        target = VSHEET.ViewSheet(p_control=control)
        # Test
        target.on_open_sheet(None, None)
        assert not patch_open.called

    @pytest.mark.get_path(cancel=False)
    def test_on_open_sheet_present(self, monkeypatch, patch_get_path):
        """| Confirm open from file.
        | Case: present file already in collection of open factsheets.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param patch_get_path: fixture :func:`.patch_get_path`.
        """
        # Setup
        class PatchOpenFactsheet:
            def __init__(self):
                self.called = False
                self.path = None
                self.time = None

            def open_factsheet(self, p_path, p_time):
                self.called = True
                self.time = p_time
                sheet = CSHEET.ControlSheet(p_path=p_path)
                self.id_sheet = sheet.tag
                CSHEET.g_control_app._roster_sheets[self.id_sheet] = sheet
                return None

        patch_open = PatchOpenFactsheet()
        monkeypatch.setattr(
            CSHEET.ControlApp, 'open_factsheet', patch_open.open_factsheet)
        control = CSHEET.ControlSheet(p_path=None)
        target = VSHEET.ViewSheet(p_control=control)
        N_VIEWS = 0
        # Test
        target.on_open_sheet(None, None)
        assert patch_open.called
        assert BUI.TIME_EVENT_CURRENT == patch_open.time
        sheet = CSHEET.g_control_app._roster_sheets[patch_open.id_sheet]
        assert sheet.path is patch_get_path
        assert N_VIEWS == len(sheet._roster_views)

    def test_on_open_view_sheet(self):
        """Confirm view created and added to control."""
        # Setup
        control = CSHEET.g_control_app.open_factsheet(
            p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
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

    @pytest.mark.get_path(cancel=False)
    def test_on_save_as_sheet(self, patch_get_path):
        """| Confirm file save with save as.
        | Case: user provides file path.

        :param patch_get_path: fixture :func:`.patch_get_path`.
        """
        # Setup
        control = CSHEET.g_control_app.open_factsheet(
            p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
        target = VSHEET.ViewSheet(p_control=control)
        assert not patch_get_path.exists()
        # Test
        target.on_save_as_sheet(None, None)
        assert control.path is patch_get_path
        assert control.path.exists()

    @pytest.mark.get_path(cancel=True)
    def test_on_save_as_sheet_cancel(self, patch_get_path):
        """| Confirm file save with save as.
        | Case: user cancels save.

        :param patch_get_path: fixture :func:`.patch_get_path`.
        """
        # Setup
        control = CSHEET.g_control_app.open_factsheet(
            p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
        target = VSHEET.ViewSheet(p_control=control)
        # Test
        target.on_save_as_sheet(None, None)
        # Successful call makes no state change.

    def test_on_save_sheet(self, tmp_path):
        """| Confirm file save.
        | Case: file path defined.

        :param tmp_path: built-in fixture `Pytest tmp_path`_.
        """
        # Setup
        PATH = Path(tmp_path / 'saved_factsheet.fsg')
        control = CSHEET.g_control_app.open_factsheet(
            p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
        control._path = PATH
        target = VSHEET.ViewSheet(p_control=control)
        assert not control._path.exists()
        # Test
        target.on_save_sheet(None, None)
        assert control.path.exists()

    @pytest.mark.get_path(cancel=True)
    def test_on_save_sheet_cancel(self, patch_get_path):
        """| Confirm file save.
        | Case: no file path and user does not provide one.

        :param patch_get_path: fixture :func:`.patch_get_path`.
        """
        # Setup
        control = CSHEET.g_control_app.open_factsheet(
            p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
        target = VSHEET.ViewSheet(p_control=control)
        # Test
        target.on_save_sheet(None, None)
        # Successful call makes no state change.

    @pytest.mark.get_path(cancel=False)
    def test_on_save_sheet_none(self, patch_get_path):
        """| Confirm save to file.
        | Case: no file path and user provides one.

        :param patch_get_path: fixture :func:`.patch_get_path`.
        """
        # Setup
        control = CSHEET.g_control_app.open_factsheet(
            p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
        target = VSHEET.ViewSheet(p_control=control)
        assert not patch_get_path.exists()
        # Test
        target.on_save_sheet(None, None)
        assert patch_get_path == control.path
        assert control.path.exists()

    def test_on_show_dialog(self, monkeypatch, gtk_app_window):
        """Confirm handler displays dialog.

        See manual tests for dialog content checks.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param gtk_app_window: fixture :func:`.gtk_app_window`.
        """
        # Setup
        control = CSHEET.g_control_app.open_factsheet(
            p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
        target = VSHEET.ViewSheet(p_control=control)

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
    def test_on_toggle_search_field_inactive(self, capfd):
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
    def test_on_toggle_search_field_active(self, capfd):
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

    def test_present(self):
        """Confirm page becomes visible."""
        # Setup
        control = CSHEET.g_control_app.open_factsheet(
            p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
        target = VSHEET.ViewSheet(p_control=control)
        target._window.hide()
        # Test
        target.present(BUI.TIME_EVENT_CURRENT)
        assert target._window.get_visible()

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
        control = CSHEET.g_control_app.open_factsheet(
            p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
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

    @pytest.mark.parametrize('ERROR, CAUSE, TRACE, PRIME, SECOND', [
        (CSHEET.DumpFileError, Exception('No its not.'),
         'Exception: No its not.', 'This parrot is dead!',
         'Error source is Exception: No its not.'),
        (CSHEET.NoFileError, None,
         'Traceback (most recent call last):', 'It is a former parrot.',
         'Error source is Factsheet.')
        ])
    def test_report_error_sheet(
            self, ERROR, CAUSE, TRACE, PRIME, SECOND, monkeypatch, caplog):
        """Confirm dialog and logging for exceptions during file save.

        :param ERROR: sheet error exception.
        :param CAUSE: system exception cause of sheet error.
        :param PRIME: primary text for error dialog.
        :param TRACE: marks start of traceback copied to log.
        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param caplog: built-in fixture `Pytest caplog`_.
        """
        # Setup
        class PatchDialog:
            def __init__(self):
                self.called_destroy = False
                self.called_run = False
                self.called_prime = False
                self.prime = None
                self.called_second = False
                self.second = None

            def destroy(self):
                self.called_destroy = True

            def format_prime(self, p_msg):
                self.prime = p_msg
                self.called_prime = True

            def format_second(self, p_msg):
                self.second = p_msg
                self.called_second = True

            def run(self):
                self.called_run = True

        patch_dialog = PatchDialog()
        monkeypatch.setattr(Gtk.MessageDialog, 'destroy',
                            patch_dialog.destroy)
        monkeypatch.setattr(Gtk.MessageDialog, 'format_secondary_text',
                            patch_dialog.format_second)
        monkeypatch.setattr(Gtk.MessageDialog, 'run', patch_dialog.run)
        monkeypatch.setattr(Gtk.MessageDialog, 'set_markup',
                            patch_dialog.format_prime)

        control = CSHEET.g_control_app.open_factsheet(
            p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
        target = VSHEET.ViewSheet(p_control=control)
        I_PRIME = 0
        I_CAUSE = 1
        I_ERROR = -1
        # Test
        with pytest.raises(ERROR) as exc_info:
            raise ERROR() from CAUSE
        target._report_error_sheet(p_err=exc_info.value, p_message=PRIME)
        assert patch_dialog.called_run
        assert patch_dialog.called_destroy
        assert caplog.records
        log_prime = caplog.records[I_PRIME]
        assert 'ERROR' == log_prime.levelname
        assert PRIME == log_prime.message
        log_cause = caplog.records[I_CAUSE]
        assert 'ERROR' == log_cause.levelname
        print('log_cause: {}'.format(log_cause.message.rstrip('\n')))
        assert log_cause.message.rstrip('\n').endswith(TRACE)
        log_error = caplog.records[I_ERROR]
        assert 'ERROR' == log_error.levelname
        assert log_error.message.rstrip('\n').endswith(ERROR.__name__)
        assert patch_dialog.called_prime
        assert PRIME == patch_dialog.prime
        assert patch_dialog.called_second
        assert SECOND == patch_dialog.second

    @pytest.mark.parametrize('ERROR, PRIME', [
        (CSHEET.BackupFileError,
            'Factsheet not saved! could not make backup.',),
        (CSHEET.DumpFileError, 'Factsheet not saved! could not write file.'),
        (CSHEET.NoFileError, 'Factsheet not saved! no file selected.'),
        (CSHEET.OpenFileError, 'Factsheet not saved! could not open file.'),
        (Exception, 'Factsheet not saved! Application is broken!'),
        ])
    def test_save_sheet_except(self, monkeypatch, ERROR, PRIME, caplog):
        """| Confirm save to file.
        | Case: exceptions.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param ERROR: exception test raises.
        :param PRIME: primary text for notification.
        :param caplog: built-in fixture `Pytest caplog`_.
        """
        # Setup
        monkeypatch.setattr(Gtk.MessageDialog, 'run', lambda _s: None)

        def patch_control_save(_self, _path):
            raise ERROR()

        monkeypatch.setattr(CSHEET.ControlSheet, 'save', patch_control_save)
        control = CSHEET.g_control_app.open_factsheet(
            p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
        target = VSHEET.ViewSheet(p_control=control)
        N_PRIME = 0
        # Test
        target.save_sheet(None)
        assert caplog.records
        log_prime = caplog.records[N_PRIME]
        assert 'ERROR' == log_prime.levelname
        assert PRIME == log_prime.message
