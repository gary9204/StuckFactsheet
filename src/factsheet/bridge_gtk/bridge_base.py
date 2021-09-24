"""
Defines base for model classes that encapsulate widget toolkit classes.

.. data:: ModelGtkOpaque

    Placeholder type hint for a model component.  A GTK example is
    `Gtk.TextBuffer`_.

.. _Gtk.TextBuffer:
   https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/TextBuffer.html

.. data:: PersistGtkOpaque

    Placeholder type hint for model representation suitable
    for persistent storage.  A GTK example is the string representation
    of a `Gtk.TextBuffer`_.

.. data:: TimeEvent

    Type hint for timestamp of a user interface event.  See
    `Gtk.get_current_event_time`_.

.. _Gtk.get_current_event_time:
    https://lazka.github.io/pgi-docs/#Gtk-3.0/
    functions.html#Gtk.get_current_event_time

.. data:: TIME_EVENT_CURRENT

    Represents the current time for a user interface event.  See
    `Gdk.CURRENT_TIME`_.

.. _Gdk.CURRENT_TIME:
    https://lazka.github.io/pgi-docs/#Gdk-3.0/
    constants.html#Gdk.CURRENT_TIME

.. data:: ViewGtkOpaque

    Placeholder type hint for a view element.  A GTK example is
    `Gtk.TextView`_.

.. _Gtk.TextView:
   https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/TextView.html
"""
import abc
import gi   # type: ignore[import]
import logging
import typing

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk   # type: ignore[import]    # noqa: E402

logger = logging.getLogger('Main.bridge_base')

TimeEvent = int
TIME_EVENT_CURRENT = Gdk.CURRENT_TIME

ModelGtkOpaque = typing.TypeVar('ModelGtkOpaque')
PersistGtkOpaque = typing.TypeVar('PersistGtkOpaque')
# ViewAny = typing.Union[Gtk.Widget]
ViewGtkOpaque = typing.TypeVar('ViewGtkOpaque')


class BridgeBase(abc.ABC, typing.Generic[ModelGtkOpaque, PersistGtkOpaque]):
    """Common ancestor of model classes that encapsulate widget toolkit
    storage elements.
    """

    def __eq__(self, p_other: typing.Any) -> bool:
        """Return True when storage element of other is equivalent to
        self.

        :param p_other: object to test for equality.
        """
        if not isinstance(p_other, type(self)):
            return False

        if self._get_persist() != p_other._get_persist():
            return False

        return True

    def __getstate__(self) -> typing.Dict:
        """Return content of storage element in form pickle can store.

        Each descendant class defines its persistent contents.
        """
        state = self.__dict__.copy()
        state['ex_model'] = self._get_persist()
        del state['_model']
        return state

    def __init__(self) -> None:
        """Initialize instance with GTK storage."""
        self._model: ModelGtkOpaque

    def __setstate__(self, p_state: typing.MutableMapping) -> None:
        """Reconstruct storage element from content that pickle loads.

        :param p_state: unpickled content.
        """
        self.__dict__.update(p_state)
        self._set_persist(self.ex_model)   # type: ignore[attr-defined]
        del self.ex_model       # type: ignore[attr-defined]

    def __str__(self) -> str:
        """Return storage element as string."""
        return '<{}: {}>'.format(type(self).__name__, self._get_persist())

    @abc.abstractmethod
    def _get_persist(self) -> PersistGtkOpaque:
        """Return storage element in form suitable for persistent storage."""
        raise NotImplementedError

    @abc.abstractmethod
    def _set_persist(self, p_persist: PersistGtkOpaque) -> None:
        """Set storage element from content in persistent form.

        :param p_persist: persistent form for storage element content.
        """
        raise NotImplementedError


class FactoryGtkViewAbstract(
        abc.ABC, typing.Generic[ViewGtkOpaque]):
    """Common ancestor of factory classes for views of storage elements."""

    @abc.abstractmethod
    def __call__(self) -> ViewGtkOpaque:
        """Return toolkit-specific view of storage element."""
        raise NotImplementedError
