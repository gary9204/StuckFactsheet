"""
Unit tests for class for set of integers topics. See
:mod:`~.setint_topic`.
"""
from factsheet.content.sets.int import setint_topic as XSET_INT


class TestSetInt:
    """Unit tests for :class:`~.SetInt`."""

    def test_types(self):
        """Confirm support types defined."""
        # Setup
        # Test
        assert XSET_INT.ElementInt is not None

    def test_init(self):
        """| Confirm initialization.
        | Case: explicit arguments.
        """
        # Setup
        NAME = 'SetInt'
        SUMMARY = 'This topic represents a set of integers.'
        TITLE = 'Integer Set'
        SIZE = 0
        # Test
        target = XSET_INT.SetInt(
            p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
        assert not target._stale
        assert isinstance(target._views, dict)
        assert not target._views
        assert NAME == target.name
        assert SUMMARY == target.summary
        assert TITLE == target.title
        assert SIZE == len(target._elements)

    def test_init_default(self):
        """Confirm initialization.
        | Case: default arguments."""
        # Setup
        NAME_DEFAULT = ''
        SUMMARY_DEFAULT = ''
        TITLE_DEFAULT = ''
        # Test
        target = XSET_INT.SetInt()
        assert NAME_DEFAULT == target.name
        assert SUMMARY_DEFAULT == target.summary
        assert TITLE_DEFAULT == target.title
