"""
Defines class for set of integers topics.  See :mod:`.set_topic`.
"""
from factsheet.content.sets import set_topic as XSET
from factsheet.model import element as MELEMENT


ElementInt = MELEMENT.ElementGeneric[int]


class SetInt(XSET.Set[int]):
    """Defines class for set of integers topics.

    Class ``SetInt`` serves as a common ancestor for classes that
    represent sets of integers.  The class specializes :class:`~.Set` to
    integers.
    """

    pass
