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


def iters_section(p_model, p_it=None):
    """Return iterator over all rows at or under a given row of model.

    :param p_model: model containing rows.
    :param p_it: iterate over all descendants of thsi row.
    """
    if p_it is not None:
        yield p_it
    it_child = p_model.iter_children(p_it)
    while it_child is not None:
        yield from iters_section(p_model, it_child)
        it_child = p_model.iter_next(it_child)


@DC.dataclass
class PatchItem:
    """Placeholder item class for unit tests."""
    name: str
    tag: str = 'Target'


class PatchOutline(
        BOUTLINE.BridgeOutline[PatchItem, BOUTLINE.ViewOutlineSelect]):
    """Stub class for single-level outline tests unrelated to view."""

    def new_view(self):
        return BOUTLINE.ViewOutlineSelect()


class PatchOutlineMulti(
        BOUTLINE.BridgeOutlineMulti[PatchItem, BOUTLINE.ViewOutlineColumnar]):
    """Stub class for multi-level outline tests unrelated to view."""

    def new_view(self):
        return BOUTLINE.ViewOutlineColumnar()


@pytest.fixture(params=[BOUTLINE.BridgeOutlineColumnar[PatchItem],
                        BOUTLINE.BridgeOutlineSelect[PatchItem]])
def patch_class_outline(request):
    """Pytest fixture: Return single-level outline classes.

    Supports indirect parametrization by view.
    """
    return request.param


@pytest.fixture(params=[BOUTLINE.BridgeOutlineMultiColumnar[PatchItem],
                        BOUTLINE.BridgeOutlineMultiSelect[PatchItem]])
def patch_class_outlinemulti(request):
    """Pytest fixture: Return multi-level outline classes.

    Supports indirect parametrization by view.
    """
    return request.param


@pytest.fixture
def patch_store_multi():
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
        model = BOUTLINE.ModelOutlineMulti(GO.TYPE_PYOBJECT)
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
def patch_store_single():
    """Pytest fixture: Return :data:`.ModelOutlineSingle` model factory.

    :param p_n_items: number of items in model (default is 5).
    :param p_tag: identifies model (default is 'Target').
    """
    def new_model(p_n_items=5, p_tag='Target'):
        model = BOUTLINE.ModelOutlineSingle(GO.TYPE_PYOBJECT)
        for i in range(p_n_items):
            name = 'Item {}'.format(i)
            item = PatchItem(name=name, tag=p_tag)
            row = [item]
            _ = model.append(row)
        return model

    return new_model


@pytest.fixture
def snippet_store_multi():
    """Pytest fixture: Return :data:`.ModelOutlineMulti` model snippet.
    The structure of the snippet is as shown below.

    :param tag: identifies snippet (default is 'Snippet').

        | Item axx
        |     Item aax
        |         Item aab
        |         Item aaa
    """
    model = BOUTLINE.ModelOutlineMulti(GO.TYPE_PYOBJECT)
    item = PatchItem('Item axx', 'Snippet')
    i_axx = model.append(None, [item])
    item = PatchItem('Item aax', 'Snippet')
    i_aax = model.append(i_axx, [item])
    item = PatchItem('Item aaa', 'Snippet')
    _i_aaa = model.append(i_aax, [item])
    item = PatchItem('Item aab', 'Snippet')
    _i_aab = model.append(i_aax, [item])
    return model


