"""
Unit tests for topic class defining initial segment of natural numbers.
See :mod:`~.SegInt_topic`.
"""
import pytest   # type: ignore[import]

from factsheet.model import setindexed as MSET
from factsheet.content.sets.int import segint_topic as XSET_INT


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
        NAME = 'Parrot'
        SUMMARY = 'This parrot is no more.'
        TITLE = 'Parrot Sketch'
        target_left = XSET_INT.SegInt(
            p_name=NAME, p_summary=SUMMARY, p_title=TITLE, p_bound=BOUND_L)
        target_right = XSET_INT.SegInt(
            p_name=NAME, p_summary=SUMMARY, p_title=TITLE, p_bound=BOUND_R)
        # Test
        assert (target_left == target_right) is RESULT

    def test_eq_info(self):
        """| Confirm equality comparison.
        | Case: identification information check.
        """
        # Setup
        NAME = 'Parrot'
        SUMMARY = 'This parrot is no more.'
        TITLE_MATCH = 'Parrot Sketch'
        TITLE_DIFFER = 'Something completely different.'
        BOUND = 5
        reference = XSET_INT.SegInt(p_name=NAME, p_summary=SUMMARY,
                                    p_title=TITLE_MATCH, p_bound=BOUND)
        target_match = XSET_INT.SegInt(p_name=NAME, p_summary=SUMMARY,
                                       p_title=TITLE_MATCH, p_bound=BOUND)
        target_differ = XSET_INT.SegInt(p_name=NAME, p_summary=SUMMARY,
                                        p_title=TITLE_DIFFER, p_bound=BOUND)
        # Test
        assert reference.__eq__(target_match)
        assert not reference.__eq__(target_differ)

    def test_eq_type(self):
        """| Confirm equality comparson.
        | Case: type check.
        """
        # Setup
        NAME = 'Parrot'
        SUMMARY = 'This parrot is no more.'
        TITLE = 'Parrot Sketch'
        BOUND = 5
        reference = XSET_INT.SegInt(p_name=NAME, p_summary=SUMMARY,
                                    p_title=TITLE, p_bound=BOUND)
        OTHER = 'Something completely different.'
        # Test
        assert not reference.__eq__(OTHER)

    def test_init(self):
        """| Confirm initialization.
        | Case: explicit arguments with positive bound.
        """
        # Setup
        NAME = 'SegInt'
        SUMMARY = 'This topic represents a set of integers.'
        TITLE = 'Integer Set'
        SCOPE = MSET.SetIndexed
        BOUND = 5
        # Test
        target = XSET_INT.SegInt(
            p_name=NAME, p_summary=SUMMARY, p_title=TITLE, p_bound=BOUND)
        assert not target._stale
        assert isinstance(target._views, dict)
        assert not target._views
        assert NAME == target.name
        assert SUMMARY == target.summary
        assert TITLE == target.title
        assert isinstance(target._scope, SCOPE)
        assert BOUND == len(target._scope)

    def test_init_default(self):
        """| Confirm initialization.
        | Case: default arguments.
        """
        # Setup
        NAME_DEFAULT = ''
        SUMMARY_DEFAULT = ''
        TITLE_DEFAULT = ''
        BOUND_DEFAULT = 1
        # Test
        target = XSET_INT.SegInt()
        assert NAME_DEFAULT == target.name
        assert SUMMARY_DEFAULT == target.summary
        assert TITLE_DEFAULT == target.title
        assert BOUND_DEFAULT == len(target._scope)

    def test_init_guard(self):
        """| Confirm initialization.
        | Case: default arguments except negative bound.
        """
        # Setup
        BOUND = -42
        SIZE = 1
        # Test
        target = XSET_INT.SegInt(p_bound=BOUND)
        assert SIZE == len(target._scope)

    @pytest.mark.parametrize('BOUND_R, TITLE_R, BOUND_N, TITLE_N', [
        (5, 'N(5)', 5, 'N(5)'),
        (1, 'N(1)', 1, 'N(1)'),
        (3.14159, 'N(Pi)', 3, 'N(Pi)'),
        (0, 'Oops 0', 1,
         'N(1) - given bound was not a positive integer.'),
        (-1, 'Oops -1', 1,
         'N(1) - given bound was not a positive integer.'),
        ('3.14159', 'Oops str', 1,
         'N(1) - given bound was not a positive integer.'),
        (None, 'Oops None', 1,
         'N(1) - given bound was not a positive integer.'),
        ])
    def test_guard_bound(self, BOUND_R, TITLE_R, BOUND_N, TITLE_N):
        """Confirm bound check."""
        # Setup
        target = XSET_INT.SegInt()
        # Test
        bound_new, title_new = target.guard_bound(BOUND_R, TITLE_R)
        assert BOUND_N == bound_new
        assert TITLE_N == title_new
