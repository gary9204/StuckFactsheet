"""
Unit tests for bridge classes to encapsulate witget toolkit outline
classes. See :mod:`.bridge_outline`.

.. include:: /test/refs_include_pytest.txt
"""
import dataclasses as DC
import gi   # type: ignore[import]
import pytest   # type: ignore[import]
import typing

import factsheet.bridge_gtk.bridge_outline as BOUTLINE

gi.require_version('Gtk', '3.0')
from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class TestFactoryChooserOutline:
    """Unit tests for :class:`.FactoryChooserOutline`."""

    @pytest.mark.parametrize('SUBTYPE, TYPE_UI_MODEL', [
        ('MULTI', BOUTLINE.UiModelOutlineMulti),
        ('SINGLE', BOUTLINE.UiModelOutlineSingle),
        ], indirect=['SUBTYPE'])
    def test_init(self, SUBTYPE, TYPE_UI_MODEL):
        """Confirm storage initialization.

        :param SUBTYPE: identifies outline model subclass under test.
        :param TYPE_UI_MODEL: user interface model type for outline.
        """
        # Setup
        outline = SUBTYPE
        # Test
        target_type = BOUTLINE.FactoryChooserOutline[TYPE_UI_MODEL, PatchItem]
        target = target_type(p_model_outline=outline)
        assert target._ui_model is outline.ui_model

    @pytest.mark.parametrize('SUBTYPE, TYPE_UI_MODEL', [
        ('MULTI', BOUTLINE.UiModelOutlineMulti),
        ('SINGLE', BOUTLINE.UiModelOutlineSingle),
        ], indirect=['SUBTYPE'])
    def test_call(self, SUBTYPE, TYPE_UI_MODEL):
        """Confirm return is a view for choosing from model.

        :param SUBTYPE: identifies outline model subclass under test.
        :param TYPE_UI_MODEL: user interface model type for outline.
        """
        # Setup
        outline = SUBTYPE
        target_type = BOUTLINE.FactoryChooserOutline[TYPE_UI_MODEL, PatchItem]
        target = target_type(p_model_outline=outline)
        # Test
        chooser = target()
        assert isinstance(chooser, Gtk.ComboBox)
        assert chooser.get_model() is outline.ui_model


class TestViewChooserOutline:
    """Unit tests for :class:`.FactoryViewOutline`."""

    @pytest.mark.parametrize('SUBTYPE, TYPE_UI_MODEL', [
        ('MULTI', BOUTLINE.UiModelOutlineMulti),
        ('SINGLE', BOUTLINE.UiModelOutlineSingle),
        ], indirect=['SUBTYPE'])
    def test_init(self, SUBTYPE, TYPE_UI_MODEL):
        """Confirm storage initialization.

        :param SUBTYPE: identifies outline model subclass under test.
        :param TYPE_UI_MODEL: user interface model type for outline.
        """
        # Setup
        outline = SUBTYPE
        # Test
        target_type = BOUTLINE.FactoryViewOutline[TYPE_UI_MODEL, PatchItem]
        target = target_type(p_model_outline=outline)
        assert target._ui_model is outline.ui_model

    @pytest.mark.parametrize('SUBTYPE, TYPE_UI_MODEL', [
        ('MULTI', BOUTLINE.UiModelOutlineMulti),
        ('SINGLE', BOUTLINE.UiModelOutlineSingle),
        ], indirect=['SUBTYPE'])
    def test_call(self, SUBTYPE, TYPE_UI_MODEL):
        """Confirm return is a view for outline.

        :param SUBTYPE: identifies outline model subclass under test.
        :param TYPE_UI_MODEL: user interface model type for outline.
        """
        # Setup
        outline = SUBTYPE
        target_type = BOUTLINE.FactoryViewOutline[TYPE_UI_MODEL, PatchItem]
        target = target_type(p_model_outline=outline)
        # Test
        view = target()
        assert isinstance(view, Gtk.TreeView)
        assert view.get_model() is outline.ui_model


