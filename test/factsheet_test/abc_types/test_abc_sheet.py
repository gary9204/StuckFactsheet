"""
Unit tests for sheet abstract data type classes.
"""


import factsheet.abc_types.abc_sheet as ASHEET


class TestObserverSheet:
    """
    Unit tests for Sheet abstract data
    """

    def test_update_name(self):
        """Confirm interface defined."""
        # Setup
        obs = ASHEET.ObserverSheet()
        # Test
        assert obs.update_name() is None

    def test_detach(self):
        """Confirm interface defined."""
        # Setup
        obs = ASHEET.ObserverSheet()
        # Test
        assert obs.detach() is None
