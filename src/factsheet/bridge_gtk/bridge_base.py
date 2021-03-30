"""
Defines base for model classes that encapsulate widget toolkit classes.

.. data:: ModelOpaque

    Placeholder type hint for a model component.  A GTK example is
    `Gtk.TextBuffer`_.

.. _Gtk.TextBuffer:
   https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/TextBuffer.html

.. data:: PersistOpaque

    Placeholder type hint for model representation suitable
    for persistent storage.  A GTK example is the string representation
    of a `Gtk.TextBuffer`_.

.. data:: ViewOpaque

    Placeholder type hint for a view element.  A GTK example is
    `Gtk.TextView`_.

.. _Gtk.TextView:
   https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/TextView.html
"""
import abc
import logging
import typing

logger = logging.getLogger('Main.bridge_base')

ModelOpaque = typing.TypeVar('ModelOpaque')
PersistOpaque = typing.TypeVar('PersistOpaque')
ViewOpaque = typing.TypeVar('ViewOpaque')


class BridgeBase(abc.ABC,
                 typing.Generic[ModelOpaque, PersistOpaque, ViewOpaque],):
    """Common ancestor of model classes that encapsulate storage
    elements of toolkit.

    In addition to a storage element, a :class:`BridgeBase` object has
    transient content for toolkit view elements associated with the
    storage element.

    A :class:`BridgeBase` iterator returns the associated views.
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
        self._model = self._new_model()
        self._init_transients()

    def _init_transients(self) -> None:
        """Set transient content for initialization and pickling."""
        pass

    def __setstate__(self, p_state: typing.MutableMapping) -> None:
        """Reconstruct storage element from content that pickle loads.

        Reconstructed model has no bound views.

        :param p_state: unpickled content.
        """
        self.__dict__.update(p_state)
        self._model = self._new_model()
        self._init_transients()
        self._set_persist(self.ex_model)   # type: ignore[attr-defined]
        del self.ex_model       # type: ignore[attr-defined]

    def __str__(self) -> str:
        """Return storage element as string."""
        return '<{}: {}>'.format(type(self).__name__, self._get_persist())

    @abc.abstractmethod
    def _get_persist(self) -> PersistOpaque:
        """Return storage element in form suitable for persistent storage."""
        raise NotImplementedError

    @abc.abstractmethod
    def _new_model(self) -> ModelOpaque:
        """Return toolkit-specific storage element."""
        raise NotImplementedError

    @abc.abstractmethod
    def new_view(self) -> ViewOpaque:
        """Return toolkit-specific view element."""
        raise NotImplementedError

    @abc.abstractmethod
    def _set_persist(self, p_persist: PersistOpaque) -> None:
        """Set storage element from content in persistent form.

        :param p_persist: persistent form for storage element content.
        """
        raise NotImplementedError
