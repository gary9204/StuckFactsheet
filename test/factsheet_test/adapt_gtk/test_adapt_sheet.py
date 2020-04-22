"""
Unit tests for GTK-based classes implementing abstract outline classes.
See :mod:`.adapt_outline`.
"""
import gi   # type: ignore[import]
import pytest   # type: ignore[import]

from factsheet.abc_types import abc_sheet as ABC_SHEET
from factsheet.adapt_gtk import adapt_sheet as ASHEET

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


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

    def test_init(self, patch_item):
        """Confirm initialization."""
        # Setup
        patch_template = patch_item()
        index = None
        # Test
        target = ASHEET.AdaptTreeStoreTemplate()
        assert target is not None
        index_new = target.insert_before(patch_template, index)
        assert index_new is not None
        assert isinstance(index_new, Gtk.TreeIter)


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
        assert target._view.get_model() is OUTLINE._store

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
        i_first = OUTLINE._store.get_iter_first()
        for _ in range(I_TARGET):
            i_target = OUTLINE._store.iter_next(i_first)
        TEMPLATE = OUTLINE.get_item(i_target)
        renderer = Gtk.CellRendererText()
        target = ASHEET.AdaptTreeViewTemplate()
        target.set_model(OUTLINE)
        # Test
        target._name_cell_data(
            None, renderer, OUTLINE._store, i_target, None)
        assert TEMPLATE.name == renderer.get_property('text')
        with pytest.raises(TypeError,
                           match='property markup is not readable'):
            assert TEMPLATE.name == renderer.get_property('markup')

    def test_title_cell_data(self, patch_outline):
        """Confirm renderer property is set."""
        # Setup
        OUTLINE = patch_outline
        I_TARGET = 1
        i_first = OUTLINE._store.get_iter_first()
        for _ in range(I_TARGET):
            i_target = OUTLINE._store.iter_next(i_first)
        TEMPLATE = OUTLINE.get_item(i_target)
        renderer = Gtk.CellRendererText()
        target = ASHEET.AdaptTreeViewTemplate()
        # Test
        target._title_cell_data(
            None, renderer, OUTLINE._store, i_target, None)
        assert TEMPLATE.title == renderer.get_property('text')
        with pytest.raises(TypeError,
                           match='property markup is not readable'):
            assert TEMPLATE.name == renderer.get_property('markup')
