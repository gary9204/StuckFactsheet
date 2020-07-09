"""
Defines class for modular addition operation topics.  See
:mod:`.opint_topic`.
"""
import typing

from factsheet.content.ops.int import opint_topic as XOP_INT
from factsheet.content.sets.int import setint_topic as XSET_INT


class PlusModN(XOP_INT.OperationInt):
    """Defines class for modular addition operation topics.

    Class ``PlusModN`` represents modular addition on a set of integers.
    The set need not contain a complete set of congruence class
    representatives, in which case, the operation may be partial.

    :param p_name: name of modular addition topic.
    :param p_summary: summary for modular addition topic.
    :param p_title: title of modular addition topic.
    :param p_set: set of integers topic.
    :param p_modulus: modulus of congruence relation.
        If modulus is not an integer greater than 1, the class
        initializer sets the modulus to a safe value and sets title to
        warn of change.
    :param kwargs: keyword arguments for superclass.

    .. admonition:: About Equality

        Two ``PlusModN`` operations are equal when they have the equal
        moduli, equal sets of integers, and equal identification
        information.
    """

    def __eq__(self, p_other: typing.Any) -> bool:
        """Return True if other is modular addition with equal
        attributes or False otherwise.

        :param p_other: object for comparison.
        """
        if not isinstance(p_other, PlusModN):
            return False

        if not super().__eq__(p_other):
            return False

        if self._modulus != p_other._modulus:
            return False

        if self._set != p_other._set:
            return False

        return True

    def __init__(self, *, p_name: str = '', p_summary: str = '',
                 p_title: str = '', p_set: XSET_INT.SetInt, p_modulus: int,
                 **kwargs) -> None:
        modulus, title = self._guard_modulus(p_modulus, p_title)
        super().__init__(p_name=p_name, p_summary=p_summary, p_title=title,
                         p_set=p_set, **kwargs)
        self._modulus = modulus
        self._reps = self._reduce_reps(p_set)

    def _guard_modulus(self, p_modulus_pre: int, p_title_pre: str
                       ) -> typing.Tuple[int, str]:
        """As needed, coerce modulus to safe value and signal change.

        :param p_modulus_pre: given modulus for congruence.
        :param p_title_pre: given title for operation topic.
        :returns:
            | (p_modulus_pre, p_title_pre) when given modulus is safe;
            | (2, warning) otherwise.
        """
        MODULUS_MIN: int = 2
        MODULUS_INVALID: int = -1

        title_post = p_title_pre
        try:
            modulus_post = int(p_modulus_pre)
        except (TypeError, ValueError):
            modulus_post = MODULUS_INVALID

        if modulus_post < MODULUS_MIN:
            modulus_post = MODULUS_MIN
            title_post = ('Plus mod 2 - given modulus was not an integer '
                          'greater than 1.')
        return modulus_post, title_post

    def _op(self, left: XSET_INT.ElementInt, right: XSET_INT.ElementInt
            ) -> typing.Optional[XSET_INT.ElementInt]:
        """Return image of element pair under operation or None.

        Return None when operation is partial and sum of pair is not
        defined.

        :param left: lefthand operand.
        :param right: righthand operand.
        """
        if (left not in self._set) or (right not in self._set):
            return None

        key = (left.member + right.member) % self._modulus
        try:
            element = self._reps[key]
        except KeyError:
            return None

        return element

    def _reduce_reps(self, p_set: XSET_INT.SetInt
                     ) -> typing.Dict[int, XSET_INT.ElementInt]:
        """Return reduced collection of congruence class representatives.

        The set may contain multiple elements from the same congruence
        class.  This method returns a map with at most one
        representative from each congruence class. If two or more
        elements belong to the same congruence class, the map includes
        only the last such element encountered.  If the set does not
        contain a complete set of congruence class representatives,
        neither will the map.  Each map key is congruent to the member
        of the corresponding element.
        """
        reps = dict()
        for element in p_set:
            key = element.member % self._modulus
            reps[key] = element
        return reps
