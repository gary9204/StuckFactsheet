"""
Unit tests for class to select a topic specification.  See
:mod:`.select_spec`.

.. include:: /test/refs_include_pytest.txt
"""
import gi   # type: ignore[import]
import logging
import pytest   # type: ignore[import]

import factsheet.bridge_ui as BUI
import factsheet.model.idcore as MIDCORE
import factsheet.view.chooser_item as VCHOOSER_ITEM
import factsheet.view.ui as UI

gi.require_version('Gtk', '3.0')
from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class ItemStub(MIDCORE.IdCore[
        BUI.ModelTextMarkup, BUI.ModelTextMarkup, BUI.ModelTextMarkup]):
    """Stub for item based on :class:`.IdCore`."""

    def __init__(self, p_name='No name', p_summary='No summary',
                 p_title='No title'):
        self._name = BUI.ModelTextMarkup(p_text=p_name)
        self._summary = BUI.ModelTextMarkup(p_text=p_summary)
        self._title = BUI.ModelTextMarkup(p_text=p_title)
        super().__init__()


@pytest.fixture
def new_ui():
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
    outline_view = factory_view()
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
    return model_outline, outline_view


class TestFieldsIdCore:
    """Unit tests for :class:`.FieldsId`."""

    def test_members(self):
        """Confirm member definitions."""
        # Setup
        # Test
        assert not bool(VCHOOSER_ITEM.FieldsId.VOID)
        assert VCHOOSER_ITEM.FieldsId.NAME
        assert VCHOOSER_ITEM.FieldsId.SUMMARY
        assert VCHOOSER_ITEM.FieldsId.TITLE


