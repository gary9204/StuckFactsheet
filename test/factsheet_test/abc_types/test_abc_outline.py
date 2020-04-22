"""
Unit tests for abstract classes for content outlines. See
:mod:`.abc_outline`.
"""
import pytest   # type: ignore[import]

from factsheet.abc_types import abc_outline as ABC_OUTLINE


class TestAbstractTypes:
    """Unit tests for supporting abstract types."""

    def test_types(self):
        """Confirm supporting types defined."""
        # Setup
        # Test
        assert ABC_OUTLINE.AbstractIndex is not None
        assert ABC_OUTLINE.AbstractItem is not None


class TestAbstractOutline:
    """Unit tests for :class:`.AbstractOutline`."""

    def test_abstract_class(self):
        """Confirm the class is abstract."""
        # Setup
        class ClassOutline(ABC_OUTLINE.AbstractOutline[int, int]):
            pass

        # Test
        with pytest.raises(TypeError):
            _ = ClassOutline()

    @pytest.mark.parametrize('name_method', [
        'get_item',
        'insert_before',
        ])
    def test_must_override(self, name_method):
        """Confirm each method must be overridden."""
        # Setup
        class PatchAbstractOutline(ABC_OUTLINE.AbstractOutline[int, int]):
            # def attach_view(self, _v): pass

            # def detach_view(self, _v): pass

            # def extract(self): super().get_infoid()

            # def insert_after(self): super().get_infoid()

            def get_item(self): _ = super().get_item(0)

            def insert_before(self): _ = super().insert_before(0, 0)

        target = PatchAbstractOutline()
        # Test
        with pytest.raises(NotImplementedError):
            method = getattr(target, name_method)
            method()


class TestAbstractViewOutline:
    """Unit tests for :class:`.AbstractViewOutline`."""

    def test_abstract_class(self):
        """Confirm the class is abstract."""
        # Setup
        # Test
        with pytest.raises(TypeError):
            _ = ABC_OUTLINE.AbstractViewOutline()

    @pytest.mark.parametrize('name_method', [
        'set_model',
        ])
    def test_must_override(self, name_method):
        """Confirm each method must be overridden."""
        # Setup
        class PatchAbstractViewOutline(ABC_OUTLINE.AbstractViewOutline):
            def set_model(self): _ = super().set_model(None)

        target = PatchAbstractViewOutline()
        # Test
        with pytest.raises(NotImplementedError):
            method = getattr(target, name_method)
            method()
