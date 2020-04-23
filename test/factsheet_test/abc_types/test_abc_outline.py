"""
Unit tests for abstract classes for outlines. See
:mod:`.abc_outline`.
"""
import pytest   # type: ignore[import]

from factsheet.abc_types import abc_outline as ABC_OUTLINE


class TestAbstractTypes:
    """Unit tests for supporting, generic types."""

    def test_types(self):
        """Confirm supporting types defined."""
        # Setup
        # Test
        assert ABC_OUTLINE.GenericIndex is not None
        assert ABC_OUTLINE.GenericItem is not None


class TestAbstractOutline:
    """Unit tests for :class:`.AbstractOutline`."""

    def test_abstract_class(self):
        """Confirm class is abstract."""
        # Setup
        class ClassOutline(ABC_OUTLINE.AbstractOutline[int, int]):
            pass

        # Test
        with pytest.raises(TypeError):
            _ = ClassOutline()

    @pytest.mark.parametrize('name_method', [
        '__eq__',
        '__ne__',
        'copy_section',
        'extract_section',
        'find_next',
        'get_item',
        'indices',
        'insert_after',
        'insert_before',
        ])
    def test_must_override(self, name_method):
        """Confirm each method must be overridden."""
        # Setup
        class PatchAbstractOutline(ABC_OUTLINE.AbstractOutline[int, int]):
            def __eq__(self): return super().__eq__(0)  # type: ignore[misc]

            def __ne__(self): return super().__ne__(0)  # type: ignore[misc]

            def copy_section(self): super().copy_section(None, 0, 0)

            def extract_section(self): super().extract_section(0)

            def find_next(self): return super().find_next(None)

            def get_item(self): return super().get_item(0)

            def indices(self): return super().indices(0)

            def insert_after(self): return super().insert_after(0, 0)

            def insert_before(self): return super().insert_before(0, 0)

        target = PatchAbstractOutline()
        # Test
        with pytest.raises(NotImplementedError):
            method = getattr(target, name_method)
            method()


class TestAbstractViewOutline:
    """Unit tests for :class:`.AbstractViewOutline`."""

    def test_abstract_class(self):
        """Confirm class is abstract."""
        # Setup
        # Test
        with pytest.raises(TypeError):
            _ = ABC_OUTLINE.AbstractViewOutline()

    @pytest.mark.parametrize('name_method', [
        'get_selected',
        'select',
        'set_model',
        ])
    def test_must_override(self, name_method):
        """Confirm each method must be overridden."""
        # Setup
        class PatchAbstractViewOutline(ABC_OUTLINE.AbstractViewOutline):
            def get_selected(self): return super().get_selected()

            def select(self): return super().select(None)

            def set_model(self): return super().set_model(None)

        target = PatchAbstractViewOutline()
        # Test
        with pytest.raises(NotImplementedError):
            method = getattr(target, name_method)
            method()
