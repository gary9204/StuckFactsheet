"""
Unit tests for bridge classes to encapsulate witget toolkit outline
classes. See :mod:`.bridge_outline`.
"""
import dataclasses as DC
import gi   # type: ignore[import]
import pytest   # type: ignore[import]
import typing

import factsheet.bridge_gtk.bridge_outline as BOUTLINE

gi.require_version('Gtk', '3.0')
from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


def gtk_model_to_names(p_tree_model):
    """Return dictionary of names in an outline indexed by line."""
    C_ITEM = 0
    persist = dict()
    for row in iter_section(p_tree_model):
        path_str = p_tree_model.get_string_from_iter(row)
        item = p_tree_model[row][C_ITEM]
        persist[path_str] = item.name
    return persist


def iter_section(p_model, p_it=None):
    """Return iterator over all rows at or under a given row of
    `Gtk.TreeModel`_.

    :param p_model: model containing rows.
    :param p_it: iterate over this row and all of its descendants.

    _Gtk.TreeModel: https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/
    TreeModel.html#Gtk.TreeModel
    """
    if p_it is not None:
        yield p_it
    it_child = p_model.iter_children(p_it)
    while it_child is not None:
        yield from iter_section(p_model, it_child)
        it_child = p_model.iter_next(it_child)


@pytest.fixture
def NAMES(request, new_names_model_multi, new_names_model_single):
    """Pytest fixture: Return dictionary of names for identified outline."""
    # Setup
    FACTORY = dict(MULTI=new_names_model_multi, SINGLE=new_names_model_single)
    names = FACTORY[request.param]()
    return names


