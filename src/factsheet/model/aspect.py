"""
Defines classes for presentation of fact values.

.. data:: ValueAny

    Type hint for arbitrary fact value.

.. data:: ViewAspectPlain

    Type hint for plain text presentation of a fact value.
"""
import abc
import gi   # type: ignore[import]
import typing

import factsheet.bridge_ui as BUI

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402

ValueAny = typing.Any
ValueOpaque = typing.TypeVar('ValueOpaque')
# ViewAspectBridge = typing.TypeVar('ViewAspectBridge')
ViewAspectOpaque = typing.TypeVar('ViewAspectOpaque')
ViewAspectPlain = typing.Union[Gtk.Label]


class Aspect(abc.ABC, typing.Generic[ValueOpaque, ViewAspectOpaque]):
    """Presentation for the value a fact.

    There may be multiple ways to present the value of a fact.  For
    example, a fact value may have presentations as plain text,
    formatted text, a list, or a table.  Class :class:`~.Aspect`
    puts a fact value to a form suitable for a presentation and manages
    views of that presentation.
    """

    @abc.abstractmethod
    def __eq__(self, p_other: typing.Any) -> bool:
        """Return True when p_other has comparable type.

        :param p_other: object to compare with self.
        """
        if not isinstance(p_other, type(self)):
            return False

        return True

    @abc.abstractmethod
    def __init__(self) -> None:
        """Initialize with default presentation."""
        raise NotImplementedError

    @abc.abstractmethod
    def clear_presentation(self) -> None:
        """Clear presentation to default.

        Typically, the default presentation is blank or empty for a fact
        with no value.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def new_view(self) -> ViewAspectOpaque:
        """Return new view of the presentation."""
        raise NotImplementedError

    @abc.abstractmethod
    def set_presentation(self, p_value: ValueOpaque) -> None:
        """Set presentation to match given value.

        :param p_value: fact value to use for presentation.
        """
        raise NotImplementedError


# class AspectBridge(Aspect[BasisBridge, ViewAspectBridge],
#                    typing.Generic[ViewAspectBridge]):
#     """Adapts a fact aspect stored as a bridge class."""
#
#     def __eq__(self, p_other: typing.Any) -> bool:
#         """Return True when p_other is comparable type with same
#         content.
#
#         :param p_other: object to compare with self.
#         """
#         if not super().__eq__(p_other):
#             return False
#
#         if self._presentation != p_other._basis:
#             return False
#
#         return True
#
#     def __init__(self, p_value: BasisBridge) -> None:
#         """Initialize instance.
#
#         :param p_value: aspect of fact to use for presentation.
#         """
#         self._presentation = p_value
#
#     def new_view(self) -> ViewAspectBridge:
#         """Return new view of fact presentation."""
#         return self._presentation.new_view()
#
#     def set_presentation(self) -> None:
#         """Synchronize presentation with fact information."""
#         pass


class AspectPlain(Aspect[ValueAny, ViewAspectPlain]):
    """Plain text presentation of a fact value."""

    def __eq__(self, p_other: typing.Any) -> bool:
        """Return True when p_other is comparable type with same text.

        :param p_other: object to compare with self.
        """
        if not super().__eq__(p_other):
            return False

        if self._presentation != p_other._presentation:
            return False

        return True

    def __init__(self) -> None:
        """Initialize blank text presentation."""
        self._presentation = BUI.BridgeTextStatic()
        self.clear_presentation()

    def clear_presentation(self) -> None:
        """Clear presentation to blank default."""
        self._presentation.text = ''

    def new_view(self) -> ViewAspectPlain:
        """Return new view of presentation."""
        return self._presentation.new_view()

    def set_presentation(self, p_value: ValueAny) -> None:
        """Set presentation to match given value.

        :param p_value: fact value to use for presentation.
        """
        self._presentation.text = str(p_value)
