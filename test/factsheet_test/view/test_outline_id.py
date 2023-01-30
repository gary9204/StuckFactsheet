"""
Unit tests for classes of visual elements of identity item outlines.
See :mod:`.outline_id`.

.. include:: /test/refs_include_pytest.txt
"""
import gi   # type: ignore[import]
from gi.repository import Gio   # type: ignore[import]
from gi.repository import GObject as GO  # type: ignore[import]
import logging
import pytest

import factsheet.bridge_ui as BUI
import factsheet.model.idcore as MIDCORE
import factsheet.view.id as VID
import factsheet.view.outline_id as VOUTLINE_ID
import factsheet.view.ui as UI

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # noqa: E402


Name = BUI.x_b_t_ModelTextMarkup
Summary = BUI.ModelTextStyled
Title = BUI.x_b_t_ModelTextMarkup


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


class ItemStub(MIDCORE.IdCore[
        BUI.x_b_t_ModelTextMarkup, BUI.x_b_t_ModelTextMarkup, BUI.x_b_t_ModelTextMarkup]):
    """Stub for item based on :class:`.IdCore`."""

    def __init__(self, p_name='No name', p_summary='No summary',
                 p_title='No title'):
        self._name = BUI.x_b_t_ModelTextMarkup(p_text=p_name)
        self._summary = BUI.x_b_t_ModelTextMarkup(p_text=p_summary)
        self._title = BUI.x_b_t_ModelTextMarkup(p_text=p_title)
        super().__init__()


@pytest.fixture
def new_ui_outline():
    """Pytest fixture: Return model and view for outline of stub items.

    The outline is as follows.

        | name_0xx | title_0xx | summary_0xx
        |     name_00x | title_00x | summary_00x
        |         name_000 | title_000 | summary_000
        |     name_01x | title_01x | summary_01x
        | name_1xx | title_1xx | summary_1xx
        |     name_10x | title_10x | summary_10x
        |     name_11x | title_11x | summary_11x
        |         name_110 | title_110 | summary_110
        |         name_111 | title_111 | summary_111
        |         name_112 | title_112 | summary_112
    """
    model_outline = BUI.ModelOutlineMulti[ItemStub]()
    factory_view = (
        BUI.FactoryViewOutline[BUI.ModelOutlineMulti, ItemStub](model_outline))
    view_outline = factory_view()
    item = ItemStub(
        p_name='name_0xx', p_title='title_0xx', p_summary='summary_0xx')
    line_0xx = model_outline.insert_after(item, None)
    item = ItemStub(
        p_name='name_00x', p_title='title_00x', p_summary='summary_00x')
    line_00x = model_outline.insert_child(item, line_0xx)
    item = ItemStub(
        p_name='name_000', p_title='title_000', p_summary='summary_000')
    _line_000 = model_outline.insert_child(item, line_00x)
    item = ItemStub(
        p_name='name_01x', p_title='title_01x', p_summary='summary_01x')
    _line_01x = model_outline.insert_child(item, line_0xx)
    item = ItemStub(
        p_name='name_1xx', p_title='title_1xx', p_summary='summary_1xx')
    line_1xx = model_outline.insert_after(item, line_0xx)
    item = ItemStub(
        p_name='name_10x', p_title='title_10x', p_summary='summary_10x')
    _line_10x = model_outline.insert_child(item, line_1xx)
    item = ItemStub(
        p_name='name_11x', p_title='title_11x', p_summary='summary_11x')
    line_11x = model_outline.insert_child(item, line_1xx)
    item = ItemStub(
        p_name='name_110', p_title='title_110', p_summary='summary_110')
    _line_110 = model_outline.insert_child(item, line_11x)
    item = ItemStub(
        p_name='name_111', p_title='title_111', p_summary='summary_111')
    _line_111 = model_outline.insert_child(item, line_11x)
    item = ItemStub(
        p_name='name_112', p_title='title_112', p_summary='summary_112')
    _line_112 = model_outline.insert_child(item, line_11x)
    return model_outline, view_outline


class TestInitColumnsOutlineId:
    """Unit tests for :class:`.InitColumnsOutlineId`."""

    def test_init(self, new_ui_outline):
        """Confirm initialization of columns.

        :param new_ui_outline: fixture :func:`.new_ui_outline`.
        """
        # Setup
        N_COLUMNS = 2
        C_NAME = 0
        TITLE_C_NAME = 'Name'
        C_TITLE = 1
        TITLE_C_TITLE = 'Title'
        _outline, ui_view = new_ui_outline
        actions = Gio.SimpleActionGroup()
        # Test
        target = VOUTLINE_ID.InitColumnsOutlineId(ui_view, actions)
        columns = ui_view.get_columns()
        assert target._column_name is columns[C_NAME]
        assert TITLE_C_NAME == columns[C_NAME].get_title()
        assert target._column_title is columns[C_TITLE]
        assert TITLE_C_TITLE == columns[C_TITLE].get_title()
        assert N_COLUMNS == len(columns)
        assert actions.lookup_action('cycle-columns') is not None

    @pytest.mark.parametrize('METHOD, LINE_STR, EXPECT', [
        ('_markup_cell_name', '0', 'name_0xx'),
        ('_markup_cell_name', '1:1', 'name_11x'),
        ('_markup_cell_title', '0:1', 'title_01x'),
        ('_markup_cell_title', '1:1:2', 'title_112'),
        ])
    def test_markup_cell(self, new_ui_outline, METHOD, LINE_STR, EXPECT):
        """Confirm cell data function updates column text.

        :param new_ui_outline: fixture :func:`.new_ui_outline`.
        :param METHOD: markup method under test.
        :param LINE_STR: line in outline.
        :param EXPECT: text to expect in cell.
        """
        # Setup
        outline, ui_view = new_ui_outline
        ui_model = outline.ui_model
        target = VOUTLINE_ID.InitColumnsOutlineId(ui_view)
        target_method = getattr(target, METHOD)
        column = Gtk.TreeViewColumn()
        render = Gtk.CellRendererText()
        column.pack_start(render, expand=True)
        line = ui_model.get_iter_from_string(str(LINE_STR))
        # Test
        target_method(None, render, ui_model, line, None)
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
        target = VOUTLINE_ID.InitColumnsOutlineId(ui_view)
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

    @pytest.mark.parametrize('PRE_NAME, PRE_TITLE, POST_NAME, POST_TITLE', [
        (False, True, True, True),
        (True, True, True, False),
        (True, False, False, True),
        ])
    def test_cycle_columns(
            self, new_ui_outline, PRE_NAME, PRE_TITLE, POST_NAME, POST_TITLE):
        """Confirm visible column switches.

        :param new_ui_outline: fixture :func:`.new_ui_outline`.
        :param PRE_NAME: visibility of name column before switch.
        :param PRE_TITLE: visibility of title column before switch.
        :param POST_NAME: visibility of name column after switch.
        :param POST_TITLE: visibility of title column after switch.
        """
        # Setup
        _outline, ui_view = new_ui_outline
        target = VOUTLINE_ID.InitColumnsOutlineId(ui_view)
        I_COLUMN_NAME = 0
        column_name = ui_view.get_column(I_COLUMN_NAME)
        column_name.set_visible(PRE_NAME)
        I_COLUMN_TITLE = 1
        column_title = ui_view.get_column(I_COLUMN_TITLE)
        column_title.set_visible(PRE_TITLE)
        # Test
        target.cycle_columns(None, None)
        assert column_name.get_visible() is POST_NAME
        assert column_title.get_visible() is POST_TITLE