class TestSelectItem:
    """Unit tests for :class:`.ChooserItem`."""

    def test_no_summary(self):
        """Confirm class attribute definition."""
        # Setup
        target = VCHOOSER_ITEM.ChooserItem
        EXPECT = 'Please choose an item in the outline above.'
        # Test
        assert isinstance(target.NO_SUMMARY, str)
        assert EXPECT == target.NO_SUMMARY

    def test_init(self, new_ui):
        """Confirm initialization orchestration.

        :param new_ui: fixture :func:`.new_ui`.
        """
        # Setup
        MODEL_OUTLINE, VIEW_OUTLINE = new_ui
        # Test
        target = VCHOOSER_ITEM.ChooserItem(p_view_outline=VIEW_OUTLINE)
        assert isinstance(target._ui_chooser, Gtk.Paned)
        assert target._ui_chooser.get_visible()
        assert target._ui_view_outline is VIEW_OUTLINE
        assert target._ui_view_outline.get_model() is MODEL_OUTLINE.ui_model
        assert target._ui_view_outline.get_visible()
        assert target.NO_SUMMARY == target._summary.text
        assert VCHOOSER_ITEM.FieldsId.NAME == target._scope_search

    def test_init_search(self, new_ui, monkeypatch):
        """Confirm initialization of search bar.

        :param new_ui: fixture :func:`.new_ui`.
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
                    ui_search=Gtk.SearchBar(),
                    ui_header=Gtk.HeaderBar(),
                    ui_search_in_name=Gtk.CheckButton(),
                    ui_search_in_summary=Gtk.CheckButton(),
                    ui_search_in_title=Gtk.CheckButton(),
                    ui_search_entry=Gtk.Entry(),
                    )

            def set_equal_func(self, *args):
                self.equal_func_args = args

        _MODEL_OUTLINE, VIEW_OUTLINE = new_ui
        target = VCHOOSER_ITEM.ChooserItem(p_view_outline=VIEW_OUTLINE)

        patch_call = PatchCall()
        monkeypatch.setattr(
            UI.GetUiElementByStr, '__call__', patch_call.__call__)
        monkeypatch.setattr(
            Gtk.TreeView, 'set_search_equal_func', patch_call.set_equal_func)
        get_ui_element = UI.GetUiElementByStr(p_string_ui='')
        C_FIRST = 0
        # Test
        target._init_search(get_ui_element)
        assert VCHOOSER_ITEM.FieldsId.NAME == target._scope_search
        assert target._search_bar is patch_call.stubs['ui_search']
        assert target._ui_view_outline.get_enable_search()
        assert C_FIRST == target._ui_view_outline.get_search_column()
        assert target._ui_view_outline.get_search_entry(
            ) is patch_call.stubs['ui_search_entry']
        equal_func, extra = patch_call.equal_func_args
        assert target._match_spec_ne == equal_func
        assert extra is None

    @pytest.mark.parametrize('NAME_SIGNAL, NAME_BUTTON, ORIGIN, N_DEFAULT', [
        ('toggled', 'ui_search_in_name', Gtk.CheckButton, 0),
        ('toggled', 'ui_search_in_summary', Gtk.CheckButton, 0),
        ('toggled', 'ui_search_in_title', Gtk.CheckButton, 0),
        ])
    def test_init_search_signals(self, new_ui, monkeypatch, NAME_SIGNAL,
                                 NAME_BUTTON, ORIGIN, N_DEFAULT):
        """Confirm initialization of signal connections.

        :param new_ui: fixture :func:`.new_ui`.
        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        :param NAME_SIGNAL: name of signal.
        :param NAME_BUTTON: name of scope button connected to signal.
        :param ORIGIN: GTK class of connected button.
        :param N_DEFAULT: number of default handlers.
        """
        # Setup
        class PatchCall:
            def __call__(self, p_id_ui):
                stub = self.stubs.get(p_id_ui)
                return stub

            def __init__(self):
                self.stubs = dict(
                    ui_search=Gtk.SearchBar(),
                    ui_header=Gtk.HeaderBar(),
                    ui_search_in_name=Gtk.CheckButton(),
                    ui_search_in_summary=Gtk.CheckButton(),
                    ui_search_in_title=Gtk.CheckButton(),
                    ui_search_entry=Gtk.Entry(),
                    )

            def set_equal_func(self, *args):
                self.equal_func_args = args

        _MODEL_OUTLINE, VIEW_OUTLINE = new_ui
        target = VCHOOSER_ITEM.ChooserItem(p_view_outline=VIEW_OUTLINE)

        patch_call = PatchCall()
        monkeypatch.setattr(
            UI.GetUiElementByStr, '__call__', patch_call.__call__)
        monkeypatch.setattr(
            Gtk.TreeView, 'set_search_equal_func', patch_call.set_equal_func)
        get_ui_element = UI.GetUiElementByStr(p_string_ui='')

        origin_gtype = GO.type_from_name(GO.type_name(ORIGIN))
        signal = GO.signal_lookup(NAME_SIGNAL, origin_gtype)
        # Test
        target._init_search(get_ui_element)
        button = patch_call.stubs[NAME_BUTTON]
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

    @pytest.mark.parametrize(
        'NAME_SIGNAL, NAME_ATTRIBUTE, ORIGIN, N_DEFAULT', [
            ('changed', '_ui_selection', Gtk.TreeSelection, 0),
            ])
    def test_init_signals(
            self, new_ui, NAME_SIGNAL, NAME_ATTRIBUTE, ORIGIN, N_DEFAULT):
        """Confirm initialization of signal connections.

        :param new_ui: fixture :func:`.new_ui`.
        :param NAME_SIGNAL: name of signal.
        :param NAME_ATTRIBUTE: name of attribute connected to signal.
        :param ORIGIN: GTK class of connected attribute.
        :param N_DEFAULT: number of default handlers.
        """
        # Setup
        _MODEL_OUTLINE, VIEW_OUTLINE = new_ui
        target = VCHOOSER_ITEM.ChooserItem(p_view_outline=VIEW_OUTLINE)
        origin_gtype = GO.type_from_name(GO.type_name(ORIGIN))
        signal = GO.signal_lookup(NAME_SIGNAL, origin_gtype)
        # Test
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

    def test_init_summary(self, new_ui, monkeypatch):
        """Confirm initialization of spec summary.

        :param new_ui: fixture :func:`.new_ui`.
        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        class PatchCall:
            def __init__(self):
                self.id_ui = 'Oops!'
                self.site = Gtk.Viewport()

            def __call__(self, p_id_ui):
                self.id_ui = p_id_ui
                return self.site

        UI_ID = 'ui_site_summary'
        _MODEL_OUTLINE, VIEW_OUTLINE = new_ui
        target = VCHOOSER_ITEM.ChooserItem(p_view_outline=VIEW_OUTLINE)

        patch_call = PatchCall()
        monkeypatch.setattr(
            UI.GetUiElementByStr, '__call__', patch_call.__call__)
        get_ui_element = UI.GetUiElementByStr(p_string_ui='')
        # Test
        target._init_summary(get_ui_element)
        assert UI_ID == patch_call.id_ui
        view_summary = patch_call.site.get_child()
        assert target._summary.ui_model is view_summary.get_buffer()
        assert view_summary.get_visible()
        assert view_summary.get_wrap_mode() is Gtk.WrapMode.WORD_CHAR

    def test_init_view_outline(self, new_ui, monkeypatch):
        """Confirm initialization of spec outline.

        :param new_ui: fixture :func:`.new_ui`.
        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        class PatchCall:
            def __init__(self):
                self.id_ui = 'Oops!'
                self.site = Gtk.ScrolledWindow()

            def __call__(self, p_id_ui):
                self.id_ui = p_id_ui
                return self.site

        UI_ID = 'ui_site_outline'
        N_COLUMNS = 2
        C_NAME = 0
        TITLE_C_NAME = 'Name'
        C_TITLE = 1
        TITLE_C_TITLE = 'Title'
        MODEL_OUTLINE, VIEW_OUTLINE = new_ui
        target = VCHOOSER_ITEM.ChooserItem(p_view_outline=VIEW_OUTLINE)

        factory_view = (BUI.FactoryViewOutline[
            BUI.ModelOutlineMulti, ItemStub](MODEL_OUTLINE))
        VIEW_PATCH = factory_view()
        target._ui_view_outline = VIEW_PATCH

        patch_call = PatchCall()
        monkeypatch.setattr(
            UI.GetUiElementByStr, '__call__', patch_call.__call__)
        get_ui_element = UI.GetUiElementByStr(p_string_ui='')
        # Test
        target._init_view_outline(get_ui_element)
        assert UI_ID == patch_call.id_ui
        assert target._ui_view_outline is patch_call.site.get_child()
        columns = target._ui_view_outline.get_columns()
        assert TITLE_C_NAME == target._column_name.get_title()
        assert target._column_name is columns[C_NAME]
        assert TITLE_C_TITLE == target._column_title.get_title()
        assert target._column_title is columns[C_TITLE]
        assert N_COLUMNS == len(columns)
        assert target._ui_selection is target._ui_view_outline.get_selection()
        # assert target._ui_view_outline.get_visible()

    def test_sync_to_search(self, new_ui, monkeypatch):
        """Confirm initialization of search bar.

        :param new_ui: fixture :func:`.new_ui`.
        :param monkeypatch: built-in fixture `Pytest monkeypatch`_.
        """
        # Setup
        class PatchCall:
            def __init__(self):
                self.binding_args = None

            def bind_property(self, *args):
                self.binding_args = args

        _MODEL_OUTLINE, VIEW_OUTLINE = new_ui
        target = VCHOOSER_ITEM.ChooserItem(p_view_outline=VIEW_OUTLINE)

        patch_call = PatchCall()
        monkeypatch.setattr(
            Gtk.ToggleButton, 'bind_property', patch_call.bind_property)
        BUTTON = VCHOOSER_ITEM.ButtonFind()
        PROP_SOURCE = 'active'
        PROP_TARGET = 'search-mode-enabled'
        # Test
        target.sync_to_search(BUTTON)
        prop_source, target_bind, prop_target, flags = patch_call.binding_args
        assert PROP_SOURCE == prop_source
        assert isinstance(target_bind, Gtk.SearchBar)
        assert PROP_TARGET == prop_target
        assert GO.BindingFlags.BIDIRECTIONAL == flags

    @pytest.mark.parametrize('METHOD, LINE_STR, EXPECT', [
        ('_markup_cell_name', '0', 'name_0xx'),
        ('_markup_cell_name', '1:1', 'name_11x'),
        ('_markup_cell_title', '1', 'title_1xx'),
        ('_markup_cell_title', '1:1:2', 'title_112'),
        ])
    def test_markup_cell(self, new_ui, METHOD, LINE_STR, EXPECT):
        """Confirm cell data function updates column text.

        :param new_ui: fixture :func:`.new_ui`.
        :param METHOD: markup method under test.
        :param LINE_STR: line of sample item as string.
        :param EXPECT: text to expect in cell.
        """
        # Setup
        MODEL_OUTLINE, VIEW_OUTLINE = new_ui
        target = VCHOOSER_ITEM.ChooserItem(p_view_outline=VIEW_OUTLINE)
        target_method = getattr(target, METHOD)
        column = Gtk.TreeViewColumn()
        render = Gtk.CellRendererText()
        column.pack_start(render, expand=True)
        line = MODEL_OUTLINE.ui_model.get_iter_from_string(LINE_STR)
        # Test
        target_method(None, render, MODEL_OUTLINE.ui_model, line, None)
        assert EXPECT == render.get_property('text')

    @pytest.mark.parametrize('METHOD', [
        ('_markup_cell_name'),
        ('_markup_cell_title'),
        ])
    def test_markup_cell_none(self, METHOD):
        """Confirm cell data function updates column text.

        :param METHOD: markup method under test.
        """
        # Setup
        MODEL_OUTLINE = BUI.ModelOutlineMulti[ItemStub]()
        MODEL_OUTLINE.ui_model.append(None, [None])
        VIEW_OUTLINE = BUI.ViewOutline()
        VIEW_OUTLINE.set_model(MODEL_OUTLINE.ui_model)
        target = VCHOOSER_ITEM.ChooserItem(p_view_outline=VIEW_OUTLINE)
        target_method = getattr(target, METHOD)
        column = Gtk.TreeViewColumn()
        render = Gtk.CellRendererText()
        column.pack_start(render, expand=True)
        line = MODEL_OUTLINE.ui_model.get_iter_first()
        EXPECT = 'Missing'
        # Test
        target_method(None, render, MODEL_OUTLINE.ui_model, line, None)
        assert EXPECT == render.get_property('text')

    def test_on_changed_selection(self, new_ui):
        """| Confirm summary shown matches chosen spec.
        | Case: a spec at line choosen.

        :param new_ui: fixture :func:`.new_ui`.
        """
        # Setup
        MODEL_OUTLINE, VIEW_OUTLINE = new_ui
        VIEW_OUTLINE.expand_all()
        target = VCHOOSER_ITEM.ChooserItem(p_view_outline=VIEW_OUTLINE)
        LINE_STR = '1:0'
        line = MODEL_OUTLINE.ui_model.get_iter_from_string(LINE_STR)
        summary_expect = 'summary_10x'
        target._ui_selection.select_iter(line)
        target._summary.text = 'Oops'
        # Test
        target.on_changed_selection(None)
        assert summary_expect == target._summary.text

    def test_on_changed_selection_absent(self, new_ui):
        """| Confirm summary shown matches chosen spec.
        | Case: no spec at line choosen.

        :param new_ui: fixture :func:`.new_ui`.
        """
        # Setup
        MODEL_OUTLINE = BUI.ModelOutlineMulti[ItemStub]()
        MODEL_OUTLINE.ui_model.append(None, [None])
        VIEW_OUTLINE = BUI.ViewOutline()
        VIEW_OUTLINE.set_model(MODEL_OUTLINE.ui_model)
        target = VCHOOSER_ITEM.ChooserItem(p_view_outline=VIEW_OUTLINE)
        target._ui_view_outline.expand_all()
        line = MODEL_OUTLINE.ui_model.get_iter_first()
        assert line is not None
        target._ui_selection.select_iter(line)
        target._summary.text = 'Oops'
        # Test
        target.on_changed_selection(None)
        assert target.NO_SUMMARY == target._summary.text

    def test_on_changed_selection_none(self, new_ui):
        """| Confirm summary shown matches chosen spec.
        | Case: no spec is choosen.

        :param new_ui: fixture :func:`.new_ui`.
        """
        # Setup
        _MODEL_OUTLINE, VIEW_OUTLINE = new_ui
        VIEW_OUTLINE.expand_all()
        target = VCHOOSER_ITEM.ChooserItem(p_view_outline=VIEW_OUTLINE)
        target._ui_view_outline.expand_all()
        target._ui_selection.unselect_all()
        target._summary.text = 'Oops'
        # Test
        target.on_changed_selection(None)
        assert target.NO_SUMMARY == target._summary.text

    @pytest.mark.parametrize('SCOPE, ACTIVE, FIELD, EXPECT', [
        (VCHOOSER_ITEM.FieldsId.VOID, True, VCHOOSER_ITEM.FieldsId.NAME,
         VCHOOSER_ITEM.FieldsId.NAME),
        (VCHOOSER_ITEM.FieldsId.VOID, True, VCHOOSER_ITEM.FieldsId.SUMMARY,
         VCHOOSER_ITEM.FieldsId.SUMMARY),
        (VCHOOSER_ITEM.FieldsId.VOID, True, VCHOOSER_ITEM.FieldsId.TITLE,
         VCHOOSER_ITEM.FieldsId.TITLE),
        (~VCHOOSER_ITEM.FieldsId.VOID, False, VCHOOSER_ITEM.FieldsId.NAME,
         VCHOOSER_ITEM.FieldsId.SUMMARY | VCHOOSER_ITEM.FieldsId.TITLE),
        ])
    def test_on_changed_search_scope(
            self, new_ui, SCOPE, ACTIVE, FIELD, EXPECT):
        """Confirm change in search scope.

        :param new_ui: fixture :func:`.new_ui`.
        :param SCOPE: fields identifying scope of search.
        :param ACTIVE: True when scope button set to active.
        :param FIELD: changed scope field.
        :param EXPECT: expected result.
        """
        # Setup
        _MODEL_OUTLINE, VIEW_OUTLINE = new_ui
        target = VCHOOSER_ITEM.ChooserItem(p_view_outline=VIEW_OUTLINE)
        target._scope_search = SCOPE
        button = Gtk.ToggleButton(active=ACTIVE)
        # Test
        target.on_changed_search_scope(button, FIELD)
        assert EXPECT == target._scope_search

    @pytest.mark.parametrize('SCOPE, PATH_ITEM, MATCH_KEY, EXPECT, EXPANDED', [
        (VCHOOSER_ITEM.FieldsId.VOID, '1:0', 'name 01x', True, False),
        (VCHOOSER_ITEM.FieldsId.NAME, '0:1', 'name_01x', False, False),
        (VCHOOSER_ITEM.FieldsId.NAME, '0', 'e_0x', False, False),
        (VCHOOSER_ITEM.FieldsId.NAME, '0', '$e_0x', True, True),
        (VCHOOSER_ITEM.FieldsId.VOID, '1', 'summary_1xx', True, False),
        (VCHOOSER_ITEM.FieldsId.SUMMARY, '1', 'summary_1xx', False, False),
        (VCHOOSER_ITEM.FieldsId.SUMMARY, '1:1:1', 'y_111', False, False),
        (VCHOOSER_ITEM.FieldsId.SUMMARY, '1:1:1', 'y_11$', True, True),
        (VCHOOSER_ITEM.FieldsId.VOID, '0:0:0', 'title_000', True, False),
        (VCHOOSER_ITEM.FieldsId.TITLE, '0:0:0', 'title_000', False, False),
        (VCHOOSER_ITEM.FieldsId.TITLE, '1:1', 'le_1', False, False),
        (VCHOOSER_ITEM.FieldsId.TITLE, '1:1', 'le_11', False, False),
        (VCHOOSER_ITEM.FieldsId.TITLE, '1:1', 'le$11', True, True),
            ])
    def test_match_spec_ne(self, new_ui, monkeypatch,
                           SCOPE, PATH_ITEM, MATCH_KEY, EXPECT, EXPANDED):
        """Confirm method returns False when field matches search key.

        :param new_ui: fixture :func:`.new_ui`.
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

        MODEL_OUTLINE, VIEW_OUTLINE = new_ui
        target = VCHOOSER_ITEM.ChooserItem(p_view_outline=VIEW_OUTLINE)
        target._scope_search = SCOPE
        line = MODEL_OUTLINE.ui_model.get_iter_from_string(PATH_ITEM)
        # Test
        actual = target._match_spec_ne(
            MODEL_OUTLINE.ui_model, None, MATCH_KEY, line, None)
        assert actual is EXPECT
        assert patch_expand.called is EXPANDED
        if EXPANDED:
            assert PATH_ITEM == patch_expand.path.to_string()

    def test_match_spec_ne_absent(self, caplog):
        """Confirm method returns True and logs warning when spec is None.

        :param caplog: built-in fixture `Pytest caplog`_.
        """
        # Setup
        MODEL_OUTLINE = BUI.ModelOutlineMulti[ItemStub]()
        MODEL_OUTLINE.ui_model.append(None, [None])
        VIEW_OUTLINE = BUI.ViewOutline()
        VIEW_OUTLINE.set_model(MODEL_OUTLINE.ui_model)
        target = VCHOOSER_ITEM.ChooserItem(p_view_outline=VIEW_OUTLINE)
        MATCH_KEY = 'name'
        line = MODEL_OUTLINE.ui_model.get_iter_first()
        N_LOGS = 1
        LAST = -1
        log_message = ('Outline contains None at line "0"'
                       ' (ChooserItem._match_spec_ne)')
        # Test
        actual = target._match_spec_ne(
            MODEL_OUTLINE.ui_model, None, MATCH_KEY, line, None)
        assert actual
        assert N_LOGS == len(caplog.records)
        record = caplog.records[LAST]
        assert log_message == record.message
        assert 'WARNING' == record.levelname

    @pytest.mark.parametrize('NAME_PROP, NAME_ATTR', [
        ('ui_chooser', '_ui_chooser'),
        ])
    def test_property_access(self, new_ui, NAME_PROP, NAME_ATTR):
        """Confirm access limits of each property.

        :param new_ui: fixture :func:`.new_ui`.
        :param NAME_PROP: name of property.
        :param NAME_ATTR: name of attribute.
        """
        # Setup
        _MODEL_OUTLINE, VIEW_OUTLINE = new_ui
        target = VCHOOSER_ITEM.ChooserItem(p_view_outline=VIEW_OUTLINE)
        attr = getattr(target, NAME_ATTR)
        CLASS = VCHOOSER_ITEM.ChooserItem
        target_prop = getattr(CLASS, NAME_PROP)
        # Test
        assert target_prop.fget is not None
        assert target_prop.fget(target) is attr
        assert target_prop.fset is None
        assert target_prop.fdel is None


class TestModule:
    """Unit tests for module-level components of :mod:`.select_spec`."""

    @pytest.mark.parametrize('ATTR, TYPE_EXPECT', [
        (VCHOOSER_ITEM.logger, logging.Logger),
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
        # (VTOPICS.UiEditorTopics, Gtk.Frame),
        (VCHOOSER_ITEM.ButtonFind, Gtk.ToggleButton),
        (VCHOOSER_ITEM.FactoryDisplaySummary, BUI.FactoryDisplayTextStyled),
        (VCHOOSER_ITEM.ModelSummary, BUI.ModelTextStyled),
        (VCHOOSER_ITEM.UiChooserItem, Gtk.Paned),
        (VCHOOSER_ITEM.ViewOutlineItem, BUI.ViewOutline),
        ])
    def test_types(self, TYPE_TARGET, TYPE_EXPECT):
        """Confirm type alias definitions.

        :param TYPE_TARGET: type alias under test.
        :param TYPE_EXPECT: type expected.
        """
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_EXPECT
