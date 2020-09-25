"""
Unit tests for class defining initial segment of natural numbers topic.
See :mod:`~.segint_topic`.
"""
import pytest   # type: ignore[import]

import factsheet.model.setindexed as MSET
import factsheet.content.sets.int.segint_topic as XSEGINT
import factsheet.content.sets.int.setint_topic as XSETINT


class TestSegInt:
    """Unit tests for :class:`~.SegInt`."""

    @pytest.mark.parametrize('BOUND_L, BOUND_R, RESULT', [
        (1, 1, True),
        (1, 3, False),
        (5, 3, False),
        (6, 6, True),
        ])
    def test_eq_sets(self, BOUND_L, BOUND_R, RESULT):
        """| Confirm equality comparison.
        | Case: indexed set checks.
        """
        # Setup
        target_left = XSEGINT.SegInt(p_bound=BOUND_L)
        target_right = XSEGINT.SegInt(p_bound=BOUND_R)
        # Test
        assert (target_left == target_right) is RESULT

    def test_init(self):
        """| Confirm initialization.
        | Case: positive bound with check of elements.
        """
        # Setup
        BOUND = 5
        ELEMENTS = MSET.SetIndexed[int](p_members=range(BOUND))
        # Test
        target = XSEGINT.SegInt(p_bound=BOUND)
        assert isinstance(target, XSETINT.SetInt)
        assert ELEMENTS == target.elements

    @pytest.mark.parametrize('BOUND_RAW, BOUND', [
        (5, 5),
        (1, 1),
        (3.14159, 3),
        (0, 1),
        (-1, 1),
        ('3.14159', 1),
        (None, 1),
        ])
    def test_init_bound(self, BOUND_RAW, BOUND):
        """| Confirm initialization.
        | Case: bound checks.
        """
        # Setup
        # Test
        target = XSEGINT.SegInt(p_bound=BOUND_RAW)
        assert BOUND == len(target.elements)
