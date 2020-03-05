"""
Unit tests for factsheet document abstract data type classes.
"""
import pytest   # type: ignore[import]

import factsheet.abc_types.abc_sheet as ABC_SHEET


class TestFactoryInfoId:
    """Unit tests for interface :class:`.InterfaceSignalsSheet`."""

    def test_abstract_class(self):
        """Confirm the interface class is abstract."""
        # Setup
        # Test
        with pytest.raises(TypeError):
            _ = ABC_SHEET.InterfaceSignalsSheet()

    @pytest.mark.parametrize('name_method', [
        'detach',
        'update_name',
        ])
    def test_must_override(self, name_method):
        """Confirm each method must be overridden."""
        # Setup
        class PatchFactory(ABC_SHEET.InterfaceSignalsSheet):
            def detach(self): super().detach()

            def update_name(self): super().update_name()

        target = PatchFactory()
        # Test
        with pytest.raises(NotImplementedError):
            method = getattr(target, name_method)
            method()