class TestBridgeOutline:
    """Unit tests for :class:`~.BridgeOutline`."""

    def test_constants(self, patch_class_outline):
        """Confirm definition of class constants."""
        # Setup
        C_ITEM = 0
        # Test
        assert C_ITEM == patch_class_outline._C_ITEM

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (BOUTLINE.BridgeOutline, 'new_view'),
        ])
    def test_method_abstract(self, CLASS, NAME_METHOD):
        """Confirm each abstract method is specified."""
        # Setup
        # Test
        assert hasattr(CLASS, '__abstractmethods__')
        assert NAME_METHOD in CLASS.__abstractmethods__

    def test_eq(self, patch_class_outline, patch_store_single):
        """Confirm equality comparison.

        #. Case: type difference.
        #. Case: lines difference.
        #. Case: items difference.
        #. Case: equivalent.
        """
        # Setup
        source = patch_class_outline()
        source._model = patch_store_single()
        ITEM_DIFFER = PatchItem(name='Something completely different.')
        PATH_DIFFER = '2'
        # Test: type difference.
        assert not source.__eq__(ITEM_DIFFER)
        # Test: lines difference.
        target = patch_class_outline()
        target._model = patch_store_single()
        target._model.append([ITEM_DIFFER])
        assert not source.__eq__(target)
        # Test: items difference.
        target = patch_class_outline()
        target._model = patch_store_single()
        iter_differ = target._model.get_iter_from_string(PATH_DIFFER)
        target._model.set_value(
            iter_differ, patch_class_outline._C_ITEM, ITEM_DIFFER)
        assert not source.__eq__(target)
        # Test: equivalent.
        target = patch_class_outline()
        target._model = patch_store_single()
        assert source.__eq__(target)
        assert not source.__ne__(target)

    def test_init(self, patch_class_outline):
        """Confirm initialization."""
        # Setup
        # Test
        target = patch_class_outline()
        assert isinstance(target._views, dict)
        assert not target._views
        assert isinstance(target._model, BOUTLINE.ModelOutlineSingle)

    @pytest.mark.parametrize('PATCH_CLASS, VIEW', [
        (BOUTLINE.BridgeOutlineColumnar, BOUTLINE.ViewOutlineColumnar()),
        (BOUTLINE.BridgeOutlineSelect, BOUTLINE.ViewOutlineSelect()),
        ])
    def test_bind(self, PATCH_CLASS, VIEW):
        """Confirm toolkit element association."""
        # Setup
        target = PATCH_CLASS()
        # Test
        target._bind(VIEW)
        assert target._model is VIEW.get_model()

    def test_clear(self, patch_store_single):
        """Confirm removal of all items."""
        # Setup
        N_ITEMS = 5
        target = PatchOutline()
        model = patch_store_single(N_ITEMS)
        target._model = model
        # Test
        target.clear()
        assert not len(target._model)

    @pytest.mark.parametrize('N_ITEMS, LINE', [
        (5, '0'),
        (5, '2'),
        (5, '4'),
        ])
    def test_get_item(self, patch_store_single, N_ITEMS, LINE):
        """Confirm get from outline."""
        # Setup
        target = PatchOutline()
        model = patch_store_single(N_ITEMS)
        target._model = model
        line = model.get_iter_from_string(LINE)
        # Test
        item = target.get_item(line)
        assert item is model.get_value(line, PatchOutline._C_ITEM)

    @pytest.mark.parametrize('N_ITEMS, LINE', [
        (5, '0'),
        (5, '2'),
        (5, '4'),
        ])
    def test_get_item_direct(self, patch_store_single, N_ITEMS, LINE):
        """Confirm get from store element."""
        # Setup
        model = patch_store_single(N_ITEMS)
        line = model.get_iter_from_string(LINE)
        # Test
        item = PatchOutline.get_item_direct(model, line)
        assert item is model.get_value(line, PatchOutline._C_ITEM)

    def test_get_persist(self, patch_class_outline, patch_store_single):
        """Confirm export to persistent form."""
        # Setup
        N_ITEMS = 5
        target = patch_class_outline()
        model = patch_store_single(N_ITEMS)
        target._model = model
        expect = dict()
        for it in iters_section(model):
            path_str = model.get_string_from_iter(it)
            item = model.get_value(it, patch_class_outline._C_ITEM)
            expect[path_str] = item
        # Test
        assert expect == target._get_persist()

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
    def test_insert(self, patch_store_single, N_ITEMS,
                    METHOD, INSERT, PARENT, BEFORE, AFTER):
        """Confirm item insertion."""
        # Setup
        target = PatchOutline()
        model = patch_store_single(N_ITEMS)
        target._model = model
        expect = list()
        for place in [PARENT, BEFORE, AFTER]:
            item = None
            if place is not None:
                line = model.get_iter_from_string(place)
                item = model.get_value(line, PatchOutline._C_ITEM)
            expect.append((place, item))
        NAME = 'Something completely different'
        item_new = PatchItem(name=NAME)
        line_insert = None
        if INSERT is not None:
            line_insert = model.get_iter_from_string(INSERT)
        method_target = getattr(target, METHOD)
        # Test
        line_new = method_target(item_new, line_insert)
        assert item_new == model.get_value(line_new, PatchOutline._C_ITEM)
        line_parent = model.iter_parent(line_new)
        line_before = model.iter_previous(line_new)
        line_after = model.iter_next(line_new)
        actual = [line_parent, line_before, line_after]
        for (place, item), line in zip(expect, actual):
            if line is None:
                assert place is None
            else:
                assert item is model.get_value(line, PatchOutline._C_ITEM)

    def test_items(self, patch_store_single):
        """Confirm iterator over items."""
        # Setup
        N_ITEMS = 5
        target = PatchOutline()
        model = patch_store_single(N_ITEMS)
        target._model = model
        items = list()
        line = model.get_iter_first()
        while line is not None:
            item = model.get_value(line, PatchOutline._C_ITEM)
            items.append(item)
            line = model.iter_next(line)
        # Test
        assert items == list(target.items())

    def test_lines(self, patch_store_single):
        """Confirm iterator over lines."""
        # Setup
        N_ITEMS = 5
        target = PatchOutline()
        model = patch_store_single(N_ITEMS)
        target._model = model
        paths = list()
        line = model.get_iter_first()
        while line is not None:
            path = model.get_path(line)
            paths.append(path)
            line = model.iter_next(line)
        # Test
        assert paths == [target._model.get_path(l) for l in target.lines()]

    @pytest.mark.parametrize('PATCH_CLASS, VIEW', [
        (BOUTLINE.BridgeOutlineColumnar, BOUTLINE.ViewOutlineColumnar()),
        (BOUTLINE.BridgeOutlineSelect, BOUTLINE.ViewOutlineSelect()),
        ])
    def test_loose(self, PATCH_CLASS, VIEW):
        """Confirm toolkit element disassociation."""
        # Setup
        target = PATCH_CLASS()
        target._bind(VIEW)
        # Test
        target._loose(VIEW)
        assert VIEW.get_model() is None

    def test_new_model(self):
        """Confirm storage element."""
        # Setup
        N_COLUMNS = 1
        target = PatchOutline()
        # Test
        model = target._new_model()
        assert isinstance(model, BOUTLINE.ModelOutlineSingle)
        assert N_COLUMNS == model.get_n_columns()
        assert not len(model)

    @pytest.mark.parametrize('N_ITEMS, PATH_PARENT', [
        (5, None),
        (5, '0'),
        (5, '2'),
        (5, '4'),
        ])
    def test_remove(self, patch_store_single, N_ITEMS, PATH_PARENT):
        """Confirm item removal."""
        # Setup
        expect = PatchOutlineMulti()
        expect._model = patch_store_single(N_ITEMS)
        if PATH_PARENT is not None:
            it_expect = expect._model.get_iter_from_string(PATH_PARENT)
            expect._model.remove(it_expect)

        target = PatchOutline()
        target._model = patch_store_single(N_ITEMS)
        it_target = None
        if PATH_PARENT is not None:
            it_target = target._model.get_iter_from_string(PATH_PARENT)
        # Test
        target.remove(it_target)
        assert expect._get_persist() == target._get_persist()

    def test_set_persist(self, patch_class_outline, patch_store_single):
        """Confirm import from persistent form."""
        # Setup
        N_ITEMS = 5
        target = patch_class_outline()
        model = patch_store_single(N_ITEMS)
        persist = dict()
        for it in iters_section(model):
            path_str = model.get_string_from_iter(it)
            item = model.get_value(it, patch_class_outline._C_ITEM)
            persist[path_str] = item
        # Test
        target._set_persist(persist)
        assert persist == target._get_persist()


