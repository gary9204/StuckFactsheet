"""
Defines unit tests for fact classes for a generic set.  See
:mod:`.set_fact`.
"""
import pytest   # type: ignore[import]
import types

from factsheet.content.sets import set_facts as XFACTS_SET
from factsheet.content.sets import set_topic as XSET
from factsheet.model import fact as MFACT
from factsheet.model import infoid as MINFOID
from factsheet.model import setindexed as MSET


@pytest.fixture
def patch_topic():
    """Pytest fixture returns stock topic."""
    def new_topic(p_size_set):
        members = list(range(p_size_set))
        topic = XSET.Set(p_members=members)
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
        target = XFACTS_SET.ElementsSet(p_topic=TOPIC)
        assert isinstance(target._infoid, MINFOID.InfoId)
        assert NAME == target.name
        assert SUMMARY == target.summary
        assert TITLE == target.title
        assert target._value is None
        assert target._status is MFACT.StatusOfFact.BLOCKED
        assert not target._stale
        assert isinstance(target._blocks, dict)
        assert not target._blocks
        assert target._topic.elements is TOPIC.elements

    def test_check(self, patch_topic, patch_class_block_fact):
        """Confirm default check."""
        # Setup
        SIZE = 5
        TOPIC = patch_topic(p_size_set=SIZE)
        value = TOPIC._elements
        target = XFACTS_SET.ElementsSet(p_topic=TOPIC)
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
        """Confirm default clear."""
        # Setup
        SIZE = 5
        TOPIC = patch_topic(p_size_set=SIZE)
        target = XFACTS_SET.ElementsSet(p_topic=TOPIC)
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
        target = XFACTS_SET.SearchSet(p_topic=TOPIC)
        assert isinstance(target._infoid, MINFOID.InfoId)
        assert NAME == target.name
        assert SUMMARY == target.summary
        assert TITLE == target.title
        assert target._value is None
        assert target._status is MFACT.StatusOfFact.BLOCKED
        assert not target._stale
        assert isinstance(target._blocks, dict)
        assert not target._blocks
        assert target._topic.elements is TOPIC.elements

    def test_check(self, patch_topic, patch_class_block_fact):
        """Confirm default check."""
        # Setup
        SIZE = 5
        TOPIC = patch_topic(p_size_set=SIZE)
        MEMBER = 3
        NONMEMBER = 'Parrot'
        value = TOPIC._elements.find_element
        target = XFACTS_SET.SearchSet(p_topic=TOPIC)
        PatchBlockFact = patch_class_block_fact
        block = PatchBlockFact()
        target.attach_block(block)
        target.set_fresh()
        # Test
        result = target.check()
        assert target.is_stale()
        assert block.called_update
        assert isinstance(target._value, types.FunctionType)
        assert value(p_member=MEMBER) == target._value(MEMBER)
        assert target._value(NONMEMBER) is None
        assert target._status is MFACT.StatusOfFact.DEFINED
        assert result is MFACT.StatusOfFact.DEFINED

    def test_clear(self, patch_topic, patch_class_block_fact):
        """Confirm default clear."""
        # Setup
        SIZE = 5
        TOPIC = patch_topic(p_size_set=SIZE)
        target = XFACTS_SET.SearchSet(p_topic=TOPIC)
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
        target = XFACTS_SET.SizeSet(p_topic=TOPIC)
        assert isinstance(target._infoid, MINFOID.InfoId)
        assert NAME == target.name
        assert SUMMARY == target.summary
        assert TITLE == target.title
        assert target._value is None
        assert target._status is MFACT.StatusOfFact.BLOCKED
        assert not target._stale
        assert isinstance(target._blocks, dict)
        assert not target._blocks
        assert target._topic.elements is TOPIC.elements

    def test_check(self, patch_topic, patch_class_block_fact):
        """Confirm default check."""
        # Setup
        SIZE = 5
        TOPIC = patch_topic(p_size_set=SIZE)
        value = len(TOPIC._elements)
        target = XFACTS_SET.SizeSet(p_topic=TOPIC)
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
        """Confirm default clear."""
        # Setup
        SIZE = 5
        TOPIC = patch_topic(p_size_set=SIZE)
        target = XFACTS_SET.SizeSet(p_topic=TOPIC)
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
    """Unit test for type definitions in :mod:`set_facts`."""

    def test_types(self):
        """Confirm local copies of type hints."""
        # Setup
        # Test
        assert XFACTS_SET.ElementOpaque is MSET.ElementOpaque
        assert XFACTS_SET.MemberOpaque is MSET.MemberOpaque
