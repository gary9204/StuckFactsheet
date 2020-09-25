"""
Defines unit tests for fact classes for a set of integers.  See
:mod:`.setint_facts`.
"""
import pytest   # type: ignore[import]
# import typing


import factsheet.content.sets.int.setint_facts as XFACTS_SETINT
import factsheet.content.sets.int.setint_topic as XSETINT
import factsheet.content.sets.set_facts as XFACTS_SET


# @pytest.fixture
# def patch_topic():
#     """Pytest fixture returns stock topic."""
#     def new_topic(p_size_set):
#         members = list(range(p_size_set))
#         topic = XSETINT.SetInt(p_members=members)
#         return topic

#     return new_topic


class TestElementsSetInt:
    """Unit tests for :class:`.ElementsSetInt`."""

    def test_specialize(self):
        """Confirm specialization of :class:`.ElementSet`."""
        # Setup
        # Test
        assert issubclass(
            XFACTS_SETINT.ElementsSetInt, XFACTS_SET.ElementsSet)
        assert not issubclass(
            XFACTS_SET.ElementsSet, XFACTS_SETINT.ElementsSetInt)

    # def test_init(self, patch_topic):
    #     """Confirm initialization."""
    #     # Setup
    #     SIZE = 5
    #     TOPIC = patch_topic(p_size_set=SIZE)
    #     NAME = 'Elements'
    #     SUMMARY = ('{} provides the elements of set {}.'
    #                ''.format(NAME, TOPIC.name))
    #     TITLE = 'Set Elements'
    #     # Test
    #     target = XFACTS_SETINT.ElementsSetInt(p_topic=TOPIC)
    #     assert isinstance(target._infoid, MINFOID.InfoId)
    #     assert NAME == target.name
    #     assert SUMMARY == target.summary
    #     assert TITLE == target.title
    #     assert target._value is None
    #     assert target._status is MFACT.StatusOfFact.BLOCKED
    #     assert not target._stale
    #     assert isinstance(target._blocks, dict)
    #     assert not target._blocks
    #     assert target._topic.elements is TOPIC.elements

    # def test_check(self, patch_topic, patch_class_block_fact):
    #     """Confirm default check."""
    #     # Setup
    #     SIZE = 5
    #     TOPIC = patch_topic(p_size_set=SIZE)
    #     value = TOPIC._elements
    #     target = XFACTS_SETINT.ElementsSetInt(p_topic=TOPIC)
    #     PatchBlockFact = patch_class_block_fact
    #     block = PatchBlockFact()
    #     target.attach_block(block)
    #     target.set_fresh()
    #     # Test
    #     result = target.check()
    #     assert target.is_stale()
    #     assert block.called_update
    #     assert value == target._value
    #     assert target._status is MFACT.StatusOfFact.DEFINED
    #     assert result is MFACT.StatusOfFact.DEFINED

    # def test_clear(self, patch_topic, patch_class_block_fact):
    #     """Confirm default clear."""
    #     # Setup
    #     SIZE = 5
    #     TOPIC = patch_topic(p_size_set=SIZE)
    #     target = XFACTS_SETINT.ElementsSetInt(p_topic=TOPIC)
    #     target._value = 'Something completely different.'
    #     target._status = MFACT.StatusOfFact.DEFINED
    #     PatchBlockFact = patch_class_block_fact
    #     block = PatchBlockFact()
    #     target.attach_block(block)
    #     target.set_fresh()
    #     # Test
    #     target.clear()
    #     assert target.is_stale()
    #     assert block.called_update
    #     assert target._value is None
    #     assert target._status is MFACT.StatusOfFact.UNCHECKED