class TestBridgeOutlineColumnar:
    """Unit tests for :class:`~.BridgeOutlineColumnar`."""

    def test_new_view(self):
        """Confirm view element."""
        # Setup
        target = BOUTLINE.BridgeOutlineColumnar()
        # Test
        view = target.new_view()
        assert isinstance(view, BOUTLINE.ViewOutlineColumnar)


class TestBridgeOutlineSelect:
    """Unit tests for :class:`~.BridgeOutlineSelect`."""

    def test_new_view(self):
        """Confirm view element."""
        # Setup
        target = BOUTLINE.BridgeOutlineSelect()
        # Test
        view = target.new_view()
        assert isinstance(view, BOUTLINE.ViewOutlineSelect)


class TestBridgeOutlineMulti:
    """Unit tests for :class:`~.BridgeOutlineMulti`."""

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (BOUTLINE.BridgeOutlineMulti, 'new_view'),
        ])
    def test_method_abstract(self, CLASS, NAME_METHOD):
        """Confirm each abstract method is specified."""
        # Setup
        # Test
        assert hasattr(CLASS, '__abstractmethods__')
        assert NAME_METHOD in CLASS.__abstractmethods__

    def test_eq(self, patch_class_outlinemulti, patch_store_multi):
        """Confirm equality comparison.

        #. Case: type difference.
        #. Case: lines difference.
        #. Case: items difference.
        #. Case: equivalent.
        """
        # Setup
        source = patch_class_outlinemulti()
        source._model = patch_store_multi()
        ITEM_DIFFER = PatchItem(name='Something completely different.')
        PATH_DIFFER = '1:0'
        # Test: type difference.
        assert not source.__eq__(ITEM_DIFFER)
        # Test: lines difference.
        target = patch_class_outlinemulti()
        target._model = patch_store_multi()
        target._model.append(None, [ITEM_DIFFER])
        assert not source.__eq__(target)
        # Test: items difference.
        target = patch_class_outlinemulti()
        target._model = patch_store_multi()
        iter_differ = target._model.get_iter_from_string(PATH_DIFFER)
        target._model.set_value(
            iter_differ, patch_class_outlinemulti._C_ITEM, ITEM_DIFFER)
        assert not source.__eq__(target)
        # Test: equivalent.
        target = patch_class_outlinemulti()
        target._model = patch_store_multi()
        assert source.__eq__(target)
        assert not source.__ne__(target)

    def test_init(self, patch_class_outlinemulti):
        """Confirm initialization."""
        # Setup
        # Test
        target = patch_class_outlinemulti()
        assert isinstance(target._views, dict)
        assert not target._views
        assert isinstance(target._model, BOUTLINE.ModelOutlineMulti)

    @pytest.mark.parametrize('PATCH_CLASS, VIEW', [
        (BOUTLINE.BridgeOutlineMultiColumnar, BOUTLINE.ViewOutlineColumnar()),
        (BOUTLINE.BridgeOutlineMultiSelect, BOUTLINE.ViewOutlineSelect()),
        ])
    def test_bind(self, PATCH_CLASS, VIEW):
        """Confirm toolkit element association."""
        # Setup
        target = PATCH_CLASS()
        # Test
        target._bind(VIEW)
        assert target._model is VIEW.get_model()

    def test_clear(self, patch_store_multi):
        """Confirm removal of all items."""
        # Setup
        target = PatchOutlineMulti()
        model = patch_store_multi()
        target._model = model
        # Test
        target.clear()
        assert not len(target._model)

    @pytest.mark.parametrize(', LINE', [
        '0',
        '1:0',
        '1:1:1',
        ])
    def test_get_item(self, patch_store_multi, LINE):
        """Confirm get from outline."""
        # Setup
        target = PatchOutlineMulti()
        model = patch_store_multi()
        target._model = model
        line = model.get_iter_from_string(LINE)
        # Test
        item = target.get_item(line)
        assert item is model.get_value(line, PatchOutlineMulti._C_ITEM)

    @pytest.mark.parametrize('LINE', [
        '1',
        '0:1',
        '0:0:0',
        ])
    def test_get_item_direct(self, patch_store_multi, LINE):
        """Confirm get from store element."""
        # Setup
        model = patch_store_multi()
        line = model.get_iter_from_string(LINE)
        # Test
        item = PatchOutlineMulti.get_item_direct(model, line)
        assert item is model.get_value(line, PatchOutlineMulti._C_ITEM)

    def test_get_persist(self, patch_class_outlinemulti, patch_store_multi):
        """Confirm export to persistent form."""
        # Setup
        target = patch_class_outlinemulti()
        model = patch_store_multi()
        target._model = model
        expect = dict()
        for it in iters_section(model):
            path_str = model.get_string_from_iter(it)
            item = model.get_value(it, patch_class_outlinemulti._C_ITEM)
            expect[path_str] = item
        # Test
        assert expect == target._get_persist()

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
    def test_insert(self, patch_store_multi,
                    METHOD, INSERT, PARENT, BEFORE, AFTER, CHILD):
        """Confirm item insertion."""
        # Setup
        target = PatchOutlineMulti()
        model = patch_store_multi()
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
    def test_insert_section(self, patch_store_multi, PATH_TARGET):
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
        expect._model = patch_store_multi()
        it_expect = None
        if PATH_TARGET is not None:
            it_expect = expect._model.get_iter_from_string(PATH_TARGET)
        it_a = expect._model.append(it_expect, [item_a])
        _ = expect._model.append(it_a, [item_aa])
        _ = expect._model.append(it_expect, [item_b])

        target = PatchOutlineMulti()
        target._model = patch_store_multi()
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
            self, patch_store_multi, PATH_TARGET, snippet_store_multi):
        """| Confirm section insertion at all target levels.
        | Case: source section has parent and has no children.
        """
        # Setup
        source = PatchOutlineMulti()
        snippet = snippet_store_multi
        source._model = snippet

        expect = PatchOutlineMulti()
        expect._model = patch_store_multi()
        it_expect = None
        if PATH_TARGET is not None:
            it_expect = expect._model.get_iter_from_string(PATH_TARGET)
        PATH_LEAF_2 = '0:0:1'
        it_leaf_2 = snippet.get_iter_from_string(PATH_LEAF_2)
        row = list(snippet[it_leaf_2])
        _ = expect._model.append(it_expect, row)

        target = PatchOutlineMulti()
        target._model = patch_store_multi()
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
            self, patch_store_multi, PATH_TARGET, snippet_store_multi):
        """| Confirm section insertion at all target levels.
        | Case: source section has parent and has children.
        """
        # Setup
        source = PatchOutlineMulti()
        snippet = snippet_store_multi
        source._model = snippet

        expect = PatchOutlineMulti()
        expect._model = patch_store_multi()
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
        target._model = patch_store_multi()
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
            self, patch_store_multi, PATH_TARGET, snippet_store_multi):
        """| Confirm section insertion at all target levels.
        | Case: source section has no parent and has children.
        """
        source = PatchOutlineMulti()
        snippet = snippet_store_multi
        source._model = snippet

        expect = PatchOutlineMulti()
        expect._model = patch_store_multi()
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
        target._model = patch_store_multi()
        it_target = None
        if PATH_TARGET is not None:
            it_target = target._model.get_iter_from_string(PATH_TARGET)
        # Test
        target.insert_section(source, it_target, it_top)
        assert expect._get_persist() == target._get_persist()

    def test_items(self, patch_store_multi):
        """Confirm iterator over items in entire outline."""
        # Setup
        model = patch_store_multi()
        target = PatchOutlineMulti()
        target._model = model
        root = None
        lines = iters_section(model, root)
        items = [model.get_value(l, PatchOutline._C_ITEM) for l in lines]
        # Test
        assert items == list(target.items())

    @pytest.mark.parametrize('ROOT', [
        None,
        '1',
        '0:0',
        '1:1:0',
        ])
    def test_items_section(self, patch_store_multi, ROOT):
        """Confirm iterator over items in section."""
        # Setup
        model = patch_store_multi()
        target = PatchOutlineMulti()
        target._model = model
        root = None
        if ROOT is not None:
            root = model.get_iter_from_string(ROOT)
        lines = iters_section(model, root)
        items = [model.get_value(l, PatchOutline._C_ITEM) for l in lines]
        # Test
        assert items == list(target.items_section(root))

    def test_lines(self, patch_store_multi):
        """Confirm iterator over lines in entire outline."""
        # Setup
        model = patch_store_multi()
        target = PatchOutlineMulti()
        target._model = model
        ROOT = None
        # Test
        for it_model, line in zip(iters_section(model, ROOT), target.lines()):
            path_model = model.get_string_from_iter(it_model)
            path_line = target._model.get_string_from_iter(line)
            assert path_model == path_line

    @pytest.mark.parametrize('ROOT', [
        None,
        '1',
        '0:0',
        '1:1:0',
        ])
    def test_lines_section(self, patch_store_multi, ROOT):
        """Confirm iterator over lines in section."""
        # Setup
        model = patch_store_multi()
        target = PatchOutlineMulti()
        target._model = model
        root = None
        if ROOT is not None:
            root = model.get_iter_from_string(ROOT)
        # Test
        for it_model, line in zip(
                iters_section(model, root), target.lines_section(root)):
            path_model = model.get_string_from_iter(it_model)
            path_line = target._model.get_string_from_iter(line)
            assert path_model == path_line

    @pytest.mark.parametrize('PATCH_CLASS, VIEW', [
        (BOUTLINE.BridgeOutlineMultiColumnar, BOUTLINE.ViewOutlineColumnar()),
        (BOUTLINE.BridgeOutlineMultiSelect, BOUTLINE.ViewOutlineSelect()),
        ])
    def test_loose(self, PATCH_CLASS, VIEW):
        """Confirm toolkit element disassociation."""
        # Setup
        target = PATCH_CLASS()
        target._bind(VIEW)
        # Test
        target._loose(VIEW)
        assert VIEW.get_model() is None

    def test_new_model(self):
        """Confirm storage element."""
        # Setup
        N_COLUMNS = 1
        target = PatchOutlineMulti()
        # Test
        model = target._new_model()
        assert isinstance(model, BOUTLINE.ModelOutlineMulti)
        assert N_COLUMNS == model.get_n_columns()
        assert not len(model)

    @pytest.mark.parametrize('PATH_PARENT', [
        None,
        '0',
        '0:0',
        '1:1:1',
        ])
    def test_remove(self, patch_store_multi, PATH_PARENT):
        """Confirm section removal."""
        # Setup
        expect = PatchOutlineMulti()
        expect._model = patch_store_multi()
        if PATH_PARENT is not None:
            it_expect = expect._model.get_iter_from_string(PATH_PARENT)
            expect._model.remove(it_expect)

        target = PatchOutlineMulti()
        target._model = patch_store_multi()
        it_target = None
        if PATH_PARENT is not None:
            it_target = target._model.get_iter_from_string(PATH_PARENT)
        # Test
        target.remove(it_target)
        assert expect._get_persist() == target._get_persist()

    def test_set_persist(self, patch_class_outlinemulti, patch_store_multi):
        """Confirm import from persistent form."""
        # Setup
        target = patch_class_outlinemulti()
        model = patch_store_multi()
        persist = dict()
        for it in iters_section(model):
            path_str = model.get_string_from_iter(it)
            item = model.get_value(it, patch_class_outlinemulti._C_ITEM)
            persist[path_str] = item
        # Test
        target._set_persist(persist)
        assert persist == target._get_persist()


