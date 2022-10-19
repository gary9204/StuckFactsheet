"""
Model facade, control, and factory classes for markup text.

Classes support formatting text with manually-entered markup.

.. data:: IdObserverMarkup

    Type for identity of an :class:`.ObserverAbc` object.  See
    :func:`~.text_markup_gtk3.id_observer_markup`.

.. data:: ObserverMarkupAbc

    Abstract interface specializing :class:`.ObserverAbc` to GTK 3.

.. data:: StoreUiTextMarkup

    GTK 3 type for storing markup text.

.. data:: VOID_ID_OBSERVER_MARKUP

    Identity distinct from all possible :data:`.IdObserverMarkup`
    identities.
"""
import gi   # type: ignore[import]
import logging
import typing

import factsheet.ui_bricks.ui_abc.brick_abc as BABC
import factsheet.ui_bricks.ui_abc.text_abc as BTEXTABC

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]  # noqa: E402

IdObserverMarkup = typing.NewType('IdObserverMarkup', int)
StoreUiTextMarkup = typing.Union[Gtk.EntryBuffer]
ObserverMarkupAbc = BABC.ObserverAbc[StoreUiTextMarkup]

VOID_ID_OBSERVER_MARKUP = IdObserverMarkup(0)

logger = logging.getLogger('Main.markup_gtk3')


def id_observer_markup(p_observer: ObserverMarkupAbc) -> IdObserverMarkup:
    """Return identity for given observer.

    Function specializes builtin `id`_ to :class:`.ObserverAbc`.

    :param p_observer: observer to identify.

    .. _`id`: https://docs.python.org/3.9/library/functions.html#id
    """
    return IdObserverMarkup(id(p_observer))


class ControlTextMarkupGtk3(
        BABC.BypassAbc, BABC.SubjectAbc, BABC.TrackChangesAbc,
        BTEXTABC.ControlTextAbc[StoreUiTextMarkup]):
    """Transient aspects of text model with manually-entered markup.

    This class supports both GTK 3 (:class:`.BypassAbc`) and local
    (:class:`.SubjectAbc`) communication mechanisms with views.
    """

    def __init__(self, p_model: 'ModelTextMarkupGtk3' = None) -> None:
        """Initialize model and change marks.

        :param p_model: model to associate with this control.  If None,
            create a new model.
        """
        super().__init__(p_model)
        self._changed = False
        self._observers: typing.MutableMapping[
            IdObserverMarkup, ObserverMarkupAbc] = dict()

    def attach(self, p_observer: ObserverMarkupAbc) -> None:
        """Start notifying an observer.

        Log warning when control is notifying observer already.

        :param p_observer: start to notify this observer.
        """
        id_obsever = id_observer_markup(p_observer)
        if id_obsever not in self._observers.keys():
            self._observers[id_obsever] = p_observer
        else:
            logger.warning(
                'Observer already being notified. id: {} ({}.{})'.format(
                    hex(id_obsever),
                    self.__class__.__name__, self.attach.__name__))

    def bypass(self) -> StoreUiTextMarkup:
        """Return model text as  GTK 3 object."""
        return self._model.get_store_ui()

    def detach(self, p_observer: ObserverMarkupAbc) -> None:
        """Stop notifying an observer.

        Log warning when control is not notifying observer.

        :param p_observer: cease to notify this observer.
        """
        id_obsever = id_observer_markup(p_observer)
        try:
            _ = self._observers.pop(id_obsever)
        except KeyError:
            logger.warning(
                'Observer not being notified. id: {} ({}.{})'.format(
                    hex(id_obsever),
                    self.__class__.__name__, self.detach.__name__))

    def has_changed(self) -> bool:
        """Return True if and only if text with markup has changed."""
        return self._changed

    def has_not_changed(self) -> bool:
        """Return True if and only if text with markup has not changed."""
        return not self._changed

    def mark_changed(self) -> None:
        """Mark text with markup as changed."""
        self._changed = True

    def mark_not_changed(self) -> None:
        """Mark text with markup as not changed."""
        self._changed = False

    def new_model(self) -> 'ModelTextMarkupGtk3':
        """Return new text model facade for control initialization."""
        return ModelTextMarkupGtk3(p_control=self)

    def notify(self) -> None:
        """Notify all observers."""
        store = self._model.get_store_ui()
        for observer in self._observers.values():
            observer.on_notice(p_store_ui=store)

    def on_model_change(self) -> None:
        """Update transient aspects of model.

        Update includes tracking changes (see
        :class:`.TrackChangesAbc`) and notifying observers (see
        :class:`.SubjectAbc` and :class:`.ObserverAbc`).
        """
        self.mark_changed()
        self.notify()


class ModelTextMarkupGtk3(
        BTEXTABC.ModelTextAbc[StoreUiTextMarkup]):
    """Persistent aspects of text model with manually-entered markup.

    This class is a facade for text model based on GTK 3.
    """

    def get_store_py(self) -> str:
        """Return model text with markup as string."""
        raise NotImplementedError

    def get_store_ui(self) -> StoreUiTextMarkup:
        """Return model text with markup as GTK 3 object."""
        return self._store_ui

    def new_control(self) -> ControlTextMarkupGtk3:
        """Return new control for text model facade for initialization."""
        return ControlTextMarkupGtk3(p_model=self)

    def new_store_ui(self) -> StoreUiTextMarkup:
        """Return new GTK 3 object for model facade for initialization."""
        return StoreUiTextMarkup()

    def set_store_ui(self, p_store_py: str) -> None:
        """Set facade text and markup from string.

        :param p_store_py: text and markup to store.
        """
        raise NotImplementedError
