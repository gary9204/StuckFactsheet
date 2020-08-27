"""
Defines fact classes for a generic set.  See :mod:`.set_topic`.

.. attribute:: StatusOfFact

Indicates whether user has checked fact and outcome of check.  See
:mod:`.abc_fact`.

..
    data:: IdFact

    Type for fact identifiers.  Defined in :mod:`.abc_fact`.

.. data:: MemberGeneric

    Generic type for member component of set element.  Defined in
    :mod:`.setindexed`.

.. data:: StatusOfFact

    Indicates whether user has checked fact and outcome of check.
    Defined in :mod:`.abc_fact`.

..
    data:: ValueOfFact

    Type for fact value including fact status.  Defined in
    :mod:`.abc_fact`.
"""
import typing

from factsheet.model import fact as MFACT
from factsheet.model import setindexed as MSET


# from factsheet.model.fact import IdFact
from factsheet.abc_types.abc_fact import StatusOfFact
from factsheet.content.sets import set_topic as XSET
from factsheet.model.element import IndexElement
from factsheet.model.setindexed import MemberGeneric
ValueAny = typing.TypeVar('ValueAny')
# from factsheet.model.fact import ValueOfFact


class ElementsSet(MFACT.Fact, typing.Generic[MemberGeneric, ValueAny]):
    """Fact that provides elements of a set topic.

    :param p_topic: set topic for fact.
    """

    def __init__(self, *, p_topic: XSET.Set) -> None:
        NAME = 'Elements'
        SUMMARY = ('{} provides the elements of set {}.'
                   ''.format(NAME, p_topic.name))
        TITLE = 'Set Elements'
        super().__init__(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
        # STUB: pending topic revision
        self._elements = p_topic._elements

    def check(self, **_kwargs: typing.Any) -> MFACT.StatusOfFact:
        """Set fact value and set corresponding state of fact check."""
        self._value = str(self._elements)
        self._status = StatusOfFact.DEFINED
        return super().check()

    def clear(self, **_kwargs: typing.Any) -> None:
        """Clear fact value and set state of fact check to unchecked."""
        self._value = None
        self._status = StatusOfFact.UNCHECKED
        super().clear()


class SearchSet(MFACT.Fact, typing.Generic[MemberGeneric, ValueAny]):
    """Fact that provides element of a set topic corresponding to given
    object.

    :param p_topic: set topic for fact.
    """

    def __init__(self, *, p_topic: XSET.Set) -> None:
        NAME = 'Search'
        SUMMARY = ('{} provides function to find element of set {} '
                   'coresponding to given item.'.format(NAME, p_topic.name))
        TITLE = 'Find Element'
        super().__init__(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
        # STUB: pending topic revision
        self._elements = p_topic._elements

    def check(self, **_kwargs: typing.Any) -> MFACT.StatusOfFact:
        """Set fact value and set corresponding state of fact check."""
        self._value = self._elements.find_element(p_index=IndexElement(0))
        self._status = StatusOfFact.DEFINED
        return super().check()

    def clear(self, **_kwargs: typing.Any) -> None:
        """Clear fact value and set state of fact check to unchecked."""
        self._value = None
        self._status = StatusOfFact.UNCHECKED
        super().clear()


class SizeSet(MFACT.Fact, typing.Generic[MemberGeneric, ValueAny]):
    """Fact that provides size of set topic .

    :param p_topic: set topic for fact.
    """

    def __init__(self, *, p_topic: XSET.Set) -> None:
        NAME = 'Size'
        SUMMARY = ('{} provides cardinality of set {}.'
                   ''.format(NAME, p_topic.name))
        TITLE = 'Set Size'
        super().__init__(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
        # STUB: pending topic revision
        self._elements = p_topic._elements

    def check(self, **_kwargs: typing.Any) -> MFACT.StatusOfFact:
        """Set fact value and set corresponding state of fact check."""
        self._value = len(self._elements)
        self._status = StatusOfFact.DEFINED
        return super().check()

    def clear(self, **_kwargs: typing.Any) -> None:
        """Clear fact value and set state of fact check to unchecked."""
        self._value = None
        self._status = StatusOfFact.UNCHECKED
        super().clear()
