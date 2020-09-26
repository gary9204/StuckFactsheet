"""
Defines fact classes for a generic set.  See :mod:`.topic_set`.

.. data:: ElementOpaque

    Generic type for element of set.  See :mod:`.setindexed`.

.. data:: IndexOpaque

    Generic type for index component of set element.  See
    :mod:`.setindexed`.

.. data:: MemberOpaque

    Generic type for member component of set element.  See
    :mod:`.setindexed`.
"""
import typing

import factsheet.model.fact as MFACT
import factsheet.model.setindexed as MSET
import factsheet.content.sets.topic_set as SET

from factsheet.model.setindexed import ElementOpaque
from factsheet.model.setindexed import MemberOpaque


class ElementsSet(MFACT.Fact[SET.Set[MemberOpaque],
                             MSET.SetIndexed[MemberOpaque]]):
    """Fact that provides elements of a set topic.

    :param p_topic: set topic for fact.
    """

    def __init__(self, *, p_topic: SET.Set[MemberOpaque]) -> None:
        NAME = 'Elements'
        SUMMARY = ('{} provides the elements of set {}.'
                   ''.format(NAME, p_topic.name))
        TITLE = 'Set Elements'
        super().__init__(p_topic=p_topic)
        self.init_identity(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
        # STUB: pending topic revision

    def check(self) -> MFACT.StatusOfFact:
        """Set fact value and set corresponding state of fact check."""
        self._value = self._topic.elements
        self._status = MFACT.StatusOfFact.DEFINED
        return super().check()

    def clear(self) -> None:
        """Clear fact value and set state of fact check to unchecked."""
        self._value = None
        self._status = MFACT.StatusOfFact.UNCHECKED
        super().clear()


class SearchSet(
        MFACT.Fact[SET.Set[MemberOpaque], typing.Callable[[MemberOpaque],
                   typing.Optional[ElementOpaque[MemberOpaque]]]]):
    """Fact that provides function that returns element of a set topic
    given an object object.  The function returns None when the object
    is not a member of the set.

    :param p_topic: set topic for fact.
    """

    def __init__(self, *, p_topic: SET.Set[MemberOpaque]) -> None:
        NAME = 'Search'
        SUMMARY = ('{} provides function to find element of set {} '
                   'coresponding to given item.'.format(NAME, p_topic.name))
        TITLE = 'Find Element'
        super().__init__(p_topic=p_topic)
        self.init_identity(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
        # STUB: pending topic revision

    def check(self) -> MFACT.StatusOfFact:
        """Set fact value and set corresponding state of fact check."""
        def search(p_member: MemberOpaque
                   ) -> typing.Optional[ElementOpaque[MemberOpaque]]:
            return self._topic.elements.find_element(p_member=p_member)

        self._value = search
        self._status = MFACT.StatusOfFact.DEFINED
        return super().check()

    def clear(self: typing.Any) -> None:
        """Clear fact value and set state of fact check to unchecked."""
        self._value = None
        self._status = MFACT.StatusOfFact.UNCHECKED
        super().clear()


class SizeSet(MFACT.Fact[SET.Set[MemberOpaque], int]):
    """Fact that provides size of set topic .

    :param p_topic: set topic for fact.
    """

    def __init__(self, *, p_topic: SET.Set[MemberOpaque]) -> None:
        NAME = 'Size'
        SUMMARY = ('{} provides cardinality of set {}.'
                   ''.format(NAME, p_topic.name))
        TITLE = 'Set Size'
        super().__init__(p_topic=p_topic)
        self.init_identity(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
        # STUB: pending topic revision

    def check(self) -> MFACT.StatusOfFact:
        """Set fact value and set corresponding state of fact check."""
        self._value = len(self._topic.elements)
        self._status = MFACT.StatusOfFact.DEFINED
        return super().check()

    def clear(self) -> None:
        """Clear fact value and set state of fact check to unchecked."""
        self._value = None
        self._status = MFACT.StatusOfFact.UNCHECKED
        super().clear()
