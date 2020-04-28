"""
Unit tests for GTK-based classes implementing abstract outline classes.
See :mod:`.adapt_sheet`.
"""
import gi   # type: ignore[import]
import pytest   # type: ignore[import]

from factsheet.abc_types import abc_sheet as ABC_SHEET
from factsheet.adapt_gtk import adapt_outline as AOUTLINE
from factsheet.adapt_gtk import adapt_sheet as ASHEET

gi.require_version('Gtk', '3.0')
from gi.repository import GObject as GO  # type: ignore[import] # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class PatchTemplate(ABC_SHEET.AbstractTemplate):
    """Placeholder template item class for unit tests."""
    def __init__(self, p_name='Parrot',
                 p_summary='This parrot is no more.',
                 p_title='The Dead Parrot Sketch'):
        self._name = p_name
        self._summary = p_summary
        self._title = p_title

    def __call__(self): return 'Topic Stub'

    def __eq__(self, px_other):
        if not isinstance(px_other, PatchTemplate):
            return False
        return (self.name == px_other.name
                ) and (self.summary == px_other.summary
                       ) and (self.title == px_other.title)

    @property
    def name(self): return self._name

    @property
    def summary(self): return self._summary

    @property
    def title(self): return self._title


@pytest.fixture
def new_outline_model():
    """Pytest fixture returns outline model factory.  Parameter p_tag
    labels each item in summary.  The structure of each model is as
    follows.

        | name_0xx | title_0xx
        |     name_00x | title_00x
        |         name_000 | title_000
        |     name_01x | title_01x
        | name_1xx | title_1xx
        |     name_10x | title_10x
        |     name_11x | title_11x
        |         name_110 | title_110
        |         name_111 | title_111
        |         name_112 | title_112
    """
    def new_model(p_tag='Target'):
        model = Gtk.TreeStore(GO.TYPE_PYOBJECT)

        item = PatchTemplate('name_0xx', p_title='title_0xx', p_summary=p_tag)
        i_0xx = model.append(None, [item])
        item = PatchTemplate('name_00x', p_title='title_00x', p_summary=p_tag)
        i_00x = model.append(i_0xx, [item])
        item = PatchTemplate('name_000', p_title='title_000', p_summary=p_tag)
        _i_000 = model.append(i_00x, [item])
        item = PatchTemplate('name_01x', p_title='title_01x', p_summary=p_tag)
        i_0xx = model.append(i_0xx, [item])
        item = PatchTemplate('name_1xx', p_title='title_1xx', p_summary=p_tag)
        i_1xx = model.append(None, [item])
        item = PatchTemplate('name_10x', p_title='title_10x', p_summary=p_tag)
        _i_10x = model.append(i_1xx, [item])
        item = PatchTemplate('name_11x', p_title='title_11x', p_summary=p_tag)
        i_11x = model.append(i_1xx, [item])
        item = PatchTemplate('name_110', p_title='title_110', p_summary=p_tag)
        _i_110 = model.append(i_11x, [item])
        item = PatchTemplate('name_111', p_title='title_111', p_summary=p_tag)
        _i_111 = model.append(i_11x, [item])
        item = PatchTemplate('name_112', p_title='title_112', p_summary=p_tag)
        _i_112 = model.append(i_11x, [item])
        return model

    return new_model


@pytest.fixture
def patch_item():
    """Pytext fixture returns stub item for outline contents."""
    class PatchItem(ABC_SHEET.AbstractTemplate):
        def __init__(self, p_name='Nemo', p_summary='I am no one.',
                     p_title='No One'):
            self._name = p_name
            self._summary = p_summary
            self._title = p_title

        def __call__(self): return 'Topic Stub'

        @property
        def name(self): return self._name

        @property
        def summary(self): return self._summary

        @property
        def title(self): return self._title

    return PatchItem


@pytest.fixture
def patch_outline(patch_item):
    """Pytext fixture returns stub tree store."""
    tree_store = ASHEET.AdaptTreeStoreTemplate()
    N_ITEMS = 3
    index = None
    for i in range(N_ITEMS):
        item = patch_item('Item {}'.format(i))
        index = tree_store.insert_before(item, index)

    return tree_store


