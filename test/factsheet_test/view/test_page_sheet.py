"""
Unit tests for class to display Factsheet document.  See
:mod:`.page_sheet`.
"""
from pathlib import Path
import pytest   # type: ignore[import]

from factsheet.abc_types import abc_outline as ABC_OUTLINE
from factsheet.abc_types import abc_sheet as ABC_SHEET
from factsheet.adapt_gtk import adapt_outline as AOUTLINE
from factsheet.adapt_gtk import adapt_sheet as ASHEET
from factsheet.content.note import note_spec as XNOTE_SPEC
from factsheet.control import pool as CPOOL
from factsheet.control import control_sheet as CSHEET
from factsheet.model import sheet as MSHEET
from factsheet.model import topic as MTOPIC
from factsheet.view import query_place as QPLACE
from factsheet.view import query_template as QTEMPLATE
from factsheet.view import page_sheet as VSHEET
from factsheet.view import scenes as VSCENES
from factsheet.view import pane_topic as VTOPIC
from factsheet.view import types_view as VTYPES
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


class PatchSafe(CSHEET.ControlSheet):
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


WINDOW_ANCHOR = Gtk.Window()


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
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)

        assert target._control is None
        assert isinstance(target._window, Gtk.ApplicationWindow)
        assert target._window.get_application() is factsheet

        # Components
        assert isinstance(target._context_name, Gtk.Popover)
        assert isinstance(target._context_summary, Gtk.Expander)
        assert isinstance(target._flip_summary, Gtk.CheckButton)
        assert isinstance(
            target._view_topics, ABC_OUTLINE.AbstractViewOutline)
        assert target._view_topics.scope_search is ~ASHEET.FieldsTopic.VOID
        assert target._view_topics.gtk_view.get_reorderable()
        assert target._view_topics.gtk_view.get_parent() is not None
        assert isinstance(target._cursor_topics, Gtk.TreeSelection)
        assert isinstance(target._scenes_topic, VSCENES.Scenes)
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
        assert target._window.lookup_action('go-first-topic') is not None
        assert target._window.lookup_action('go-last-topic') is not None
        assert target._window.lookup_action('delete-topic') is not None
        assert target._window.lookup_action('clear-topics') is not None
        assert target._window.lookup_action('show-help-topics') is not None

        assert not target._close_window
        assert target._window.is_visible()
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    @pytest.mark.parametrize(
        'NAME_SIGNAL, NAME_ATTRIBUTE, ORIGIN, N_DEFAULT', [
            ('closed', '_context_name', Gtk.Popover, 0),
            ('delete-event', '_window', Gtk.ApplicationWindow, 0),
            ('changed', '_cursor_topics', Gtk.TreeSelection, 0),
            ])
    def test_init_signals(self, NAME_SIGNAL, NAME_ATTRIBUTE, ORIGIN,
                          N_DEFAULT, patch_factsheet, capfd):
        """Confirm initialization of signal connections."""
        # Setup
        origin_gtype = GO.type_from_name(GO.type_name(ORIGIN))
        signal = GO.signal_lookup(NAME_SIGNAL, origin_gtype)
        factsheet = patch_factsheet()
        # Test
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)

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
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)

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
        """Confirm window of page hidden and closed."""
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
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)
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

    def test_close_topic(self, patch_factsheet, capfd, new_outline_topics):
        """Confirm pane removed from scenes and closed"""
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)
        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.ControlSheet.new(sheets_active)
        target.link_factsheet(target, control)

        outline_topics = new_outline_topics()
        topics = outline_topics._gtk_model
        view = target._view_topics.gtk_view
        view.set_model(topics)
        for index in outline_topics.indices():
            topic = outline_topics.get_item(index)
            control = target._control._add_new_control_topic(topic)
            pane = VTOPIC.PaneTopic(pm_control=control)
            target._scenes_topic.add_scene(
                pane.gtk_pane, hex(topic.id_topic))

        target._cursor_topics.unselect_all()
        PATH_CURRENT = '0:0:0'
        i_remove = topics.get_iter_from_string(PATH_CURRENT)
        topic_remove = AOUTLINE.get_item_gtk(topics, i_remove)
        id_remove = topic_remove.id_topic
        NAME_DEFAULT = 'Default'
        # Test
        target.close_topic(id_remove)
        is_scene = target._scenes_topic.show_scene(hex(id_remove))
        assert NAME_DEFAULT == is_scene
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
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)
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
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)
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
        control = CSHEET.ControlSheet.new(sheets_active)
        page = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        # page._window.set_skip_pager_hint(True)
        page._window.set_skip_taskbar_hint(True)
        # Test
        VSHEET.PageSheet.link_factsheet(page, control)
        assert page._control is control
        model = page._view_topics.gtk_view.get_model()
        assert model is not None
        assert page._query_place is not None
        query_view_topics = page._query_place._view_topics
        assert query_view_topics.gtk_view.get_model() is model
        # Teardown
        page._window.destroy()
        del page._window
        del factsheet

    @pytest.mark.parametrize('ACTION, LABEL', [
        (Gtk.FileChooserAction.SAVE, 'Save'),
        (Gtk.FileChooserAction.OPEN, 'Open'),
        ])
    def test_make_dialog_file(
            self, patch_factsheet, capfd, ACTION, LABEL):
        """Confirm construction of dialog for file save."""
        # Setup
        factsheet = patch_factsheet()
        source = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        # source._window.set_skip_pager_hint(True)
        source._window.set_skip_taskbar_hint(True)
        FILTERS = set(['Factsheet', 'Any'])
        # Test
        target = source._make_dialog_file(ACTION)
        assert isinstance(target, Gtk.FileChooserDialog)
        assert target.get_action() is ACTION
        assert target.get_transient_for() is source._window
        assert target.get_destroy_with_parent()
        if ACTION is Gtk.FileChooserAction.SAVE:
            assert target.get_do_overwrite_confirmation()

        button = target.get_widget_for_response(Gtk.ResponseType.CANCEL)
        assert 'Cancel' == button.get_label()

        button = target.get_widget_for_response(Gtk.ResponseType.APPLY)
        assert LABEL == button.get_label()
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
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)
        assert isinstance(target, VSHEET.PageSheet)
        assert target._window.get_application() is factsheet
        control = target._control
        assert isinstance(control, CSHEET.ControlSheet)
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_new_view_topics(self, patch_factsheet, capfd):
        """ """
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)
        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.ControlSheet.new(sheets_active)
        target.link_factsheet(target, control)

        # Test
        view_new = target.new_view_topics()
        assert isinstance(view_new, VTYPES.ViewOutlineTopics)
        model = target._view_topics.gtk_view.get_model()
        assert view_new.gtk_view.get_model() is model
        # Teardown

    def test_on_changed_cursor(
            self, patch_factsheet, capfd, new_outline_topics):
        """| Confirm updates when current topic changes.
        | Case: change to topic with scene.
        """
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)
        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.ControlSheet.new(sheets_active)
        target.link_factsheet(target, control)

        outline_topics = new_outline_topics()
        topics = outline_topics._gtk_model
        view = target._view_topics.gtk_view
        view.set_model(topics)
        for index in outline_topics.indices():
            topic = outline_topics.get_item(index)
            control = target._control._add_new_control_topic(topic)
            pane = VTOPIC.PaneTopic(pm_control=control)
            target._scenes_topic.add_scene(
                pane.gtk_pane, hex(topic.id_topic))

        view.expand_all()
        PATH_CURRENT = '0:0:0'
        i_current = topics.get_iter_from_string(PATH_CURRENT)
        topic_current = AOUTLINE.get_item_gtk(topics, i_current)
        # Test
        target._cursor_topics.select_iter(i_current)
        id_visible = target._scenes_topic.get_scene_visible()
        assert id_visible == hex(topic_current.id_topic)
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_on_changed_cursor_new(
            self, patch_factsheet, capfd, new_outline_topics):
        """| Confirm updates when current topic changes.
        | Case: change to topic without scene.
        """
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)
        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.ControlSheet.new(sheets_active)
        target.link_factsheet(target, control)

        outline_topics = new_outline_topics()
        topics = outline_topics._gtk_model
        view = target._view_topics.gtk_view
        view.set_model(topics)
        for index in outline_topics.indices():
            topic = outline_topics.get_item(index)
            control = target._control._add_new_control_topic(topic)
            pane = VTOPIC.PaneTopic(pm_control=control)
            target._scenes_topic.add_scene(
                pane.gtk_pane, hex(topic.id_topic))

        view.expand_all()
        PATH_CURRENT = '0:0:0'
        i_current = topics.get_iter_from_string(PATH_CURRENT)
        topic_current = AOUTLINE.get_item_gtk(topics, i_current)
        target._scenes_topic.remove_scene(hex(topic_current.id_topic))
        # Test
        target._cursor_topics.select_iter(i_current)
        topic_visible = target._scenes_topic.get_scene_visible()
        assert topic_visible == hex(topic_current.id_topic)
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_on_changed_cursor_no_control(
            self, patch_factsheet, capfd, new_outline_topics, monkeypatch):
        """| Confirm updates when current topic changes.
        | Case: change to topic without scene.
        """
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)
        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.ControlSheet.new(sheets_active)
        target.link_factsheet(target, control)

        outline_topics = new_outline_topics()
        topics = outline_topics._gtk_model
        view = target._view_topics.gtk_view
        view.set_model(topics)
        for index in outline_topics.indices():
            topic = outline_topics.get_item(index)
            control = target._control._add_new_control_topic(topic)
            pane = VTOPIC.PaneTopic(pm_control=control)
            target._scenes_topic.add_scene(
                pane.gtk_pane, hex(topic.id_topic))

        monkeypatch.setattr(
            CSHEET.ControlSheet, 'get_control_topic', lambda _s, _t: None)

        view.expand_all()
        PATH_INIT = '0'
        i_init = topics.get_iter_from_string(PATH_INIT)
        target._cursor_topics.select_iter(i_init)

        PATH_CURRENT = '0:0:0'
        i_current = topics.get_iter_from_string(PATH_CURRENT)
        topic_current = AOUTLINE.get_item_gtk(topics, i_current)
        target._scenes_topic.remove_scene(hex(topic_current.id_topic))
        NAME_DEFAULT = 'Default'
        # Test
        target._cursor_topics.select_iter(i_current)
        topic_visible = target._scenes_topic.get_scene_visible()
        assert NAME_DEFAULT == topic_visible
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_on_changed_cursor_to_none(
            self, patch_factsheet, capfd, new_outline_topics):
        """| Confirm updates when current topic changes.
        | Case: change to no current topic.
        """
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)
        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.ControlSheet.new(sheets_active)
        target.link_factsheet(target, control)

        outline_topics = new_outline_topics()
        topics = outline_topics._gtk_model
        view = target._view_topics.gtk_view
        view.set_model(topics)
        for index in outline_topics.indices():
            topic = outline_topics.get_item(index)
            control = target._control._add_new_control_topic(topic)
            pane = VTOPIC.PaneTopic(pm_control=control)
            target._scenes_topic.add_scene(
                pane.gtk_pane, hex(topic.id_topic))

        # pane_none = Gtk.Label(label='No pane')
        # target._scenes_topic.add_scene(
        #     pane_none, target._scenes_topic.ID_NONE)

        target._cursor_topics.unselect_all()
        NAME_DEFAULT = 'Default'
        # Test
        target.on_changed_cursor(target._cursor_topics)
        id_visible = target._scenes_topic.get_scene_visible()
        assert NAME_DEFAULT == id_visible
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_on_changed_cursor_no_topic(
            self, patch_factsheet, capfd, new_outline_topics):
        """| Confirm updates when current topic changes.
        | Case: change to a topic is that is None.
        """
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)
        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.ControlSheet.new(sheets_active)
        target.link_factsheet(target, control)

        outline_topics = new_outline_topics()
        topics = outline_topics._gtk_model
        view = target._view_topics.gtk_view
        view.set_model(topics)
        for index in outline_topics.indices():
            topic = outline_topics.get_item(index)
            control = target._control._add_new_control_topic(topic)
            pane = VTOPIC.PaneTopic(pm_control=control)
            target._scenes_topic.add_scene(
                pane.gtk_pane, hex(topic.id_topic))

        view.expand_all()
        PATH_CURRENT = '0:0:0'
        i_current = topics.get_iter_from_string(PATH_CURRENT)
        target._cursor_topics.select_iter(i_current)
        topics[i_current][AOUTLINE.AdaptTreeStore.N_COLUMN_ITEM] = None
        NAME_DEFAULT = 'Default'
        # Test
        target.on_changed_cursor(target._cursor_topics)
        id_visible = target._scenes_topic.get_scene_visible()
        assert NAME_DEFAULT == id_visible
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
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)

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
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)

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
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)

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
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)

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
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)

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
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)

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
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)

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

    def test_on_delete_topic(
            self, monkeypatch, patch_factsheet, capfd, new_outline_topics):
        """| Confirm topic removal.
        | Case: Topic selected.
        """
        # Setup
        class PatchExtract:
            def __init__(self):
                self.called = False
                self.index = None

            def extract_topic(self, p_index):
                self.called = True
                self.index = p_index

        patch_extract = PatchExtract()
        monkeypatch.setattr(
            CSHEET.ControlSheet, 'extract_topic', patch_extract.extract_topic)

        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)

        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.ControlSheet.new(sheets_active)
        target.link_factsheet(target, control)

        outline_topics = new_outline_topics()
        topics = outline_topics._gtk_model
        i_first = topics.get_iter_first()
        path_first = topics.get_string_from_iter(i_first)
        view = target._view_topics.gtk_view
        view.set_model(topics)
        view.expand_all()
        cursor = view.get_selection()
        cursor.select_iter(i_first)
        # Test
        target.on_delete_topic(None, None)
        assert patch_extract.called
        path_target = topics.get_string_from_iter(patch_extract.index)
        assert path_first == path_target
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_on_delete_topic_none(
            self, monkeypatch, patch_factsheet, capfd):
        """| Confirm topic removal.
        | Case: No topic selected.
        """
        # Setup
        class PatchExtract:
            def __init__(self): self.called = False

            def extract_topic(self, _index): self.called = True

        patch_extract = PatchExtract()
        monkeypatch.setattr(
            CSHEET.ControlSheet, 'extract_topic', patch_extract.extract_topic)
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)

        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.ControlSheet.new(sheets_active)
        target.link_factsheet(target, control)
        # Test
        target.on_delete_topic(None, None)
        assert not patch_extract.called
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_on_clear_topics(
            self, monkeypatch, patch_factsheet, capfd):
        # Setup
        class PatchClear:
            def __init__(self): self.called = False

            def clear(self): self.called = True

        patch_clear = PatchClear()
        monkeypatch.setattr(
            CSHEET.ControlSheet, 'clear', patch_clear.clear)
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)

        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.ControlSheet.new(sheets_active)
        target.link_factsheet(target, control)
        # Test
        target.on_clear_topics(None, None)
        assert patch_clear.called
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

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
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)

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
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_on_go_first_topic(
            self, patch_factsheet, capfd, new_outline_topics):
        """| Confirm first topic selection.
        | Case: Topic outline is not empty.
        """
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)
        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.ControlSheet.new(sheets_active)
        target.link_factsheet(target, control)

        outline_topics = new_outline_topics()
        topics = outline_topics._gtk_model
        i_first = topics.get_iter_first()
        path_first = topics.get_path(i_first)
        item_first = AOUTLINE.get_item_gtk(topics, i_first)
        view = target._view_topics.gtk_view
        view.set_model(topics)
        cursor = view.get_selection()
        cursor.unselect_all()
        # Test
        target.on_go_first_topic(None, None)
        model, index = cursor.get_selected()
        assert model is topics
        path_target = model.get_path(index)
        assert path_first == path_target
        item_target = AOUTLINE.get_item_gtk(model, index)
        assert item_target is item_first
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_on_go_first_topic_none(
            self, monkeypatch, patch_factsheet, capfd):
        """| Confirm first topic selection.
        | Case: topic outline is empty.
        """
        # Setup
        class PatchSelect:
            def __init__(self): self.called = False

            def select_iter(self, _index):
                self.called = True

        patch_select = PatchSelect()
        monkeypatch.setattr(
            Gtk.TreeSelection, 'select_iter', patch_select.select_iter)

        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)

        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.ControlSheet.new(sheets_active)
        target.link_factsheet(target, control)
        # Test
        target.on_go_first_topic(None, None)
        assert not patch_select.called
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_on_go_last_topic(
            self, patch_factsheet, capfd, new_outline_topics):
        """| Confirm last topic selection.
        | Case: Topic outline is not empty; last topic is not top level.
        """
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)

        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.ControlSheet.new(sheets_active)
        target.link_factsheet(target, control)

        outline_topics = new_outline_topics()
        topics = outline_topics._gtk_model
        PATH_LAST = '1:1:2'
        i_last = topics.get_iter(PATH_LAST)
        item_last = AOUTLINE.get_item_gtk(topics, i_last)
        view = target._view_topics.gtk_view
        view.set_model(topics)
        cursor = view.get_selection()
        cursor.unselect_all()
        # Test
        target.on_go_last_topic(None, None)
        model, index = cursor.get_selected()
        assert model is topics
        path_target = model.get_string_from_iter(index)
        assert PATH_LAST == path_target
        item_target = AOUTLINE.get_item_gtk(model, index)
        assert item_target is item_last
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_on_go_last_topic_none(
            self, monkeypatch, patch_factsheet, capfd):
        """| Confirm last topic selection.
        | Case: topic outline is empty.
        """
        # Setup
        class PatchSelect:
            def __init__(self): self.called = False

            def select_iter(self, _index):
                self.called = True

        patch_select = PatchSelect()
        monkeypatch.setattr(
            Gtk.TreeSelection, 'select_iter', patch_select.select_iter)

        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)

        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.ControlSheet.new(sheets_active)
        target.link_factsheet(target, control)
        # Test
        target.on_go_last_topic(None, None)
        assert not patch_select.called
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_on_go_last_topic_top(
            self, patch_factsheet, capfd, new_outline_topics):
        """| Confirm last topic selection.
        | Case: Topic outline is not empty; last topic is top level.
        """
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)

        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.ControlSheet.new(sheets_active)
        target.link_factsheet(target, control)

        outline_topics = new_outline_topics()
        topics = outline_topics._gtk_model
        PATH_LAST = '1'
        i_last = topics.get_iter(PATH_LAST)
        i_prune = topics.iter_children(i_last)
        while i_prune:
            is_valid = topics.remove(i_prune)
            if not is_valid:
                i_prune = None
        item_last = AOUTLINE.get_item_gtk(topics, i_last)
        view = target._view_topics.gtk_view
        view.set_model(topics)
        cursor = view.get_selection()
        cursor.unselect_all()
        # Test
        target.on_go_last_topic(None, None)
        model, index = cursor.get_selected()
        assert model is topics
        path_target = model.get_string_from_iter(index)
        assert PATH_LAST == path_target
        item_target = AOUTLINE.get_item_gtk(model, index)
        assert item_target is item_last
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
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)

        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.ControlSheet.new(sheets_active)
        target.link_factsheet(target, control)
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
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)

        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.ControlSheet.new(sheets_active)
        target.link_factsheet(target, control)
        gtk_model = target._view_topics.gtk_view.get_model()
        NAME = 'Parrot'
        SUMMARY = 'A sketch about customer service.'
        TITLE = 'The Parrot Sketch'
        topic = MTOPIC.Topic(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
        index_0 = gtk_model.append(None, [topic])

        PATH_EXPECT = '0:0'
        placement = QPLACE.Placement(index_0, QPLACE.Order.CHILD)
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

        patch_template = PatchCall(topic)
        monkeypatch.setattr(
            XNOTE_SPEC.SpecNote, '__call__', patch_template.__call__)
        # Test
        target.on_new_topic(None, None)
        assert patch_place.called
        assert patch_query_template.called
        assert patch_template.called
        id_visible = target._scenes_topic.show_scene(hex(topic.id_topic))
        assert id_visible == hex(topic.id_topic)
        topics, i_new = target._cursor_topics.get_selected()
        assert PATH_EXPECT == gtk_model.get_string_from_iter(i_new)
        topic_new = AOUTLINE.get_item_gtk(topics, i_new)
        assert topic_new is topic
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

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
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)

        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.ControlSheet.new(sheets_active)
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
        monkeypatch.setattr(CSHEET.ControlSheet, 'insert_topic_child',
                            patch_insert.insert_topic_child)
        # Test
        target.on_new_topic(None, None)
        assert not patch_query_template.called
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

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
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)

        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.ControlSheet.new(sheets_active)
        target.link_factsheet(target, control)

        patch_query_template = PatchCall(None)
        monkeypatch.setattr(QTEMPLATE.QueryTemplate, '__call__',
                            patch_query_template.__call__)
        # Test
        target.on_new_topic(None, None)
        # Return from call shows guard against template = None
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

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
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)

        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.ControlSheet.new(sheets_active)
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
            XNOTE_SPEC.SpecNote, '__call__', patch_template.__call__)

        class PatchInsert:
            def __init__(self): self.called = False

            def insert_topic_child(self, _t, _a): self.called = True

        patch_insert = PatchInsert()
        monkeypatch.setattr(CSHEET.ControlSheet, 'insert_topic_child',
                            patch_insert.insert_topic_child)
        # Test
        target.on_new_topic(None, None)
        assert not patch_insert.called
        # Teardown
        target._window.destroy()
        del target._window
        del factsheet

    def test_on_open_page(self, patch_factsheet, capfd):
        """Confirm response to request to open new view."""
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)

        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.ControlSheet.new(sheets_active)
        target._control = control
        # Test
        target.on_open_page(None, None)
        model = control._model
        assert 1 == model.n_pages()
        for page in model._pages.values():
            assert page._control is control
            assert page._query_place is not None
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
                return CSHEET.ControlSheet(p_pool)

        patch_page = PatchPageSheet()
        monkeypatch.setattr(
            VSHEET.PageSheet, 'open_factsheet', patch_page.open_factsheet)

        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)

        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.ControlSheet.new(sheets_active)
        target.link_factsheet(target, control)
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
                return CSHEET.ControlSheet()

        patch_page = PatchPageSheet()
        monkeypatch.setattr(
            VSHEET.PageSheet, 'open_factsheet', patch_page.open_factsheet)

        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)
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
            CSHEET.ControlSheet, 'new_name', patch_new_name.new_name)

        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)

        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.ControlSheet.new(sheets_active)
        target.link_factsheet(target, control)
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
            CSHEET.ControlSheet, 'new_name', patch_new_name.new_name)

        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)

        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.ControlSheet.new(sheets_active)
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
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)

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
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)

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
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)

        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.ControlSheet.new(sheets_active)
        target.link_factsheet(target, control)
        PATH = Path(tmp_path / 'saved_factsheet.fsg')
        control._path = PATH
        assert not control._path.exists()
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
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)

        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.ControlSheet.new(sheets_active)
        target.link_factsheet(target, control)
        control._path = None
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
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)

        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.ControlSheet.new(sheets_active)
        target.link_factsheet(target, control)
        PATH_OLD = Path(tmp_path / 'old_factsheet.fsg')
        control._path = PATH_OLD
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
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)
        target._window.hide()

        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.ControlSheet.new(sheets_active)
        target.link_factsheet(target, control)
        control._path = None
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
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)

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
        del window

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
        # target_page._window.set_skip_pager_hint(True)
        target_page._window.set_skip_taskbar_hint(True)

        target = target_page._view_topics
        SEARCH_ALL = ~ASHEET.FieldsTopic.VOID
        target.scope_search = SEARCH_ALL
        button = Gtk.ToggleButton(active=False)
        # Test
        target_page.on_toggle_search_field(button, ASHEET.FieldsTopic.NAME)
        assert not target.scope_search & ASHEET.FieldsTopic.NAME
        assert target.scope_search & ASHEET.FieldsTopic.TITLE
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
        # target_page._window.set_skip_pager_hint(True)
        target_page._window.set_skip_taskbar_hint(True)

        target = target_page._view_topics
        SEARCH_NONE = ASHEET.FieldsTopic.VOID
        target.scope_search = SEARCH_NONE
        button = Gtk.ToggleButton(active=True)
        # Test - not active
        target_page.on_toggle_search_field(button, ASHEET.FieldsTopic.TITLE)
        assert target.scope_search & ASHEET.FieldsTopic.TITLE
        assert not target.scope_search & ASHEET.FieldsTopic.NAME
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
            control = CSHEET.ControlSheet(sheets_active)
            control._model = MSHEET.Sheet()
            control._path = p_path
            control._sheets_active = p_pool
            return control

        monkeypatch.setattr(CSHEET.ControlSheet, 'open', patch_open)
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
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)

        assert isinstance(target, VSHEET.PageSheet)
        assert target._window.get_application() is factsheet
        control = target._control
        assert isinstance(control, CSHEET.ControlSheet)
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
        monkeypatch.setattr(CSHEET.ControlSheet, 'present_factsheet',
                            patch_present.present_factsheet)

        PATH_MISS = Path(tmp_path / 'miss.fsg')
        PATH_NONE = None
        PATH_HIT = Path(tmp_path / 'hit.fsg')
        paths = [PATH_MISS, PATH_NONE, PATH_HIT]

        sheets_active = CPOOL.PoolSheets()
        for path in paths:
            control = CSHEET.ControlSheet.new(sheets_active)
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
        # Teardown
        # None - no window created

    def test_present(self, patch_factsheet, capfd):
        """Confirm page becomes visible."""
        # Setup
        factsheet = patch_factsheet()
        target = VSHEET.PageSheet(px_app=factsheet)
        snapshot = capfd.readouterr()   # Resets the internal buffer
        assert not snapshot.out
        assert 'Gtk-CRITICAL' in snapshot.err
        assert 'GApplication::startup signal' in snapshot.err
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)

        sheets_active = CPOOL.PoolSheets()
        control = CSHEET.ControlSheet.new(sheets_active)
        target.link_factsheet(target, control)
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
        # target._window.set_skip_pager_hint(True)
        # target._window.set_skip_taskbar_hint(True)
        target._window.set_transient_for(WINDOW_ANCHOR)

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
