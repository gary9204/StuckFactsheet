"""
Unit tests for topic class for binary operation on a set of integers.
See :mod:`~.opint_topic`.
"""
from factsheet.content.ops.int import opint_topic as XOP_INT
from factsheet.model import setindexed as MSET


class TestOperationInt:
    """Unit tests for :class:`~.OperationInt`."""

    def test_init(self):
        """| Confirm initialization.
        | Case: explicit arguments.
        """
        # Setup
        NAME = 'OpInt'
        SUMMARY = ('This topic represents a bniary operation on a set of '
                   'integers.')
        TITLE = 'Binary Operation on an Integer Set'
        MEMBERS = [1, 2, 3]
        SET = MSET.SetIndexed[int](p_members=MEMBERS)
        # Test
        target = XOP_INT.OperationInt(
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
        """| Confirm initialization.
        | Case: default arguments.
        """
        # Setup
        NAME_DEFAULT = ''
        SUMMARY_DEFAULT = ''
        TITLE_DEFAULT = ''
        MEMBERS = list()
        SET = MSET.SetIndexed[int](MEMBERS)
        # Test
        target = XOP_INT.OperationInt(p_set=SET)
        assert NAME_DEFAULT == target.name
        assert SUMMARY_DEFAULT == target.summary
        assert TITLE_DEFAULT == target.title
