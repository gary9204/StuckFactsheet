"""
Defines unit tests for fact classes for a generic set.  See
:mod:`.set_fact`.
"""
import dataclasses as DC
import pytest   # type: ignore[import]
# import typing


from factsheet.abc_types import abc_fact as ABC_FACT
from factsheet.content.sets import set_facts as XSET_FACTS
from factsheet.content.sets import set_topic as XSET
# from factsheet.model import element as MELEMENT
# from factsheet.model import setindexed as MSET
from factsheet.model import fact as MFACT
from factsheet.model import infoid as MINFOID
from factsheet.model import setindexed as MSET


@pytest.fixture
def patch_elements():
    """TBD"""
    SIZE = 5
    elements = MSET.SetIndexed[int](p_members=list(range(SIZE)))
    return elements


@pytest.fixture
def patch_topic():
    """TBD"""
    def new_topic(p_size_set):
        members = list(range(p_size_set))
        NAME = 'Parrots'
        SUMMARY = 'This topic is a lovely collection of parrots.'
        TITLE = 'Parrot Shop'
        topic = XSET.Set(
            p_name=NAME, p_summary=SUMMARY, p_title=TITLE, p_members=members)
        return topic

    return new_topic


class TestElementsSet:
    """Unit tests for :class:`.ElementsSet`."""

    def test_init(self, patch_topic):
        """Confirm initialization."""
        # Setup
        SIZE = 5
        TOPIC = patch_topic(p_size_set=SIZE)
        NAME = 'Elements'
        SUMMARY = ('{} provides the elements of set {}.'
                   ''.format(NAME, TOPIC.name))
        TITLE = 'Set Elements'
        # Test
        target = XSET_FACTS.ElementsSet(p_topic=TOPIC)
        assert isinstance(target._infoid, MINFOID.InfoId)
        assert NAME == target.name
        assert SUMMARY == target.summary
        assert TITLE == target.title
        assert target._value is None
        assert target._status is MFACT.StatusOfFact.BLOCKED
        assert not target._stale
        assert isinstance(target._blocks, dict)
        assert not target._blocks
        assert target._elements is TOPIC._elements

    def test_check(self, patch_topic, patch_class_block_fact):
        """Confirm default check."""
        # Setup
        SIZE = 5
        TOPIC = patch_topic(p_size_set=SIZE)
        value = str(TOPIC._elements)
        target = XSET_FACTS.ElementsSet(p_topic=TOPIC)
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
        """Confirm default check."""
        # Setup
        SIZE = 5
        TOPIC = patch_topic(p_size_set=SIZE)
        target = XSET_FACTS.ElementsSet(p_topic=TOPIC)
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


class TestSearchSet:
    """Unit tests for :class:`.SearchSet`."""

    def test_init(self, patch_topic):
        """Confirm initialization."""
        # Setup
        SIZE = 5
        TOPIC = patch_topic(p_size_set=SIZE)
        NAME = 'Search'
        SUMMARY = ('{} provides function to find element of set {} '
                   'coresponding to given item.'.format(NAME, TOPIC.name))
        TITLE = 'Find Element'
        # Test
        target = XSET_FACTS.SearchSet(p_topic=TOPIC)
        assert isinstance(target._infoid, MINFOID.InfoId)
        assert NAME == target.name
        assert SUMMARY == target.summary
        assert TITLE == target.title
        assert target._value is None
        assert target._status is MFACT.StatusOfFact.BLOCKED
        assert not target._stale
        assert isinstance(target._blocks, dict)
        assert not target._blocks
        assert target._elements is TOPIC._elements

    def test_check(self, patch_topic, patch_class_block_fact):
        """Confirm default check."""
        # Setup
        SIZE = 5
        TOPIC = patch_topic(p_size_set=SIZE)
        I_FIRST = 0
        value = TOPIC._elements.find_element(p_index=I_FIRST)
        target = XSET_FACTS.SearchSet(p_topic=TOPIC)
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
        """Confirm default check."""
        # Setup
        SIZE = 5
        TOPIC = patch_topic(p_size_set=SIZE)
        target = XSET_FACTS.SearchSet(p_topic=TOPIC)
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


class TestSizeSet:
    """Unit tests for :class:`.SizeSet`."""

    def test_init(self, patch_topic):
        """Confirm initialization."""
        # Setup
        SIZE = 5
        TOPIC = patch_topic(p_size_set=SIZE)
        NAME = 'Size'
        SUMMARY = ('{} provides cardinality of set {}.'
                   ''.format(NAME, TOPIC.name))
        TITLE = 'Set Size'
        # Test
        target = XSET_FACTS.SizeSet(p_topic=TOPIC)
        assert isinstance(target._infoid, MINFOID.InfoId)
        assert NAME == target.name
        assert SUMMARY == target.summary
        assert TITLE == target.title
        assert target._value is None
        assert target._status is MFACT.StatusOfFact.BLOCKED
        assert not target._stale
        assert isinstance(target._blocks, dict)
        assert not target._blocks
        assert target._elements is TOPIC._elements

    def test_check(self, patch_topic, patch_class_block_fact):
        """Confirm default check."""
        # Setup
        SIZE = 5
        TOPIC = patch_topic(p_size_set=SIZE)
        value = len(TOPIC._elements)
        target = XSET_FACTS.SizeSet(p_topic=TOPIC)
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
        """Confirm default check."""
        # Setup
        SIZE = 5
        TOPIC = patch_topic(p_size_set=SIZE)
        target = XSET_FACTS.SizeSet(p_topic=TOPIC)
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
        assert XSET_FACTS.StatusOfFact is ABC_FACT.StatusOfFact
        assert XSET_FACTS.ValueAny is not None
