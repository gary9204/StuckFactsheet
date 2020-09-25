"""
Defines fact classes for a generic operation.  See :mod:`.op_topic`.

.. data:: MemberOpaque

    Generic type for member component of set element.  See
    :mod:`.setindexed`.
"""
import factsheet.content.ops.op_topic as OP
import factsheet.model.fact as MFACT

from factsheet.model.setindexed import MemberOpaque


class Closed(MFACT.Fact[OP.Operation[MemberOpaque], bool]):
    """Fact that an operation topic is closed on its set.

    :param p_topic: operation topic for fact.
    """

    def __init__(self, *, p_topic: OP.Operation[MemberOpaque]) -> None:
        super().__init__(p_topic=p_topic)
        NAME = 'Closed'
        SUMMARY = ('{} is True when {}\'s set is closed under the operation.'
                   ''.format(NAME, self._topic.name))
        TITLE = '{} Is Closed'.format(self._topic.name)
        self.init_identity(p_name=NAME, p_summary=SUMMARY, p_title=TITLE)
        self._op = self._topic.op
        self._set_op = self._topic.set_op
        # STUB: pending topic revision

    def check(self) -> MFACT.StatusOfFact:
        """Set fact value and set corresponding state of fact check."""
        self._value = True
        for a in self._set_op:
            for b in self._set_op:
                if self._op(a, b) is None:
                    self._value = False
                    break
            if not self._value:
                break

        self._status = MFACT.StatusOfFact.DEFINED
        return super().check()

    def clear(self) -> None:
        """Clear fact value and set state of fact check to unchecked."""
        self._value = None
        self._status = MFACT.StatusOfFact.UNCHECKED
        super().clear()
