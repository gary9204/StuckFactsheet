"""
Unit tests for abstract base class to track file against model.

See :mod:`.abc_stalefile`.
"""
import pytest   # type: ignore[import]

from factsheet.abc_types import abc_stalefile as ABC_STALEFILE


class TestInterfaceStaleFile:
    """Unit tests for interfaces to detect out-of-date model.
    See :class:`.InterfaceStaleFile`."""

    def test_abstract_class(self):
        """Confirm the interface class is abstract."""
        # Setup
        # Test
        with pytest.raises(TypeError):
            _ = ABC_STALEFILE.InterfaceStaleFile()

    @pytest.mark.parametrize('name_method', [
        'is_fresh',
        'is_stale',
        'set_fresh',
        'set_stale',
        ])
    def test_must_override(self, name_method):
        """Confirm each method must be overridden."""
        # Setup
        class PatchInterface(ABC_STALEFILE.InterfaceStaleFile):
            def is_fresh(self): super().is_fresh()

            def is_stale(self): super().is_stale()

            def set_fresh(self): super().set_fresh()

            def set_stale(self): super().set_stale()

        target = PatchInterface()
        # Test
        with pytest.raises(NotImplementedError):
            method = getattr(target, name_method)
            method()
