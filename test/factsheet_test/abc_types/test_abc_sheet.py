"""
Unit tests for factsheet document abstract data type classes.
"""
import pytest   # type: ignore[import]

import factsheet.abc_types.abc_sheet as ABC_SHEET


class TestFactoryInfoId:
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
        'update_name',
        ])
    def test_must_override(self, name_method):
        """Confirm each method must be overridden."""
        # Setup
        class PatchFactory(ABC_SHEET.InterfacePageSheet):
            def close_page(self): super().close_page()

            def get_infoid(self): super().get_infoid()

            def present(self): super().present(None)

            def update_name(self): super().update_name()

        target = PatchFactory()
        # Test
        with pytest.raises(NotImplementedError):
            method = getattr(target, name_method)
            method()