class TestInitMotionOutlineId:
    """Unit tests for :class;`.InitMotionOutlineId`."""

    @pytest.mark.parametrize('NAME_ACTION', [
        'collapse',
        'expand',
        'go-first',
        'go-last',
        ])
    def test_init(self, new_ui_outline, NAME_ACTION):
        """Confirm outline display actions added to group.

        :param new_ui_outline: fixture :func:`.new_ui_outline`.
        :param NAME_ACTION: name of action under test.
        """
        # Setup
        _outline, ui_view = new_ui_outline
        actions = Gio.SimpleActionGroup()
        # Test
        target = VOUTLINE_ID.InitMotionOutlineId(ui_view, actions)
        assert target._ui_view_outline is ui_view
        assert actions.lookup_action(NAME_ACTION) is not None

    @pytest.mark.parametrize('NAME, COLLAPSE', [
        ('collapse', True),
        ('expand', False),
        ('unknown-action', False),
        ])
    def test_change_depth(self, monkeypatch, new_ui_outline, NAME, COLLAPSE):
        """Confirm actions that change depth shown of outline.

        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param new_ui_outline: fixture :func:`.new_ui_outline`.
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
        _outline, ui_view = new_ui_outline
        actions = Gio.SimpleActionGroup()
        action_unknown = Gio.SimpleAction.new('unknown-action', None)
        actions.add_action(action_unknown)
        target = VOUTLINE_ID.InitMotionOutlineId(ui_view, actions)
        action = actions.lookup_action(NAME)
        # Test
        target.change_depth(action, None)
        assert patch.called_collapse is COLLAPSE
        assert patch.called_expand is not COLLAPSE

    def test_go_first_item(self, new_ui_outline):
        """| Confirm first item selection.
        | Case: outline is not empty.

        :param new_ui_outline: fixture :func:`.new_ui_outline`.
        """
        # Setup
        outline, ui_view = new_ui_outline
        actions = Gio.SimpleActionGroup()
        target = VOUTLINE_ID.InitMotionOutlineId(ui_view, actions)
        ui_view.expand_all()
        PATH_START = '1:0'
        line_start = outline.ui_model.get_iter_from_string(PATH_START)
        ui_selection = ui_view.get_selection()
        ui_selection.select_iter(line_start)
        NAME_EXPECT = 'name_0xx'
        # Test
        target.go_first_item(None, None)
        _model, line = ui_selection.get_selected()
        assert line is not None
        item_id = outline.get_item(line)
        assert NAME_EXPECT == item_id.name.text

    def test_go_first_item_none(self, empty_model_outline):
        """| Confirm first item selection.
        | Case: outline is empty.

        :param empty_model_outline: fixture :func:`.empty_model_outline`.
        """
        outline = empty_model_outline
        ui_view = Gtk.TreeView(model=outline.ui_model)
        actions = Gio.SimpleActionGroup()
        target = VOUTLINE_ID.InitMotionOutlineId(ui_view, actions)
        ui_selection = ui_view.get_selection()
        # Test
        target.go_first_item(None, None)
        _, line = ui_selection.get_selected()
        assert line is None

    def test_go_last_item(self, new_ui_outline):
        """| Confirm last item selection.
        | Case: outline is not empty; last item is not top level.

        :param new_ui_outline: fixture :func:`.new_ui_outline`.
        """
        outline, ui_view = new_ui_outline
        actions = Gio.SimpleActionGroup()
        target = VOUTLINE_ID.InitMotionOutlineId(ui_view, actions)
        PATH_START = '1'
        line_start = outline.ui_model.get_iter_from_string(PATH_START)
        ui_selection = ui_view.get_selection()
        ui_selection.select_iter(line_start)
        NAME_EXPECT = 'name_112'
        # Test
        target.go_last_item(None, None)
        _model, line = ui_selection.get_selected()
        assert line is not None
        item_id = outline.get_item(line)
        assert NAME_EXPECT == item_id.name.text

    def test_go_last_item_none(self, empty_model_outline):
        """| Confirm last item selection.
        | Case: item outline is empty.

        :param empty_model_outline: fixture :func:`.empty_model_outline`.
        """
        outline = empty_model_outline
        ui_view = Gtk.TreeView(model=outline.ui_model)
        actions = Gio.SimpleActionGroup()
        target = VOUTLINE_ID.InitMotionOutlineId(ui_view, actions)
        ui_selection = ui_view.get_selection()
        # Test
        target.go_last_item(None, None)
        _, line = ui_selection.get_selected()
        assert line is None


class TestInitSearchOutlineId:
    """Unit tests for :class:`.InitSearchOutlineId`."""

    @pytest.mark.parametrize('ID', [
        'ui_kit_search_id',
        'ui_search_entry',
        'ui_search_name',
        'ui_search_summary',
        'ui_search_title',
        ])
    def test_ui_text(self, ID):
        # Setup
        # Test
        assert 'id="{}"'.format(ID) in VOUTLINE_ID.InitSearchOutlineId._UI_TEXT

    def test_init(self, monkeypatch, new_ui_outline):
        """Confirm initialization of search element for outline."""
        # Setup
        class PatchGetUi:
            def __call__(self, p_id_ui):
                stub = self.stubs[p_id_ui]
                return stub

            def __init__(self):
                self.equal_func_args = None
                self.stubs = dict(
                    ui_kit_search_id=Gtk.Box(),
                    ui_search_name=Gtk.CheckButton(),
                    ui_search_summary=Gtk.CheckButton(),
                    ui_search_title=Gtk.CheckButton(),
                    ui_search_entry=Gtk.SearchEntry(),
                    )

            def set_equal_func(self, *args):
                self.equal_func_args = args

        patch_get_ui = PatchGetUi()
        monkeypatch.setattr(
            UI.GetUiElementByStr, '__call__', patch_get_ui.__call__)
        monkeypatch.setattr(
            Gtk.TreeView, 'set_search_equal_func', patch_get_ui.set_equal_func)
        _outline, ui_view_outline = new_ui_outline
        ui_view_search = VOUTLINE_ID.UiSearchOutlineId()
        kit_search = patch_get_ui.stubs['ui_kit_search_id']
        C_FIRST = 0
        # Test
        target = VOUTLINE_ID.InitSearchOutlineId(
            ui_view_outline, ui_view_search)
        assert kit_search.is_ancestor(ui_view_search)
        assert VID.FieldsId.NAME == target._scope_search
        assert C_FIRST == ui_view_outline.get_search_column()
        assert ui_view_outline.get_search_entry(
            ) is patch_get_ui.stubs['ui_search_entry']
        equal_func, extra = patch_get_ui.equal_func_args
        assert target._match_spec_ne == equal_func
        assert extra is ui_view_outline

    @pytest.mark.parametrize('NAME_SIGNAL, NAME_BUTTON, ORIGIN, N_DEFAULT', [
        ('toggled', 'ui_search_name', Gtk.CheckButton, 0),
        ('toggled', 'ui_search_summary', Gtk.CheckButton, 0),
        ('toggled', 'ui_search_title', Gtk.CheckButton, 0),
        ])
    def test_init_search_signals(self, monkeypatch, new_ui_outline,
                                 NAME_SIGNAL, NAME_BUTTON, ORIGIN, N_DEFAULT):
        """Confirm initialization of signal connections.

        :param new_ui_outline: fixture :func:`.new_ui_outline`.
        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param NAME_SIGNAL: name of signal.
        :param NAME_BUTTON: name of scope button connected to signal.
        :param ORIGIN: GTK class of connected button.
        :param N_DEFAULT: number of default handlers.
        """
        # Setup
        class PatchGetUi:
            def __call__(self, p_id_ui):
                stub = self.stubs[p_id_ui]
                return stub

            def __init__(self):
                self.equal_func_args = None
                self.stubs = dict(
                    ui_kit_search_id=Gtk.Box(),
                    ui_search_name=Gtk.CheckButton(),
                    ui_search_summary=Gtk.CheckButton(),
                    ui_search_title=Gtk.CheckButton(),
                    ui_search_entry=Gtk.SearchEntry(),
                    )

            def set_equal_func(self, *args):
                self.equal_func_args = args

        patch_get_ui = PatchGetUi()
        monkeypatch.setattr(
            UI.GetUiElementByStr, '__call__', patch_get_ui.__call__)
        monkeypatch.setattr(
            Gtk.TreeView, 'set_search_equal_func', patch_get_ui.set_equal_func)
        _outline, ui_view_outline = new_ui_outline
        ui_view_search = VOUTLINE_ID.UiSearchOutlineId()
        # Test
        _target = VOUTLINE_ID.InitSearchOutlineId(
            ui_view_outline, ui_view_search)

        origin_gtype = GO.type_from_name(GO.type_name(ORIGIN))
        signal = GO.signal_lookup(NAME_SIGNAL, origin_gtype)
        button = patch_get_ui.stubs[NAME_BUTTON]
        n_handlers = 0
        while True:
            id_signal = GO.signal_handler_find(
                button, GO.SignalMatchType.ID, signal,
                0, None, None, None)
            if 0 == id_signal:
                break

            n_handlers += 1
            GO.signal_handler_disconnect(button, id_signal)

        assert N_DEFAULT + 1 == n_handlers

    @pytest.mark.parametrize('SCOPE, PATH_ITEM, MATCH_KEY, EXPECT, EXPANDED', [
        (VID.FieldsId.VOID, '1:0', 'name 01x', True, False),
        (VID.FieldsId.NAME, '0:1', 'name_01x', False, False),
        (VID.FieldsId.NAME, '0', 'e_0x', False, False),
        (VID.FieldsId.NAME, '0', '$e_0x', True, True),
        (VID.FieldsId.VOID, '1', 'summary_1xx', True, False),
        (VID.FieldsId.SUMMARY, '1', 'summary_1xx', False, False),
        (VID.FieldsId.SUMMARY, '1:1:1', 'y_111', False, False),
        (VID.FieldsId.SUMMARY, '1:1:1', 'y_11$', True, True),
        (VID.FieldsId.VOID, '0:0:0', 'title_000', True, False),
        (VID.FieldsId.TITLE, '0:0:0', 'title_000', False, False),
        (VID.FieldsId.TITLE, '1:1', 'le_1', False, False),
        (VID.FieldsId.TITLE, '1:1', 'le_11', False, False),
        (VID.FieldsId.TITLE, '1:1', 'le$11', True, True),
        ])
    def test_match_spec_ne(self, new_ui_outline, monkeypatch,
                           SCOPE, PATH_ITEM, MATCH_KEY, EXPECT, EXPANDED):
        """Confirm method returns False when item field matches search key.

        :param new_ui_outline: fixture :func:`.new_ui_outline`.
        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param SCOPE: field identifying scope of search.
        :param PATH_SPEC: path to spec to match.
        :param MATCH_KEY: value to match in spec field.
        :param EXPECT: expected result.
        :param EXPANDED: True when method should expand spec outline.
        """
        # Setup
        class PatchExpand:
            def __init__(self):
                self.called = False
                self.path = None

            def expand_row(self, p, _a):
                self.called = True
                self.path = p

        patch_expand = PatchExpand()
        monkeypatch.setattr(
            Gtk.TreeView, 'expand_row', patch_expand.expand_row)

        outline, ui_view_outline = new_ui_outline
        ui_view_search = VOUTLINE_ID.UiSearchOutlineId()
        target = VOUTLINE_ID.InitSearchOutlineId(
            ui_view_outline, ui_view_search)
        target._scope_search = SCOPE
        line = outline.ui_model.get_iter_from_string(PATH_ITEM)
        # Test
        actual = target._match_spec_ne(
            outline.ui_model, None, MATCH_KEY, line, ui_view_outline)
        assert actual is EXPECT
        assert patch_expand.called is EXPANDED
        if EXPANDED:
            assert PATH_ITEM == patch_expand.path.to_string()

    def test_match_spec_ne_absent(self, new_ui_outline, caplog):
        """Confirm method returns True and logs warning when item is None.

        :param new_ui_outline: fixture :func:`.new_ui_outline`.
        :param caplog: built-in fixture `Pytest caplog`_.
        """
        # Setup
        outline, ui_view_outline = new_ui_outline
        ui_view_search = VOUTLINE_ID.UiSearchOutlineId()
        target = VOUTLINE_ID.InitSearchOutlineId(
            ui_view_outline, ui_view_search)
        outline.clear()
        outline.ui_model.append(None, [None])
        line = outline.ui_model.get_iter_first()
        MATCH_KEY = 'name'
        N_LOGS = 1
        LAST = -1
        log_message = ('Outline contains None at line "0"'
                       ' (InitSearchOutlineId._match_spec_ne)')
        # Test
        actual = target._match_spec_ne(
            outline.ui_model, None, MATCH_KEY, line, None)
        assert actual
        assert N_LOGS == len(caplog.records)
        record = caplog.records[LAST]
        assert log_message == record.message
        assert 'WARNING' == record.levelname

    @pytest.mark.parametrize('SCOPE, ACTIVE, FIELD, EXPECT', [
        (VID.FieldsId.VOID, True, VID.FieldsId.NAME,
         VID.FieldsId.NAME),
        (VID.FieldsId.VOID, True, VID.FieldsId.SUMMARY,
         VID.FieldsId.SUMMARY),
        (VID.FieldsId.VOID, True, VID.FieldsId.TITLE,
         VID.FieldsId.TITLE),
        (~VID.FieldsId.VOID, False, VID.FieldsId.NAME,
         VID.FieldsId.SUMMARY | VID.FieldsId.TITLE),
        ])
    def test_on_changed_search_scope(
            self, new_ui_outline, SCOPE, ACTIVE, FIELD, EXPECT):
        """Confirm change in search scope.

        :param new_ui_outline: fixture :func:`.new_ui_outline`.
        :param SCOPE: fields identifying scope of search.
        :param ACTIVE: True when scope button set to active.
        :param FIELD: changed scope field.
        :param EXPECT: expected result scope of search.
        """
        # Setup
        _outline, ui_view_outline = new_ui_outline
        ui_view_search = VOUTLINE_ID.UiSearchOutlineId()
        target = VOUTLINE_ID.InitSearchOutlineId(
            ui_view_outline, ui_view_search)
        target._scope_search = SCOPE
        button = Gtk.ToggleButton(active=ACTIVE)
        # Test
        target.on_changed_search_scope(button, FIELD)
        assert EXPECT == target._scope_search


class TestInitSummaryOutlineId:
    """Unit tests for :class:`.InitSummaryOutlineId`."""

    def test_no_summary(self):
        """Confirm class attribute definition."""
        # Setup
        target = VOUTLINE_ID.InitSummaryOutlineId
        EXPECT = 'Please select an item in the outline.'
        # Test
        assert isinstance(target.NO_SUMMARY, str)
        assert EXPECT == target.NO_SUMMARY

    def test_init(self, new_ui_outline):
        """Confirm initialization of updateing of item summary.

        :param new_ui_outline: fixture :func:`.new_ui_outline`.
        """
        # Setup
        _outline, ui_view_outline = new_ui_outline
        model_summary = VOUTLINE_ID.ModelSummary()
        # Test
        target = VOUTLINE_ID.InitSummaryOutlineId(
            ui_view_outline, model_summary)
        assert target._model_summary == model_summary

    def test_init_signal_change(self, new_ui_outline):
        """Confirm initialization of topic selection change signal.

        :param new_ui_outline: fixture :func:`.new_ui_outline`.
        """
        # Setup
        # Modified test of single signal from indirect source.
        _outline, ui_view_outline = new_ui_outline
        model_summary = VOUTLINE_ID.ModelSummary()
        _target = VOUTLINE_ID.InitSummaryOutlineId(
            ui_view_outline, model_summary)
        NAME_SIGNAL = 'changed'
        ORIGIN = Gtk.TreeSelection
        N_DEFAULT = 0
        origin_gtype = GO.type_from_name(GO.type_name(ORIGIN))
        signal = GO.signal_lookup(NAME_SIGNAL, origin_gtype)
        # Test
        attribute = ui_view_outline.get_selection()
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

    def test_on_changed_selection(self, new_ui_outline):
        """| Confirm summary shown matches chosen item.
        | Case: a item at line chosen.

        :param new_ui_outline: fixture :func:`.new_ui_outline`.
        """
        # Setup
        outline, ui_view_outline = new_ui_outline
        model_summary = VOUTLINE_ID.ModelSummary()
        target = VOUTLINE_ID.InitSummaryOutlineId(
            ui_view_outline, model_summary)
        target._model_summary.text = 'Oops'
        LINE_STR = '1:0'
        line = outline.ui_model.get_iter_from_string(LINE_STR)
        summary_expect = 'summary_10x'
        ui_view_outline.expand_all()
        selection = ui_view_outline.get_selection()
        selection.select_iter(line)
        # Test
        target.on_changed_selection(selection)
        assert summary_expect == target._model_summary.text

    def test_on_changed_selection_absent(self, new_ui_outline):
        """| Confirm summary shown matches chosen item.
        | Case: no item at line chosen.

        :param new_ui_outline: fixture :func:`.new_ui_outline`.
        """
        # Setup
        outline, ui_view_outline = new_ui_outline
        model_summary = VOUTLINE_ID.ModelSummary()
        target = VOUTLINE_ID.InitSummaryOutlineId(
            ui_view_outline, model_summary)
        target._model_summary.text = 'Oops'
        outline.clear()
        outline.ui_model.append(None, [None])
        line = outline.ui_model.get_iter_first()
        ui_view_outline.expand_all()
        selection = ui_view_outline.get_selection()
        selection.select_iter(line)
        # Test
        target.on_changed_selection(selection)
        assert target.NO_SUMMARY == target._model_summary.text

    def test_on_changed_selection_none(self, new_ui_outline):
        """| Confirm summary shown matches chosen item.
        | Case: no line is chosen.

        :param new_ui_outline: fixture :func:`.new_ui_outline`.
        """
        # Setup
        _outline, ui_view_outline = new_ui_outline
        model_summary = VOUTLINE_ID.ModelSummary()
        target = VOUTLINE_ID.InitSummaryOutlineId(
            ui_view_outline, model_summary)
        target._model_summary.text = 'Oops'
        ui_view_outline.expand_all()
        selection = ui_view_outline.get_selection()
        selection.unselect_all()
        # Test
        target.on_changed_selection(selection)
        assert target.NO_SUMMARY == target._model_summary.text


class TestSelectorItem:
    """Unit tests for :class:`.SelectorItem`."""

    @pytest.mark.parametrize('ID', [
        'ui_kit_selector_id',
        'ui_button_search',
        'ui_site_search',
        'ui_site_outline_id',
        'ui_site_summary',
        ])
    def test_ui_text(self, ID):
        # Setup
        # Test
        assert 'id="{}"'.format(ID) in VOUTLINE_ID.SelectorItem._UI_TEXT

    def test_init(self, new_ui_outline):
        """Confirm attribute initialization.

        :param new_ui_outline: fixture :func:`.new_ui_outline`.
        """
        # Setup
        outline, view_outline = new_ui_outline
        # Test
        target = VOUTLINE_ID.SelectorItem(p_ui_outline=view_outline)
        assert isinstance(target._ui_selector, Gtk.Box)
        assert target._ui_selector.get_visible()
        # assert target._ui_view_outline is VIEW_OUTLINE
        # assert target._ui_view_outline.get_model() is MODEL_OUTLINE.ui_model
        # assert target._ui_view_outline.get_visible()
        # assert target.NO_SUMMARY == target._summary.text
        # assert VID.FieldsId.NAME == target._scope_search

    def test_init_kit(self, monkeypatch, new_ui_outline):
        """Confirm orchestration component initializations.

        :param new_ui_outline: fixture :func:`.new_ui_outline`.
        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        class PatchCall:
            def __call__(self, p_id_ui):
                stub = self.stubs.get(p_id_ui)
                return stub

            def __init__(self):
                self.stubs = dict(
                    ui_kit_selector_id=Gtk.Box(),
                    ui_button_search=Gtk.ToggleButton(active=False),
                    ui_site_outline_id=Gtk.ScrolledWindow(),
                    ui_site_search=Gtk.Box(),
                    ui_site_summary=Gtk.ScrolledWindow(),
                    )

        patch_call = PatchCall()
        monkeypatch.setattr(
            UI.GetUiElementByStr, '__call__', patch_call.__call__)

        class PatchInit:
            def __init__(self):
                self.columns_ui_outline = None
                self.columns_actions = None
                self.columns_ui_outline = None
                self.motion_actions = None
                self.search_ui_outline = None
                self.search_search = None

            def init_columns(self, p_ui_outline, p_actions):
                self.columns_ui_outline = p_ui_outline
                self.columns_actions = p_actions

            def init_motion(self, p_ui_outline, p_actions):
                self.motion_ui_outline = p_ui_outline
                self.motion_actions = p_actions

            def init_search(self, p_ui_outline, p_search):
                self.search_ui_outline = p_ui_outline
                self.search_search = p_search

            def init_summary(self, p_ui_outline, p_summary):
                self.summary_ui_outline = p_ui_outline
                self.summary_model = p_summary

        patch_init = PatchInit()
        monkeypatch.setattr(VOUTLINE_ID.InitColumnsOutlineId,
                            '__init__', patch_init.init_columns)
        monkeypatch.setattr(VOUTLINE_ID.InitMotionOutlineId,
                            '__init__', patch_init.init_motion)
        monkeypatch.setattr(VOUTLINE_ID.InitSearchOutlineId,
                            '__init__', patch_init.init_search)
        monkeypatch.setattr(VOUTLINE_ID.InitSummaryOutlineId,
                            '__init__', patch_init.init_summary)

        _outline, view_outline = new_ui_outline
        # Test
        _target = VOUTLINE_ID.SelectorItem(p_ui_outline=view_outline)
        actions = view_outline.get_action_group('outline')
        assert patch_init.columns_ui_outline is view_outline
        assert patch_init.columns_actions is actions
        assert patch_init.motion_ui_outline is view_outline
        assert patch_init.motion_actions is actions
        assert patch_init.search_ui_outline is view_outline
        assert isinstance(
            patch_init.search_search, VOUTLINE_ID.UiSearchOutlineId)
        assert patch_init.summary_ui_outline is view_outline
        assert isinstance(
            patch_init.summary_model, VOUTLINE_ID.ModelSummary)

    def test_init_place(self, monkeypatch, new_ui_outline):
        """Confirm orchestration component initializations.

        :param new_ui_outline: fixture :func:`.new_ui_outline`.
        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        class PatchCall:
            def __call__(self, p_id_ui):
                stub = self.stubs.get(p_id_ui)
                return stub

            def __init__(self):
                # self.binding = None
                # self.connections = list()
                self.equal_func_args = None
                self.stubs = dict(
                    ui_kit_selector_id=Gtk.Box(),
                    ui_button_search=Gtk.ToggleButton(active=False),
                    ui_site_outline_id=Gtk.ScrolledWindow(),
                    ui_site_search=Gtk.Box(),
                    ui_site_summary=Gtk.ScrolledWindow(),
                    )

        patch_call = PatchCall()
        monkeypatch.setattr(
            UI.GetUiElementByStr, '__call__', patch_call.__call__)

        class PatchInit:
            def init_pass(self, *args, **kwargs):
                pass

            def init_summary(self, p_ui_view_outline, p_model_summary):
                self.model_summary = p_model_summary
                del p_ui_view_outline

        patch_init = PatchInit()
        monkeypatch.setattr(VOUTLINE_ID.InitColumnsOutlineId,
                            '__init__', patch_init.init_pass)
        monkeypatch.setattr(VOUTLINE_ID.InitMotionOutlineId,
                            '__init__', patch_init.init_pass)
        monkeypatch.setattr(VOUTLINE_ID.InitSearchOutlineId,
                            '__init__', patch_init.init_pass)
        monkeypatch.setattr(VOUTLINE_ID.InitSummaryOutlineId,
                            '__init__', patch_init.init_summary)

        _outline, view_outline = new_ui_outline
        I_FIRST = 0
        # Test
        _target = VOUTLINE_ID.SelectorItem(p_ui_outline=view_outline)
        box_outline = patch_call.stubs['ui_site_outline_id']
        view_outline_target = box_outline.get_children()[I_FIRST]
        assert view_outline_target is view_outline
        box_search = patch_call.stubs['ui_site_search']
        ui_search = box_search.get_children()[I_FIRST]
        assert isinstance(ui_search, VOUTLINE_ID.UiSearchOutlineId)
        site_summary = patch_call.stubs['ui_site_summary']
        ui_summary = site_summary.get_child()
        assert isinstance(ui_summary, VOUTLINE_ID.DisplaySummary)
        assert ui_summary.get_buffer() is patch_init.model_summary.ui_model

    @pytest.mark.parametrize('NAME_PROP, NAME_ATTR', [
        ('ui_selector', '_ui_selector'),
        ])
    def test_property_access(self, new_ui_outline, NAME_PROP, NAME_ATTR):
        """Confirm access limits of each property.

        :param new_ui_outline: fixture :func:`.new_ui_outline`.
        :param NAME_PROP: name of property.
        :param NAME_ATTR: name of attribute.
        """
        # Setup
        _outline, view_outline = new_ui_outline
        target = VOUTLINE_ID.SelectorItem(p_ui_outline=view_outline)
        attr = getattr(target, NAME_ATTR)
        CLASS = VOUTLINE_ID.SelectorItem
        target_prop = getattr(CLASS, NAME_PROP)
        # Test
        assert target_prop.fget is not None
        assert target_prop.fget(target) is attr
        assert target_prop.fset is None
        assert target_prop.fdel is None

    # def test_init_search(self, new_ui_outline, monkeypatch):
    #     """Confirm initialization of search bar.
    #
    #     :param new_ui_outline: fixture :func:`.new_ui_outline`.
    #     """
    #     # Setup
    #     class PatchCall:
    #         def __call__(self, p_id_ui):
    #             stub = self.stubs.get(p_id_ui)
    #             return stub
    #
    #         def __init__(self):
    #             # self.binding = None
    #             # self.connections = list()
    #             self.equal_func_args = None
    #             self.stubs = dict(
    #                 ui_search=Gtk.SearchBar(),
    #                 ui_header=Gtk.HeaderBar(),
    #                 ui_search_in_name=Gtk.CheckButton(),
    #                 ui_search_in_summary=Gtk.CheckButton(),
    #                 ui_search_in_title=Gtk.CheckButton(),
    #                 ui_search_entry=Gtk.Entry(),
    #                 )
    #
    #         def set_equal_func(self, *args):
    #             self.equal_func_args = args
    #
    #     _MODEL_OUTLINE, VIEW_OUTLINE = new_ui_outline
    #     target = VOUTLINE_ID.SelectorItem(p_view_outline=VIEW_OUTLINE)
    #
    #     patch_call = PatchCall()
    #     monkeypatch.setattr(
    #         UI.GetUiElementByStr, '__call__', patch_call.__call__)
    #     monkeypatch.setattr(
    #         Gtk.TreeView, 'set_search_equal_func', patch_call.set_equal_func)
    #     get_ui_element = UI.GetUiElementByStr(p_string_ui='')
    #     C_FIRST = 0
    #     # Test
    #     target._init_search(get_ui_element)
    #     assert VID.FieldsId.NAME == target._scope_search
    #     assert target._search_bar is patch_call.stubs['ui_search']
    #     assert target._ui_view_outline.get_enable_search()
    #     assert C_FIRST == target._ui_view_outline.get_search_column()
    #     assert target._ui_view_outline.get_search_entry(
    #         ) is patch_call.stubs['ui_search_entry']
    #     equal_func, extra = patch_call.equal_func_args
    #     assert target._match_spec_ne == equal_func
    #     assert extra is None

    # @pytest.mark.parametrize('NAME_SIGNAL, NAME_BUTTON, ORIGIN, N_DEFAULT', [
    #     ('toggled', 'ui_search_in_name', Gtk.CheckButton, 0),
    #     ('toggled', 'ui_search_in_summary', Gtk.CheckButton, 0),
    #     ('toggled', 'ui_search_in_title', Gtk.CheckButton, 0),
    #     ])
    # def test_init_search_signals(self, new_ui_outline, monkeypatch, NAME_SIGNAL,
    #                              NAME_BUTTON, ORIGIN, N_DEFAULT):
    #     """Confirm initialization of signal connections.
    #
    #     :param new_ui_outline: fixture :func:`.new_ui_outline`.
    #     :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
    #     :param NAME_SIGNAL: name of signal.
    #     :param NAME_BUTTON: name of scope button connected to signal.
    #     :param ORIGIN: GTK class of connected button.
    #     :param N_DEFAULT: number of default handlers.
    #     """
    #     # Setup
    #     class PatchCall:
    #         def __call__(self, p_id_ui):
    #             stub = self.stubs.get(p_id_ui)
    #             return stub
    #
    #         def __init__(self):
    #             self.stubs = dict(
    #                 ui_search=Gtk.SearchBar(),
    #                 ui_header=Gtk.HeaderBar(),
    #                 ui_search_in_name=Gtk.CheckButton(),
    #                 ui_search_in_summary=Gtk.CheckButton(),
    #                 ui_search_in_title=Gtk.CheckButton(),
    #                 ui_search_entry=Gtk.Entry(),
    #                 )
    #
    #         def set_equal_func(self, *args):
    #             self.equal_func_args = args
    #
    #     _MODEL_OUTLINE, VIEW_OUTLINE = new_ui_outline
    #     target = VOUTLINE_ID.SelectorItem(p_view_outline=VIEW_OUTLINE)
    #
    #     patch_call = PatchCall()
    #     monkeypatch.setattr(
    #         UI.GetUiElementByStr, '__call__', patch_call.__call__)
    #     monkeypatch.setattr(
    #         Gtk.TreeView, 'set_search_equal_func', patch_call.set_equal_func)
    #     get_ui_element = UI.GetUiElementByStr(p_string_ui='')
    #
    #     origin_gtype = GO.type_from_name(GO.type_name(ORIGIN))
    #     signal = GO.signal_lookup(NAME_SIGNAL, origin_gtype)
    #     # Test
    #     target._init_search(get_ui_element)
    #     button = patch_call.stubs[NAME_BUTTON]
    #     n_handlers = 0
    #     while True:
    #         id_signal = GO.signal_handler_find(
    #             button, GO.SignalMatchType.ID, signal,
    #             0, None, None, None)
    #         if 0 == id_signal:
    #             break
    #
    #         n_handlers += 1
    #         GO.signal_handler_disconnect(button, id_signal)
    #
    #     assert N_DEFAULT + 1 == n_handlers

    # @pytest.mark.parametrize(
    #     'NAME_SIGNAL, NAME_ATTRIBUTE, ORIGIN, N_DEFAULT', [
    #         ('changed', '_ui_selection', Gtk.TreeSelection, 0),
    #         ])
    # def test_init_signals(self, new_ui_outline, NAME_SIGNAL,
    #                       NAME_ATTRIBUTE, ORIGIN, N_DEFAULT):
    #     """Confirm initialization of signal connections.
    #
    #     :param new_ui_outline: fixture :func:`.new_ui_outline`.
    #     :param NAME_SIGNAL: name of signal.
    #     :param NAME_ATTRIBUTE: name of attribute connected to signal.
    #     :param ORIGIN: GTK class of connected attribute.
    #     :param N_DEFAULT: number of default handlers.
    #     """
    #     # Setup
    #     _MODEL_OUTLINE, VIEW_OUTLINE = new_ui_outline
    #     target = VOUTLINE_ID.SelectorItem(p_view_outline=VIEW_OUTLINE)
    #     origin_gtype = GO.type_from_name(GO.type_name(ORIGIN))
    #     signal = GO.signal_lookup(NAME_SIGNAL, origin_gtype)
    #     # Test
    #     attribute = getattr(target, NAME_ATTRIBUTE)
    #     n_handlers = 0
    #     while True:
    #         id_signal = GO.signal_handler_find(
    #             attribute, GO.SignalMatchType.ID, signal,
    #             0, None, None, None)
    #         if 0 == id_signal:
    #             break
    #
    #         n_handlers += 1
    #         GO.signal_handler_disconnect(attribute, id_signal)
    #
    #     assert N_DEFAULT + 1 == n_handlers

    # def test_init_summary(self, new_ui_outline, monkeypatch):
    #     """Confirm initialization of spec summary.
    #
    #     :param new_ui_outline: fixture :func:`.new_ui_outline`.
    #     :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
    #     """
    #     # Setup
    #     class PatchCall:
    #         def __init__(self):
    #             self.id_ui = 'Oops!'
    #             self.site = Gtk.Viewport()
    #
    #         def __call__(self, p_id_ui):
    #             self.id_ui = p_id_ui
    #             return self.site
    #
    #     UI_ID = 'ui_site_summary'
    #     _MODEL_OUTLINE, VIEW_OUTLINE = new_ui_outline
    #     target = VOUTLINE_ID.SelectorItem(p_view_outline=VIEW_OUTLINE)
    #
    #     patch_call = PatchCall()
    #     monkeypatch.setattr(
    #         UI.GetUiElementByStr, '__call__', patch_call.__call__)
    #     get_ui_element = UI.GetUiElementByStr(p_string_ui='')
    #     # Test
    #     target._init_summary(get_ui_element)
    #     assert UI_ID == patch_call.id_ui
    #     view_summary = patch_call.site.get_child()
    #     assert target._summary.ui_model is view_summary.get_buffer()
    #     assert view_summary.get_visible()
    #     assert view_summary.get_wrap_mode() is Gtk.WrapMode.WORD_CHAR

    # def test_init_view_outline(self, new_ui_outline, monkeypatch):
    #     """Confirm initialization of items outline.
    #
    #     :param new_ui_outline: fixture :func:`.new_ui_outline`.
    #     :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
    #     """
    #     # Setup
    #     class PatchCall:
    #         def __init__(self):
    #             self.id_ui = 'Oops!'
    #             self.site = Gtk.ScrolledWindow()
    #
    #         def __call__(self, p_id_ui):
    #             self.id_ui = p_id_ui
    #             return self.site
    #
    #     UI_ID = 'ui_site_outline'
    #     N_COLUMNS = 2
    #     C_NAME = 0
    #     TITLE_C_NAME = 'Name'
    #     C_TITLE = 1
    #     TITLE_C_TITLE = 'Title'
    #     MODEL_OUTLINE, VIEW_OUTLINE = new_ui_outline
    #     target = VOUTLINE_ID.SelectorItem(p_view_outline=VIEW_OUTLINE)
    #
    #     factory_view = (BUI.FactoryViewOutline[
    #         BUI.ModelOutlineMulti, ItemStub](MODEL_OUTLINE))
    #     VIEW_PATCH = factory_view()
    #     target._ui_view_outline = VIEW_PATCH
    #
    #     patch_call = PatchCall()
    #     monkeypatch.setattr(
    #         UI.GetUiElementByStr, '__call__', patch_call.__call__)
    #     get_ui_element = UI.GetUiElementByStr(p_string_ui='')
    #     # Test
    #     target._init_view_outline(get_ui_element)
    #     assert UI_ID == patch_call.id_ui
    #     assert target._ui_view_outline is patch_call.site.get_child()
    #     columns = target._ui_view_outline.get_columns()
    #     assert TITLE_C_NAME == target._column_name.get_title()
    #     assert target._column_name is columns[C_NAME]
    #     assert TITLE_C_TITLE == target._column_title.get_title()
    #     assert target._column_title is columns[C_TITLE]
    #     assert N_COLUMNS == len(columns)
    #     assert target._ui_selection is target._ui_view_outline.get_selection()
    #     # assert target._ui_view_outline.get_visible()

    # def test_sync_to_search(self, new_ui_outline, monkeypatch):
    #     """Confirm sync of button to show/hide of search.
    #
    #     :param new_ui_outline: fixture :func:`.new_ui_outline`.
    #     :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
    #     """
    #     # Setup
    #     class PatchCall:
    #         def __init__(self):
    #             self.binding_args = None
    #
    #         def bind_property(self, *args):
    #             self.binding_args = args
    #
    #     _MODEL_OUTLINE, VIEW_OUTLINE = new_ui_outline
    #     target = VOUTLINE_ID.SelectorItem(p_view_outline=VIEW_OUTLINE)
    #
    #     patch_call = PatchCall()
    #     monkeypatch.setattr(
    #         Gtk.ToggleButton, 'bind_property', patch_call.bind_property)
    #     BUTTON = VOUTLINE_ID.UiButtonFind()
    #     PROP_SOURCE = 'active'
    #     PROP_TARGET = 'search-mode-enabled'
    #     # Test
    #     target.sync_to_search(BUTTON)
    #     prop_source, target_bind, prop_target, flags = patch_call.binding_args
    #     assert PROP_SOURCE == prop_source
    #     assert isinstance(target_bind, Gtk.SearchBar)
    #     assert PROP_TARGET == prop_target
    #     assert GO.BindingFlags.BIDIRECTIONAL == flags

    # @pytest.mark.parametrize('METHOD, LINE_STR, EXPECT', [
    #     ('_markup_cell_name', '0', 'name_0xx'),
    #     ('_markup_cell_name', '1:1', 'name_11x'),
    #     ('_markup_cell_title', '1', 'title_1xx'),
    #     ('_markup_cell_title', '1:1:2', 'title_112'),
    #     ])
    # def test_markup_cell(self, new_ui_outline, METHOD, LINE_STR, EXPECT):
    #     """| Confirm cell data function updates column text.
    #     | Case: item in outline is not None.
    #
    #     :param new_ui_outline: fixture :func:`.new_ui_outline`.
    #     :param METHOD: markup method under test.
    #     :param LINE_STR: line of sample item as string.
    #     :param EXPECT: text to expect in cell.
    #     """
    #     # Setup
    #     MODEL_OUTLINE, VIEW_OUTLINE = new_ui_outline
    #     target = VOUTLINE_ID.SelectorItem(p_view_outline=VIEW_OUTLINE)
    #     target_method = getattr(target, METHOD)
    #     column = Gtk.TreeViewColumn()
    #     render = Gtk.CellRendererText()
    #     column.pack_start(render, expand=True)
    #     line = MODEL_OUTLINE.ui_model.get_iter_from_string(LINE_STR)
    #     # Test
    #     target_method(None, render, MODEL_OUTLINE.ui_model, line, None)
    #     assert EXPECT == render.get_property('text')

    # @pytest.mark.parametrize('METHOD', [
    #     ('_markup_cell_name'),
    #     ('_markup_cell_title'),
    #     ])
    # def test_markup_cell_none(self, METHOD):
    #     """| Confirm cell data function updates column text.
    #     | Case: item in outline is None.
    #
    #     :param METHOD: markup method under test.
    #     """
    #     # Setup
    #     MODEL_OUTLINE = BUI.ModelOutlineMulti[ItemStub]()
    #     MODEL_OUTLINE.ui_model.append(None, [None])
    #     VIEW_OUTLINE = BUI.ViewOutline()
    #     VIEW_OUTLINE.set_model(MODEL_OUTLINE.ui_model)
    #     target = VOUTLINE_ID.SelectorItem(p_view_outline=VIEW_OUTLINE)
    #     target_method = getattr(target, METHOD)
    #     column = Gtk.TreeViewColumn()
    #     render = Gtk.CellRendererText()
    #     column.pack_start(render, expand=True)
    #     line = MODEL_OUTLINE.ui_model.get_iter_first()
    #     EXPECT = 'Missing'
    #     # Test
    #     target_method(None, render, MODEL_OUTLINE.ui_model, line, None)
    #     assert EXPECT == render.get_property('text')

    # def test_on_changed_selection(self, new_ui_outline):
    #     """| Confirm summary shown matches chosen item.
    #     | Case: a item at line chosen.
    #
    #     :param new_ui_outline: fixture :func:`.new_ui_outline`.
    #     """
    #     # Setup
    #     MODEL_OUTLINE, VIEW_OUTLINE = new_ui_outline
    #     VIEW_OUTLINE.expand_all()
    #     target = VOUTLINE_ID.SelectorItem(p_view_outline=VIEW_OUTLINE)
    #     LINE_STR = '1:0'
    #     line = MODEL_OUTLINE.ui_model.get_iter_from_string(LINE_STR)
    #     summary_expect = 'summary_10x'
    #     target._ui_selection.select_iter(line)
    #     target._summary.text = 'Oops'
    #     # Test
    #     target.on_changed_selection(None)
    #     assert summary_expect == target._summary.text

    # def test_on_changed_selection_absent(self, new_ui_outline):
    #     """| Confirm summary shown matches chosen item.
    #     | Case: no item at line chosen.
    #
    #     :param new_ui_outline: fixture :func:`.new_ui_outline`.
    #     """
    #     # Setup
    #     MODEL_OUTLINE = BUI.ModelOutlineMulti[ItemStub]()
    #     MODEL_OUTLINE.ui_model.append(None, [None])
    #     VIEW_OUTLINE = BUI.ViewOutline()
    #     VIEW_OUTLINE.set_model(MODEL_OUTLINE.ui_model)
    #     target = VOUTLINE_ID.SelectorItem(p_view_outline=VIEW_OUTLINE)
    #     target._ui_view_outline.expand_all()
    #     line = MODEL_OUTLINE.ui_model.get_iter_first()
    #     assert line is not None
    #     target._ui_selection.select_iter(line)
    #     target._summary.text = 'Oops'
    #     # Test
    #     target.on_changed_selection(None)
    #     assert target.NO_SUMMARY == target._summary.text

    # def test_on_changed_selection_none(self, new_ui_outline):
    #     """| Confirm summary shown matches chosen item.
    #     | Case: no line is chosen.
    #
    #     :param new_ui_outline: fixture :func:`.new_ui_outline`.
    #     """
    #     # Setup
    #     _MODEL_OUTLINE, VIEW_OUTLINE = new_ui_outline
    #     VIEW_OUTLINE.expand_all()
    #     target = VOUTLINE_ID.SelectorItem(p_view_outline=VIEW_OUTLINE)
    #     target._ui_view_outline.expand_all()
    #     target._ui_selection.unselect_all()
    #     target._summary.text = 'Oops'
    #     # Test
    #     target.on_changed_selection(None)
    #     assert target.NO_SUMMARY == target._summary.text

    # @pytest.mark.parametrize('SCOPE, ACTIVE, FIELD, EXPECT', [
    #     (VID.FieldsId.VOID, True, VID.FieldsId.NAME,
    #      VID.FieldsId.NAME),
    #     (VID.FieldsId.VOID, True, VID.FieldsId.SUMMARY,
    #      VID.FieldsId.SUMMARY),
    #     (VID.FieldsId.VOID, True, VID.FieldsId.TITLE,
    #      VID.FieldsId.TITLE),
    #     (~VID.FieldsId.VOID, False, VID.FieldsId.NAME,
    #      VID.FieldsId.SUMMARY | VID.FieldsId.TITLE),
    #     ])
    # def test_on_changed_search_scope(
    #         self, new_ui_outline, SCOPE, ACTIVE, FIELD, EXPECT):
    #     """Confirm change in search scope.
    #
    #     :param new_ui_outline: fixture :func:`.new_ui_outline`.
    #     :param SCOPE: fields identifying scope of search.
    #     :param ACTIVE: True when scope button set to active.
    #     :param FIELD: changed scope field.
    #     :param EXPECT: expected result scope of search.
    #     """
    #     # Setup
    #     _MODEL_OUTLINE, VIEW_OUTLINE = new_ui_outline
    #     target = VOUTLINE_ID.SelectorItem(p_view_outline=VIEW_OUTLINE)
    #     target._scope_search = SCOPE
    #     button = Gtk.ToggleButton(active=ACTIVE)
    #     # Test
    #     target.on_changed_search_scope(button, FIELD)
    #     assert EXPECT == target._scope_search

    # @pytest.mark.parametrize('SCOPE, PATH_ITEM, MATCH_KEY, EXPECT, EXPANDED', [
    #     (VID.FieldsId.VOID, '1:0', 'name 01x', True, False),
    #     (VID.FieldsId.NAME, '0:1', 'name_01x', False, False),
    #     (VID.FieldsId.NAME, '0', 'e_0x', False, False),
    #     (VID.FieldsId.NAME, '0', '$e_0x', True, True),
    #     (VID.FieldsId.VOID, '1', 'summary_1xx', True, False),
    #     (VID.FieldsId.SUMMARY, '1', 'summary_1xx', False, False),
    #     (VID.FieldsId.SUMMARY, '1:1:1', 'y_111', False, False),
    #     (VID.FieldsId.SUMMARY, '1:1:1', 'y_11$', True, True),
    #     (VID.FieldsId.VOID, '0:0:0', 'title_000', True, False),
    #     (VID.FieldsId.TITLE, '0:0:0', 'title_000', False, False),
    #     (VID.FieldsId.TITLE, '1:1', 'le_1', False, False),
    #     (VID.FieldsId.TITLE, '1:1', 'le_11', False, False),
    #     (VID.FieldsId.TITLE, '1:1', 'le$11', True, True),
    #         ])
    # def test_match_spec_ne(self, new_ui_outline, monkeypatch,
    #                        SCOPE, PATH_ITEM, MATCH_KEY, EXPECT, EXPANDED):
    #     """Confirm method returns False when item field matches search key.
    #
    #     :param new_ui_outline: fixture :func:`.new_ui_outline`.
    #     :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
    #     :param SCOPE: field identifying scope of search.
    #     :param PATH_SPEC: path to spec to match.
    #     :param MATCH_KEY: value to match in spec field.
    #     :param EXPECT: expected result.
    #     :param EXPANDED: True when method should expand spec outline.
    #     """
    #     # Setup
    #     class PatchExpand:
    #         def __init__(self):
    #             self.called = False
    #             self.path = None
    #
    #         def expand_row(self, p, _a):
    #             self.called = True
    #             self.path = p
    #
    #     patch_expand = PatchExpand()
    #     monkeypatch.setattr(
    #         Gtk.TreeView, 'expand_row', patch_expand.expand_row)
    #
    #     MODEL_OUTLINE, VIEW_OUTLINE = new_ui_outline
    #     target = VOUTLINE_ID.SelectorItem(p_view_outline=VIEW_OUTLINE)
    #     target._scope_search = SCOPE
    #     line = MODEL_OUTLINE.ui_model.get_iter_from_string(PATH_ITEM)
    #     # Test
    #     actual = target._match_spec_ne(
    #         MODEL_OUTLINE.ui_model, None, MATCH_KEY, line, None)
    #     assert actual is EXPECT
    #     assert patch_expand.called is EXPANDED
    #     if EXPANDED:
    #         assert PATH_ITEM == patch_expand.path.to_string()

    # def test_match_spec_ne_absent(self, caplog):
    #     """Confirm method returns True and logs warning when item is None.
    #
    #     :param caplog: built-in fixture `Pytest caplog`_.
    #     """
    #     # Setup
    #     MODEL_OUTLINE = BUI.ModelOutlineMulti[ItemStub]()
    #     MODEL_OUTLINE.ui_model.append(None, [None])
    #     VIEW_OUTLINE = BUI.ViewOutline()
    #     VIEW_OUTLINE.set_model(MODEL_OUTLINE.ui_model)
    #     target = VOUTLINE_ID.SelectorItem(p_view_outline=VIEW_OUTLINE)
    #     MATCH_KEY = 'name'
    #     line = MODEL_OUTLINE.ui_model.get_iter_first()
    #     N_LOGS = 1
    #     LAST = -1
    #     log_message = ('Outline contains None at line "0"'
    #                    ' (SelectorItem._match_spec_ne)')
    #     # Test
    #     actual = target._match_spec_ne(
    #         MODEL_OUTLINE.ui_model, None, MATCH_KEY, line, None)
    #     assert actual
    #     assert N_LOGS == len(caplog.records)
    #     record = caplog.records[LAST]
    #     assert log_message == record.message
    #     assert 'WARNING' == record.levelname

    # @pytest.mark.parametrize('NAME_PROP, NAME_ATTR', [
    #     ('ui_chooser', '_ui_chooser'),
    #     ])
    # def test_property_access(self, new_ui_outline, NAME_PROP, NAME_ATTR):
    #     """Confirm access limits of each property.
    #
    #     :param new_ui_outline: fixture :func:`.new_ui_outline`.
    #     :param NAME_PROP: name of property.
    #     :param NAME_ATTR: name of attribute.
    #     """
    #     # Setup
    #     _MODEL_OUTLINE, VIEW_OUTLINE = new_ui_outline
    #     target = VOUTLINE_ID.SelectorItem(p_view_outline=VIEW_OUTLINE)
    #     attr = getattr(target, NAME_ATTR)
    #     CLASS = VOUTLINE_ID.SelectorItem
    #     target_prop = getattr(CLASS, NAME_PROP)
    #     # Test
    #     assert target_prop.fget is not None
    #     assert target_prop.fget(target) is attr
    #     assert target_prop.fset is None
    #     assert target_prop.fdel is None


