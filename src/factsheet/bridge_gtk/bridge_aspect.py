"""
Defines bridge classes that encapsulate widget toolkit fact aspect
classes.
"""
import abc
import gi   # type: ignore[import]
import logging
import typing

import factsheet.bridge_gtk.bridge_base as BBASE
from factsheet.model.fact import Fact

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402

FactOpaque = typing.TypeVar('FactOpaque')
FactAny = int

ModelAspectOpaque = typing.TypeVar('ModelAspectOpaque')
ModelAspectPlain = int

PersistAspectOpaque = typing.TypeVar('PersistAspectOpaque')
PersistAspectPlain = int

ViewAspectOpaque = typing.TypeVar('ViewAspectOpaque')
ViewAspectPlain = typing.Union[Gtk.Label]

logger = logging.getLogger('Main.bridge_aspect')


class Aspect(BBASE.BridgeBase[
            ModelAspectOpaque, PersistAspectOpaque, ViewAspectOpaque],
        typing.Generic[ModelAspectOpaque, PersistAspectOpaque,
                       ViewAspectOpaque, FactOpaque]):
    """Common ancestor of fact value aspects.

    A aspect for a fact value provides the value in a form compatible
    with a GTK display element.  The display element is called an
    aspect.

    Aspects have transient data for attached aspects in addition to
    persistant value representation.
    """

    @abc.abstractmethod
    def set(self, p_fact: typing.Optional[FactOpaque]) -> None:
        """Set value representation along with attached aspects.

        :param p_aspect: value to aspect.
        """
        raise NotImplementedError


class AspectPlain(Aspect[ModelAspectPlain, PersistAspectPlain,
                         ViewAspectPlain, FactAny]):
    """Plain text aspect for a fact value.

    :param p_aspect: fact value to aspect.
    """

    # def __getstate__(self) -> typing.Dict:
    #     """Return aspect in form pickle can persist.

    #     Persistent form of aspect consists of value representation only.
    #     """
    #     raise NotImplementedError
    #     # state = self.__dict__.copy()
    #     # del state['_aspects']
    #     # return state

    # def __init__(self) -> None:
    #     # self.__init_transient()
    #     # self.clear()

    # def __init_transient(self) -> None:
    #     """Helper ensures initialization and pickling are consistent."""
    #     raise NotImplementedError
    #     # self._aspects: typing.MutableMapping[int, ViewAspectOpaque] = dict()

    # def __setstate__(self, px_state: typing.Dict) -> None:
    #     """Reconstruct aspect from state pickle loads.

    #     Reconstructed aspect has no aspects attached.

    #     :param px_state: unpickled state of stored aspect.
    #     """
    #     raise NotImplementedError
    #     # self.__dict__.update(px_state)
    #     # self.__init_transient()

    def _bind(self, p_view: ViewAspectPlain):
        """Form toolkit-specific connection between view element and
        storage element.

        :param p_view: view to bind.
        """
        raise NotImplementedError

    def _get_persist(self) -> PersistAspectPlain:
        """Return storage element in form suitable for persistent storage."""
        raise NotImplementedError

    def _loose(self, p_view: ViewAspectPlain):
        """Break toolkit-specific connection between view element and
        storage element.

        :param p_view: view to loose.
        """
        raise NotImplementedError

    def _new_model(self) -> ModelAspectPlain:
        """Return toolkit-specific storage element."""
        raise NotImplementedError

    def set(self, p_fact: typing.Optional[FactAny]) -> None:
        """Set value representation along with attached aspects.

        :param p_aspect: value to aspect.
        """
        raise NotImplementedError
        # self._value_gtk = str(p_aspect)
        # for view in self._views.values():
        #     view.set_text(self._model)

    def _set_persist(self, p_persist: PersistAspectPlain) -> None:
        """Set storage element from content in persistent form.

        :param p_persist: persistent form for storage element content.
        """
        raise NotImplementedError
