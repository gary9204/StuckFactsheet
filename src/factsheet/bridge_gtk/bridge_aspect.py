"""
Defines bridge classes that encapsulate widget toolkit fact aspect
classes.

.. data:: ModelAspectPlain

    Type hint for element to store a plain text aspect.

.. data:: PersistAspectPlain

    Type hint for plain text aspect representation suitable for
    persistent storage.

.. data:: SourceOpaque

    Placeholder type hint for source of an aspect.

.. data:: ViewAspectPlain

    Type hint for GTK element to view a plain text aspect.  See
    `Gtk.Label`_.

.. _`Gtk.Label`:
    https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Label.html
"""
import abc
import gi   # type: ignore[import]
import typing

import factsheet.bridge_gtk.bridge_base as BBASE

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402

ModelAspectOpaque = typing.TypeVar('ModelAspectOpaque')
ModelAspectPlain = str
PersistAspectOpaque = typing.TypeVar('PersistAspectOpaque')
PersistAspectPlain = str
SourceOpaque = typing.TypeVar('SourceOpaque')
ViewAspectOpaque = typing.TypeVar('ViewAspectOpaque')
ViewAspectPlain = typing.Union[Gtk.Label]


class BridgeAspect(BBASE.BridgeBase[
        ModelAspectOpaque, PersistAspectOpaque, ViewAspectOpaque],
        typing.Generic[ModelAspectOpaque, PersistAspectOpaque,
                       ViewAspectOpaque, SourceOpaque]):
    """Encapsulates widget toolkit classes to represent an aspect of a
    fact.

    Aspects represent the value of a fact as well as fact metadata.
    Examples of value aspects include plain text and tabular
    representations.  Examples of metadata aspects include fact status
    and dependencies.

    An aspect has transient data for attached views in addition to a
    persistant storage representation.
    """

    @abc.abstractmethod
    def transcribe(self, p_source: typing.Optional[SourceOpaque]
                   ) -> PersistAspectOpaque:
        """Return persistent representation of source.

        When source is None, return empty representation.

        :param p_source: value or metadata for aspect.
        """
        raise NotImplementedError

    def refresh(self, p_source: typing.Optional[SourceOpaque]) -> None:
        """Set aspect storage element and attached view elements from
        source.

        When source is None, clear elements.

        :param p_source: value or metadata for aspect.
        """
        persist = self.transcribe(p_source)
        self._set_persist(persist)


class BridgeAspectPlain(BridgeAspect[
        ModelAspectPlain, PersistAspectPlain, ViewAspectPlain, SourceOpaque]):
    """Plain text aspect for a fact."""

    def _bind(self, p_view: ViewAspectPlain):
        """Form toolkit-specific connection between view element and
        storage element.

        :param p_view: view to bind.
        """
        p_view.set_label(self._model)

    def _get_persist(self) -> PersistAspectPlain:
        """Return aspect representation in form suitable for persistent
        storage.
        """
        return self._model

    def _loose(self, p_view: ViewAspectPlain) -> None:
        """Break toolkit-specific connection between view element and
        storage element.

        :param p_view: view to loose.
        """
        p_view.set_label('')

    def _new_model(self) -> ModelAspectPlain:
        """Return toolkit-specific storage element."""
        return ModelAspectPlain()

    def _new_view(self) -> ViewAspectPlain:
        """Return toolkit-specific view element."""
        return ViewAspectPlain()

    def transcribe(self, p_source: typing.Optional[SourceOpaque]
                   ) -> PersistAspectPlain:
        """Return plain text representation of source.

        When source is None, return empty plain text.

        :param p_source: value or metadata for aspect.
        """
        persist = ''
        if p_source is not None:
            persist = str(p_source)
        return persist

    def _set_persist(self, p_persist: PersistAspectPlain) -> None:
        """Update representation elements from persistent form of aspect.

        :param p_persist: persistent form of plain text aspect.
        """
        self._model = p_persist
        for view in self._views.values():
            view.set_label(self._model)
