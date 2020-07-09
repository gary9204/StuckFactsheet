"""
Defines ancestor topic class binary operation on a set of integers.  See
:mod:`.op_topic`.
"""
import typing   # noqa

from factsheet.content.ops import op_topic as XOP


class OperationInt(XOP.Operation[int]):
    """Defines ancestor topic class for binary operation on a set of
    integers.

    Class ``OperationInt`` serves as a common ancestor for classes that
    represent binary operations on sets of integers.  The class
    specializes :class:`~.Operation` to integers.
    """

    pass
