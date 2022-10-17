import gi   # type: ignore[import]
import typing

import factsheet.ui_bricks.ui_abc.brick_abc as BABC
import factsheet.ui_bricks.ui_abc.text_abc as BTEXTABC

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]  # noqa: E402

StoreUiDisplay = typing.Union[Gtk.Label]
StoreUiTextMarkup = typing.Union[Gtk.EntryBuffer]


class ControlTextMarkupGtk3(
        BABC.BypassAbc, BABC.SubjectAbc, BABC.TrackChangesAbc,
        BTEXTABC.ControlTextAbc[StoreUiTextMarkup]):
    """Transient aspects of text model with manually-entered markup.

    This class supports both GTK 3 (BypassAbc) and local (SubjectAbc)
    communication mechanisms with views.
    """

    def __init__(self, p_model: 'ModelTextMarkupGtk3' = None) -> None:
        """Initialize model and change marks.

        :param p_model: model to associate with this control.  If None,
            create a new model.
        """
        super().__init__(p_model)
        self._changed = False

    def attach(self, p_observer: BABC.ObserverAbc[StoreUiTextMarkup]) -> None:
        """Start notifying an observer.

        :param p_observer: start to notify this observer.
        """
        raise NotImplementedError

    def bypass(self) -> StoreUiTextMarkup:
        """Return GTK 3 storage component for a model."""
        raise NotImplementedError

    def detach(self, p_observer: BABC.ObserverAbc[StoreUiTextMarkup]) -> None:
        """Stop notifying an observer.

        :param p_observer: cease to notify this observer.
        """
        raise NotImplementedError

    def has_changed(self) -> bool:
        """Return True if and only if text with markup has changed."""
        raise NotImplementedError

    def has_not_changed(self) -> bool:
        """Return True if and only if text with markup has not changed."""
        raise NotImplementedError

    def mark_changed(self) -> None:
        """Mark text with markup as changed"""
        raise NotImplementedError

    def mark_not_changed(self) -> None:
        """Mark text with markup as not changed."""
        raise NotImplementedError

    def notify(self) -> None:
        """Notify all observers."""
        raise NotImplementedError

    def new_model(self) -> 'ModelTextMarkupGtk3':
        """Return new text model facade for control initialization."""
        return ModelTextMarkupGtk3(p_control=self)

    def on_model_change(self) -> None:
        """Update transient aspects of model.

        Update includes tracking changes (see
        :class:`.TrackChangesAbc`) and notifying observers (see
        :class:`.SubjectAbc` and :class:`.ObserverAbc`).
        """
        raise NotImplementedError


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
        raise NotImplementedError

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
