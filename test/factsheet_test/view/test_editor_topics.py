"""
Unit etsts for class to display and edit topics outline of a factsheet.
See :mod:`.editor_topics`.
"""
import pytest  # type: ignore[import]
import gi   # type: ignore[import]

import factsheet.bridge_ui as BUI
import factsheet.control.control_sheet as CSHEET
import factsheet.model.topic as MTOPIC
import factsheet.view.ui as UI
import factsheet.view.editor_topics as VTOPICS

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class TestEditorTopics:
    """Unit tests for :class:`.editor_topics`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
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
        assert target._ui_outline_topics.get_model() is (
            target._control_sheet.new_view_topics._ui_model)
        columns = target._ui_outline_topics.get_columns()
        assert N_COLUMNS == len(columns)
        assert TITLE_C_NAME == columns[C_NAME].get_title()
        assert TITLE_C_TITLE == columns[C_TITLE].get_title()

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