def gtk_model_to_names(p_model):
    """Return dictionary of names in a `Gtk.TreeModel`_ indexed by line.

    :param p_model: model to extract names from.

    .. _Gtk.TreeModel:
        https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/TreeModel.html
    """
    C_ITEM = 0
    persist = dict()
    for row in iter_section(p_model):
        path_str = p_model.get_string_from_iter(row)
        item = p_model[row][C_ITEM]
        persist[path_str] = item.name
    return persist


def iter_section(p_model, p_it=None):
    """Return iterator over all rows at or under a given row of
    `Gtk.TreeModel`_.

    :param p_model: model containing rows.
    :param p_it: iterate over this row and all of its descendants.
    """
    if p_it is not None:
        yield p_it
    it_child = p_model.iter_children(p_it)
    while it_child is not None:
        yield from iter_section(p_model, it_child)
        it_child = p_model.iter_next(it_child)


def insert_snippet_children(p_model, p_path) -> BOUTLINE.LineOutline:
    """Insert snippet into :data:`.UiModelOutlineMulti` at given path.

    The snippet includes a line with children as shown below.

        |     Item cxx
        |         Item cax
        |         Item cbx

    The function places the snipppet as the last child of line at given
    path.  If line is None, the snippet is placed at the end of the
    outline.

    :param p_model: model in which to insert snippet.
    :param p_path: path to parent for snippet.
    :returns: line of snippet root in model.
    """
    line = None
    if p_path is not None:
        line = p_model.get_iter_from_string(p_path)
    item = PatchItem('Item cxx', 'Children')
    i_cxx = p_model.append(line, [item])
    item = PatchItem('Item cax', 'Children')
    _i_cax = p_model.append(i_cxx, [item])
    item = PatchItem('Item cbx', 'Children')
    _i_cbx = p_model.append(i_cxx, [item])
    return i_cxx


def insert_snippet_multiple(p_model, p_path) -> BOUTLINE.LineOutline:
    """Insert snippet into :data:`.UiModelOutlineMulti` at given path.

    The snippet includes multiple levels as shown below.

        | Item mxx
        |     Item max
        |         Item maa
        |         Item mab

    The function places the snipppet as the last child of line at given
    path.  If line is None, the snippet is placed at the end of the
    outline.

    :param p_model: model in which to insert snippet.
    :param p_path: path to parent for snippet.
    :returns: line of snippet root in model.
    """
    line = None
    if p_path is not None:
        line = p_model.get_iter_from_string(p_path)
    item = PatchItem('Item mxx', 'Multiple')
    i_mxx = p_model.append(line, [item])
    item = PatchItem('Item max', 'Multiple')
    i_max = p_model.append(i_mxx, [item])
    item = PatchItem('Item maa', 'Multiple')
    _i_maa = p_model.append(i_max, [item])
    item = PatchItem('Item mab', 'Multiple')
    _i_mab = p_model.append(i_max, [item])
    return i_mxx


def insert_snippet_single(p_model, p_path) -> BOUTLINE.LineOutline:
    """Insert snippet into :data:`.UiModelOutlineMulti` at given path.

    The snippet includes a single line as shown below.

        | Item sxx

    The function places the snipppet as the last child of line at given
    path.  If line is None, the snippet is placed at the end of the
    outline.

    :param p_model: model in which to insert snippet.
    :param p_path: path to parent for snippet.
    :returns: line of snippet root in model.
    """
    line = None
    if p_path is not None:
        line = p_model.get_iter_from_string(p_path)
    item = PatchItem('Item sxx', 'Single')
    i_sxx = p_model.append(line, [item])
    return i_sxx


@pytest.fixture
def NAMES(request, new_names_model_multi, new_names_model_single):
    """Pytest fixture: Return names of items in outline.

    :param request: built-in fixture `Pytest request`_ identifies type
        of outline.
    :param new_names_model_multi: fixture :func:`.new_names_model_multi`.
    :param new_names_model_single: fixture :func:`.new_names_model_single`.
    """
    # Setup
    FACTORY = dict(MULTI=new_names_model_multi, SINGLE=new_names_model_single)
    names = FACTORY[request.param]()
    return names


