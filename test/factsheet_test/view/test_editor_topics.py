"""
Unit etsts for class to display and edit topics outline of a factsheet.
See :mod:`.editor_topics`.

.. include:: /test/refs_include_pytest.txt
"""
import gi   # type: ignore[import]
import logging
import pytest  # type: ignore[import]

import factsheet.bridge_ui as BUI
import factsheet.control.control_sheet as CSHEET
import factsheet.model.topic as MTOPIC
import factsheet.view.ui as UI
import factsheet.view.editor_topics as VTOPICS

gi.require_version('Gtk', '3.0')
from gi.repository import Gio   # type: ignore[import]    # noqa: E402
from gi.repository import GObject as GO  # type: ignore[import]    # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class TestEditorTopics:
    """Unit tests for :class:`.editor_topics`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        NAME_ACTIONS = 'outline_topics'
        control_sheet = CSHEET.ControlSheet(p_path=None)
        N_COLUMNS = 2
        C_NAME = 0
        TITLE_C_NAME = 'Name'
        C_TITLE = 1
        TITLE_C_TITLE = 'Title'
        # Test
        target = VTOPICS.EditorTopics(p_control_sheet=control_sheet)
        assert target._control_sheet is control_sheet
        assert isinstance(target._ui_view, Gtk.Frame)
        actions = target._ui_view.get_action_group(NAME_ACTIONS)
        assert isinstance(actions, Gio.SimpleActionGroup)
        assert target._ui_outline_topics.get_model() is (
            target._control_sheet.new_view_topics._ui_model)
        columns = target._ui_outline_topics.get_columns()
        assert N_COLUMNS == len(columns)
        assert TITLE_C_NAME == columns[C_NAME].get_title()
        assert TITLE_C_TITLE == columns[C_TITLE].get_title()

    @pytest.mark.parametrize('NAME_ACTION', [
        'collapse-outline',
        'expand-outline',
        ])
    def test_init_actions(self, NAME_ACTION):
        """Confirm initialization of actions for toolbar buttons."""
        # Setup
        control_sheet = CSHEET.ControlSheet(p_path=None)
        target = VTOPICS.EditorTopics(p_control_sheet=control_sheet)
        NAME_ACTIONS = 'outline_topics'
        # Test
        target._init_actions()
        actions = target._ui_view.get_action_group(NAME_ACTIONS)
        assert isinstance(actions, Gio.SimpleActionGroup)
        assert actions.lookup_action(NAME_ACTION) is not None

    @pytest.mark.skip(reason='transitioning to actions from signals')
    def test_init_buttons_depth(self, monkeypatch):
        """Confirm initialization of expand and contract buttons."""
        # Setup
        EXPECT = dict(ui_tool_collapse_outline='clicked',
                      ui_tool_expand_outline='clicked')
        control_sheet = CSHEET.ControlSheet(p_path=None)
        target = VTOPICS.EditorTopics(p_control_sheet=control_sheet)
        get_ui_view = UI.GetUiViewByStr(p_string_ui='')

        class PatchCalls:
            def __init__(self):
                self.signals = dict()

            def get_ui_view(self, p_id_button):
                self.signals[p_id_button] = None
                return Gtk.Button

            def connect(self, p_signal, _handler):
                id_button, _ = self.signals.popitem()
                self.signals[id_button] = p_signal

        patch_calls = PatchCalls()
        monkeypatch.setattr(
            UI.GetUiViewByStr, '__call__', patch_calls.get_ui_view)
        monkeypatch.setattr(Gtk.Button, 'connect', patch_calls.connect)
        # Test
        target._init_buttons_depth(get_ui_view)
        for id_button, signal in EXPECT.items():
            assert signal == patch_calls.signals[id_button]

    @pytest.mark.skip(reason='pending signal implemenation')
    @pytest.mark.parametrize(
        'NAME_SIGNAL, NAME_ATTRIBUTE, ORIGIN, N_DEFAULT', [
            # ('closed', '_context_name', Gtk.Popover, 0),
            # ('delete-event', '_window', Gtk.ApplicationWindow, 0),
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
        # # Setup
        # assert False
        # origin_gtype = GO.type_from_name(GO.type_name(ORIGIN))
        # signal = GO.signal_lookup(NAME_SIGNAL, origin_gtype)
        # control = CSHEET.g_control_app.open_factsheet(
        #     p_path=None, p_time=BUI.TIME_EVENT_CURRENT)
        # target = VSHEET.ViewSheet(p_control=control)
        # # Test
        # # # target._window.set_skip_pager_hint(True)
        # # # target._window.set_skip_taskbar_hint(True)
        # target._window.set_transient_for(gtk_app_window)
        #
        # attribute = getattr(target, NAME_ATTRIBUTE)
        # n_handlers = 0
        # while True:
        #     id_signal = GO.signal_handler_find(
        #         attribute, GO.SignalMatchType.ID, signal,
        #         0, None, None, None)
        #     if 0 == id_signal:
        #         break
        #
        #     n_handlers += 1
        #     GO.signal_handler_disconnect(attribute, id_signal)
        #
        # assert N_DEFAULT + 1 == n_handlers

    @pytest.mark.parametrize('METHOD, I_LINE, EXPECT', [
        ('_markup_cell_name', 0, 'Name 0'),
        ('_markup_cell_name', 3, 'Name 3'),
        ('_markup_cell_title', 2, 'Title 2'),
        ('_markup_cell_title', 4, 'Title 4'),
        ])
    def test_markup_cell(self, METHOD, I_LINE, EXPECT):
        """Confirm cell data function updates column text."""
        # Setup
        control_sheet = CSHEET.ControlSheet(p_path=None)
        control_sheet.clear()
        N_TOPICS = 5
        for i in range(N_TOPICS):
            name = 'Name {}'.format(i)
            title = 'Title {}'.format(i)
            topic = MTOPIC.Topic(p_name=name, p_summary='', p_title=title)
            control_sheet.insert_topic_before(p_topic=topic, p_line=None)
        target = VTOPICS.EditorTopics(p_control_sheet=control_sheet)
        target_method = getattr(target, METHOD)
        column = Gtk.TreeViewColumn()
        render = Gtk.CellRendererText()
        column.pack_start(render, expand=True)
        ui_model_topics = control_sheet._model._topics.ui_model
        line = ui_model_topics.get_iter_from_string(str(I_LINE))
        # Test
        target_method(None, render, None, line, None)
        assert EXPECT == render.get_property('text')

    @pytest.mark.parametrize('METHOD', [
        ('_markup_cell_name'),
        ('_markup_cell_title'),
        ])
    def test_markup_cell_none(self, METHOD):
        """Confirm cell data function updates column text."""
        # Setup
        control_sheet = CSHEET.ControlSheet(p_path=None)
        control_sheet.clear()
        target = VTOPICS.EditorTopics(p_control_sheet=control_sheet)
        target_method = getattr(target, METHOD)
        column = Gtk.TreeViewColumn()
        render = Gtk.CellRendererText()
        column.pack_start(render, expand=True)
        ui_model_topics = control_sheet._model._topics.ui_model
        ui_model_topics.append(None, [None])
        line = ui_model_topics.get_iter_first()
        EXPECT = 'Missing'
        # Test
        target_method(None, render, None, line, None)
        assert EXPECT == render.get_property('text')

    def test_new_column_name(self):
        """Confirm name column construction."""
        # Setup
        control_sheet = CSHEET.ControlSheet(p_path=None)
        control_sheet.clear()
        target = VTOPICS.EditorTopics(p_control_sheet=control_sheet)
        TITLE = 'Name'
        I_NAME = 0
        WIDTH_MIN = 12
        # Test
        column = target._new_column_name()
        assert isinstance(column, Gtk.TreeViewColumn)
        assert TITLE == column.get_title()
        cells = column.get_cells()
        render = cells[I_NAME]
        assert isinstance(render, Gtk.CellRendererText)
        assert column.get_clickable()
        assert WIDTH_MIN == column.get_min_width()
        assert column.get_resizable()
        assert column.get_reorderable()

    def test_new_column_title(self):
        """Confirm title column construction."""
        # Setup
        control_sheet = CSHEET.ControlSheet(p_path=None)
        control_sheet.clear()
        target = VTOPICS.EditorTopics(p_control_sheet=control_sheet)
        TITLE = 'Title'
        I_TITLE = 0
        WIDTH_MIN = 12
        # Test
        column = target._new_column_title()
        assert isinstance(column, Gtk.TreeViewColumn)
        assert TITLE == column.get_title()
        cells = column.get_cells()
        render = cells[I_TITLE]
        assert isinstance(render, Gtk.CellRendererText)
        assert column.get_clickable()
        assert WIDTH_MIN == column.get_min_width()
        assert column.get_resizable()
        assert column.get_reorderable()

    @pytest.mark.parametrize('NAME, COLLAPSE', [
        ('collapse-outline', True),
        ('expand-outline', False),
        ])
    def test_on_change_depth(self, monkeypatch, NAME, COLLAPSE):
        """Confirm actions that change depth shown of topics outline.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param NAME: name of action under test.
        :param COLLAPSE: whether method should collapse outline.
        """
        # Setup
        class PatchTreeView:
            def __init__(self):
                self.called_collapse = False
                self.called_expand = False

            def collapse_all(self):
                self.called_collapse = True

            def expand_all(self):
                self.called_expand = True

        patch = PatchTreeView()
        monkeypatch.setattr(Gtk.TreeView, 'collapse_all', patch.collapse_all)
        monkeypatch.setattr(Gtk.TreeView, 'expand_all', patch.expand_all)
        control_sheet = CSHEET.ControlSheet(p_path=None)
        target = VTOPICS.EditorTopics(p_control_sheet=control_sheet)
        actions = target._ui_view.get_action_group('outline_topics')
        action = actions.lookup_action(NAME)
        # Test
        target.on_change_depth(action, None)
        assert patch.called_collapse is COLLAPSE
        assert patch.called_expand is not COLLAPSE

    def test_on_change_depth_warn(self, caplog):
        """Confirm warning for unexpected action.

        :param caplog: built-in fixture `Pytest caplog`_.
        """
        # Setup
        control_sheet = CSHEET.ControlSheet(p_path=None)
        target = VTOPICS.EditorTopics(p_control_sheet=control_sheet)
        NAME = 'Oops'
        action = Gio.SimpleAction.new(NAME, None)
        N_LOGS = 1
        LAST = -1
        log_message = ('Unexpected action: ' + NAME +
                       ' (EditorTopics.on_change_depth)')
        # Test
        target.on_change_depth(action, None)
        assert N_LOGS == len(caplog.records)
        record = caplog.records[LAST]
        assert log_message == record.message
        assert 'WARNING' == record.levelname

    @pytest.mark.skip(reason='stub method pending implementation')
    def test_on_new_topic(self, capfd):
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

    @pytest.mark.parametrize('NAME_PROP, NAME_ATTR', [
        ('ui_view', '_ui_view'),
        ])
    def test_property_access(
            self, NAME_PROP, NAME_ATTR):
        """Confirm access limits of each property.

        :param NAME_PROP: name of property.
        :param NAME_ATTR: name of attribute.
        """
        # Setup
        control_sheet = CSHEET.ControlSheet(p_path=None)
        target = VTOPICS.EditorTopics(p_control_sheet=control_sheet)
        attr = getattr(target, NAME_ATTR)
        CLASS = VTOPICS.EditorTopics
        target_prop = getattr(CLASS, NAME_PROP)
        # Test
        assert target_prop.fget is not None
        assert target_prop.fget(target) is attr
        assert target_prop.fset is None
        assert target_prop.fdel is None


class TestModule:
    """Unit tests for module-level components of :mod:`.editor_topics`."""

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_EXPECT', [
        (VTOPICS.UiEditorTopics, Gtk.Frame),
        ])
    def test_types(self, TYPE_TARGET, TYPE_EXPECT):
        """Confirm type alias definitions.

        :param TYPE_TARGET: type alias under test.
        :param TYPE_EXPECT: type expected.
        """
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_EXPECT

    @pytest.mark.parametrize('ATTR, TYPE_EXPECT', [
        (VTOPICS.logger, logging.Logger),
        ])
    def test_attributes(self, ATTR, TYPE_EXPECT):
        """Confirm type alias definitions.

        :param TYPE_TARGET: type alias under test.
        :param TYPE_EXPECT: type expected.
        """
        # Setup
        # Test
        assert isinstance(ATTR, TYPE_EXPECT)
