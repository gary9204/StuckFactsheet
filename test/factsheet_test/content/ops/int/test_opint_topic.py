"""
Unit tests for topic class for binary operation on a set of integers.
See :mod:`~.opint_topic`.
"""
import factsheet.content.ops.int.opint_topic as XOPINT
import factsheet.content.ops.op_topic as XOP


class TestOperationInt:
    """Unit tests for :class:`~.OperationInt`."""

    def test_specialize(self):
        """Confirm specialization of :class:`.Operation`."""
        # Setup
        # Test
        assert issubclass(XOPINT.OperationInt, XOP.Operation)
        assert not issubclass(XOP.Operation, XOPINT.OperationInt)

    # def test_init(self):
    #     """| Confirm initialization.
    #     | Case: explicit arguments.
    #     """
    #     # Setup
    #     NAME = 'OpInt'
    #     SUMMARY = ('This topic represents a bniary operation on a set of '
    #                'integers.')
    #     TITLE = 'Binary Operation on an Integer Set'
    #     MEMBERS = [1, 2, 3]
    #     SET = MSET.SetIndexed[int](p_members=MEMBERS)
    #     # Test
    #     target = XOP_INT.OperationInt(
    #         p_name=NAME, p_summary=SUMMARY, p_title=TITLE, p_set=SET)
    #     assert not target._stale
    #     assert isinstance(target._forms, dict)
    #     assert not target._forms
    #     assert NAME == target.name
    #     assert SUMMARY == target.summary
    #     assert TITLE == target.title
    #     assert target._set is SET
    #     assert target._op(None, None) is None

    # def test_init_default(self):
    #     """| Confirm initialization.
    #     | Case: default arguments.
    #     """
    #     # Setup
    #     NAME_DEFAULT = ''
    #     SUMMARY_DEFAULT = ''
    #     TITLE_DEFAULT = ''
    #     MEMBERS = list()
    #     SET = MSET.SetIndexed[int](MEMBERS)
    #     # Test
    #     target = XOP_INT.OperationInt(p_set=SET)
    #     assert NAME_DEFAULT == target.name
    #     assert SUMMARY_DEFAULT == target.summary
    #     assert TITLE_DEFAULT == target.title