class TestModuleChooserItem:
    """Unit tests for module-level components of :mod:`.chooser_item`."""

    @pytest.mark.parametrize('ATTR, TYPE_EXPECT', [
        (VOUTLINE_ID.logger, logging.Logger),
        ])
    def test_attributes(self, ATTR, TYPE_EXPECT):
        """Confirm global attribute definitions.

        :param ATTR: global attibute under test.
        :param TYPE_EXPECT: type expected.
        """
        # Setup
        # Test
        assert isinstance(ATTR, TYPE_EXPECT)

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_EXPECT', [
        (VOUTLINE_ID.UiButtonFind, Gtk.ToggleButton),
        (VOUTLINE_ID.UiButtonSearchScope, Gtk.ToggleButton),
        (VOUTLINE_ID.FactoryDisplaySummary, BUI.FactoryDisplayTextStyled),
        (VOUTLINE_ID.ModelSummary, BUI.ModelTextStyled),
        (VOUTLINE_ID.UiSelectorItem, Gtk.Box),
        (VOUTLINE_ID.UiViewOutline, BUI.ViewOutline),
        ])
    def test_types(self, TYPE_TARGET, TYPE_EXPECT):
        """Confirm type alias definitions.

        :param TYPE_TARGET: type alias under test.
        :param TYPE_EXPECT: type expected.
        """
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_EXPECT


