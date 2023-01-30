"""
Defines class for initial segment of natural numbers topics.  See
:mod:`.topic_setint`.
"""
import factsheet.content.sets.int.topic_setint as XSETINT


class SegInt(XSETINT.SetInt):
    """Defines topic for initial segment of integers.

    Class ``SegInt`` represents sets of nautral numbers of the form
    [0, `k`) for `k` a positive integer.

    :param p_bound: upper bound for segment. Default is 1.
    :param kwargs: keyword arguments for superclass.

    .. admonition:: About Equality

        Two initial segments are equal when they have equal
        identification information and equal indexed sets.
    """

    def __init__(self, *, p_bound: int = 1, **kwargs) -> None:
        BOUND_MIN: int = 1
        try:
            bound = int(p_bound)
        except (TypeError, ValueError):
            bound = BOUND_MIN
        if bound < BOUND_MIN:
            bound = BOUND_MIN

        members = range(bound)
        super().__init__(p_members=members, **kwargs)