class TestBridgeOutlineMultiColumnar:
    """Unit tests for :class:`~.BridgeOutlineMultiColumnar`."""

    def test_new_view(self):
        """Confirm view element."""
        # Setup
        target = BOUTLINE.BridgeOutlineMultiColumnar()
        # Test
        view = target.new_view()
        assert isinstance(view, BOUTLINE.ViewOutlineColumnar)


class TestBridgeOutlineMultiSelect:
    """Unit tests for :class:`~.BridgeOutlineMultiSelect`."""

    def test_new_view(self):
        """Confirm view element."""
        # Setup
        target = BOUTLINE.BridgeOutlineMultiSelect()
        # Test
        view = target.new_view()
        assert isinstance(view, BOUTLINE.ViewOutlineSelect)


class TestInterfaceOutline:
    """Unit tests for :class:`~.InterfaceOutline`."""

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (BOUTLINE.InterfaceOutline, 'get_item'),
        (BOUTLINE.InterfaceOutline, 'get_item_direct'),
        (BOUTLINE.InterfaceOutline, 'insert_after'),
        (BOUTLINE.InterfaceOutline, 'insert_before'),
        (BOUTLINE.InterfaceOutline, 'items'),
        (BOUTLINE.InterfaceOutline, 'lines'),
        (BOUTLINE.InterfaceOutline, 'remove'),
        ])
    def test_method_abstract(self, CLASS, NAME_METHOD):
        """Confirm each abstract method is specified."""
        # Setup
        # Test
        assert hasattr(CLASS, '__abstractmethods__')
        assert NAME_METHOD in CLASS.__abstractmethods__