# class TestSetupUiDisplayOutlinesId:
#     """Unit tests for :class:`.TailorUiDisplayOutlinesId`."""
#
#     def test_init(self, new_model_outline):
#         """Confirm initialization orchestration.
#
#         :param new_model_outline: fixture :func:`.new_model_outline`.
#         """
#         # Setup
#         N_COLUMNS = 2
#         OUTLINE = new_model_outline()
#         ui_view = Gtk.TreeView(model=OUTLINE.ui_model)
#         actions = Gio.SimpleActionGroup()
#         NAME_ACTION = 'go-first'
#         # Test
#         target = VOUTLINE_ID.SetupUiDisplayOutlineId(
#             p_ui_view=ui_view, p_action_group=actions)
#         assert target._ui_view is ui_view
#         columns = target.ui_view.get_columns()
#         assert N_COLUMNS == len(columns)
#         assert actions.lookup_action(NAME_ACTION) is not None
#
#     @pytest.mark.parametrize('NAME_ACTION', [
#         'collapse',
#         'expand',
#         'go-first',
#         'go-last',
#         'cycle-columns',
#         ])
#     def test_init_actions(self, new_model_outline, NAME_ACTION):
#         """Confirm outline display actions added to group.
#
#         :param new_model_outline: fixture :func:`.new_model_outline`.
#         :param NAME_ACTION: name of action under test.
#         """
#         # Setup
#         OUTLINE = new_model_outline()
#         ui_view = Gtk.TreeView(model=OUTLINE.ui_model)
#         target = VOUTLINE_ID.SetupUiDisplayOutlineId(p_ui_view=ui_view)
#         actions = Gio.SimpleActionGroup()
#         # Test
#         target._init_actions(actions)
#         assert actions.lookup_action(NAME_ACTION) is not None
#
#     def test_init_columns(self, new_model_outline):
#         """Confirm initialization of columns.
#
#         :param new_model_outline: fixture :func:`.new_model_outline`.
#         """
#         # Setup
#         N_COLUMNS = 2
#         C_NAME = 0
#         TITLE_C_NAME = 'Name'
#         C_TITLE = 1
#         TITLE_C_TITLE = 'Title'
#         OUTLINE = new_model_outline()
#         ui_view = Gtk.TreeView(model=OUTLINE.ui_model)
#         target = VOUTLINE_ID.SetupUiDisplayOutlineId(p_ui_view=ui_view)
#         for column in ui_view.get_columns():
#             ui_view.remove_column(column)
#         # Test
#         target._init_columns()
#         # assert target._ui_selection is ui_view.get_selection()
#         columns = target.ui_view.get_columns()
#         assert target._column_name is columns[C_NAME]
#         assert TITLE_C_NAME == columns[C_NAME].get_title()
#         assert target._column_title is columns[C_TITLE]
#         assert TITLE_C_TITLE == columns[C_TITLE].get_title()
#         assert N_COLUMNS == len(columns)
#
#     def test_init_search(self, new_model_outline):
#         """Confirm initialization of columns.
#
#         :param new_model_outline: fixture :func:`.new_model_outline`.
#         """
#         # Setup
#         OUTLINE = new_model_outline()
#         ui_view = Gtk.TreeView(model=OUTLINE.ui_model)
#         target = VOUTLINE_ID.SetupUiDisplayOutlineId(p_ui_view=ui_view)
#         entry_search = Gtk.Entry()
#         box_button = Gtk.Box()
#         search = VOUTLINE_ID.UiSearchOutlineId()
#         search.add(entry_search)
#         search.add(box_button)
#         # Test
#         target._init_search(search)
#         revealer = search.get_child()
#         box_top = revealer.get_child()
#         assert isinstance(box_top, Gtk.Box)
#
#     # https://stackoverflow.com/questions/70771227/
#     #    why-wont-my-searchentry-grow-inside-its-searchbar
#     # def test_init_search(self, new_ui_outline, monkeypatch):
#     #     """Confirm initialization of search bar.
#     #
#     #     :param new_ui_outline: fixture :func:`.new_ui_outline`.
#     #     :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
#     #     """
#     #     # Setup
#     #     class PatchCall:
#     #         def __call__(self, p_id_ui):
#     #             stub = self.stubs.get(p_id_ui)
#     #             return stub
#     #
#     #         def __init__(self):
#     #             # self.binding = None
#     #             # self.connections = list()
#     #             self.equal_func_args = None
#     #             self.stubs = dict(
#     #                 ui_search=Gtk.SearchBar(),
#     #                 ui_header=Gtk.HeaderBar(),
#     #                 ui_search_in_name=Gtk.CheckButton(),
#     #                 ui_search_in_summary=Gtk.CheckButton(),
#     #                 ui_search_in_title=Gtk.CheckButton(),
#     #                 ui_search_entry=Gtk.Entry(),
#     #                 )
#     #
#     #         def set_equal_func(self, *args):
#     #             self.equal_func_args = args
#     #
#     #     _MODEL_OUTLINE, VIEW_OUTLINE = new_ui_outline
#     #     target = VOUTLINE_ID.SelectorItem(p_view_outline=VIEW_OUTLINE)
#     #
#     #     patch_call = PatchCall()
#     #     monkeypatch.setattr(
#     #         UI.GetUiElementByStr, '__call__', patch_call.__call__)
#     #     monkeypatch.setattr(
#     #         Gtk.TreeView, 'set_search_equal_func', patch_call.set_equal_func)
#     #     get_ui_element = UI.GetUiElementByStr(p_string_ui='')
#     #     C_FIRST = 0
#     #     # Test
#     #     target._init_search(get_ui_element)
#     #     assert VID.FieldsId.NAME == target._scope_search
#     #     assert target._search_bar is patch_call.stubs['ui_search']
#     #     assert target._ui_view_outline.get_enable_search()
#     #     assert C_FIRST == target._ui_view_outline.get_search_column()
#     #     assert target._ui_view_outline.get_search_entry(
#     #         ) is patch_call.stubs['ui_search_entry']
#     #     equal_func, extra = patch_call.equal_func_args
#     #     assert target._match_spec_ne == equal_func
#     #     assert extra is None
#     #
#     # @pytest.mark.parametrize('NAME_SIGNAL, NAME_BUTTON, ORIGIN, N_DEFAULT', [
#     #     ('toggled', 'ui_search_in_name', Gtk.CheckButton, 0),
#     #     ('toggled', 'ui_search_in_summary', Gtk.CheckButton, 0),
#     #     ('toggled', 'ui_search_in_title', Gtk.CheckButton, 0),
#     #     ])
#     # def test_init_search_signals(self, new_ui_outline, monkeypatch, NAME_SIGNAL,
#     #                              NAME_BUTTON, ORIGIN, N_DEFAULT):
#     #     """Confirm initialization of signal connections.
#     #
#     #     :param new_ui_outline: fixture :func:`.new_ui_outline`.
#     #     :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
#     #     :param NAME_SIGNAL: name of signal.
#     #     :param NAME_BUTTON: name of scope button connected to signal.
#     #     :param ORIGIN: GTK class of connected button.
#     #     :param N_DEFAULT: number of default handlers.
#     #     """
#     #     # Setup
#     #     class PatchCall:
#     #         def __call__(self, p_id_ui):
#     #             stub = self.stubs.get(p_id_ui)
#     #             return stub
#     #
#     #         def __init__(self):
#     #             self.stubs = dict(
#     #                 ui_search=Gtk.SearchBar(),
#     #                 ui_header=Gtk.HeaderBar(),
#     #                 ui_search_in_name=Gtk.CheckButton(),
#     #                 ui_search_in_summary=Gtk.CheckButton(),
#     #                 ui_search_in_title=Gtk.CheckButton(),
#     #                 ui_search_entry=Gtk.Entry(),
#     #                 )
#     #
#     #         def set_equal_func(self, *args):
#     #             self.equal_func_args = args
#     #
#     #     _MODEL_OUTLINE, VIEW_OUTLINE = new_ui_outline
#     #     target = VOUTLINE_ID.SelectorItem(p_view_outline=VIEW_OUTLINE)
#     #
#     #     patch_call = PatchCall()
#     #     monkeypatch.setattr(
#     #         UI.GetUiElementByStr, '__call__', patch_call.__call__)
#     #     monkeypatch.setattr(
#     #         Gtk.TreeView, 'set_search_equal_func', patch_call.set_equal_func)
#     #     get_ui_element = UI.GetUiElementByStr(p_string_ui='')
#     #
#     #     origin_gtype = GO.type_from_name(GO.type_name(ORIGIN))
#     #     signal = GO.signal_lookup(NAME_SIGNAL, origin_gtype)
#     #     # Test
#     #     target._init_search(get_ui_element)
#     #     button = patch_call.stubs[NAME_BUTTON]
#     #     n_handlers = 0
#     #     while True:
#     #         id_signal = GO.signal_handler_find(
#     #             button, GO.SignalMatchType.ID, signal,
#     #             0, None, None, None)
#     #         if 0 == id_signal:
#     #             break
#     #
#     #         n_handlers += 1
#     #         GO.signal_handler_disconnect(button, id_signal)
#     #
#     #     assert N_DEFAULT + 1 == n_handlers
#
#     @pytest.mark.parametrize('METHOD, I_LINE, EXPECT', [
#         ('_markup_cell_name', 0, 'Name 0'),
#         ('_markup_cell_name', 3, 'Name 3'),
#         ('_markup_cell_title', 2, 'Title 2'),
#         ('_markup_cell_title', 4, 'Title 4'),
#         ])
#     def test_markup_cell(self, empty_model_outline, METHOD, I_LINE, EXPECT):
#         """Confirm cell data function updates column text.
#
#         :param METHOD: markup method under test.
#         :param I_LINE: index in outline of sample line.
#         :param EXPECT: text to expect in cell.
#         """
#         # Setup
#         N_ITEMS = 5
#         outline = empty_model_outline
#         for i in range(N_ITEMS):
#             name = 'Name {}'.format(i)
#             title = 'Title {}'.format(i)
#             item = ItemId(p_name=name, p_summary='', p_title=title)
#             outline.insert_before(p_item=item, p_line=None)
#         ui_view = Gtk.TreeView(model=outline.ui_model)
#         target = VOUTLINE_ID.SetupUiDisplayOutlineId(p_ui_view=ui_view)
#         target_method = getattr(target, METHOD)
#         column = Gtk.TreeViewColumn()
#         render = Gtk.CellRendererText()
#         column.pack_start(render, expand=True)
#         line = outline.ui_model.get_iter_from_string(str(I_LINE))
#         # Test
#         target_method(None, render, outline.ui_model, line, None)
#         assert EXPECT == render.get_property('text')
#
#     @pytest.mark.parametrize('METHOD', [
#         ('_markup_cell_name'),
#         ('_markup_cell_title'),
#         ])
#     def test_markup_cell_none(self, empty_model_outline, METHOD):
#         """Confirm cell data function updates column text.
#
#         :param METHOD: markup method under test.
#         """
#         # Setup
#         outline = empty_model_outline
#         ui_view = Gtk.TreeView(model=outline.ui_model)
#         target = VOUTLINE_ID.SetupUiDisplayOutlineId(p_ui_view=ui_view)
#         target_method = getattr(target, METHOD)
#         column = Gtk.TreeViewColumn()
#         render = Gtk.CellRendererText()
#         column.pack_start(render, expand=True)
#         outline.ui_model.append(None, [None])
#         line = outline.ui_model.get_iter_first()
#         EXPECT = 'Missing'
#         # Test
#         target_method(None, render, outline.ui_model, line, None)
#         assert EXPECT == render.get_property('text')
#
#     @pytest.mark.parametrize('NAME, COLLAPSE', [
#         ('collapse', True),
#         ('expand', False),
#         ])
#     def test_on_change_depth(
#             self, monkeypatch, new_model_outline, NAME, COLLAPSE):
#         """Confirm actions that change depth shown of outline.
#
#         :param new_model_outline: fixture :func:`.new_model_outline`.
#         :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
#         :param NAME: name of action under test.
#         :param COLLAPSE: whether method should collapse outline.
#         """
#         # Setup
#         class PatchTreeView:
#             def __init__(self):
#                 self.called_collapse = False
#                 self.called_expand = False
#
#             def collapse_all(self):
#                 self.called_collapse = True
#
#             def expand_all(self):
#                 self.called_expand = True
#
#         patch = PatchTreeView()
#         monkeypatch.setattr(Gtk.TreeView, 'collapse_all', patch.collapse_all)
#         monkeypatch.setattr(Gtk.TreeView, 'expand_all', patch.expand_all)
#         OUTLINE = new_model_outline()
#         ui_view = Gtk.TreeView(model=OUTLINE.ui_model)
#         target = VOUTLINE_ID.SetupUiDisplayOutlineId(p_ui_view=ui_view)
#         actions = Gio.SimpleActionGroup()
#         target._init_actions(p_action_group=actions)
#         action = actions.lookup_action(NAME)
#         # Test
#         target.on_change_depth(action, None)
#         assert patch.called_collapse is COLLAPSE
#         assert patch.called_expand is not COLLAPSE
#
#     def test_on_change_depth_undefined(self, monkeypatch, new_model_outline):
#         """Confirm expand outline for unexpected action.
#
#         :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
#         :param new_model_outline: fixture :func:`.new_model_outline`.
#         """
#         class PatchTreeView:
#             def __init__(self):
#                 self.called_collapse = False
#                 self.called_expand = False
#
#             def collapse_all(self):
#                 self.called_collapse = True
#
#             def expand_all(self):
#                 self.called_expand = True
#
#         patch = PatchTreeView()
#         monkeypatch.setattr(Gtk.TreeView, 'collapse_all', patch.collapse_all)
#         monkeypatch.setattr(Gtk.TreeView, 'expand_all', patch.expand_all)
#         OUTLINE = new_model_outline()
#         ui_view = Gtk.TreeView(model=OUTLINE.ui_model)
#         target = VOUTLINE_ID.SetupUiDisplayOutlineId(p_ui_view=ui_view)
#         NAME = 'undefined-action'
#         action = Gio.SimpleAction.new(NAME, None)
#         # Test
#         target.on_change_depth(action, None)
#         assert patch.called_collapse is False
#         assert patch.called_expand is True
#
#     def test_on_go_first_item(self, new_model_outline):
#         """| Confirm first item selection.
#         | Case: outline is not empty.
#
#         :param new_model_outline: fixture :func:`.new_model_outline`.
#         """
#         # Setup
#         OUTLINE = new_model_outline()
#         ui_view = Gtk.TreeView(model=OUTLINE.ui_model)
#         ui_selection = ui_view.get_selection()
#         target = VOUTLINE_ID.SetupUiDisplayOutlineId(p_ui_view=ui_view)
#         PATH_START = '3:0:0'
#         line_start = OUTLINE.ui_model.get_iter_from_string(PATH_START)
#         ui_selection.select_iter(line_start)
#         NAME_EXPECT = 'Name 0'
#         # Test
#         target.on_go_first_item(None, None)
#         model, line = ui_selection.get_selected()
#         assert line is not None
#         item_id = BUI.ModelOutline.get_item_direct(model, line)
#         assert NAME_EXPECT == item_id.name.text
#
#     def test_on_go_first_item_none(self, empty_model_outline):
#         """| Confirm first item selection.
#         | Case: outline is empty.
#
#         :param empty_model_outline: fixture :func:`.empty_model_outline`.
#         """
#         OUTLINE = empty_model_outline
#         ui_view = Gtk.TreeView(model=OUTLINE.ui_model)
#         ui_selection = ui_view.get_selection()
#         target = VOUTLINE_ID.SetupUiDisplayOutlineId(p_ui_view=ui_view)
#         # Test
#         target.on_go_first_item(None, None)
#         _, line = ui_selection.get_selected()
#         assert line is None
#
#     def test_on_go_last_item(self, new_model_outline):
#         """| Confirm last item selection.
#         | Case: outline is not empty; last item is not top level.
#
#         :param new_model_outline: fixture :func:`.new_model_outline`.
#         """
#         N_WIDTH = 4
#         N_DEPTH = 5
#         I_LAST = N_WIDTH + N_DEPTH - 1
#         OUTLINE = new_model_outline(N_WIDTH, N_DEPTH)
#         ui_view = Gtk.TreeView(model=OUTLINE.ui_model)
#         ui_selection = ui_view.get_selection()
#         target = VOUTLINE_ID.SetupUiDisplayOutlineId(p_ui_view=ui_view)
#         model, _ = ui_selection.get_selected()
#         PATH_START = '3:0:0'
#         line_start = model.get_iter_from_string(PATH_START)
#         ui_selection.select_iter(line_start)
#         EXPECT_NAME = 'Name ' + str(I_LAST)
#         # Test
#         target.on_go_last_item(None, None)
#         model, line = ui_selection.get_selected()
#         assert line is not None
#         item_id = BUI.ModelOutline.get_item_direct(model, line)
#         assert EXPECT_NAME == item_id.name.text
#
#     def test_on_go_last_item_none(self, empty_model_outline):
#         """| Confirm last item selection.
#         | Case: item outline is empty.
#
#         :param empty_model_outline: fixture :func:`.empty_model_outline`.
#         """
#         OUTLINE = empty_model_outline
#         ui_view = Gtk.TreeView(model=OUTLINE.ui_model)
#         ui_selection = ui_view.get_selection()
#         target = VOUTLINE_ID.SetupUiDisplayOutlineId(p_ui_view=ui_view)
#         # Test
#         target.on_go_last_item(None, None)
#         _, line = ui_selection.get_selected()
#         assert line is None
#
#     @pytest.mark.skip
#     @pytest.mark.parametrize('PRE_NAME, PRE_TITLE, POST_NAME, POST_TITLE', [
#         (False, True, True, True),
#         (True, True, True, False),
#         (True, False, False, True),
#         ])
#     def test_on_switch_columns(self, new_model_outline, PRE_NAME,
#                                PRE_TITLE, POST_NAME, POST_TITLE):
#         """Confirm visual column switches.
#
#         :param new_model_outline: fixture :func:`.new_model_outline`.
#         :param PRE_NAME: visibility of name column before switch.
#         :param PRE_TITLE: visibility of title column before switch.
#         :param POST_NAME: visibility of name column after switch.
#         :param POST_TITLE: visibility of title column after switch.
#         """
#         # Setup
#         OUTLINE = new_model_outline()
#         ui_view = Gtk.TreeView(model=OUTLINE.ui_model)
#         target = VOUTLINE_ID.SetupUiDisplayOutlineId(p_ui_view=ui_view)
#         I_COLUMN_NAME = 0
#         column_name = target._ui_view.get_column(I_COLUMN_NAME)
#         column_name.set_visible(PRE_NAME)
#         I_COLUMN_TITLE = 1
#         column_title = target._ui_view.get_column(I_COLUMN_TITLE)
#         column_title.set_visible(PRE_TITLE)
#         # Test
#         target.on_switch_columns(None, None)
#         assert column_name.get_visible() is POST_NAME
#         assert column_title.get_visible() is POST_TITLE
#
#     @pytest.mark.skip(reason='pending removal')
#     @pytest.mark.parametrize('NAME_PROP, NAME_ATTR', [
#         ('ui_selection', '_ui_selection'),
#         ('ui_view', '_ui_view'),
#         ])
#     def test_property_access(self, new_model_outline, NAME_PROP, NAME_ATTR):
#         """Confirm access limits of each property.
#
#         :param new_model_outline: fixture :func:`.new_model_outline`.
#         :param NAME_PROP: name of property.
#         :param NAME_ATTR: name of attribute.
#         """
#         # Setup
#         OUTLINE = new_model_outline()
#         ui_view = Gtk.TreeView(model=OUTLINE.ui_model)
#         target = VOUTLINE_ID.SetupUiDisplayOutlineId(p_ui_view=ui_view)
#         attr = getattr(target, NAME_ATTR)
#         CLASS = VOUTLINE_ID.SetupUiDisplayOutlineId
#         target_prop = getattr(CLASS, NAME_PROP)
#         # Test
#         assert target_prop.fget is not None
#         assert target_prop.fget(target) is attr
#         assert target_prop.fset is None
#         assert target_prop.fdel is None


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
