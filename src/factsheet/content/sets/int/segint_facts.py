"""
Defines fact classes for a generic set.  See :mod:`.set_topic`.

..
    data:: IdFact

    Type for fact identifiers.  Defined in :mod:`.abc_fact`.

..
    data:: MemberGeneric

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
# from factsheet.model import setindexed as MSET
from factsheet.content.sets.int import segint_topic as XSEGINT


# from factsheet.model.fact import IdFact
from factsheet.abc_types.abc_fact import StatusOfFact
# from factsheet.model.element import IndexElement
# from factsheet.model.setindexed import MemberGeneric
ValueAny = typing.TypeVar('ValueAny')
# from factsheet.model.fact import ValueOfFact


class BoundSegInt(MFACT.Fact):
    """Fact that provides upper bound of initial segment topic.

    :param p_topic: initial segment of natural numbers topic for fact.
    """

    def __init__(self, *, p_topic: XSEGINT.SegInt) -> None:
        NAME = 'Bound'
        SUMMARY = ('{} provides upper bound of {}, an initial segment of '
                   'natural numbers.'.format(NAME, p_topic.name))
        TITLE = 'Segment Upper Bound'
        super().__init__(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
        # STUB: pending topic revision
        self._bound = len(p_topic._elements)

    def check(self, **_kwargs: typing.Any) -> MFACT.StatusOfFact:
        """Set fact value and set corresponding state of fact check."""
        self._value = str(self._bound)
        self._status = StatusOfFact.DEFINED
        return super().check()

    def clear(self, **_kwargs: typing.Any) -> None:
        """Clear fact value and set state of fact check to unchecked."""
        self._value = None
        self._status = StatusOfFact.UNCHECKED
        super().clear()
