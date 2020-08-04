"""
Defines ancestor class for set topics.  See :mod:`.topic`.
"""
import typing

from factsheet.model import element as MELEMENT
from factsheet.model import setindexed as MSET
from factsheet.model import topic as MTOPIC

MemberGeneric = typing.TypeVar('MemberGeneric')


class Set(MTOPIC.Topic, typing.Generic[MemberGeneric]):
    """Defines ancestor class for set topics.

    Class ``Set`` serves as a common ancestor class for topics that
    represent sets.  The class augments class :class:`~.Topic` with
    class :class:`~.SetIndexed`.

    :param p_name: name of set topic.
    :param p_summary: summary of set topic.
    :param p_title: title of set topic.
    :param p_members: members for topic's set.
    :param kwargs: keyword arguments for superclass.

    .. admonition:: About Equality

        Two set topics are equal when they have equal identification
        information and equal indexed sets of elements.
    """

    def __contains__(self, p_other: typing.Any) -> bool:
        """Return True when object is indexed element in set topic.

        :param p_other: object to test.
        """
        return p_other in self._elements

    def __eq__(self, p_other: typing.Any) -> bool:
        """Return True if other is set topic with same attributes, or
        False otherwise.

        :param p_other: object to test for equality.
        """
        if not isinstance(p_other, Set):
            return False

        if not super().__eq__(p_other):
            return False

        if self._elements != p_other._elements:
            return False

        return True

    def __init__(
            self, *, p_name: str = '', p_summary: str = '', p_title: str = '',
            p_members: typing.Optional[typing.Iterable[MemberGeneric]] = None,
            **kwargs: typing.Dict) -> None:
        super().__init__(
            p_name=p_name, p_summary=p_summary, p_title=p_title, **kwargs)
        members = p_members if p_members is not None else list()
        self._elements = MSET.SetIndexed[MemberGeneric](p_members=members)

    def __iter__(self) -> typing.Iterator[
            MELEMENT.ElementGeneric[MemberGeneric]]:
        """Return iterator over indexed elements in set topic."""
        return iter(self._elements)
