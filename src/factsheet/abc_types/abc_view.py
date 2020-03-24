"""
Defines abstract data type classes for :mod:`factsheet.view` classes.
"""
import typing

from factsheet.adapt_gtk import adapt_view as AVIEW


AbstractTextView = typing.TypeVar(
    'AbstractTextView', AVIEW.AdaptEntry, AVIEW.AdaptTextView)
