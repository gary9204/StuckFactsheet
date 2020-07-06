"""
Defines ancestor topic class for set of integers.  See
:mod:`.set_topic`.
"""
from factsheet.content.sets import set_topic as XSET
from factsheet.model import setindexed as MSET


class SetInt(XSET.Set):
    """Defines ancestor topic class for sets of integers.

    Class ``SetInt`` serves as a common ancestor for classes that
    represent sets of integers.  The class provides an empty set (of
    integers) as default content.  It does not add any features to
    :class:`~.Set`.

    :param p_name: name of set of integers.
    :param p_summary: summary of set of integers.
    :param p_title: title of set of integers.
    """

    def __init__(self, *, p_name: str = '', p_summary: str = '',
                 p_title: str = '') -> None:
        super().__init__(p_name=p_name, p_summary=p_summary, p_title=p_title)
        self._scope = MSET.SetIndexed[int]()