@pytest.fixture
def new_gtk_model_multi():
    """Pytest fixture: Return `Gtk.TreeStore`_ model factory.

    The structure of each model is as shown below.

        | Item 0xx
        |     Item 00x
        |         Item 000
        |     Item 01x
        | Item 1xx
        |     Item 10x
        |     Item 11x
        |         Item 110
        |         Item 111
        |         Item 112

    :param factory p_tag: identifies model (default is 'Target').

    .. _`Gtk.TreeStore`:
        https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/TreeStore.html
    """
    def new_model(p_tag='Target'):
        model = Gtk.TreeStore(GO.TYPE_PYOBJECT)
        item = PatchItem('Item 0xx', p_tag)
        i_0xx = model.append(None, [item])
        item = PatchItem('Item 00x', p_tag)
        i_00x = model.append(i_0xx, [item])
        item = PatchItem('Item 000', p_tag)
        _i_000 = model.append(i_00x, [item])
        item = PatchItem('Item 01x', p_tag)
        i_0xx = model.append(i_0xx, [item])
        item = PatchItem('Item 1xx', p_tag)
        i_1xx = model.append(None, [item])
        item = PatchItem('Item 10x', p_tag)
        _i_10x = model.append(i_1xx, [item])
        item = PatchItem('Item 11x', p_tag)
        i_11x = model.append(i_1xx, [item])
        item = PatchItem('Item 110', p_tag)
        _i_110 = model.append(i_11x, [item])
        item = PatchItem('Item 111', p_tag)
        _i_111 = model.append(i_11x, [item])
        item = PatchItem('Item 112', p_tag)
        _i_112 = model.append(i_11x, [item])
        return model

    return new_model


@pytest.fixture
def new_gtk_model_single():
    """Pytest fixture: Return `Gtk.ListStore`_ model factory.

    The structure of each model is as shown below.

        | Item 0
        | Item 1
        | Item 2
        | ...

    :param factory p_n_items: number of items in model (default is 5).
    :param factory p_tag: identifies model (default is 'Target').

    .. _`Gtk.ListStore`:
        https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/ListStore.html
    """
    def new_model(p_n_items=5, p_tag='Target'):
        model = Gtk.ListStore(GO.TYPE_PYOBJECT)
        for i in range(p_n_items):
            name = 'Item {}'.format(i)
            item = PatchItem(name=name, tag=p_tag)
            row = [item]
            _ = model.append(row)
        return model

    return new_model


@pytest.fixture
def new_names_model_multi():
    """Pytest fixture: Return factory for names in model returned by
    :func:`.new_gtk_model_multi`.

    This fixture primarily serves to validate test fixtures and
    functions.
    """
    def new_names():
        names = {
            '0': 'Item 0xx',            # Position 0
            '0:0': 'Item 00x',          # Position 1
            '0:0:0': 'Item 000',        # Position 2
            '0:1': 'Item 01x',          # Position 3
            '1': 'Item 1xx',            # Position 4
            '1:0': 'Item 10x',          # Position 5
            '1:1': 'Item 11x',          # Position 6
            '1:1:0': 'Item 110',        # Position 7
            '1:1:1': 'Item 111',        # Position 8
            '1:1:2': 'Item 112',        # Position 9
            }
        return names

    return new_names


@pytest.fixture
def new_names_model_single():
    """Pytest fixture: Return factory for names in model returned by
    :func:`.new_gtk_model_single`.

    This fixture primarily serves to validate test fixtures and
    functions.
    """
    def new_names():
        names = {
            '0': 'Item 0',
            '1': 'Item 1',
            '2': 'Item 2',
            '3': 'Item 3',
            '4': 'Item 4',
            }
        return names

    return new_names


@pytest.fixture
def new_patch_multi(new_gtk_model_multi):
    """Pytest fixture: Return factory for multi-level outlines.

    Each outline is patched with non-empty model.

    :param new_gtk_model_multi: fixture :func:`.new_gtk_model_multi`.
    """
    def new_multi():
        outline = BOUTLINE.ModelOutlineMulti[PatchItem]()
        outline._ui_model = new_gtk_model_multi()
        return outline

    return new_multi


