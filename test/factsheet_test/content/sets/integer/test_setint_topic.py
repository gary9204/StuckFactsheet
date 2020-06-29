"""
Unit tests for set of integer topic class. See :mod:`~.setint_topic`.
"""
from factsheet.model import infoid as MINFOID
from factsheet.model import setindexed as MSET
from factsheet.content.sets.integer import setint_topic as XSET_INT


class TestSetInt:
    """Unit tests for :class:`~.SetInt`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        NAME = 'SetInt'
        SUMMARY = 'This topic represents a set of integers.'
        TITLE = 'Integer Set'
        SCOPE = MSET.SetIndexed
        SIZE = 0
        # Test
        target = XSET_INT.SetInt(
            p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
        assert not target._stale
        assert isinstance(target._views, dict)
        assert not target._views
        assert isinstance(target._infoid, MINFOID.InfoId)
        assert NAME == target._infoid.name
        assert SUMMARY == target._infoid.summary
        assert TITLE == target._infoid.title
        assert isinstance(target._scope, SCOPE)
        assert SIZE == len(target._scope)

    def test_init_default(self):
        """Confirm initialization with default arguments."""
        # Setup
        NAME_DEFAULT = ''
        SUMMARY_DEFAULT = ''
        TITLE_DEFAULT = ''
        # Test
        target = XSET_INT.SetInt()
        assert NAME_DEFAULT == target._infoid.name
        assert SUMMARY_DEFAULT == target._infoid.summary
        assert TITLE_DEFAULT == target._infoid.title
