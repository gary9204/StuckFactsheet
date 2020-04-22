"""
Unit tests for GTK-based classes implementing abstract outline classes.
See :mod:`.adapt_outline`.
"""
import gi   # type: ignore[import]
import pytest   # type: ignore[import]

from factsheet.adapt_gtk import adapt_outline as AOUTLINE

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


@pytest.fixture
def patch_item():
    """Pytext fixture returns stub item for outline contents."""
    class PatchItem:
        def __init__(self, p_name='Nemo'): self.name = p_name

    return PatchItem


@pytest.fixture
def patch_tree_store(patch_item):
    """Pytext fixture returns outline of PatchItem objects."""
    class PatchTreeStore(AOUTLINE.AdaptTreeStore[patch_item]):
        pass

    return PatchTreeStore


class TestAdaptIndex:
    """Unit tests for supporting abstract types."""

    def test_types(self):
        """Confirm supporting types defined."""
        # Setup
        # Test
        assert AOUTLINE.AdaptIndex is not None
        assert issubclass(Gtk.TreeIter, AOUTLINE.AdaptIndex)


class TestAdaptTreeStore:
    """Unit tests for :class:`AdaptTreeStore`."""

    def test_init(self, patch_tree_store):
        """Confirm initialization."""
        # Setup
        # Test
        target = patch_tree_store()
        assert target is not None
        assert isinstance(target._store, Gtk.TreeStore)

    def test_get_item(self, patch_tree_store, patch_item):
        """Confirm get."""
        # Setup
        source = patch_tree_store()
        N_ITEMS = 3
        I_TARGET = 1
        i_setup = None
        items = list()
        for i in range(N_ITEMS):
            item = patch_item('Item {}'.format(i))
            items.append(item)
            i_setup = source.insert_before(item, i_setup)
        i_first = source._store.get_iter_first()
        for _ in range(I_TARGET):
            i_target = source._store.iter_next(i_first)
        # Test
        target = source.get_item(i_target)
        assert target is items[I_TARGET]

    def test_insert_before(self, patch_tree_store, patch_item):
        """Confirm insertion."""
        # Setup
        target = patch_tree_store()
        N_ITEMS = 3
        items = list()
        for i in range(N_ITEMS):
            items.append(patch_item('Item {}'.format(i)))
        index = None
        # Test
        for item in items:
            index = target.insert_before(item, index)
            assert isinstance(index, AOUTLINE.AdaptIndex)
            assert index is not None
            assert target._store[index][0] is item
