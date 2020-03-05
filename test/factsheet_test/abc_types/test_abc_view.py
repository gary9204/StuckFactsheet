"""
Unit tests for View abstract data type classes.

See :mod:`.abc_view`.
"""
from factsheet.abc_types import abc_view as ABC_VIEW
from factsheet.adapt_gtk import adapt_view as AVIEW


class TestAbstractTextView:
    """Unit tests for View type :data:`.AbstractTextView`."""

    def test_constraints(self):
        """Confirm definition of :data:`.AbstractTextView`."""
        # Setup
        constraints = [AVIEW.AdaptEntry, AVIEW.AdaptTextView]
        # Test
        target = ABC_VIEW.AbstractTextView.__constraints__
        for c in constraints:
            assert c in target
        assert len(constraints) == len(target)
