"""
Defines class for modular addition operation topics.  See
:mod:`.opint_topic`.
"""
import typing

import factsheet.content.ops.int.opint_topic as XOPINT
import factsheet.content.sets.int.setint_topic as XSETINT

from factsheet.content.sets.int.setint_topic import ElementInt


class PlusModN(XOPINT.OperationInt):
    """Defines class for modular addition operation topics.

    Class ``PlusModN`` represents modular addition on a set of integers.
    The set need not contain a complete set of congruence class
    representatives, in which case, the operation may be partial.

    :param p_set: set of integers topic.
    :param p_modulus: modulus of congruence relation.
        If modulus is not an integer greater than 1, the class
        initializer sets the modulus to a safe value.
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
        if not super().__eq__(p_other):
            return False

        if self._modulus != p_other._modulus:
            return False

        return True

    def __init__(self, *, p_set: XSETINT.SetInt, p_modulus: int,
                 **kwargs) -> None:
        super().__init__(p_set=p_set, **kwargs)
        MODULUS_MIN = 2
        try:
            self._modulus = int(p_modulus)
        except (TypeError, ValueError):
            self._modulus = MODULUS_MIN
        if self._modulus < MODULUS_MIN:
            self._modulus = MODULUS_MIN
        self._reps = self._reduce_reps(p_set)

    def _op(self, left: ElementInt, right: ElementInt
            ) -> typing.Optional[ElementInt]:
        """Return image of element pair under operation or None.

        Return None when operation is partial and sum of pair is not
        defined.

        :param left: lefthand operand.
        :param right: righthand operand.
        """
        if (left not in self._set_op) or (right not in self._set_op):
            return None

        key = (left.member + right.member) % self._modulus
        try:
            element = self._reps[key]
        except KeyError:
            return None

        return element

    def _reduce_reps(self, p_set: XSETINT.SetInt
                     ) -> typing.Dict[int, ElementInt]:
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
