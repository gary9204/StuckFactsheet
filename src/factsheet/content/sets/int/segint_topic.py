"""
Defines topic class for initial segment of natural numbers.  See
:mod:`.setint_topic`.
"""
import typing

from factsheet.content.sets.int import setint_topic as XSETINT
from factsheet.model import setindexed as MSET


class SegInt(XSETINT.SetInt):
    """Defines topic class for initial segment of integers.

    Class ``SegInt`` represents sets of nautral numbers of the form
    [0, `k`) for `k` a positive integer.

    :param p_name: name of segment.
    :param p_summary: summary for segment.
    :param p_title: title of segment.
    :param p_bound: upper bound for segment. Default is 1.

    .. admonition:: About Equality

        Two initial segments are equal when they have equal
        identification information and equal indexed sets.
    """

    def __eq__(self, p_other: typing.Any) -> bool:
        """Return True if other is initial segment with equal attributes,
        or False otherwise.

        :param p_other: object for comparison.
        """
        if not isinstance(p_other, SegInt):
            return False

        if not super().__eq__(p_other):
            return False

        if self._scope != p_other._scope:
            return False

        return True

    def __init__(self, *, p_name: str = '', p_summary: str = '',
                 p_title: str = '', p_bound: int = 1) -> None:
        bound, title = self.guard_bound(p_bound, p_title)
        super().__init__(p_name=p_name, p_summary=p_summary, p_title=title)
        self._scope = MSET.SetIndexed[int](range(bound))

    def guard_bound(self, p_bound_raw: int, p_title_raw: str
                    ) -> typing.Tuple[int, str]:
        """As needed, coerce bound to safe value and signal change.

        If bound is not a positive integer, set the bound to 1 and
        set title to warn of change.

        :param p_bound_raw: given upper bound.
        :param p_title_raw: given title for set.
        :returns:
            | (p_bound_raw, p_title_raw) when bound is a positive integer;
            | (1, warning) otherwise.
        """
        BOUND_MIN: int = 1
        BOUND_INVALID: int = -1

        title_new = p_title_raw
        try:
            bound_new = int(p_bound_raw)
        except (TypeError, ValueError):
            bound_new = BOUND_INVALID

        if bound_new < BOUND_MIN:
            bound_new = BOUND_MIN
            title_new = 'N(1) - given bound was not a positive integer.'
        return bound_new, title_new
