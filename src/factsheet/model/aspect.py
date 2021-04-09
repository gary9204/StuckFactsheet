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
ViewAspectAny = typing.Union[Gtk.Widget]
ViewAspectOpaque = typing.TypeVar('ViewAspectOpaque')
ViewAspectPlain = typing.Union[Gtk.Label]


class Aspect(abc.ABC, typing.Generic[BasisOpaque, ViewAspectOpaque]):
    """Adapts a fact for a particular presentation.

    A fact may have a variety of presentations such as plain text,
    formatted text, a list, or a table.  An Aspect adapts a fact to a
    form suitable for a particular presentation.

    :param p_basis: portion of fact used for presentation.
    """
    @abc.abstractmethod
    def __init__(self, p_basis: BasisOpaque) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def clear(self) -> None:
        """Remove fact information from aspect."""
        raise NotImplementedError

    @abc.abstractmethod
    def new_view(self) -> ViewAspectOpaque:
        """Return new view of aspect for presentation."""
        raise NotImplementedError


class AspectPlain(Aspect[BasisAny, ViewAspectPlain]):
    """Adapts a fact for plain text presentation.

    :param p_basis: portion of fact used for presentation.
    """
    def __init__(self, p_basis: BasisAny) -> None:
        self._aspect = BUI.BridgeTextStatic()
        self._aspect.text = str(p_basis)

    def clear(self) -> None:
        """Remove fact information from aspect."""
        self._aspect.text = ''

    def new_view(self) -> ViewAspectPlain:
        """Return new view of aspect for presentation."""
        view = self._aspect.new_view()
        return view
