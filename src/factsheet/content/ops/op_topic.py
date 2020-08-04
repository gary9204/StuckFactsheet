"""
Defines ancestor class for binary operation topics.
See :mod:`.topic`.
"""
import typing

from factsheet.content.sets import set_topic as XSET
from factsheet.model import element as MELEMENT
from factsheet.model import topic as MTOPIC


MemberGeneric = typing.TypeVar('MemberGeneric')
Element = MELEMENT.ElementGeneric[MemberGeneric]


class Operation(MTOPIC.Topic, typing.Generic[MemberGeneric]):
    """Defines ancestor class for binary operation topics.

    Class ``Operation`` serves as a common ancestor class for topics
    that represent binary operations on a set.  The class augments
    class :class:`~.Topic` with class :class:`~.Set`.

    :param p_name: name of operation.
    :param p_summary: summary of operation.
    :param p_title: title of operation.
    :param p_set: underlying set topic on which operation acts.
    :param kwargs: keyword arguments for superclass.
    """

    def __init__(self, *, p_name: str = '', p_summary: str = '',
                 p_title: str = '', p_set: XSET.Set[MemberGeneric],
                 **kwargs) -> None:
        super().__init__(
            p_name=p_name, p_summary=p_summary, p_title=p_title, **kwargs)
        self._set = p_set

    def _op(self, _left: Element, _right: Element) -> typing.Optional[Element]:
        """Return image of element pair under operation.

        Return None when operation is partial and element pair is not
        defined.

        :param left: lefthand operand.
        :param right: righthand operand.
        """
        return None
