"""
Defines fact classes for a generic set.  See :mod:`.set_topic`.
"""
import factsheet.content.sets.int.segint_topic as XSEGINT
import factsheet.model.fact as MFACT


class BoundSegInt(MFACT.Fact[XSEGINT.SegInt, int]):
    """Fact that provides upper bound of initial segment topic.

    :param p_topic: initial segment of natural numbers topic for fact.
    """

    def __init__(self, *, p_topic: XSEGINT.SegInt) -> None:
        super().__init__(p_topic=p_topic)
        self._bound = len(p_topic.elements)
        NAME = 'Bound'
        SUMMARY = ('{} provides upper bound of {}, an initial segment of '
                   'natural numbers.'.format(NAME, p_topic.name))
        TITLE = 'Segment Upper Bound'
        self.init_identity(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
        # STUB: pending topic revision

    def check(self) -> MFACT.StatusOfFact:
        """Set fact value and set corresponding state of fact check."""
        self._value = self._bound
        self._status = MFACT.StatusOfFact.DEFINED
        return super().check()

    def clear(self) -> None:
        """Clear fact value and set state of fact check to unchecked."""
        self._value = None
        self._status = MFACT.StatusOfFact.UNCHECKED
        super().clear()
