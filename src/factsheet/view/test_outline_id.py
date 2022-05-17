"""
Unit tests for classes of visual elements of identity item outlines.
See :mod:`.outline_id`.
"""
import gi   # type: ignore[import]
from gi.repository import Gio   # type: ignore[import]
import pytest

import factsheet.bridge_ui as BUI
import factsheet.model.idcore as MIDCORE
import factsheet.view.outline_id as VOUTLINE_ID

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # noqa: E402


Name = BUI.ModelTextMarkup
Summary = BUI.ModelTextStyled
Title = BUI.ModelTextMarkup


class ItemId(MIDCORE.IdCore[Name, Summary, Title]):
    """Minimal subclass of :class:`.IdCore`."""

    def __init__(self, *, p_name, p_summary, p_title, **kwargs) -> None:
        """TBD"""
        self._name = Name(p_text=p_name)
        self._summary = Summary(p_text=p_summary)
        self._title = Title(p_text=p_title)
        super().__init__(**kwargs)


@pytest.fixture
def new_model_outline():
    """Pytest fixture: return factory for an ItemId outline model."""

    def factory(p_n_width=4, p_n_depth=5):
        """Return multi-level outline model containing ItemId.

        :param p_n_width: number of top-level items.
        :param p_n_depth: number of descendant levels under last
            stop-level item.
        """
        model = BUI.ModelOutlineMulti[ItemId]()
        line = None
        for i in range(p_n_width):
            name = 'Name {}'.format(i)
            title = 'Title {}'.format(i)
            item = ItemId(p_name=name, p_summary='', p_title=title)
            line = model.insert_after(p_item=item, p_line=line)
        for j in range(p_n_depth):
            name = 'Name {}'.format(p_n_width + j)
            title = 'Title {}'.format(p_n_width + 1)
            item = ItemId(p_name=name, p_summary='', p_title=title)
            line = model.insert_child(p_item=item, p_line=line)
        return model

    return factory


@pytest.fixture
def empty_model_outline():
    """Pytest fixture: return empty outline model."""
    return BUI.ModelOutlineMulti[ItemId]()