@pytest.fixture
def new_patch_single(new_gtk_model_single):
    """Pytest fixture: Return factory for single-level outlines.

    Each outline is patched with non-empty model.

    :param new_gtk_model_single: fixture :func:`.new_gtk_model_single`.
    """
    def new_single():
        outline = BOUTLINE.ModelOutlineSingle[PatchItem]()
        outline._ui_model = new_gtk_model_single()
        return outline

    return new_single


@DC.dataclass
class PatchItem:
    """Placeholder item class for unit tests.

    :param name: name to identify an item.
    :param tag: string to identify all items in a section or model.
    """
    name: str
    tag: str = 'Target'


class TestCheckFixtures:
    """Unit tests to check test fixtures and test module functions."""

    def test_model_multi(self, new_gtk_model_multi, new_names_model_multi):
        """Confirm multi-level model structure and content.

        :param new_gtk_model_multi: fixture :func:`.new_gtk_model_multi`.
        :param new_names_model_multi: fixture :func:`.new_names_model_multi`.
        """
        # Setup
        model = new_gtk_model_multi()
        names = new_names_model_multi()
        # Test
        target = gtk_model_to_names(model)
        assert names == target

    def test_model_single(
            self, new_gtk_model_single, new_names_model_single):
        """Confirm single-level model structure and content.

        :param new_gtk_model_single: fixture :func:`.new_gtk_model_single`.
        :param new_names_model_single: fixture :func:`.new_names_model_single`.
        """
        # Setup
        model = new_gtk_model_single()
        names = new_names_model_single()
        # Test
        target = gtk_model_to_names(model)
        assert names == target