class TestSearchSet:
    """Unit tests for :class:`.SearchSet`."""

    # def test_init(self, patch_topic):
    #     """Confirm initialization."""
    #     # Setup
    #     SIZE = 5
    #     TOPIC = patch_topic(p_size_set=SIZE)
    #     NAME = 'Search'
    #     SUMMARY = ('{} provides function to find element of set {} '
    #                'coresponding to given item.'.format(NAME, TOPIC.name))
    #     TITLE = 'Find Element'
    #     # Test
    #     target = XFACTS_SETINT.SearchSetInt(p_topic=TOPIC)
    #     assert isinstance(target._infoid, MINFOID.InfoId)
    #     assert NAME == target.name
    #     assert SUMMARY == target.summary
    #     assert TITLE == target.title
    #     assert target._value is None
    #     assert target._status is MFACT.StatusOfFact.BLOCKED
    #     assert not target._stale
    #     assert isinstance(target._blocks, dict)
    #     assert not target._blocks
    #     assert target._topic.elements is TOPIC.elements

    # def test_check(self, patch_topic, patch_class_block_fact):
    #     """Confirm default check."""
    #     # Setup
    #     SIZE = 5
    #     TOPIC = patch_topic(p_size_set=SIZE)
    #     I_FIRST = 0
    #     value = TOPIC._elements.find_element(p_index=I_FIRST)
    #     target = XFACTS_SETINT.SearchSetInt(p_topic=TOPIC)
    #     PatchBlockFact = patch_class_block_fact
    #     block = PatchBlockFact()
    #     target.attach_block(block)
    #     target.set_fresh()
    #     # Test
    #     result = target.check()
    #     assert target.is_stale()
    #     assert block.called_update
    #     assert value == target._value
    #     assert target._status is MFACT.StatusOfFact.DEFINED
    #     assert result is MFACT.StatusOfFact.DEFINED

    # def test_clear(self, patch_topic, patch_class_block_fact):
    #     """Confirm default clear."""
    #     # Setup
    #     SIZE = 5
    #     TOPIC = patch_topic(p_size_set=SIZE)
    #     target = XFACTS_SETINT.SearchSetInt(p_topic=TOPIC)
    #     target._value = 'Something completely different.'
    #     target._status = MFACT.StatusOfFact.DEFINED
    #     PatchBlockFact = patch_class_block_fact
    #     block = PatchBlockFact()
    #     target.attach_block(block)
    #     target.set_fresh()
    #     # Test
    #     target.clear()
    #     assert target.is_stale()
    #     assert block.called_update
    #     assert target._value is None
    #     assert target._status is MFACT.StatusOfFact.UNCHECKED


class TestSizeSet:
    """Unit tests for :class:`.SizeSet`."""

    # def test_init(self, patch_topic):
    #     """Confirm initialization."""
    #     # Setup
    #     SIZE = 5
    #     TOPIC = patch_topic(p_size_set=SIZE)
    #     NAME = 'Size'
    #     SUMMARY = ('{} provides cardinality of set {}.'
    #                ''.format(NAME, TOPIC.name))
    #     TITLE = 'Set Size'
    #     # Test
    #     target = XFACTS_SETINT.SizeSet(p_topic=TOPIC)
    #     assert isinstance(target._infoid, MINFOID.InfoId)
    #     assert NAME == target.name
    #     assert SUMMARY == target.summary
    #     assert TITLE == target.title
    #     assert target._value is None
    #     assert target._status is MFACT.StatusOfFact.BLOCKED
    #     assert not target._stale
    #     assert isinstance(target._blocks, dict)
    #     assert not target._blocks
    #     assert target._topic.elements is TOPIC.elements

    # def test_check(self, patch_topic, patch_class_block_fact):
    #     """Confirm default check."""
    #     # Setup
    #     SIZE = 5
    #     TOPIC = patch_topic(p_size_set=SIZE)
    #     value = len(TOPIC._elements)
    #     target = XFACTS_SETINT.SizeSet(p_topic=TOPIC)
    #     PatchBlockFact = patch_class_block_fact
    #     block = PatchBlockFact()
    #     target.attach_block(block)
    #     target.set_fresh()
    #     # Test
    #     result = target.check()
    #     assert target.is_stale()
    #     assert block.called_update
    #     assert value == target._value
    #     assert target._status is MFACT.StatusOfFact.DEFINED
    #     assert result is MFACT.StatusOfFact.DEFINED

    # def test_clear(self, patch_topic, patch_class_block_fact):
    #     """Confirm default clear."""
    #     # Setup
    #     SIZE = 5
    #     TOPIC = patch_topic(p_size_set=SIZE)
    #     target = XFACTS_SETINT.SizeSet(p_topic=TOPIC)
    #     target._status = MFACT.StatusOfFact.DEFINED
    #     PatchBlockFact = patch_class_block_fact
    #     block = PatchBlockFact()
    #     target.attach_block(block)
    #     target.set_fresh()
    #     # Test
    #     target.clear()
    #     assert target.is_stale()
    #     assert block.called_update
    #     assert target._value is None
    #     assert target._status is MFACT.StatusOfFact.UNCHECKED


# class TestTypesSet:
#     """Unit test for type alias definitions in :mod:`set_facts`."""

    # def test_types(self):
    #     """TBD"""
    #     # Setup
    #     # Test
    #     # assert XFACTS_SETINT.IdFact is ABC_FACT.IdFact
    #     # assert XFACTS_SETINT.MemberOpaque is ABC_FACT.MemberOpaque
    #     #     Not testable at runtime [misc]
    #     assert XFACTS_SETINT.StatusOfFact is ABC_FACT.StatusOfFact
    #     assert XFACTS_SETINT.ValueAny is not None
