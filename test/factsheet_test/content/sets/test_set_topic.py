"""
Unit tests for set topic class. See :mod:`~.set_topic`.
"""
from factsheet.model import infoid as MINFOID
from factsheet.content.sets import set_topic as XSET


class TestSet:
    """Unit tests for :class:`~.Set`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        NAME = 'Set'
        SUMMARY = 'This topic represents a mathematical set.'
        TITLE = 'Set Topic'
        # Test
        target = XSET.Set(
            p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
        assert not target._stale
        assert isinstance(target._views, dict)
        assert not target._views
        assert isinstance(target._infoid, MINFOID.InfoId)
        assert NAME == target._infoid.name
        assert SUMMARY == target._infoid.summary
        assert TITLE == target._infoid.title

    def test_init_default(self):
        """Confirm initialization with default arguments."""
        # Setup
        NAME_DEFAULT = ''
        SUMMARY_DEFAULT = ''
        TITLE_DEFAULT = ''
        # Test
        target = XSET.Set()
        assert NAME_DEFAULT == target._infoid.name
        assert SUMMARY_DEFAULT == target._infoid.summary
        assert TITLE_DEFAULT == target._infoid.title
