"""
factsheet_test.test_app - unit tests for Factsheet applicaton entry.
"""

import pytest   # type: ignore[import]

import factsheet.app as APP


class TestApp:
    """
    Unit tests for Factsheet application entry.
    """

    def test_main(self):
        """Confirm initialization."""
        # Setup
        # Test
        with pytest.raises(NotImplementedError):
            assert APP.main()
