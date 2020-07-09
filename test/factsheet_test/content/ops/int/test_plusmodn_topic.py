"""
Unit tests for class defining modular arithmetic operation topics.
See :mod:`~.plusmodn_topic`.
"""
import collections as COL
import pytest   # type: ignore[import]

from factsheet.content.ops.int import plusmodn_topic as XPLUS_N
from factsheet.content.sets.int import segint_topic as XSEG_INT
from factsheet.content.sets.int import setint_topic as XSET_INT
from factsheet.model import setindexed as MSET

IE = MSET.IndexElement
Element = XSET_INT.ElementInt


@pytest.fixture
def patch_new_segment():
    """Pytest fixture to provide integer segment factory function."""
    def new_segment(p_bound=3):
        name = 'N({})'.format(p_bound)
        segment = XSEG_INT.SegInt(p_name=name, p_bound=p_bound)
        return segment

    return new_segment


class TestPlusModN:
    """Unit tests for :class:`~.PlusModN`."""

    def test_eq_info(self, patch_new_segment):
        """| Confirm equality comparison.
        | Case: identification information check.
        """
        # Setup
        NAME = 'Parrot'
        SUMMARY = 'This parrot is no more.'
        TITLE_MATCH = 'Parrot Sketch'
        TITLE_DIFFER = 'Something completely different.'
        SIZE_SET = 5
        SET = patch_new_segment(SIZE_SET)
        MODULUS = 5
        reference = XPLUS_N.PlusModN(
            p_name=NAME, p_summary=SUMMARY, p_title=TITLE_MATCH,
            p_set=SET, p_modulus=MODULUS)
        target_match = XPLUS_N.PlusModN(
            p_name=NAME, p_summary=SUMMARY, p_title=TITLE_MATCH,
            p_set=SET, p_modulus=MODULUS)
        target_differ = XPLUS_N.PlusModN(
            p_name=NAME, p_summary=SUMMARY, p_title=TITLE_DIFFER,
            p_set=SET, p_modulus=MODULUS)
        # Test
        assert not reference.__eq__(target_differ)
        assert reference.__eq__(target_match)

    @pytest.mark.parametrize('MODULUS_L, MODULUS_R, RESULT', [
        (2, 2, True),
        (2, 3, False),
        (5, 3, False),
        (6, 6, True),
        ])
    def test_eq_modulus(
            self, patch_new_segment, MODULUS_L, MODULUS_R, RESULT):
        """| Confirm equality comparison.
        | Case: modulus checks.
        """
        # Setup
        SIZE_SET = 5
        SET = patch_new_segment(SIZE_SET)
        target_left = XPLUS_N.PlusModN(p_set=SET, p_modulus=MODULUS_L)
        target_right = XPLUS_N.PlusModN(p_set=SET, p_modulus=MODULUS_R)
        # Test
        assert target_left.__eq__(target_right) is RESULT

    @pytest.mark.parametrize('SIZE_L, SIZE_R, RESULT', [
        (2, 2, True),
        (2, 3, False),
        (5, 3, False),
        (6, 6, True),
        ])
    def test_eq_sets(self, patch_new_segment, SIZE_L, SIZE_R, RESULT):
        """| Confirm equality comparison.
        | Case: set checks.
        """
        # Setup
        MODULUS = 5
        SET_L = patch_new_segment(SIZE_L)
        target_left = XPLUS_N.PlusModN(p_set=SET_L, p_modulus=MODULUS)
        SET_R = patch_new_segment(SIZE_R)
        target_right = XPLUS_N.PlusModN(p_set=SET_R, p_modulus=MODULUS)
        # Test
        assert target_left.__eq__(target_right) is RESULT

    def test_eq_type(self, patch_new_segment):
        """| Confirm equality comparson.
        | Case: type check.
        """
        # Setup
        SIZE_SET = 5
        SET = patch_new_segment(SIZE_SET)
        MODULUS = 5
        reference = XPLUS_N.PlusModN(p_set=SET, p_modulus=MODULUS)
        OTHER = 'Something completely different.'
        # Test
        assert not reference.__eq__(OTHER)

    def test_init(self, patch_new_segment):
        """| Confirm initialization.
        | Case: explicit arguments with modulus greater than one.
        """
        # Setup
        MODULUS = 6
        NAME = 'Plus mod {}'.format(MODULUS)
        SUMMARY = 'This topic represents modular addition of integers.'
        TITLE = 'Addition modulo {}'.format(MODULUS)
        SET = patch_new_segment(MODULUS)
        # Test
        target = XPLUS_N.PlusModN(
            p_name=NAME, p_summary=SUMMARY, p_title=TITLE,
            p_set=SET, p_modulus=MODULUS)
        assert not target._stale
        assert isinstance(target._views, dict)
        assert not target._views
        assert NAME == target.name
        assert SUMMARY == target.summary
        assert TITLE == target.title
        assert SET == target._set
        assert target._set is SET
        assert target._op is not None
        assert MODULUS == target._modulus
        assert target._reps is not None

    def test_init_default(self, patch_new_segment):
        """| Confirm initialization.
        | Case: default arguments.
        """
        # Setup
        MODULUS = 6
        NAME_DEFAULT = ''
        SUMMARY_DEFAULT = ''
        TITLE_DEFAULT = ''
        SET = patch_new_segment(MODULUS)
        # Test
        target = XPLUS_N.PlusModN(p_set=SET, p_modulus=MODULUS)
        assert NAME_DEFAULT == target.name
        assert SUMMARY_DEFAULT == target.summary
        assert TITLE_DEFAULT == target.title

    def test_init_guard(self, patch_new_segment):
        """| Confirm initialization.
        | Case: default arguments except negative bound.
        """
        # Setup
        SET = patch_new_segment()
        MODULUS = -42
        MODULUS_MIN = 2
        # Test
        target = XPLUS_N.PlusModN(p_set=SET, p_modulus=MODULUS)
        assert MODULUS_MIN == target._modulus

    @pytest.mark.parametrize('MODULUS_R, TITLE_R, MODULUS_N, TITLE_N', [
        (5, 'Plus mod 5', 5, 'Plus mod 5'),
        (2, 'Plus mod 2', 2, 'Plus mod 2'),
        (3.14159, 'Plus mod Pi', 3, 'Plus mod Pi'),
        (1, 'Oops 1', 2,
         'Plus mod 2 - given modulus was not an integer greater than 1.'),
        (-3, 'Oops -3', 2,
         'Plus mod 2 - given modulus was not an integer greater than 1.'),
        ('3.14159', 'Oops str', 2,
         'Plus mod 2 - given modulus was not an integer greater than 1.'),
        (None, 'Oops None', 2,
         'Plus mod 2 - given modulus was not an integer greater than 1.'),
        ])
    def test_guard_modulus(self, patch_new_segment,
                           MODULUS_R, TITLE_R, MODULUS_N, TITLE_N):
        """Confirm bound check."""
        # Setup
        SET = patch_new_segment()
        target = XPLUS_N.PlusModN(p_set=SET, p_modulus=MODULUS_R)
        # Test
        modulus_new, title_new = target._guard_modulus(MODULUS_R, TITLE_R)
        assert MODULUS_N == modulus_new
        assert TITLE_N == title_new

    @pytest.mark.parametrize('LEFT, RIGHT, RESULT', [
        (Element(member=1, index=IE(1)), Element(member=2, index=IE(2)),
            Element(member=3, index=IE(3))),
        (Element(member=1, index=IE(1)), Element(member=4, index=IE(4)),
            Element(member=5, index=IE(5))),
        (Element(member=3, index=IE(3)), Element(member=4, index=IE(4)),
            Element(member=2, index=IE(2))),
        ('Oops!', Element(member=4, index=IE(4)), None),
        (Element(member=4, index=IE(4)), 'Oops!', None),
        ])
    def test_op(self, patch_new_segment, LEFT, RIGHT, RESULT):
        """| Confirm modular addition.
        | Case: checks with complete set of representatives.
        """
        # Setup
        SIZE_SET = 7
        SET = patch_new_segment(SIZE_SET)
        MODULUS = 5
        target = XPLUS_N.PlusModN(p_set=SET, p_modulus=MODULUS)
        # Test
        assert RESULT == target._op(LEFT, RIGHT)

    def test_op_partial(self, patch_new_segment):
        """| Confirm modular addition.
        | Case: incomplete set of representatives.
        """
        # Setup
        SIZE_SET = 3
        SET = patch_new_segment(SIZE_SET)
        MODULUS = 5
        target = XPLUS_N.PlusModN(p_set=SET, p_modulus=MODULUS)
        LEFT = Element(member=1, index=IE(1))
        RIGHT = Element(member=2, index=IE(2))
        # Test
        assert target._op(LEFT, RIGHT) is None

    @pytest.mark.parametrize('SIZE_SET, MODULUS', [
        (3, 5),  # [0, 1, 2]
        (5, 5),  # [0, 1, 2, 3, 4]
        (7, 5),  # [5, 6, 2, 3, 4]
        ])
    def test_reduce_reps(self, patch_new_segment, SIZE_SET, MODULUS):
        """| Confirm reduction of congruence class representatives.
        | Case: non-empty sets.
        """
        # Setup
        SET = patch_new_segment(SIZE_SET)
        target = XPLUS_N.PlusModN(p_set=SET, p_modulus=MODULUS)
        elements = sorted(SET, key=lambda e: e.index)
        elements_rep = COL.deque(elements[-MODULUS:])
        elements_rep.rotate(SIZE_SET % MODULUS)
        reps_reference = list(enumerate(elements_rep))
        # Test
        reps_target = target._reduce_reps(SET)
        assert reps_reference == sorted(
            reps_target.items(), key=lambda m: m[0])

    def test_reduce_reps_empty(self):
        """| Confirm reduction of congruence class representatives.
        | Case: empty set.
        """
        # Setup
        SET = XSET_INT.SetInt()
        MODULUS = 5
        target = XPLUS_N.PlusModN(p_set=SET, p_modulus=MODULUS)
        # Test
        reps_target = target._reduce_reps(SET)
        assert isinstance(reps_target, dict)
        assert not reps_target
