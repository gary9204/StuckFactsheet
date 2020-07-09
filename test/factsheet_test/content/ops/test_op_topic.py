"""
Unit tests for ancestor class for binary operation topics.  See
:mod:`~.op_topic`.
"""
from factsheet.content.ops import op_topic as XOP
from factsheet.content.sets import set_topic as XSET


class TestOperation:
    """Unit tests for :class:`~.Operation`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        NAME = 'Operation'
        SUMMARY = 'This topic represents a binary operation.'
        TITLE = 'Operation Topic'
        MEMBERS = [1, 2, 3]
        SET = XSET.Set[int](p_members=MEMBERS)
        # Test
        target = XOP.Operation(
            p_name=NAME, p_summary=SUMMARY, p_title=TITLE, p_set=SET)
        assert not target._stale
        assert isinstance(target._views, dict)
        assert not target._views
        assert NAME == target.name
        assert SUMMARY == target.summary
        assert TITLE == target.title
        assert target._set is SET
        assert target._op(None, None) is None

    def test_init_default(self):
        """Confirm initialization with default arguments."""
        # Setup
        NAME_DEFAULT = ''
        SUMMARY_DEFAULT = ''
        TITLE_DEFAULT = ''
        MEMBERS = list()
        SET = XSET.Set[int](p_members=MEMBERS)
        # Test
        target = XOP.Operation(p_set=SET)
        assert NAME_DEFAULT == target.name
        assert SUMMARY_DEFAULT == target.summary
        assert TITLE_DEFAULT == target.title
        assert target._set is SET