class TestModelOutline:
    """Unit tests for :class:`.ModelOutline`."""

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (BOUTLINE.ModelOutline, 'insert_after'),
        (BOUTLINE.ModelOutline, 'insert_before'),
        (BOUTLINE.ModelOutline, 'lines'),
        (BOUTLINE.ModelOutline, '_set_persist'),
        ])
    def test_method_abstract(self, CLASS, NAME_METHOD):
        """Confirm each abstract method is specified.

        :param CLASS: abstract class under test.
        :param NAME_METHOD: confirm method with this name is abstract.
        """
        # Setup
        # Test
        assert hasattr(CLASS, '__abstractmethods__')
        assert NAME_METHOD in CLASS.__abstractmethods__

    @pytest.mark.parametrize('SUBCLASS, MODEL', [
        (BOUTLINE.ModelOutlineMulti[PatchItem], BOUTLINE.UiModelOutlineMulti),
        (BOUTLINE.ModelOutlineSingle[PatchItem],
            BOUTLINE.UiModelOutlineSingle),
        ])
    def test_init(self, SUBCLASS, MODEL):
        """Confirm initialization for each subclass.

        :param SUBCLASS: outline model subclass under test.
        :param MODEL: GTK model for outline model subclass under test.
        """
        # Setup
        C_ITEM = 0
        # Test
        assert C_ITEM == BOUTLINE.ModelOutline.C_ITEM
        target = SUBCLASS()
        assert isinstance(target._ui_model, MODEL)
        assert 0 == len(target._ui_model)

    @pytest.mark.parametrize('SUBTYPE', [
        'MULTI',
        'SINGLE',
        ], indirect=['SUBTYPE'])
    def test_clear(self, SUBTYPE):
        """Confirm all lines removed from outline.

        :param SUBTYPE: identifies outline model subclass under test.
        """
        # Setup
        target = SUBTYPE
        # Test
        target.clear()
        assert 0 == len(target._ui_model)

    @pytest.mark.parametrize('SUBTYPE, LINE, NAME', [
        ('MULTI', '0', 'Item 0xx'),
        ('MULTI', '1:0', 'Item 10x'),
        ('MULTI', '1:1:1', 'Item 111'),
        ('SINGLE', '0', 'Item 0'),
        ('SINGLE', '3', 'Item 3'),
        ('SINGLE', '4', 'Item 4'),
        ], indirect=['SUBTYPE'])
    def test_get_item(self, SUBTYPE, LINE, NAME):
        """Confirm all lines removed from outline.

        :param SUBTYPE: identifies outline model subclass under test.
        :param LINE: path to line containing item to get.
        :param NAME: name in item to get.
        """
        # Setup
        target = SUBTYPE
        model = target._ui_model
        line = model.get_iter_from_string(LINE)
        # Test
        item = target.get_item(p_line=line)
        assert NAME == item.name

    @pytest.mark.parametrize('SUBTYPE, LINE, NAME', [
        ('MULTI', '1', 'Item 1xx'),
        ('MULTI', '0:1', 'Item 01x'),
        ('MULTI', '0:0:0', 'Item 000'),
        ('SINGLE', '0', 'Item 0'),
        ('SINGLE', '2', 'Item 2'),
        ('SINGLE', '4', 'Item 4'),
        ], indirect=['SUBTYPE'])
    def test_get_item_direct(self, SUBTYPE, LINE, NAME):
        """Confirm all lines removed from outline.

        :param SUBTYPE: identifies outline model subclass under test.
        :param LINE: path to line containing item to get.
        :param NAME: name in item to get.
        """
        # Setup
        target = SUBTYPE
        model = target._ui_model
        line = model.get_iter_from_string(LINE)
        # Test
        item = target.get_item_direct(p_model=model, p_line=line)
        assert NAME == item.name

    @pytest.mark.parametrize('SUBTYPE, NAMES', [
        ('MULTI', )*2,
        ('SINGLE', )*2,
        ], indirect=True)
    def test_get_persist(self, SUBTYPE, NAMES):
        """Confirm iterator over lines.

        :param SUBTYPE: identifies outline model subclass under test.
        :param NAME: fixture that returns names of items in outline.
        """
        # Setup
        target = SUBTYPE
        # Test
        persist = target._get_persist()
        names_persist = {i: item.name for (i, item) in persist.items()}
        assert NAMES == names_persist

    @pytest.mark.parametrize('SUBTYPE, NAMES', [
        ('MULTI', )*2,
        ('SINGLE', )*2,
        ], indirect=True)
    def test_items(self, SUBTYPE, NAMES):
        """Confirm iterator over items.

        :param SUBCLASS: identifies outline model subclass under test.
        :param NAME: fixture that returns names of items in outline.
        """
        # Setup
        names_expect = list(NAMES.values())
        target = SUBTYPE
        # Test
        names_item = [i.name for i in target.items()]
        assert names_expect == names_item

    @pytest.mark.parametrize('SUBTYPE, NAMES', [
        ('MULTI', )*2,
        ('SINGLE', )*2,
        ], indirect=True)
    def test_lines(self, SUBTYPE, NAMES):
        """Confirm iterator over lines.

        :param SUBTYPE: identifies outline model subclass under test.
        :param NAME: fixture that returns names of items in outline.
        """
        # Setup
        target = SUBTYPE
        model = target._ui_model
        paths_str_names = list(NAMES.keys())
        # Test
        paths_str_lines = [model.get_string_from_iter(l)
                           for l in target.lines()]
        assert paths_str_names == paths_str_lines

    @pytest.mark.parametrize('SUBTYPE, NAMES, PATH, BEGIN, END', [
        ('MULTI', 'MULTI', None, 0, 0),
        ('MULTI', 'MULTI', '0', 0, 4),
        ('MULTI', 'MULTI', '0:0', 1, 3),
        ('MULTI', 'MULTI', '1:1:1', 8, 9),
        ('SINGLE', 'SINGLE', None, 0, 0),
        ('SINGLE', 'SINGLE', '0', 0, 1),
        ('SINGLE', 'SINGLE', '1', 1, 2),
        ('SINGLE', 'SINGLE', '4', 4, 5),
        ], indirect=['SUBTYPE', 'NAMES'])
    def test_remove(self, SUBTYPE, NAMES, PATH, BEGIN, END):
        """Confirm section removal.

        :param SUBTYPE: identifies outline model subclass under test.
        :param NAME: fixture that returns names of items in outline.
        :param PATH: path for line to remove.
        :param BEGIN: slice [BEGIN:END) contains names of lines removed.
        :param END: slice [BEGIN:END) contains names of lines removed.
        """
        # Setup
        names_before = list(NAMES.values())
        names_after = names_before[:BEGIN] + names_before[END:]
        target = SUBTYPE
        model = target._ui_model
        line = None
        if PATH is not None:
            line = model.get_iter_from_string(PATH)
        # Test
        target.remove(line)
        names_target = [item.name for item in target.items()]
        print('Expect: {}'.format(names_after))
        print('Actual: {}'.format(names_target))
        assert names_after == names_target


