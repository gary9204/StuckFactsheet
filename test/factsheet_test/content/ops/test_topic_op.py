"""
Unit tests for ancestor class for binary operation topics.  See
:mod:`~.topic_op`.
"""
import dataclasses as DC
import pytest  # type: ignore[import]
import factsheet.content.ops.topic_op as XOP
import factsheet.content.sets.topic_set as XSET


# @pytest.fixture
# def patch_new_set_op():
#     """Pytest fixture to provide set factory function."""
#     def new_set_op(p_set=3):
#         return XSET.Set(p_members=range(p_set))

#     return new_set


class TestOperation:
    """Unit tests for :class:`~.Operation`."""

    def test_eq_info(self):
        """| Confirm equality comparison.
        | Case: identification information check.
        """
        # Setup
        NAME = 'Parrot'
        SUMMARY = 'This parrot is no more.'
        TITLE_MATCH = 'Parrot Sketch'
        TITLE_DIFFER = 'Something completely different.'
        SIZE_SET = 5
        SET = XSET.Set[int](p_members=range(SIZE_SET))
        reference = XOP.Operation(p_set=SET)
        reference.init_identity(
            p_name=NAME, p_summary=SUMMARY, p_title=TITLE_MATCH)
        target_match = XOP.Operation(p_set=SET)
        target_match.init_identity(
            p_name=NAME, p_summary=SUMMARY, p_title=TITLE_MATCH)
        target_differ = XOP.Operation(p_set=SET)
        target_differ.init_identity(
            p_name=NAME, p_summary=SUMMARY, p_title=TITLE_DIFFER)
        # Test
        assert not reference.__eq__(target_differ)
        assert reference.__eq__(target_match)

    @pytest.mark.parametrize('SIZE_L, SIZE_R, RESULT', [
        (2, 2, True),
        (2, 3, False),
        (5, 3, False),
        (6, 6, True),
        ])
    def test_eq_sets(self, SIZE_L, SIZE_R, RESULT):
        """| Confirm equality comparison.
        | Case: set checks.
        """
        # Setup
        SET_L = XSET.Set[int](p_members=range(SIZE_L))
        target_left = XOP.Operation(p_set=SET_L)
        SET_R = XSET.Set[int](p_members=range(SIZE_R))
        target_right = XOP.Operation(p_set=SET_R)
        # Test
        assert target_left.__eq__(target_right) is RESULT

    # def test_eq_type(self, patch_new_segment):
    #     """| Confirm equality comparson.
    #     | Case: type check.
    #     """
    #     # Setup
    #     SIZE_SET = 5
    #     SET = patch_new_segment(SIZE_SET)
    #     MODULUS = 5
    #     reference = XOP.Operation(p_set=SET)
    #     OTHER = 'Something completely different.'
    #     # Test
    #     assert not reference.__eq__(OTHER)

    def test_init(self):
        """Confirm initialization."""
        # Setup
        MEMBERS = [1, 2, 3]
        SET = XSET.Set[int](p_members=MEMBERS)
        # Test
        target = XOP.Operation[int](p_set=SET)
        assert not target._stale
        assert isinstance(target._forms, dict)
        assert not target._forms
        assert target._set_op is SET
        assert target.op(None, None) is None

    # def test_init_default(self):
    #     """Confirm initialization with default arguments."""
    #     # Setup
    #     NAME_DEFAULT = ''
    #     SUMMARY_DEFAULT = ''
    #     TITLE_DEFAULT = ''
    #     MEMBERS = list()
    #     SET = XSET.Set[int](p_members=MEMBERS)
    #     # Test
    #     target = XOP.Operation(p_set_op=SET)
    #     assert NAME_DEFAULT == target.name
    #     assert SUMMARY_DEFAULT == target.summary
    #     assert TITLE_DEFAULT == target.title
    #     assert target._set_op is SET

    @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
        ('_set_op', 'set_op'),
        ])
    def test_property(self, patch_args_infoid, NAME_ATTR, NAME_PROP):
        """Confirm properties are get-only.

        #. Case: get
        #. Case: no set
        #. Case: no delete
        """
        # Setup
        MEMBERS = [1, 2, 3]
        SET = XSET.Set[int](p_members=MEMBERS)
        target = XOP.Operation[int](p_set=SET)
        ARGS = patch_args_infoid
        target.init_identity(**DC.asdict(ARGS))
        value_attr = getattr(target, NAME_ATTR)
        target_prop = getattr(XOP.Operation, NAME_PROP)
        value_prop = getattr(target, NAME_PROP)
        # Test: read
        assert target_prop.fget is not None
        assert str(value_attr) == str(value_prop)
        # Test: no replace
        assert target_prop.fset is None
        # Test: no delete
        assert target_prop.fdel is None