class TestInterfaceOutlineMulti:
    """Unit tests for :class:`~.InterfaceOutlineMulti`."""

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (BOUTLINE.InterfaceOutlineMulti, 'insert_child'),
        (BOUTLINE.InterfaceOutlineMulti, 'insert_section'),
        ])
    def test_method_abstract(self, CLASS, NAME_METHOD):
        """Confirm each abstract method is specified."""
        # Setup
        # Test
        assert hasattr(CLASS, '__abstractmethods__')
        assert NAME_METHOD in CLASS.__abstractmethods__


class TestBridgeOutlineTypes:
    """Unit tests for definitions of API classes and type hints in
    :mod:`.bridge_outline`.
    """

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_SOURCE', [
        (BOUTLINE.LineOutline, Gtk.TreeIter),
        (BOUTLINE.ModelOutline, Gtk.TreeModel),
        (BOUTLINE.ModelOutlineSingle, Gtk.ListStore),
        (BOUTLINE.ModelOutlineMulti, Gtk.TreeStore),
        (BOUTLINE.PersistOutline,
            typing.MutableMapping[str, BOUTLINE.ItemOpaque]),
        (BOUTLINE.ViewOutlineColumnar, Gtk.TreeView),
        (BOUTLINE.ViewOutlineSelect, Gtk.ComboBox),
        (type(BOUTLINE.ViewOutlineOpaque), typing.TypeVar),
        (BOUTLINE.ViewOutlineOpaque.__constraints__,
            (BOUTLINE.ViewOutlineColumnar, BOUTLINE.ViewOutlineSelect)),
        ])
    def test_types(self, TYPE_TARGET, TYPE_SOURCE):
        """Confirm API definitions."""
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_SOURCE