class TestModelOutlineMulti:
    """Unit tests for :class:`.ModelOutlineMulti`."""

    @pytest.mark.parametrize('METHOD, PATH, POSITION, PATH_NEW', [
            ('insert_after', None, 0, '0'),
            ('insert_after', '0', 4, '1'),
            ('insert_after', '1:0', 6, '1:1'),
            ('insert_after', '1:1:2', 10, '1:1:3'),
            ('insert_before', '0',  0, '0'),
            ('insert_before', '0:1',  3, '0:1'),
            ('insert_before', '1:1:0', 7,  '1:1:0'),
            ('insert_before', None, 10, '2'),
            ('insert_child', '0',  4, '0:2'),
            ('insert_child', '0:0',  3, '0:0:1'),
            ('insert_child', '1:1:1',  9, '1:1:1:0'),
            ('insert_child', None, 10, '2'),
            ])
    def test_insert(self, new_patch_multi, new_names_model_multi,
                    METHOD, PATH, POSITION, PATH_NEW):
        """Confirm item insertion.

        :param new_patch_multi: fixture :func:`.new_patch_multi`.
        :param new_names_model_multi: fixture
            :func:`.new_names_model_multi`.
        :param METHOD: insert method under test.
        :param PATH: path for line after which to insert item.
        :param POSITION: position of new name in list of names.
        :param PATH_NEW: path for line containing new item.
        """
        # Setup
        target = new_patch_multi()
        insert_target = getattr(target, METHOD)
        model = target._ui_model
        ITEM_NEW = PatchItem('Item New', 'Inserted')
        names = list(new_names_model_multi().values())
        _ = names.insert(POSITION, ITEM_NEW.name)
        line = None
        if PATH is not None:
            line = model.get_iter_from_string(PATH)
        # Test
        line_new = insert_target(ITEM_NEW, line)
        assert ITEM_NEW == target.get_item(line_new)
        assert PATH_NEW == model.get_string_from_iter(line_new)
        assert names == [item.name for item in target.items()]

    @pytest.mark.parametrize('SNIPPET, PATH_SOURCE, PATH_TARGET', [
        (insert_snippet_children, '0:0:0', None),
        (insert_snippet_multiple, '1', '1:0'),
        (insert_snippet_single, None, '0'),
        ])
    def test_insert_section(
            self, new_patch_multi, SNIPPET, PATH_SOURCE, PATH_TARGET):
        """| Confirm insertion of sections with representative structures.
        | Case: section is part of source outline.

        :param SNIPPET: funtion that returns section to copy.
        :param PATH_SOURCE: path to parent of snippet in source.
        :param PATH_TARGET: path in parent of section copy in target.
        """
        # Setup
        source = new_patch_multi()
        line_section = SNIPPET(source._ui_model, PATH_SOURCE)
        expect = new_patch_multi()
        _ = SNIPPET(expect._ui_model, PATH_TARGET)
        target = new_patch_multi()
        line_parent = None
        if PATH_TARGET is not None:
            line_parent = target._ui_model.get_iter_from_string(PATH_TARGET)
        # Test
        target.insert_section(source, line_parent, line_section)
        assert expect._get_persist() == target._get_persist()

    @pytest.mark.parametrize('SNIPPET, PATH_TARGET', [
        (insert_snippet_children, '1'),
        (insert_snippet_multiple, '0:0:0'),
        (insert_snippet_single, None),
        ])
    def test_insert_section_all(self, new_patch_multi, SNIPPET, PATH_TARGET):
        """| Confirm insertion of sections with representative structures.
        | Case: section is all of source outline.

        :param SNIPPET: funtion that returns section to copy.
        :param PATH_TARGET: path in parent of section copy in target.
        """
        # Setup
        source = BOUTLINE.ModelOutlineMulti()
        _ = SNIPPET(source._ui_model, None)
        line_section = None
        expect = new_patch_multi()
        _ = SNIPPET(expect._ui_model, PATH_TARGET)
        target = new_patch_multi()
        line_parent = None
        if PATH_TARGET is not None:
            line_parent = target._ui_model.get_iter_from_string(PATH_TARGET)
        # Test
        target.insert_section(source, line_parent, line_section)
        assert expect._get_persist() == target._get_persist()

    @pytest.mark.parametrize('ROOT, BEGIN, END', [
        (None, 0, 11),
        ('1', 4, 11),
        ('0:0', 1, 3),
        ('1:1:0', 7, 8),
        ])
    def test_lines_section(self, new_patch_multi, new_names_model_multi,
                           ROOT, BEGIN, END):
        """Confirm iterator over lines in section.

        :param ROOT: path to root line of section.
        :param END: slice [BEGIN:END) contains names of lines in section.
        """
        # Setup
        target = new_patch_multi()
        model = target._ui_model
        root = None
        if ROOT is not None:
            root = model.get_iter_from_string(ROOT)
        paths_str = list(new_names_model_multi().keys())
        paths_str_section = paths_str[BEGIN:END]
        # Test
        paths_str_line = [model.get_string_from_iter(l)
                          for l in target.lines_section(root)]
        assert paths_str_section == paths_str_line

    def test_set_persist(self, new_patch_multi):
        """Confirm import from persistent form.

        :param new_patch_multi: fixture :func:`.new_patch_multi`.
        """
        # Setup
        source = new_patch_multi()
        persist = source._get_persist()
        target = BOUTLINE.ModelOutlineMulti()
        # Test
        target._set_persist(persist)
        assert persist == target._get_persist()


