"""
Defines unit tests for fact classes for a generic set.  See
:mod:`.set_fact`.
"""
from factsheet.content.sets.int import facts_segint as XFACTS_SEGINT
from factsheet.content.sets.int import topic_segint as XSEGINT
from factsheet.model import fact as MFACT
from factsheet.model import infoid as MINFOID


class TestBoundSegInt:
    """Unit tests for :class:`.BoundSegInt`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        SIZE = 5
        TOPIC = XSEGINT.SegInt(p_bound=SIZE)
        NAME = 'Bound'
        SUMMARY = ('{} provides upper bound of {}, an initial segment of '
                   'natural numbers.'.format(NAME, TOPIC.name))
        TITLE = 'Segment Upper Bound'
        # Test
        target = XFACTS_SEGINT.BoundSegInt(p_topic=TOPIC)
        assert isinstance(target._infoid, MINFOID.InfoId)
        assert NAME == target.name
        assert SUMMARY == target.summary
        assert TITLE == target.title
        assert target._value is None
        assert target._status is MFACT.StatusOfFact.BLOCKED
        assert not target._stale
        assert isinstance(target._blocks, dict)
        assert not target._blocks
        assert len(TOPIC._elements) == target._bound

    def test_check(self, patch_class_block_fact):
        """Confirm check."""
        # Setup
        BOUND = 5
        TOPIC = XSEGINT.SegInt(p_bound=BOUND)
        target = XFACTS_SEGINT.BoundSegInt(p_topic=TOPIC)
        PatchBlockFact = patch_class_block_fact
        block = PatchBlockFact()
        target.attach_block(block)
        target.set_fresh()
        # Test
        result = target.check()
        assert target.is_stale()
        assert block.called_update
        assert BOUND == target._value
        assert target._status is MFACT.StatusOfFact.DEFINED
        assert result is MFACT.StatusOfFact.DEFINED

    def test_clear(self, patch_class_block_fact):
        """Confirm check."""
        # Setup
        BOUND = 5
        TOPIC = XSEGINT.SegInt(p_bound=BOUND)
        target = XFACTS_SEGINT.BoundSegInt(p_topic=TOPIC)
        target._value = 'Something completely different.'
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
