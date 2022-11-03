"""
Unit tests for :mod:`.store_py`.
"""
import pytest

import factsheet.ui_bricks.ui_abc.store_py as STOREPY


class TestModule:
    """Unit tests for module-level components of :mod:`.store_py`."""

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_EXPECT', [
        (STOREPY.StorePyMarkup, str),
        ])
    def test_types(self, TYPE_TARGET, TYPE_EXPECT):
        """Confirm type definitions.

        :param TYPE_TARGET: type under test.
        :param TYPE_EXPECT: type expected.
        """
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_EXPECT
