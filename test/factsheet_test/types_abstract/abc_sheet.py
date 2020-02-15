"""
factsheet_test.types_abstract.abc_sheet - unit tests for Sheet abstract
    data types
"""


import factsheet.types_abstract.abc_sheet as ASHEET


class TestObserverSheet:
    """
    Unit tests for Sheet abstract data
    """

    def test_on_changed_name(self):
        """Confirm interface defined."""
        # Setup
        obs = ASHEET.ObserverSheet()
        # Test
        assert obs.on_changed_name() is None

    def test_on_delete_sheet(self):
        """Confirm interface defined."""
        # Setup
        obs = ASHEET.ObserverSheet()
        # Test
        assert obs.on_delete_sheet() is None
