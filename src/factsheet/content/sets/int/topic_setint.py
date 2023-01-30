"""
Defines class for set of integers topics.  See :mod:`.topic_set`.
"""
import factsheet.content.sets .topic_set as XSET

from factsheet.model.element import ElementOpaque


ElementInt = ElementOpaque[int]


class SetInt(XSET.Set[int]):
    """Defines set of integers topic.

    Class ``SetInt`` serves as a common ancestor for classes that
    represent sets of integers.  The class specializes :class:`~.Set` to
    integers.
    """

    pass

    # def __init__(self, **kwargs: typing.Any) -> None:
    #     super().__init__(**kwargs)
    #     NAME = 'SetInt'
    #     SUMMARY = 'This topic represents a set of integers.'
    #     TITLE = 'Integer Set'
    #     self.init_identity(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
