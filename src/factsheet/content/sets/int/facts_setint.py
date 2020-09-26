"""
Defines fact classes for a set of integers.  See :mod:`.topic_setint`.
"""
import factsheet.content.sets.facts_set as XFACTS_SET


class ElementsSetInt(XFACTS_SET.ElementsSet[int]):
    """Fact that provides elements of an integer set topic.

    :param p_topic: set topic for fact.
    """

    pass

    # def __init__(self, *, p_topic: SETINT.SetInt) -> None:
    #     super().__init__(p_topic=p_topic)
    #     NAME = 'Elements'
    #     SUMMARY = ('{} provides the elements of set {}.'
    #                ''.format(NAME, p_topic.name))
    #     TITLE = 'Set Elements'
    #     self.init_identity(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
    #     # STUB: pending topic revision

    # def check(self) -> MFACT.StatusOfFact:
    #     """Set fact value and set corresponding state of fact check."""
    #     self._value = self._topic.elements
    #     self._status = StatusOfFact.DEFINED
    #     return super().check()

    # def clear(self) -> None:
    #     """Clear fact value and set state of fact check to unchecked."""
    #     self._value = None
    #     self._status = StatusOfFact.UNCHECKED
    #     super().clear()


class SearchSetInt(XFACTS_SET.SearchSet[int]):
    """Fact that provides element of a set topic corresponding to given
    object.

    :param p_topic: set topic for fact.
    """

    pass

    # def __init__(self, *, p_topic: SETINT.SetInt) -> None:
    #     super().__init__(p_topic=p_topic)
    #     NAME = 'Search'
    #     SUMMARY = ('{} provides function to find element of set {} '
    #                'coresponding to given item.'.format(NAME, p_topic.name))
    #     TITLE = 'Find Element'
    #     self.init_identity(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
    #     # STUB: pending topic revision

    # def check(self) -> MFACT.StatusOfFact:
    #     """Set fact value and set corresponding state of fact check."""
    #     self._value = self._topic.elements.find_element(
    #         p_index=IndexElement(0))
    #     self._status = StatusOfFact.DEFINED
    #     return super().check()

    # def clear(self: typing.Any) -> None:
    #     """Clear fact value and set state of fact check to unchecked."""
    #     self._value = None
    #     self._status = StatusOfFact.UNCHECKED
    #     super().clear()


class SizeSet(XFACTS_SET.SizeSet[int]):
    """Fact that provides size of set topic .

    :param p_topic: set topic for fact.
    """

    pass

    # def __init__(self, *, p_topic: SETINT.SetInt) -> None:
    #     super().__init__(p_topic=p_topic)
    #     NAME = 'Size'
    #     SUMMARY = ('{} provides cardinality of set {}.'
    #                ''.format(NAME, p_topic.name))
    #     TITLE = 'Set Size'
    #     self.init_identity(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
    #     # STUB: pending topic revision

    # def check(self) -> MFACT.StatusOfFact:
    #     """Set fact value and set corresponding state of fact check."""
    #     self._value = len(self._topic.elements)
    #     self._status = StatusOfFact.DEFINED
    #     return super().check()

    # def clear(self) -> None:
    #     """Clear fact value and set state of fact check to unchecked."""
    #     self._value = None
    #     self._status = StatusOfFact.UNCHECKED
    #     super().clear()
