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
        del state['_views']
        return state

    def __init__(self) -> None:
        self._model = self._new_model()
        self._init_transients()

    def _init_transients(self) -> None:
        """Set storage element content for initialization and pickling."""
        self._views: typing.MutableMapping[int, ViewOpaque] = dict()

    def __iter__(self) -> typing.Iterator[ViewOpaque]:
        """Return iterator over view elements associated with storage
        element.
        """
        return iter(self._views.values())

    def __setstate__(self, p_state: typing.MutableMapping) -> None:
        """Reconstruct storage element from content that pickle loads.

        Reconstructed model has no bound views.

        :param p_state: unpickled content.
        """
        self.__dict__.update(p_state)
        self._model = self._new_model()
        self._set_persist(self.ex_model)   # type: ignore[attr-defined]
        del self.ex_model       # type: ignore[attr-defined]
        self._init_transients()

    def __str__(self) -> str:
        """Return storage element as string."""
        return '<{}: {}>'.format(type(self).__name__, self._get_persist())

    def attach_view(self, p_view: ViewOpaque) -> None:
        """Associate view element with storage element.

        Log a warning when the view element already is associated with
        the storage element.

        :param p_view: view to associate.
        """
        id_view = id(p_view)
        if id_view in self._views:
            logger.warning('Duplicate view: {} ({}.{})'.format(
                hex(id_view), type(self).__name__, self.attach_view.__name__))
            return

        self._views[id_view] = p_view
        self._bind(p_view=p_view)

    @abc.abstractmethod
    def _bind(self, p_view: ViewOpaque):
        """Form toolkit-specific connection between view element and
        storage element.

        :param p_view: view to bind.
        """
        raise NotImplementedError

    def detach_all(self) -> None:
        """Disassociate all view elements from storage element."""
        views = self._views.values()
        while views:
            view = next(iter(views))
            self.detach_view(view)

    def detach_view(self, p_view: ViewOpaque) -> None:
        """Disassociate view element from storaage element.

        Log a warning when the view element is not associated with the
        storage element.

        :param p_view: view to disassociate.
        """
        id_view = id(p_view)
        try:
            view_detached = self._views.pop(id_view)
        except KeyError:
            logger.warning('Missing view: {} ({}.{})'
                           ''.format(hex(id_view), type(self).__name__,
                                     self.detach_view.__name__))
            return

        self._loose(p_view=view_detached)

    @abc.abstractmethod
    def _get_persist(self) -> PersistOpaque:
        """Return storage element in form suitable for persistent storage."""
        raise NotImplementedError

    @abc.abstractmethod
    def _loose(self, p_view: ViewOpaque):
        """Break toolkit-specific connection between view element and
        storage element.

        :param p_view: view to loose.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _new_model(self) -> ModelOpaque:
        """Return toolkit-specific storage element."""
        raise NotImplementedError

    @abc.abstractmethod
    def _set_persist(self, p_persist: PersistOpaque) -> None:
        """Set storage element from content in persistent form.

        :param p_persist: persistent form for storage element content.
        """
        raise NotImplementedError