class TestModelOutlineSingle:
    """Unit tests for :class:`.ModelOutlineSingle`."""

    @pytest.mark.parametrize('AFTER', [
            None,
            '0',
            '2',
            '4',
            ])
    def test_insert_after(
            self, new_patch_single, new_names_model_single, AFTER):
        """Confirm item insertion.

        :param new_patch_single: fixture :func:`.new_patch_single`.
        :param new_names_model_single: fixture
            :func:`.new_names_model_single`.
        :param AFTER: position after which to insert item.
        """
        # Setup
        target = new_patch_single()
        model = target._ui_model
        ITEM_NEW = PatchItem('Item New', 'Inserted')
        names = list(new_names_model_single().values())
        line = None
        position = 0
        if AFTER is not None:
            line = model.get_iter_from_string(AFTER)
            position = int(AFTER) + 1
        _ = names.insert(position, ITEM_NEW.name)
        # Test
        line_new = target.insert_after(ITEM_NEW, line)
        assert ITEM_NEW == target.get_item(line_new)
        assert names == [item.name for item in target.items()]

    @pytest.mark.parametrize('BEFORE', [
            '0',
            '2',
            '4',
            None,
            ])
    def test_insert_before(
            self, new_patch_single, new_names_model_single, BEFORE):
        """Confirm item insertion.

        :param new_patch_single: fixture :func:`.new_patch_single`.
        :param new_names_model_single: fixture
            :func:`.new_names_model_single`.
        :param BEFORE: position before which to insert item.
        """
        # Setup
        target = new_patch_single()
        model = target._ui_model
        ITEM_NEW = PatchItem('Item New', 'Inserted')
        names = list(new_names_model_single().values())
        line = None
        position = len(names)
        if BEFORE is not None:
            line = model.get_iter_from_string(BEFORE)
            position = int(BEFORE)
        _ = names.insert(position, ITEM_NEW.name)
        # Test
        line_new = target.insert_before(ITEM_NEW, line)
        assert ITEM_NEW == target.get_item(line_new)
        assert names == [item.name for item in target.items()]

    def test_set_persist(self, new_patch_single):
        """Confirm import from persistent form.

        :param new_patch_single: fixture :func:`.new_patch_single`.
        """
        # Setup
        source = new_patch_single()
        persist = source._get_persist()
        target = BOUTLINE.ModelOutlineSingle()
        # Test
        target._set_persist(persist)
        assert persist == target._get_persist()


