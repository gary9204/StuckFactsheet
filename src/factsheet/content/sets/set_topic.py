"""
Defines ancestor topic class for sets.  See :mod:`.topic`.
"""
from factsheet.model import topic as MTOPIC


class Set(MTOPIC.Topic):
    """Defines ancestor topic class for sets.

    Class ``Set`` serves as a common ancestor for classes that represent
    mathematical sets.  The class itself has no content nor does it add
    features to :class:`~.Topic`.

    :param p_name: name of set.
    :param p_summary: summary of set.
    :param p_title: title of set.
    """

    def __init__(self, *, p_name: str = '', p_summary: str = '',
                 p_title: str = '') -> None:
        super().__init__(p_name=p_name, p_summary=p_summary, p_title=p_title)
