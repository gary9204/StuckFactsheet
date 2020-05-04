"""
Unit tests for factsheet document abstract interfaces.
"""
import pytest   # type: ignore[import]

import factsheet.abc_types.abc_sheet as ABC_SHEET


class TestAbstractTemplate:
    """Unit tests for interface :class:`.AbstractTemplate`."""

    def test_abstract_class(self):
        """Confirm the interface class is abstract."""
        # Setup
        # Test
        with pytest.raises(TypeError):
            _ = ABC_SHEET.AbstractTemplate()

    @pytest.mark.parametrize('name_method', [
        '__call__',
        'name',
        'summary',
        'title',
        ])
    def test_must_override(self, name_method):
        """Confirm each method must be overridden."""
        # Setup
        class PatchTemplate(ABC_SHEET.AbstractTemplate):
            def __call__(self): return super().__call__()

            def name(self): super().name

            def summary(self): super().summary

            def title(self): super().title

        target = PatchTemplate()
        # Test
        with pytest.raises(NotImplementedError):
            method = getattr(target, name_method)
            method()


class TestEffectSafe:
    """Unit tests for members of enumeration :class:`EffectSafe`."""

    def test_effects(self):
        """Confirm member definitions."""
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
        'present_factsheet',
        ])
    def test_must_override(self, name_method):
        """Confirm each method must be overridden."""
        # Setup
        class PatchControlSheet(ABC_SHEET.InterfaceControlSheet):
            def path(self): super().path

            def present_factsheet(self): super().present_factsheet(None)

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
