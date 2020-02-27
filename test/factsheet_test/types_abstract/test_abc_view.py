"""
Unit tests for view abstract data type classes.
"""


from factsheet.types_abstract import abc_view as AVIEW


class TestAbstractTextView:
    """Unit tests for View class AbstractTextView"""

    def test_constraints(self):
        """Confirm initialization."""
        # Setup
        constraints = list()
        # Test
        target = AVIEW.AbstractTextView.__constraints__
        assert len(constraints) == len(target)
        for c in constraints:
            assert c in target
