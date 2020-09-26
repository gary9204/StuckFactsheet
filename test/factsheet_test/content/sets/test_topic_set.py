"""
Unit tests for ancestor class of set topics. See :mod:`~.topic_set`.
"""
import pytest   # type: ignore[import]

import factsheet.content.sets.topic_set as XSET
import factsheet.model.element as MELEMENT
import factsheet.model.setindexed as MSET


@pytest.fixture
def patch_members():
    """Pytest fixture returns fixed list for set members."""
    return list('abcd')


class TestSet:
    """Unit tests for topic :class:`~.Set`."""

    @pytest.mark.parametrize('MEMBER, INDEX, RESULT', [
        ('b', 1, True),
        ('a', -1, False),
        ('z', 0, False),
        ])
    def test_contains(self, patch_members, MEMBER, INDEX, RESULT):
        """| Confirm contains.
        | Case: indexed elements in and not in set.
        """
        # Setup
        MEMBERS = patch_members
        target = XSET.Set[int](p_members=MEMBERS)
        Element = MELEMENT.ElementOpaque[str]
        element = Element(p_member=MEMBER, p_index=INDEX)
        # Test
        assert target.__contains__(element) is RESULT

    @pytest.mark.parametrize('MEMBERS_L, MEMBERS_R, RESULT', [
        (list(), None, True),
        (list(), [3], False),
        ([5], list(), False),
        ([1, 2, 3], [1, 3], False),
        ([1, 0, 3], [1, 2, 3], False),
        ([1, 2], [2, 1], False),
        ([1, 2, 3], [1, 2, 3], True),
        ])
    def test_eq_elements(self, MEMBERS_L, MEMBERS_R, RESULT):
        """| Confirm equality comparison.
        | Case: indexed set checks.
        """
        # Setup
        target_left = XSET.Set[int](p_members=MEMBERS_L)
        target_right = XSET.Set[int](p_members=MEMBERS_R)
        target_right._facts = target_left._facts
        # Test
        assert target_left.__eq__(target_right) is RESULT

    def test_eq_info(self):
        """| Confirm equality comparison.
        | Case: identification information check.
        """
        # Setup
        NAME = 'Parrot'
        SUMMARY = 'This parrot is no more.'
        TITLE_MATCH = 'Parrot Sketch'
        TITLE_DIFFER = 'Something completely different.'
        MEMBERS = [1, 2, 3, 4, 5]
        reference = XSET.Set[int](p_members=MEMBERS)
        reference.init_identity(
            p_name=NAME, p_summary=SUMMARY, p_title=TITLE_MATCH)
        target_match = XSET.Set[int](p_members=MEMBERS)
        target_match.init_identity(
            p_name=NAME, p_summary=SUMMARY, p_title=TITLE_MATCH)
        target_differ = XSET.Set[int](p_members=MEMBERS)
        target_differ.init_identity(
            p_name=NAME, p_summary=SUMMARY, p_title=TITLE_DIFFER)
        # Test
        assert reference.__eq__(target_match)
        assert not reference.__eq__(target_differ)

    def test_eq_type(self):
        """| Confirm equality comparson.
        | Case: type check.
        """
        # Setup
        MEMBERS = [1, 2, 3, 4, 5]
        reference = XSET.Set[int](p_members=MEMBERS)
        OTHER = 'Something completely different.'
        # Test
        assert not reference.__eq__(OTHER)

    def test_init(self):
        """| Confirm initialization.
        | Case: explicit arguments.
        """
        # Setup
        MEMBERS = [1, 2, 3]
        reference = MSET.SetIndexed(p_members=MEMBERS)
        # Test
        target = XSET.Set[int](p_members=MEMBERS)
        assert not target._stale
        assert isinstance(target._forms, dict)
        assert not target._forms
        assert reference == target._elements

    def test_iter(self, patch_members):
        """| Confirm iterator.
        | Case: topic set non-empty.
        """
        # Setup
        target = XSET.Set[str](p_members=patch_members)
        EXPECT = dict(enumerate(patch_members))
        # Test
        assert EXPECT == {e.index: e.member for e in target}

    def test_iter_empty(self):
        """| Confirm iterator.
        | Case: topic set empty.
        """
        # Setup
        target = XSET.Set[str](p_members=list())
        EXPECT = dict()
        # Test
        assert EXPECT == dict(target)

    @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
        ('_elements', 'elements'),
        ])
    def test_property(self, patch_members, NAME_ATTR, NAME_PROP):
        """Confirm properties are get-only.

        #. Case: get
        #. Case: no set
        #. Case: no delete
        """
        # Setup
        target = XSET.Set[str](p_members=patch_members)
        value_attr = getattr(target, NAME_ATTR)
        target_prop = getattr(XSET.Set, NAME_PROP)
        value_prop = getattr(target, NAME_PROP)
        # Test: read
        assert target_prop.fget is not None
        assert str(value_attr) == str(value_prop)
        # Test: no replace
        assert target_prop.fset is None
        # Test: no delete
        assert target_prop.fdel is None
