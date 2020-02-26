"""
Unit tests for header abstract data type classes.
"""

import pytest

from factsheet.types_abstract import abc_header as AHEADER


class TestInterfaceStaleFile:
    """Unit tests for interfaces to detect out-of-date model."""

    def test_abstract_class(self):
        """Confirm the interface class is abstract."""
        # Setup
        # Test
        with pytest.raises(TypeError):
            _ = AHEADER.InterfaceStaleFile()

    @pytest.mark.parametrize('name_method', [
        'is_fresh',
        'is_stale',
        'set_fresh',
        'set_stale',
        ])
    def test_must_override(self, name_method):
        """Confirm each method must be overridden."""
        # Setup
        class PatchInterface(AHEADER.InterfaceStaleFile):
            def is_fresh(self): super().is_fresh()

            def is_stale(self): super().is_stale()

            def set_fresh(self): super().set_fresh()

            def set_stale(self): super().set_stale()

        target = PatchInterface()
        # Test
        with pytest.raises(NotImplementedError):
            _ = getattr(target, name_method)()
