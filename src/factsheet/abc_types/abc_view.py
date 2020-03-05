"""
Defines abstract data type classes for :mod:`factsheet.view` classes.

.. data:: AbstractTextView

    Abstract type that represents display of a text attribute such as a
    factsheet name or summary.
"""
import typing

from factsheet.adapt_gtk import adapt_view as AVIEW


AbstractTextView = typing.TypeVar(
    'AbstractTextView', AVIEW.AdaptEntry, AVIEW.AdaptTextView)
