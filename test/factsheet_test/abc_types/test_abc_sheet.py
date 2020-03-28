"""
Unit tests for factsheet document abstract data type classes.
"""
import pytest   # type: ignore[import]

import factsheet.abc_types.abc_sheet as ABC_SHEET


class TestEffectSafe:
    """Unit tests for enumeration members."""

    def test_effects(self):
        """Confirm member definition."""
        # Setup
        # Test
        assert ABC_SHEET.EffectSafe.COMPLETED
        assert ABC_SHEET.EffectSafe.NO_EFFECT


class TestInterfaceControlSheet:
    """Unit tests for interface :class:`.InterfaceControlSheet`.
    """
    def test_abstract_class(self):
        """Confirm the interface class is abstract."""
        # Setup
        # Test
        with pytest.raises(TypeError):
            _ = ABC_SHEET.InterfaceControlSheet()

    @pytest.mark.parametrize('name_method', [
        'path',
        ])
    def test_must_override(self, name_method):
        """Confirm each method must be overridden."""
        # Setup
        class PatchControlSheet(ABC_SHEET.InterfaceControlSheet):
            def path(self): super().path

        target = PatchControlSheet()
        # Test
        with pytest.raises(NotImplementedError):
            method = getattr(target, name_method)
            method()


class TestInterfacePageSheet:
    """Unit tests for interface :class:`.InterfacePageSheet`."""

    def test_abstract_class(self):
        """Confirm the interface class is abstract."""
        # Setup
        # Test
        with pytest.raises(TypeError):
            _ = ABC_SHEET.InterfacePageSheet()

    @pytest.mark.parametrize('name_method', [
        'close_page',
        'get_infoid',
        'present',
        'set_titles',
        ])
    def test_must_override(self, name_method):
        """Confirm each method must be overridden."""
        # Setup
        class PatchPageSheet(ABC_SHEET.InterfacePageSheet):
            def close_page(self): super().close_page()

            def get_infoid(self): super().get_infoid()

            def present(self): super().present(None)

            def set_titles(self): super().set_titles(None)

        target = PatchPageSheet()
        # Test
        with pytest.raises(NotImplementedError):
            method = getattr(target, name_method)
            method()
