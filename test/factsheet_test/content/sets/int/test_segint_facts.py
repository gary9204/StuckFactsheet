"""
Defines unit tests for fact classes for a generic set.  See
:mod:`.set_fact`.
"""
import dataclasses as DC
import pytest   # type: ignore[import]
# import typing


from factsheet.abc_types import abc_fact as ABC_FACT
from factsheet.content.sets.int import segint_facts as XSEGINT_FACTS
from factsheet.content.sets.int import segint_topic as XSEGINT
# from factsheet.model import element as MELEMENT
# from factsheet.model import setindexed as MSET
from factsheet.model import fact as MFACT
from factsheet.model import infoid as MINFOID
# from factsheet.model import setindexed as MSET


@pytest.fixture
def patch_topic():
    """TBD"""
    def new_topic(p_size_set):
        NAME = 'Parrots'
        SUMMARY = 'This topic is a lovely collection of parrots.'
        TITLE = 'Parrot Shop'
        topic = XSEGINT.SegInt(p_name=NAME, p_summary=SUMMARY,
                               p_title=TITLE, p_bound=p_size_set)
        return topic

    return new_topic


class TestBoundSegInt:
    """Unit tests for :class:`.BoundSegInt`."""

    def test_init(self, patch_topic):
        """Confirm initialization."""
        # Setup
        SIZE = 5
        TOPIC = patch_topic(p_size_set=SIZE)
        NAME = 'Bound'
        SUMMARY = ('{} provides upper bound of {}, an initial segment of '
                   'natural numbers.'.format(NAME, TOPIC.name))
        TITLE = 'Segment Upper Bound'
        # Test
        target = XSEGINT_FACTS.BoundSegInt(p_topic=TOPIC)
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

    def test_check(self, patch_topic, patch_class_block_fact):
        """Confirm check."""
        # Setup
        SIZE = 5
        TOPIC = patch_topic(p_size_set=SIZE)
        value = str(len(TOPIC._elements))
        target = XSEGINT_FACTS.BoundSegInt(p_topic=TOPIC)
        PatchBlockFact = patch_class_block_fact
        block = PatchBlockFact()
        target.attach_block(block)
        target.set_fresh()
        # Test
        result = target.check()
        assert target.is_stale()
        assert block.called_update
        assert value == target._value
        assert target._status is MFACT.StatusOfFact.DEFINED
        assert result is MFACT.StatusOfFact.DEFINED

    def test_clear(self, patch_topic, patch_class_block_fact):
        """Confirm check."""
        # Setup
        SIZE = 5
        TOPIC = patch_topic(p_size_set=SIZE)
        target = XSEGINT_FACTS.BoundSegInt(p_topic=TOPIC)
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


class TestTypesSet:
    """Unit test for type alias definitions in :mod:`set_facts`."""

    def test_types(self):
        """TBD"""
        # Setup
        # Test
        # assert XSET_FACTS.IdFact is ABC_FACT.IdFact
        # assert XSET_FACTS.MemberGeneric is ABC_FACT.MemberGeneric
        #     Not testable at runtime [misc]
        assert XSEGINT_FACTS.StatusOfFact is ABC_FACT.StatusOfFact
        assert XSEGINT_FACTS.ValueAny is not None
