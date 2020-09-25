"""
Defines unit tests for fact classes for a generic set.  See
:mod:`.op_fact`.
"""
import pytest   # type: ignore[import]

from factsheet.content.ops import op_topic as XOP
from factsheet.content.ops import facts_op as XFACTS_OP
from factsheet.content.sets import set_topic as XSET
from factsheet.model import fact as MFACT
from factsheet.model import infoid as MINFOID


@pytest.fixture
def patch_topic_closed():
    """Pytest fixture returns stock, closed operation topic."""
    class OpClosed(XOP.Operation[int]):
        def op(self, _a, _b): return 0

    def new_topic(p_size_set):
        members = list(range(p_size_set))
        topic_set = XSET.Set(p_members=members)
        topic = OpClosed(p_set=topic_set)
        topic.init_identity(p_name='Dinsdale')
        return topic

    return new_topic


class TestClosed:
    """Unit tests for :class:`.Closed`."""

    def test_init(self, patch_topic_closed):
        """Confirm initialization."""
        # Setup
        SIZE = 5
        TOPIC = patch_topic_closed(p_size_set=SIZE)
        NAME = 'Closed'
        SUMMARY = ('{} is True when {}\'s set is closed under the '
                   'operation.'.format(NAME, TOPIC.name))
        TITLE = '{} Is Closed'.format(TOPIC.name)
        # Test
        target = XFACTS_OP.Closed(p_topic=TOPIC)
        assert isinstance(target._infoid, MINFOID.InfoId)
        assert NAME == target.name
        assert SUMMARY == target.summary
        assert TITLE == target.title
        assert target._value is None
        assert target._status is MFACT.StatusOfFact.BLOCKED
        assert not target._stale
        assert isinstance(target._blocks, dict)
        assert not target._blocks
        assert target._op == TOPIC.op
        assert target._set_op == TOPIC.set_op

    def test_check_false(self, patch_class_block_fact):
        """| Confirm default check.
        | Case: operation is not closed
        """
        # Setup
        SIZE = 5
        last = SIZE - 1
        members = list(range(SIZE))
        topic_set = XSET.Set(p_members=members)

        class OpPartial(XOP.Operation[int]):
            def op(self, a, b):
                if (last == a.member) and (last == b.member):
                    return None
                else:
                    return 0

        TOPIC = OpPartial(p_set=topic_set)
        VALUE = False
        target = XFACTS_OP.Closed(p_topic=TOPIC)
        PatchBlockFact = patch_class_block_fact
        block = PatchBlockFact()
        target.attach_block(block)
        target.set_fresh()
        # Test
        result = target.check()
        assert target.is_stale()
        assert block.called_update
        assert VALUE == target._value
        assert target._status is MFACT.StatusOfFact.DEFINED
        assert result is MFACT.StatusOfFact.DEFINED

    def test_check_true(self, patch_topic_closed, patch_class_block_fact):
        """| Confirm default check.
        | Case: operation is closed
        """
        # Setup
        SIZE = 5
        TOPIC = patch_topic_closed(p_size_set=SIZE)
        VALUE = True
        target = XFACTS_OP.Closed(p_topic=TOPIC)
        PatchBlockFact = patch_class_block_fact
        block = PatchBlockFact()
        target.attach_block(block)
        target.set_fresh()
        # Test
        result = target.check()
        assert target.is_stale()
        assert block.called_update
        assert VALUE == target._value
        assert target._status is MFACT.StatusOfFact.DEFINED
        assert result is MFACT.StatusOfFact.DEFINED

    def test_clear(self, patch_topic_closed, patch_class_block_fact):
        """Confirm default clear."""
        # Setup
        SIZE = 5
        TOPIC = patch_topic_closed(p_size_set=SIZE)
        target = XFACTS_OP.Closed(p_topic=TOPIC)
        target._value = True
        target._status = MFACT.StatusOfFact.DEFINED
        PatchBlockFact = patch_class_block_fact
        block = PatchBlockFact()
        target.attach_block(block)
        target.set_fresh()
        # Test
        target.clear()
        assert target.is_stale()
        assert block.called_update
        assert target._value is None
        assert target._status is MFACT.StatusOfFact.UNCHECKED
