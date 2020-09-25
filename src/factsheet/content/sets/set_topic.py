"""
Defines ancestor class for set topics.  See :mod:`.topic`.
"""
import typing

import factsheet.model.setindexed as MSET
import factsheet.model.topic as MTOPIC

from factsheet.model.setindexed import MemberOpaque


class Set(MTOPIC.Topic, typing.Generic[MemberOpaque]):
    """Defines ancestor for set topics.

    Class ``Set`` serves as a common ancestor class for topics that
    represent sets.  The class augments class :class:`~.Topic` with
    class :class:`~.SetIndexed`.

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
        # if not isinstance(p_other, Set):
        if not isinstance(p_other, type(self)):
            return False

        if not super().__eq__(p_other):
            return False

        if self._elements != p_other._elements:
            return False

        return True

    def __init__(
            self, *,
            p_members: typing.Optional[typing.Iterable[MemberOpaque]] = None,
            **kwargs: typing.Any) -> None:
        members = p_members if p_members is not None else list()
        self._elements = MSET.SetIndexed[MemberOpaque](p_members=members)
        super().__init__(**kwargs)

    def __iter__(self) -> typing.Iterator[
            MSET.ElementOpaque[MemberOpaque]]:
        """Return iterator over indexed elements in set topic."""
        return iter(self._elements)

    @property
    def elements(self) -> MSET.SetIndexed:
        """Return elements of set."""
        return self._elements
