"""
Unit tests for classes that encapsulates user interface classes from
widget toolkit.  See :mod:`~.bridge_ui`.
"""
import pytest  # type: ignore[import]

import factsheet.bridge_gtk.bridge_base as BBASE
import factsheet.bridge_ui as BUI


class TestAdaptTypes:
    """Unit tests for definitions of API classes and type hints in
    :mod:`.adapt`.
    """

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_SOURCE', [
        (BUI.ModelOpaque, BBASE.ModelOpaque),
        (BUI.ViewOpaque, BBASE.ViewOpaque),
        ])
    def test_types(self, TYPE_TARGET, TYPE_SOURCE):
        """Confirm API definitions."""
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_SOURCE
