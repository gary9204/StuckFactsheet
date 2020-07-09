"""
Unit tests for ancestor class for set topicss. See :mod:`~.set_topic`.
"""
import pytest   # type: ignore[import]

from factsheet.content.sets import set_topic as XSET
from factsheet.model import setindexed as MSET


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
        NAME = 'Parrot'
        SUMMARY = 'This parrot is no more.'
        TITLE = 'Parrot Sketch'
        target = XSET.Set[str](p_name=NAME, p_summary=SUMMARY, p_title=TITLE,
                               p_members=patch_members)
        Element = MSET.ElementGeneric[str]
        element = Element(member=MEMBER, index=INDEX)
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
        NAME = 'Parrot'
        SUMMARY = 'This parrot is no more.'
        TITLE = 'Parrot Sketch'
        target_left = XSET.Set[int](
            p_name=NAME, p_summary=SUMMARY, p_title=TITLE, p_members=MEMBERS_L)
        target_right = XSET.Set[int](
            p_name=NAME, p_summary=SUMMARY, p_title=TITLE, p_members=MEMBERS_R)
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
        reference = XSET.Set[int](p_name=NAME, p_summary=SUMMARY,
                                  p_title=TITLE_MATCH, p_members=MEMBERS)
        target_match = XSET.Set[int](p_name=NAME, p_summary=SUMMARY,
                                     p_title=TITLE_MATCH, p_members=MEMBERS)
        target_differ = XSET.Set[int](p_name=NAME, p_summary=SUMMARY,
                                      p_title=TITLE_DIFFER, p_members=MEMBERS)
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
        MEMBERS = [1, 2, 3, 4, 5]
        reference = XSET.Set[int](p_name=NAME, p_summary=SUMMARY,
                                  p_title=TITLE, p_members=MEMBERS)
        OTHER = 'Something completely different.'
        # Test
        assert not reference.__eq__(OTHER)

    def test_init(self):
        """| Confirm initialization.
        | Case: explicit arguments.
        """
        # Setup
        NAME = 'Set'
        SUMMARY = 'This topic represents a mathematical set.'
        TITLE = 'Set Topic'
        MEMBERS = [1, 2, 3]
        reference = MSET.SetIndexed(p_members=MEMBERS)
        # Test
        target = XSET.Set[int](
            p_name=NAME, p_summary=SUMMARY, p_title=TITLE, p_members=MEMBERS)
        assert not target._stale
        assert isinstance(target._views, dict)
        assert not target._views
        assert NAME == target.name
        assert SUMMARY == target.summary
        assert TITLE == target.title
        assert reference == target._elements

    def test_init_default(self):
        """| Confirm initialization.
        | Case: default arguments.
        """
        # Setup
        NAME_DEFAULT = ''
        SUMMARY_DEFAULT = ''
        TITLE_DEFAULT = ''
        reference = MSET.SetIndexed[int]()
        # Test
        target = XSET.Set[int]()
        assert NAME_DEFAULT == target.name
        assert SUMMARY_DEFAULT == target.summary
        assert TITLE_DEFAULT == target.title
        assert reference == target._elements

    def test_iter(self, patch_members):
        """| Confirm iterator.
        | Case: topic set non-empty.
        """
        # Setup
        NAME = 'Set'
        SUMMARY = 'This topic represents a mathematical set.'
        TITLE = 'Set Topic'
        target = XSET.Set[str](p_name=NAME, p_summary=SUMMARY, p_title=TITLE,
                               p_members=patch_members)
        EXPECT = dict(enumerate(patch_members))
        # Test
        assert EXPECT == {e.index: e.member for e in target}

    def test_iter_empty(self):
        """| Confirm iterator.
        | Case: topic set empty.
        """
        # Setup
        NAME = 'Set'
        SUMMARY = 'This topic represents a mathematical set.'
        TITLE = 'Set Topic'
        target = XSET.Set[str](p_name=NAME, p_summary=SUMMARY, p_title=TITLE,
                               p_members=list())
        EXPECT = dict()
        # Test
        assert EXPECT == dict(target)