class TestTailorUiDisplayOutlinesId:
    """Unit tests for :class:`.TailorUiDisplayOutlinesId`."""

    def test_init(self, new_model_outline):
        """Confirm initialization orchestration.

        :param new_model_outline: fixture :func:`.new_model_outline`.
        """
        # Setup
        N_COLUMNS = 2
        OUTLINE = new_model_outline()
        ui_view = Gtk.TreeView(model=OUTLINE.ui_model)
        actions = Gio.SimpleActionGroup()
        NAME_ACTION = 'go-first'
        # Test
        target = VOUTLINE_ID.SetupUiDisplayOutlineId(
            p_ui_view=ui_view, p_action_group=actions)
        assert target._ui_view is ui_view
        columns = target.ui_view.get_columns()
        assert N_COLUMNS == len(columns)
        assert actions.lookup_action(NAME_ACTION) is not None

    @pytest.mark.parametrize('NAME_ACTION', [
        'collapse-outline',
        'expand-outline',
        'go-first',
        'go-last',
        'switch-columns',
        ])
    def test_init_actions(self, new_model_outline, NAME_ACTION):
        """Confirm outline display actions added to group.

        :param new_model_outline: fixture :func:`.new_model_outline`.
        :param NAME_ACTION: name of action under test.
        """
        # Setup
        OUTLINE = new_model_outline()
        ui_view = Gtk.TreeView(model=OUTLINE.ui_model)
        target = VOUTLINE_ID.SetupUiDisplayOutlineId(p_ui_view=ui_view)
        actions = Gio.SimpleActionGroup()
        # Test
        target._init_actions(actions)
        assert actions.lookup_action(NAME_ACTION) is not None

    def test_init_columns(self, new_model_outline):
        """Confirm initialization of columns.

        :param new_model_outline: fixture :func:`.new_model_outline`.
        """
        # Setup
        N_COLUMNS = 2
        C_NAME = 0
        TITLE_C_NAME = 'Name'
        C_TITLE = 1
        TITLE_C_TITLE = 'Title'
        OUTLINE = new_model_outline()
        ui_view = Gtk.TreeView(model=OUTLINE.ui_model)
        target = VOUTLINE_ID.SetupUiDisplayOutlineId(p_ui_view=ui_view)
        for column in ui_view.get_columns():
            ui_view.remove_column(column)
        # Test
        target._init_columns()
        # assert target._ui_selection is ui_view.get_selection()
        columns = target.ui_view.get_columns()
        assert target._column_name is columns[C_NAME]
        assert TITLE_C_NAME == columns[C_NAME].get_title()
        assert target._column_title is columns[C_TITLE]
        assert TITLE_C_TITLE == columns[C_TITLE].get_title()
        assert N_COLUMNS == len(columns)

    def test_init_search(self, new_model_outline):
        """Confirm initialization of columns.

        :param new_model_outline: fixture :func:`.new_model_outline`.
        """
        # Setup
        OUTLINE = new_model_outline()
        ui_view = Gtk.TreeView(model=OUTLINE.ui_model)
        target = VOUTLINE_ID.SetupUiDisplayOutlineId(p_ui_view=ui_view)
        search = VOUTLINE_ID.UiSearchOutlineId()
        # Test
        target._init_search(search)
        # Test

    @pytest.mark.parametrize('METHOD, I_LINE, EXPECT', [
        ('_markup_cell_name', 0, 'Name 0'),
        ('_markup_cell_name', 3, 'Name 3'),
        ('_markup_cell_title', 2, 'Title 2'),
        ('_markup_cell_title', 4, 'Title 4'),
        ])
    def test_markup_cell(self, empty_model_outline, METHOD, I_LINE, EXPECT):
        """Confirm cell data function updates column text.

        :param METHOD: markup method under test.
        :param I_LINE: index in outline of sample line.
        :param EXPECT: text to expect in cell.
        """
        # Setup
        N_ITEMS = 5
        outline = empty_model_outline
        for i in range(N_ITEMS):
            name = 'Name {}'.format(i)
            title = 'Title {}'.format(i)
            item = ItemId(p_name=name, p_summary='', p_title=title)
            outline.insert_before(p_item=item, p_line=None)
        ui_view = Gtk.TreeView(model=outline.ui_model)
        target = VOUTLINE_ID.SetupUiDisplayOutlineId(p_ui_view=ui_view)
        target_method = getattr(target, METHOD)
        column = Gtk.TreeViewColumn()
        render = Gtk.CellRendererText()
        column.pack_start(render, expand=True)
        line = outline.ui_model.get_iter_from_string(str(I_LINE))
        # Test
        target_method(None, render, outline.ui_model, line, None)
        assert EXPECT == render.get_property('text')

    @pytest.mark.parametrize('METHOD', [
        ('_markup_cell_name'),
        ('_markup_cell_title'),
        ])
    def test_markup_cell_none(self, empty_model_outline, METHOD):
        """Confirm cell data function updates column text.

        :param METHOD: markup method under test.
        """
        # Setup
        outline = empty_model_outline
        ui_view = Gtk.TreeView(model=outline.ui_model)
        target = VOUTLINE_ID.SetupUiDisplayOutlineId(p_ui_view=ui_view)
        target_method = getattr(target, METHOD)
        column = Gtk.TreeViewColumn()
        render = Gtk.CellRendererText()
        column.pack_start(render, expand=True)
        outline.ui_model.append(None, [None])
        line = outline.ui_model.get_iter_first()
        EXPECT = 'Missing'
        # Test
        target_method(None, render, outline.ui_model, line, None)
        assert EXPECT == render.get_property('text')

    @pytest.mark.parametrize('NAME, COLLAPSE', [
        ('collapse-outline', True),
        ('expand-outline', False),
        ])
    def test_on_change_depth(
            self, monkeypatch, new_model_outline, NAME, COLLAPSE):
        """Confirm actions that change depth shown of outline.

        :param new_model_outline: fixture :func:`.new_model_outline`.
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
        OUTLINE = new_model_outline()
        ui_view = Gtk.TreeView(model=OUTLINE.ui_model)
        target = VOUTLINE_ID.SetupUiDisplayOutlineId(p_ui_view=ui_view)
        actions = Gio.SimpleActionGroup()
        target._init_actions(p_action_group=actions)
        action = actions.lookup_action(NAME)
        # Test
        target.on_change_depth(action, None)
        assert patch.called_collapse is COLLAPSE
        assert patch.called_expand is not COLLAPSE

    def test_on_change_depth_undefined(self, monkeypatch, new_model_outline):
        """Confirm expand outline for unexpected action.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param new_model_outline: fixture :func:`.new_model_outline`.
        """
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
        OUTLINE = new_model_outline()
        ui_view = Gtk.TreeView(model=OUTLINE.ui_model)
        target = VOUTLINE_ID.SetupUiDisplayOutlineId(p_ui_view=ui_view)
        NAME = 'undefined-action'
        action = Gio.SimpleAction.new(NAME, None)
        # Test
        target.on_change_depth(action, None)
        assert patch.called_collapse is False
        assert patch.called_expand is True

    def test_on_go_first_item(self, new_model_outline):
        """| Confirm first item selection.
        | Case: outline is not empty.

        :param new_model_outline: fixture :func:`.new_model_outline`.
        """
        # Setup
        OUTLINE = new_model_outline()
        ui_view = Gtk.TreeView(model=OUTLINE.ui_model)
        ui_selection = ui_view.get_selection()
        target = VOUTLINE_ID.SetupUiDisplayOutlineId(p_ui_view=ui_view)
        PATH_START = '3:0:0'
        line_start = OUTLINE.ui_model.get_iter_from_string(PATH_START)
        ui_selection.select_iter(line_start)
        NAME_EXPECT = 'Name 0'
        # Test
        target.on_go_first_item(None, None)
        model, line = ui_selection.get_selected()
        assert line is not None
        item_id = BUI.ModelOutline.get_item_direct(model, line)
        assert NAME_EXPECT == item_id.name.text

    def test_on_go_first_item_none(self, empty_model_outline):
        """| Confirm first item selection.
        | Case: outline is empty.

        :param empty_model_outline: fixture :func:`.empty_model_outline`.
        """
        OUTLINE = empty_model_outline
        ui_view = Gtk.TreeView(model=OUTLINE.ui_model)
        ui_selection = ui_view.get_selection()
        target = VOUTLINE_ID.SetupUiDisplayOutlineId(p_ui_view=ui_view)
        # Test
        target.on_go_first_item(None, None)
        _, line = ui_selection.get_selected()
        assert line is None

    def test_on_go_last_item(self, new_model_outline):
        """| Confirm last item selection.
        | Case: outline is not empty; last item is not top level.

        :param new_model_outline: fixture :func:`.new_model_outline`.
        """
        N_WIDTH = 4
        N_DEPTH = 5
        I_LAST = N_WIDTH + N_DEPTH - 1
        OUTLINE = new_model_outline(N_WIDTH, N_DEPTH)
        ui_view = Gtk.TreeView(model=OUTLINE.ui_model)
        ui_selection = ui_view.get_selection()
        target = VOUTLINE_ID.SetupUiDisplayOutlineId(p_ui_view=ui_view)
        model, _ = ui_selection.get_selected()
        PATH_START = '3:0:0'
        line_start = model.get_iter_from_string(PATH_START)
        ui_selection.select_iter(line_start)
        EXPECT_NAME = 'Name ' + str(I_LAST)
        # Test
        target.on_go_last_item(None, None)
        model, line = ui_selection.get_selected()
        assert line is not None
        item_id = BUI.ModelOutline.get_item_direct(model, line)
        assert EXPECT_NAME == item_id.name.text

    def test_on_go_last_item_none(self, empty_model_outline):
        """| Confirm last item selection.
        | Case: item outline is empty.

        :param empty_model_outline: fixture :func:`.empty_model_outline`.
        """
        OUTLINE = empty_model_outline
        ui_view = Gtk.TreeView(model=OUTLINE.ui_model)
        ui_selection = ui_view.get_selection()
        target = VOUTLINE_ID.SetupUiDisplayOutlineId(p_ui_view=ui_view)
        # Test
        target.on_go_last_item(None, None)
        _, line = ui_selection.get_selected()
        assert line is None

    @pytest.mark.parametrize('PRE_NAME, PRE_TITLE, POST_NAME, POST_TITLE', [
        (False, True, True, True),
        (True, True, True, False),
        (True, False, False, True),
        ])
    def test_on_switch_columns(self, new_model_outline, PRE_NAME,
                               PRE_TITLE, POST_NAME, POST_TITLE):
        """Confirm visual column switches.

        :param new_model_outline: fixture :func:`.new_model_outline`.
        :param PRE_NAME: visibility of name column before switch.
        :param PRE_TITLE: visibility of title column before switch.
        :param POST_NAME: visibility of name column after switch.
        :param POST_TITLE: visibility of title column after switch.
        """
        # Setup
        OUTLINE = new_model_outline()
        ui_view = Gtk.TreeView(model=OUTLINE.ui_model)
        target = VOUTLINE_ID.SetupUiDisplayOutlineId(p_ui_view=ui_view)
        I_COLUMN_NAME = 0
        column_name = target._ui_view.get_column(I_COLUMN_NAME)
        column_name.set_visible(PRE_NAME)
        I_COLUMN_TITLE = 1
        column_title = target._ui_view.get_column(I_COLUMN_TITLE)
        column_title.set_visible(PRE_TITLE)
        # Test
        target.on_switch_columns(None, None)
        assert column_name.get_visible() is POST_NAME
        assert column_title.get_visible() is POST_TITLE

    @pytest.mark.skip(reason='pending removal')
    @pytest.mark.parametrize('NAME_PROP, NAME_ATTR', [
        ('ui_selection', '_ui_selection'),
        ('ui_view', '_ui_view'),
        ])
    def test_property_access(self, new_model_outline, NAME_PROP, NAME_ATTR):
        """Confirm access limits of each property.

        :param new_model_outline: fixture :func:`.new_model_outline`.
        :param NAME_PROP: name of property.
        :param NAME_ATTR: name of attribute.
        """
        # Setup
        OUTLINE = new_model_outline()
        ui_view = Gtk.TreeView(model=OUTLINE.ui_model)
        target = VOUTLINE_ID.SetupUiDisplayOutlineId(p_ui_view=ui_view)
        attr = getattr(target, NAME_ATTR)
        CLASS = VOUTLINE_ID.SetupUiDisplayOutlineId
        target_prop = getattr(CLASS, NAME_PROP)
        # Test
        assert target_prop.fget is not None
        assert target_prop.fget(target) is attr
        assert target_prop.fset is None
        assert target_prop.fdel is None


class TestModule:
    """Unit tests for module-level components of :mod:`.outline_ui`."""

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_EXPECT', [
        (VOUTLINE_ID.UiActionsOutlineId, Gio.SimpleActionGroup),
        (VOUTLINE_ID.UiDisplayOutlineId, Gtk.TreeView),
        (VOUTLINE_ID.UiSearchOutlineId, Gtk.SearchBar),
        ])
    def test_types(self, TYPE_TARGET, TYPE_EXPECT):
        """Confirm type alias definitions.

        :param TYPE_TARGET: type alias under test.
        :param TYPE_EXPECT: type expected.
        """
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_EXPECT
