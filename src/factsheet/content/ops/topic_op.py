"""
Defines ancestor class for binary operation topics.
See :mod:`.topic`.
"""
import typing

import factsheet.content.sets.topic_set as XSET
import factsheet.model.topic as MTOPIC


from factsheet.model.element import MemberOpaque
from factsheet.model.element import ElementOpaque
Element = ElementOpaque[MemberOpaque]


class Operation(MTOPIC.Topic, typing.Generic[MemberOpaque]):
    """Defines ancestor class for binary operation topics.

    Class ``Operation`` serves as a common ancestor class for topics
    that represent binary operations on a set.  The class augments
    class :class:`~.Topic` with class :class:`~.Set`.

    :param p_set: underlying set topic on which operation acts.
    :param kwargs: keyword arguments for superclass.
    """

    def __eq__(self, p_other: typing.Any) -> bool:
        """Return True if other is modular addition with equal
        attributes or False otherwise.

        :param p_other: object for comparison.
        """
        if not super().__eq__(p_other):
            return False

        if self._set_op != p_other._set_op:
            return False

        return True

    def __init__(self, *, p_set: XSET.Set[MemberOpaque], **kwargs) -> None:
        super().__init__(**kwargs)
        self._set_op = p_set

    def op(self, _left: Element, _right: Element) -> typing.Optional[Element]:
        """Return image of element pair under operation.

        Return None when operation is partial and element pair is not
        defined.

        :param left: lefthand operand.
        :param right: righthand operand.
        """
        return None

    @property
    def set_op(self) -> XSET.Set[MemberOpaque]:
        """Return topic set."""
        return self._set_op
