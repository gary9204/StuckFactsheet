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


class ControlMarkupGtk3(BABC.BypassAbc, BABC.SubjectAbc,
                        BTEXTABC.ControlTextAbc[StoreUiTextMarkup]):
    """Transient aspects of text model with manually-entered markup.

    This class supports both GTK 3 (:class:`.BypassAbc`) and local
    (:class:`.SubjectAbc`) communication mechanisms with views.
    """

    def __init__(self, p_model: 'ModelMarkupGtk3' = None) -> None:
        """Initialize model and observers.

        :param p_model: model to associate with this control.  If None,
            create a new model.
        """
        super().__init__(p_model)
        self._observers: typing.MutableMapping[
            IdObserverMarkup, ObserverMarkupAbc] = dict()
        self.init_signals()

    def init_signals(self) -> None:
        """Connect GTK 3 change signals from model's text store."""
        source = self._model.get_store_ui()
        _ = source.connect(
            'deleted-text', lambda *_args: self.on_model_change())
        _ = source.connect(
            'inserted-text', lambda *_args: self.on_model_change())

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
        """Return model text as GTK 3 object."""
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

    def new_model(self) -> 'ModelMarkupGtk3':
        """Return new text model facade for control initialization."""
        return ModelMarkupGtk3()

    def notify(self) -> None:
        """Notify all observers."""
        store = self._model.get_store_ui()
        for observer in self._observers.values():
            observer.on_notice(p_store_ui=store)

    def on_model_change(self) -> None:
        """Notify observers model has changed.

        See :class:`.SubjectAbc` and :class:`.ObserverAbc`).
        """
        self.notify()


class ControlMarkupTrackGtk3(ControlMarkupGtk3, BABC.TrackChangesAbc):
    """Transient aspects of text model with manually-entered markup.

    Extends :class:`.ControlMarkupGtk3` to track changes in text and
    markup.
    """

    def __init__(self, p_model: 'ModelMarkupGtk3' = None) -> None:
        """Initialize change mark.

        :param p_model: model to associate with this control.  If None,
            create a new model.
        """
        super().__init__(p_model)
        self._changed = False

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

    def on_model_change(self) -> None:
        """Extend to record that text or markup has changed.

        See :class:`.TrackChangesAbc`.
        """
        super().on_model_change()
        self.mark_changed()


class ModelMarkupGtk3(BTEXTABC.ModelTextAbc[StoreUiTextMarkup]):
    """Persistent aspects of text model with manually-entered markup.

    This class is a facade for text model based on GTK 3.
    """

    def get_store_py(self) -> BTEXTABC.StorePyTextMarkup:
        """Return model text with markup as string."""
        return self._store_ui.get_text()

    def get_store_ui(self) -> StoreUiTextMarkup:
        """Return model text with markup as GTK 3 object."""
        return self._store_ui

    def new_store_ui(self) -> StoreUiTextMarkup:
        """Return new GTK 3 object for model storage for initialization."""
        return StoreUiTextMarkup()

    def set_store_ui(self, p_store_py: BTEXTABC.StorePyTextMarkup) -> None:
        """Set text and markup from toolkit-independent storage.

        :param p_store_py: text and markup to store.
        """
        ALL = -1
        self._store_ui.set_text(p_store_py, ALL)
