"""
Unit tests for note topic class. See :mod:`~.note_topic`.
"""
from factsheet.model import infoid as MINFOID
from factsheet.content.note import note_topic as XNOTE


class TestNote:
    """Unit tests for :class:`~.Note`."""

    def test_init(self, args_infoid_stock):
        """Confirm initialization."""
        # Setup
        NAME = args_infoid_stock['p_name']
        SUMMARY = args_infoid_stock['p_summary']
        TITLE = args_infoid_stock['p_title']
        # Test
        target = XNOTE.Note(
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
        target = XNOTE.Note()
        assert NAME_DEFAULT == target._infoid.name
        assert SUMMARY_DEFAULT == target._infoid.summary
        assert TITLE_DEFAULT == target._infoid.title
