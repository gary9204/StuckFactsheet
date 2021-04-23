"""
Defines classes to adapt a fact for presentation.

.. data:: BasisOpaque


"""
import abc
import gi   # type: ignore[import]
import typing

import factsheet.bridge_ui as BUI

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402

BasisAny = typing.Any
BasisOpaque = typing.TypeVar('BasisOpaque')
ViewAspect = typing.Union[Gtk.Widget]
ViewAspectOpaque = typing.TypeVar('ViewAspectOpaque')
ViewAspectPlain = typing.Union[Gtk.Label]


class Aspect(abc.ABC, typing.Generic[BasisOpaque, ViewAspectOpaque]):
    """Adapts a fact for a particular presentation.

    A view may present differnt aspects of a fact, such as whether the
    fact has been checked or the value of the fact.  The form of a
    presentation may be plain text, formatted text, a list, a table,
    etc.  Class :class:`~.Aspect` adapts fact content to a form
    suitable for a presentation.
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
    def __init__(self, p_basis: BasisOpaque) -> None:
        """Initialize instance.

        :param p_basis: aspect of fact to use for presentation.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def new_view(self) -> ViewAspectOpaque:
        """Return new view of fact presentation."""
        raise NotImplementedError

    @abc.abstractmethod
    def refresh(self) -> None:
        """Synchronize presentation with fact aspect."""
        raise NotImplementedError


class AspectPlain(Aspect[BasisAny, ViewAspectPlain]):
    """Adapts a fact for plain text presentation."""

    def __eq__(self, p_other: typing.Any) -> bool:
        """Return True when p_other is comparable type with same text.

        :param p_other: object to compare with self.
        """
        if not super().__eq__(p_other):
            return False

        if self._basis != p_other._basis:
            return False

        return True

    def __init__(self, p_basis: BasisAny) -> None:
        """Initialize instance.

        :param p_basis: aspect of fact to use for presentation.
        """
        self._basis = p_basis
        self._bridge = BUI.BridgeTextStatic()
        self.refresh()

    def new_view(self) -> ViewAspectPlain:
        """Return new view of fact presentation."""
        return self._bridge.new_view()

    def refresh(self) -> None:
        """Set fact information in presentation."""
        self._bridge.text = str(self._basis)