@pytest.fixture
def new_gtk_model_multi():
    """Pytest fixture: Return `Gtk.TreeStore`_ model factory.
    The structure of each model is as shown below.

    :param tag: identifies model (default is 'Target').

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
def new_gtk_model_multi_snippet():
    """Pytest fixture: Return `Gtk.TreeStore`_ model snippet.
    The structure of the snippet is as shown below.

    :param tag: identifies snippet (default is 'Snippet').

        | Item axx
        |     Item aax
        |         Item aab
        |         Item aaa
    """
    model = BOUTLINE.ModelOutline(GO.TYPE_PYOBJECT)
    item = PatchItem('Item axx', 'Snippet')
    i_axx = model.append(None, [item])
    item = PatchItem('Item aax', 'Snippet')
    i_aax = model.append(i_axx, [item])
    item = PatchItem('Item aaa', 'Snippet')
    _i_aaa = model.append(i_aax, [item])
    item = PatchItem('Item aab', 'Snippet')
    _i_aab = model.append(i_aax, [item])
    return model


@pytest.fixture
def new_gtk_model_single():
    """Pytest fixture: Return `Gtk.ListStore`_ model factory.

    :param p_n_items: number of items in model (default is 5).
    :param p_tag: identifies model (default is 'Target').
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
            '0': 'Item 0xx',
            '0:0': 'Item 00x',
            '0:0:0': 'Item 000',
            '0:1': 'Item 01x',
            '1': 'Item 1xx',
            '1:0': 'Item 10x',
            '1:1': 'Item 11x',
            '1:1:0': 'Item 110',
            '1:1:1': 'Item 111',
            '1:1:2': 'Item 112',
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
    """
    def new_single():
        outline = BOUTLINE.ModelOutlineSingle[PatchItem]()
        outline._ui_model = new_gtk_model_single()
        return outline

    return new_single


@DC.dataclass
class PatchItem:
    """Placeholder item class for unit tests."""
    name: str
    tag: str = 'Target'


class TestCheckFixtures:
    """Unit tests to check test fixtures and test module functions."""

    def test_model_multi(self, new_gtk_model_multi, new_names_model_multi):
        """Confirm multi-level model structure and content."""
        # Setup
        model = new_gtk_model_multi()
        names = new_names_model_multi()
        # Test
        target = gtk_model_to_names(model)
        assert names == target

    def test_model_single(
            self, new_gtk_model_single, new_names_model_single):
        """Confirm single-level model structure and content."""
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
        """Confirm each abstract method is specified."""
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
        """Confirm initialization for each subclass."""
        # Setup
        # Test
        target = SUBCLASS()
        assert isinstance(target._ui_model, MODEL)
        assert 0 == len(target._ui_model)

    @pytest.mark.parametrize('SUBTYPE', [
        'MULTI',
        'SINGLE',
        ], indirect=['SUBTYPE'])
    def test_clear(self, SUBTYPE):
        """Confirm all lines removed from outline."""
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
        """Confirm all lines removed from outline."""
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
        """Confirm all lines removed from outline."""
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
        """Confirm iterator over lines."""
        # Setup
        target = SUBTYPE
        # Test
        persist = target._get_persist()
        names_persist = {i: item.name for (i, item) in persist.items()}
        assert NAMES == names_persist
        # names_outline = dict()
        # for line in target.lines():
        #     path_str = model.get_string_from_iter(line)
        #     item = target.get_item(line)
        #     names_items =
        # names_item = {i, i.name for i in target.items()}
        # assert names_expect == names_item

    @pytest.mark.parametrize('SUBTYPE, NAMES', [
        ('MULTI', )*2,
        ('SINGLE', )*2,
        ], indirect=True)
    def test_items(self, SUBTYPE, NAMES):
        """Confirm iterator over lines."""
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
        """Confirm iterator over lines."""
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
        """Confirm section removal."""
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

    @pytest.mark.parametrize('ROOT, BEGIN, END', [
        (None, 0, 11),
        ('1', 4, 11),
        ('0:0', 1, 3),
        ('1:1:0', 7, 8),
        ])
    def test_lines_section(self, new_patch_multi, new_names_model_multi,
                           ROOT, BEGIN, END):
        """Confirm iterator over lines in section."""
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


class TestModelOutlineSingle:
    """Unit tests for :class:`.ModelOutlineSingle`."""

    pass


@pytest.mark.skip(reason='Refactor in progress')
class TestBridgeOutline:
    """Unit tests for :class:`~.BridgeOutline`."""

    def test_constants(self, patch_class_outline):
        """Confirm definition of class constants."""
        # Setup
        C_ITEM = 0
        # Test
        assert C_ITEM == patch_class_outline._C_ITEM

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (BOUTLINE.ModelOutlineSingle, 'new_view'),
        ])
    def test_method_abstract(self, CLASS, NAME_METHOD):
        """Confirm each abstract method is specified."""
        # Setup
        # Test
        assert hasattr(CLASS, '__abstractmethods__')
        assert NAME_METHOD in CLASS.__abstractmethods__

    def test_eq(self, patch_class_outline, patch_gtk_model_single):
        """Confirm equality comparison.

        #. Case: type difference.
        #. Case: lines difference.
        #. Case: items difference.
        #. Case: equivalent.
        """
        # Setup
        source = patch_class_outline()
        source._model = patch_gtk_model_single()
        ITEM_DIFFER = PatchItem(name='Something completely different.')
        PATH_DIFFER = '2'
        # Test: type difference.
        assert not source.__eq__(ITEM_DIFFER)
        # Test: lines difference.
        target = patch_class_outline()
        target._model = patch_gtk_model_single()
        target._model.append([ITEM_DIFFER])
        assert not source.__eq__(target)
        # Test: items difference.
        target = patch_class_outline()
        target._model = patch_gtk_model_single()
        iter_differ = target._model.get_iter_from_string(PATH_DIFFER)
        target._model.set_value(
            iter_differ, patch_class_outline._C_ITEM, ITEM_DIFFER)
        assert not source.__eq__(target)
        # Test: equivalent.
        target = patch_class_outline()
        target._model = patch_gtk_model_single()
        assert source.__eq__(target)
        assert not source.__ne__(target)

    @pytest.mark.parametrize(
        'N_ITEMS, METHOD, INSERT, PARENT, BEFORE, AFTER', [
            (5, 'insert_after',  None, None, None, '0'),
            (5, 'insert_after',  '0',  None, '0',  '1'),
            (5, 'insert_after',  '2',  None, '2',  '3'),
            (5, 'insert_after',  '4',  None, '4',  None),
            (5, 'insert_before', '0',  None, None, '0'),
            (5, 'insert_before', '2',  None, '1',  '2'),
            (5, 'insert_before', '4',  None, '3',  '4'),
            (5, 'insert_before', None, None, '4',  None),
            ])
    def test_insert(self, patch_gtk_model_single, N_ITEMS,
                    METHOD, INSERT, PARENT, BEFORE, AFTER):
        """Confirm item insertion."""
        # Setup
        target = PatchOutlineSingle()
        model = patch_gtk_model_single(N_ITEMS)
        target._model = model
        expect = list()
        for place in [PARENT, BEFORE, AFTER]:
            item = None
            if place is not None:
                line = model.get_iter_from_string(place)
                item = model.get_value(line, PatchOutlineSingle._C_ITEM)
            expect.append((place, item))
        NAME = 'Something completely different'
        item_new = PatchItem(name=NAME)
        line_insert = None
        if INSERT is not None:
            line_insert = model.get_iter_from_string(INSERT)
        method_target = getattr(target, METHOD)
        # Test
        line_new = method_target(item_new, line_insert)
        assert item_new == model.get_value(line_new, PatchOutlineSingle._C_ITEM)
        line_parent = model.iter_parent(line_new)
        line_before = model.iter_previous(line_new)
        line_after = model.iter_next(line_new)
        actual = [line_parent, line_before, line_after]
        for (place, item), line in zip(expect, actual):
            if line is None:
                assert place is None
            else:
                assert item is model.get_value(line, PatchOutlineSingle._C_ITEM)

    def test_set_persist(self, patch_class_outline, patch_gtk_model_single):
        """Confirm import from persistent form."""
        # Setup
        N_ITEMS = 5
        target = patch_class_outline()
        model = patch_gtk_model_single(N_ITEMS)
        persist = dict()
        for it in iter_section(model):
            path_str = model.get_string_from_iter(it)
            item = model.get_value(it, patch_class_outline._C_ITEM)
            persist[path_str] = item
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


@pytest.mark.skip(reason='Refactor in progress')
class TestBridgeOutlineMulti:
    """Unit tests for :class:`~.BridgeOutlineMulti`."""

    def test_eq(self, patch_class_outlinemulti, patch_gtk_model_multi):
        """Confirm equality comparison.

        #. Case: type difference.
        #. Case: lines difference.
        #. Case: items difference.
        #. Case: equivalent.
        """
        # Setup
        source = patch_class_outlinemulti()
        source._model = patch_gtk_model_multi()
        ITEM_DIFFER = PatchItem(name='Something completely different.')
        PATH_DIFFER = '1:0'
        # Test: type difference.
        assert not source.__eq__(ITEM_DIFFER)
        # Test: lines difference.
        target = patch_class_outlinemulti()
        target._model = patch_gtk_model_multi()
        target._model.append(None, [ITEM_DIFFER])
        assert not source.__eq__(target)
        # Test: items difference.
        target = patch_class_outlinemulti()
        target._model = patch_gtk_model_multi()
        iter_differ = target._model.get_iter_from_string(PATH_DIFFER)
        target._model.set_value(
            iter_differ, patch_class_outlinemulti._C_ITEM, ITEM_DIFFER)
        assert not source.__eq__(target)
        # Test: equivalent.
        target = patch_class_outlinemulti()
        target._model = patch_gtk_model_multi()
        assert source.__eq__(target)
        assert not source.__ne__(target)

    @pytest.mark.parametrize(
        'METHOD, INSERT, PARENT, BEFORE, AFTER, CHILD', [
            ('insert_after',  None, None, None, '0', None),
            ('insert_after',  '0',  None, '0',  '1', None),
            ('insert_after',  '1:0',  '1', '1:0',  '1:1', None),
            ('insert_after',  '1:1:2',  '1:1', '1:1:2', None, None),
            ('insert_before', '0',  None, None, '0', None),
            ('insert_before', '0:1',  '0', '0:0',  '0:1', None),
            ('insert_before', '1:1:0',  '1:1', None,  '1:1:0', None),
            ('insert_before', None, None, '1',  None, None),
            ('insert_child', '0',  '0', '0:1', None, None),
            ('insert_child', '0:0',  '0:0', '0:0:0',  None, None),
            ('insert_child', '1:1:1',  '1:1:1', None,  None, None),
            ('insert_child', None, None, '1',  None, None),
            ])
    def test_insert(self, patch_gtk_model_multi,
                    METHOD, INSERT, PARENT, BEFORE, AFTER, CHILD):
        """Confirm item insertion."""
        # Setup
        target = PatchOutlineMulti()
        model = patch_gtk_model_multi()
        target._model = model
        expect = list()
        for place in [PARENT, BEFORE, AFTER, CHILD]:
            item = None
            if place is not None:
                line = model.get_iter_from_string(place)
                item = model.get_value(line, PatchOutlineMulti._C_ITEM)
            expect.append((place, item))
        NAME = 'Something completely different'
        item_new = PatchItem(name=NAME)
        line_insert = None
        if INSERT is not None:
            line_insert = model.get_iter_from_string(INSERT)
        method_target = getattr(target, METHOD)
        # Test
        line_new = method_target(item_new, line_insert)
        assert item_new == model.get_value(line_new, PatchOutlineMulti._C_ITEM)
        line_parent = model.iter_parent(line_new)
        line_before = model.iter_previous(line_new)
        line_after = model.iter_next(line_new)
        line_child = model.iter_children(line_new)
        actual = [line_parent, line_before, line_after, line_child]
        for (place, item), line in zip(expect, actual):
            if line is None:
                assert place is None
            else:
                assert item is model.get_value(line, PatchOutlineMulti._C_ITEM)

    @pytest.mark.parametrize('PATH_TARGET', [
        None,
        '1',
        '0:0',
        '0:1',
        ])
    def test_insert_section(self, patch_gtk_model_multi, PATH_TARGET):
        """| Confirm section insertion at all target levels.
        | Case: source section of None.
        """
        # Setup
        source = PatchOutlineMulti()
        item_a = PatchItem('Item axx', 'source')
        it_axx = source._model.append(None, [item_a])
        item_aa = PatchItem('Item aax', 'source')
        _it_aax = source._model.append(it_axx, [item_aa])
        item_b = PatchItem('Item bxx', 'source')
        _it_bxx = source._model.append(None, [item_b])

        expect = PatchOutlineMulti()
        expect._model = patch_gtk_model_multi()
        it_expect = None
        if PATH_TARGET is not None:
            it_expect = expect._model.get_iter_from_string(PATH_TARGET)
        it_a = expect._model.append(it_expect, [item_a])
        _ = expect._model.append(it_a, [item_aa])
        _ = expect._model.append(it_expect, [item_b])

        target = PatchOutlineMulti()
        target._model = patch_gtk_model_multi()
        it_target = None
        if PATH_TARGET is not None:
            it_target = target._model.get_iter_from_string(PATH_TARGET)
        # Test
        target.insert_section(source, it_target, None)
        assert expect._get_persist() == target._get_persist()

    @pytest.mark.parametrize('PATH_TARGET', [
        None,
        '0',
        '1:1',
        '0:0:0',
        ])
    def test_insert_section_leaf(
            self, patch_gtk_model_multi, PATH_TARGET, snippet_gtk_model_multi):
        """| Confirm section insertion at all target levels.
        | Case: source section has parent and has no children.
        """
        # Setup
        source = PatchOutlineMulti()
        snippet = snippet_gtk_model_multi
        source._model = snippet

        expect = PatchOutlineMulti()
        expect._model = patch_gtk_model_multi()
        it_expect = None
        if PATH_TARGET is not None:
            it_expect = expect._model.get_iter_from_string(PATH_TARGET)
        PATH_LEAF_2 = '0:0:1'
        it_leaf_2 = snippet.get_iter_from_string(PATH_LEAF_2)
        row = list(snippet[it_leaf_2])
        _ = expect._model.append(it_expect, row)

        target = PatchOutlineMulti()
        target._model = patch_gtk_model_multi()
        it_target = None
        if PATH_TARGET is not None:
            it_target = target._model.get_iter_from_string(PATH_TARGET)
        # Test
        target.insert_section(source, it_target, it_leaf_2)
        assert expect._get_persist() == target._get_persist()

    @pytest.mark.parametrize('PATH_TARGET', [
        None,
        '1',
        '0:0',
        '1:1:1',
        ])
    def test_insert_section_mid(
            self, patch_gtk_model_multi, PATH_TARGET, snippet_gtk_model_multi):
        """| Confirm section insertion at all target levels.
        | Case: source section has parent and has children.
        """
        # Setup
        source = PatchOutlineMulti()
        snippet = snippet_gtk_model_multi
        source._model = snippet

        expect = PatchOutlineMulti()
        expect._model = patch_gtk_model_multi()
        it_expect = None
        if PATH_TARGET is not None:
            it_expect = expect._model.get_iter_from_string(PATH_TARGET)
        PATH_MID = '0:0'
        it_mid = snippet.get_iter_from_string(PATH_MID)
        row = list(snippet[it_mid])
        it = expect._model.append(it_expect, row)
        PATH_LEAF_1 = '0:0:0'
        it_leaf_1 = snippet.get_iter_from_string(PATH_LEAF_1)
        row = list(snippet[it_leaf_1])
        _ = expect._model.append(it, row)
        PATH_LEAF_2 = '0:0:1'
        it_leaf_2 = snippet.get_iter_from_string(PATH_LEAF_2)
        row = list(snippet[it_leaf_2])
        _ = expect._model.append(it, row)

        target = PatchOutlineMulti()
        target._model = patch_gtk_model_multi()
        it_target = None
        if PATH_TARGET is not None:
            it_target = target._model.get_iter_from_string(PATH_TARGET)
        # Test
        target.insert_section(source, it_target, it_mid)
        assert expect._get_persist() == target._get_persist()

    @pytest.mark.parametrize('PATH_TARGET', [
        None,
        '0',
        '1:1',
        '1:0',
        ])
    def test_insert_section_top(
            self, patch_gtk_model_multi, PATH_TARGET, snippet_gtk_model_multi):
        """| Confirm section insertion at all target levels.
        | Case: source section has no parent and has children.
        """
        source = PatchOutlineMulti()
        snippet = snippet_gtk_model_multi
        source._model = snippet

        expect = PatchOutlineMulti()
        expect._model = patch_gtk_model_multi()
        it_expect = None
        if PATH_TARGET is not None:
            it_expect = expect._model.get_iter_from_string(PATH_TARGET)
        PATH_TOP = '0'
        it_top = snippet.get_iter_from_string(PATH_TOP)
        row = list(snippet[it_top])
        it = expect._model.append(it_expect, row)
        PATH_MID = '0:0'
        it_mid = snippet.get_iter_from_string(PATH_MID)
        row = list(snippet[it_mid])
        it = expect._model.append(it, row)
        PATH_LEAF_1 = '0:0:0'
        it_leaf_1 = snippet.get_iter_from_string(PATH_LEAF_1)
        row = list(snippet[it_leaf_1])
        _ = expect._model.append(it, row)
        PATH_LEAF_2 = '0:0:1'
        it_leaf_2 = snippet.get_iter_from_string(PATH_LEAF_2)
        row = list(snippet[it_leaf_2])
        _ = expect._model.append(it, row)

        target = PatchOutlineMulti()
        target._model = patch_gtk_model_multi()
        it_target = None
        if PATH_TARGET is not None:
            it_target = target._model.get_iter_from_string(PATH_TARGET)
        # Test
        target.insert_section(source, it_target, it_top)
        assert expect._get_persist() == target._get_persist()

    def test_set_persist(self, patch_class_outlinemulti, patch_gtk_model_multi):
        """Confirm import from persistent form."""
        # Setup
        target = patch_class_outlinemulti()
        model = patch_gtk_model_multi()
        persist = dict()
        for it in iter_section(model):
            path_str = model.get_string_from_iter(it)
            item = model.get_value(it, patch_class_outlinemulti._C_ITEM)
            persist[path_str] = item
        # Test
        target._set_persist(persist)
        assert persist == target._get_persist()


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
        (BOUTLINE.ChooserItem, Gtk.ComboBox),
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
def patch_gtk_model_multi():
    """Pytest fixture: Return :data:`.ModelOutlineMulti` model factory.
    The structure of each model is as shown below.

    :param tag: identifies model (default is 'Target').

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
    """
    def new_model(p_tag='Target'):
        model = BOUTLINE.ModelOutline(GO.TYPE_PYOBJECT)
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
def patch_gtk_model_single():
    """Pytest fixture: Return :data:`.ModelOutlineSingle` model factory.

    :param p_n_items: number of items in model (default is 5).
    :param p_tag: identifies model (default is 'Target').
    """
    def new_model(p_n_items=5, p_tag='Target'):
        model = BOUTLINE.ModelOutline(GO.TYPE_PYOBJECT)
        for i in range(p_n_items):
            name = 'Item {}'.format(i)
            item = PatchItem(name=name, tag=p_tag)
            row = [item]
            _ = model.append(row)
        return model

    return new_model


@pytest.fixture
def snippet_gtk_model_multi():
    """Pytest fixture: Return :data:`.ModelOutlineMulti` model snippet.
    The structure of the snippet is as shown below.

    :param tag: identifies snippet (default is 'Snippet').

        | Item axx
        |     Item aax
        |         Item aab
        |         Item aaa
    """
    model = BOUTLINE.ModelOutline(GO.TYPE_PYOBJECT)
    item = PatchItem('Item axx', 'Snippet')
    i_axx = model.append(None, [item])
    item = PatchItem('Item aax', 'Snippet')
    i_aax = model.append(i_axx, [item])
    item = PatchItem('Item aaa', 'Snippet')
    _i_aaa = model.append(i_aax, [item])
    item = PatchItem('Item aab', 'Snippet')
    _i_aab = model.append(i_aax, [item])
    return model


@pytest.fixture
def SUBTYPE(request, new_patch_multi, new_patch_single):
    """Pytest fixture: Return outline of type identified in request."""
    FACTORY = dict(MULTI=new_patch_multi, SINGLE=new_patch_single)
    outline = FACTORY[request.param]()
    return outline