class TestAdaptTreeStoreTemplate:
    """Unit tests for :class:`AdaptTreeStoreTmeplate`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        patch_template = PatchTemplate()
        INDEX = None
        # Test
        target = ASHEET.AdaptTreeStoreTemplate()
        assert target is not None
        index_new = target.insert_before(patch_template, INDEX)
        assert index_new is not None
        assert isinstance(index_new, AOUTLINE.AdaptIndex)

    def test_find_name(self, new_outline_model):
        """| Confirm search by template name.
        | Case: matching template in outline.
        """
        # Setup
        target = ASHEET.AdaptTreeStoreTemplate()
        target._model = new_outline_model(p_tag='Target')
        PATH_VALUE = '1:1:1'
        i_value = target._model.get_iter_from_string(PATH_VALUE)
        value = target.get_item(i_value).name
        PATH_AFTER = '1:1:1'
        i_after = target._model.get_iter_from_string(PATH_AFTER)
        # Test
        i_match = target.find_name(value, i_after)
        assert PATH_VALUE == target._model.get_string_from_iter(i_match)

    def test_find_name_absent(self, new_outline_model):
        """| Confirm search by template name.
        | Case: no matching template in outline.
        """
        # Setup
        VALUE = 'Something completely different'
        target = ASHEET.AdaptTreeStoreTemplate()
        target._model = new_outline_model(p_tag='Target')
        # Test
        i_match = target.find_name(VALUE)
        assert i_match is None

    def test_find_title(self, new_outline_model):
        """| Confirm search by template title.
        | Case: matching template in outline.
        """
        # Setup
        target = ASHEET.AdaptTreeStoreTemplate()
        target._model = new_outline_model(p_tag='Target')
        PATH_VALUE = '0:1'
        i_value = target._model.get_iter_from_string(PATH_VALUE)
        value = target.get_item(i_value).title
        PATH_AFTER = '0:1'
        i_after = target._model.get_iter_from_string(PATH_AFTER)
        # Test
        i_match = target.find_title(value, i_after)
        assert PATH_VALUE == target._model.get_string_from_iter(i_match)

    def test_find_title_absent(self, new_outline_model):
        """| Confirm search by template name.
        | Case: no matching template in outline.
        """
        # Setup
        VALUE = 'Something completely different'
        target = ASHEET.AdaptTreeStoreTemplate()
        target._model = new_outline_model(p_tag='Target')
        # Test
        i_match = target.find_title(VALUE)
        assert i_match is None


class TestAdaptTreeViewTemplate:
    """Unit tests for view class AdaptTreeViewTemplate."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        # Test
        target = ASHEET.AdaptTreeViewTemplate()
        assert isinstance(target._view, Gtk.TreeView)
        assert target._view.get_model() is None

    def test_set_model(self, patch_outline):
        """Confirm initialization."""
        # Setup
        OUTLINE = patch_outline
        C_NAME = 0
        C_TITLE = 1
        C_PAD = 2
        N_CELLS = 1
        target = ASHEET.AdaptTreeViewTemplate()
        # Test
        target.set_model(OUTLINE)
        assert target._view.get_model() is OUTLINE._model

        name_column = target._view.get_column(C_NAME)
        assert 'Name' == name_column.get_title()
        assert name_column.get_clickable()
        assert name_column.get_resizable()
        assert N_CELLS == len(name_column.get_cells())

        title_column = target._view.get_column(C_TITLE)
        assert 'Title' == title_column.get_title()
        assert title_column.get_clickable()
        assert title_column.get_resizable()
        assert N_CELLS == len(title_column.get_cells())

        pad_column = target._view.get_column(C_PAD)
        assert pad_column is not None
        assert pad_column.get_expand()

    def test_name_cell_data(self, patch_outline):
        """Confirm renderer property is set."""
        # Setup
        OUTLINE = patch_outline
        I_TARGET = 1
        i_first = OUTLINE._model.get_iter_first()
        for _ in range(I_TARGET):
            i_target = OUTLINE._model.iter_next(i_first)
        TEMPLATE = OUTLINE.get_item(i_target)
        renderer = Gtk.CellRendererText()
        target = ASHEET.AdaptTreeViewTemplate()
        target.set_model(OUTLINE)
        # Test
        target._name_cell_data(
            None, renderer, OUTLINE._model, i_target, None)
        assert TEMPLATE.name == renderer.get_property('text')
        with pytest.raises(TypeError,
                           match='property markup is not readable'):
            assert TEMPLATE.name == renderer.get_property('markup')

    def test_title_cell_data(self, patch_outline):
        """Confirm renderer property is set."""
        # Setup
        OUTLINE = patch_outline
        I_TARGET = 1
        i_first = OUTLINE._model.get_iter_first()
        for _ in range(I_TARGET):
            i_target = OUTLINE._model.iter_next(i_first)
        TEMPLATE = OUTLINE.get_item(i_target)
        renderer = Gtk.CellRendererText()
        target = ASHEET.AdaptTreeViewTemplate()
        # Test
        target._title_cell_data(
            None, renderer, OUTLINE._model, i_target, None)
        assert TEMPLATE.title == renderer.get_property('text')
        with pytest.raises(TypeError,
                           match='property markup is not readable'):
            assert TEMPLATE.name == renderer.get_property('markup')