# @pytest.mark.skip(reason='Refactor in progress')
# class TestBridgeOutlineColumnar:
#     """Unit tests for :class:`~.BridgeOutlineColumnar`."""
#
#     def test_new_view(self):
#         """Confirm view element."""
#         # Setup
#         target = BOUTLINE.BridgeOutlineColumnar()
#         # Test
#         view = target.new_view()
#         assert isinstance(view, BOUTLINE.ViewOutlineColumnar)
#         assert target._model is view.get_model()


# @pytest.mark.skip(reason='Refactor in progress')
# class TestBridgeOutlineSelect:
#     """Unit tests for :class:`~.BridgeOutlineSelect`."""
#
#     def test_new_view(self):
#         """Confirm view element."""
#         # Setup
#         target = BOUTLINE.BridgeOutlineSelect()
#         # Test
#         view = target.new_view()
#         assert isinstance(view, BOUTLINE.ViewOutlineSelect)
#         assert target._model is view.get_model()


# @pytest.mark.skip(reason='Refactor in progress')
# class TestBridgeOutlineMultiColumnar:
#     """Unit tests for :class:`~.BridgeOutlineMultiColumnar`."""
#
#     def test_new_view(self):
#         """Confirm view element."""
#         # Setup
#         target = BOUTLINE.BridgeOutlineMultiColumnar()
#         # Test
#         view = target.new_view()
#         assert isinstance(view, BOUTLINE.ViewOutlineColumnar)
#         assert target._model is view.get_model()


# @pytest.mark.skip(reason='Refactor in progress')
# class TestBridgeOutlineMultiSelect:
#     """Unit tests for :class:`~.BridgeOutlineMultiSelect`."""
#
#     def test_new_view(self):
#         """Confirm view element."""
#         # Setup
#         target = BOUTLINE.BridgeOutlineMultiSelect()
#         # Test
#         view = target.new_view()
#         assert isinstance(view, BOUTLINE.ViewOutlineSelect)
#         assert target._model is view.get_model()


class TestBridgeOutlineTypes:
    """Unit tests for definitions of API classes and type hints in
    :mod:`.bridge_outline`.
    """

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_EXPECT', [
        (BOUTLINE.ChooserOutline, Gtk.ComboBox),
        (BOUTLINE.LineOutline, Gtk.TreeIter),
        (BOUTLINE.PersistOutline,
            typing.MutableMapping[str, BOUTLINE.ItemOpaque]),
        # (BOUTLINE.UiModelOutline, Gtk.TreeModel),
        (type(BOUTLINE.UiModelOutline), typing.TypeVar),
        (BOUTLINE.UiModelOutline.__constraints__, (
            BOUTLINE.UiModelOutlineMulti, BOUTLINE.UiModelOutlineSingle)),
        (BOUTLINE.UiModelOutlineMulti, Gtk.TreeStore),
        (BOUTLINE.UiModelOutlineSingle, Gtk.ListStore),
        (BOUTLINE.ViewOutline, Gtk.TreeView),
        ])
    def test_types(self, TYPE_TARGET, TYPE_EXPECT):
        """Confirm type hint definitions.

        :param TYPE_TARGET: type hint under test.
        :param TYPE_EXPECT: type expected.
        """
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_EXPECT


@pytest.fixture
def SUBTYPE(request, new_patch_multi, new_patch_single):
    """Pytest fixture: Return outline of type identified in request.

    :param request: built-in fixture `Pytest request`_.
    :param new_patch_multi: fixture :func:`.new_patch_multi`.
    :param new_patch_single: fixture :func:`.new_patch_single`.
    """
    FACTORY = dict(MULTI=new_patch_multi, SINGLE=new_patch_single)
    outline = FACTORY[request.param]()
    return outline
