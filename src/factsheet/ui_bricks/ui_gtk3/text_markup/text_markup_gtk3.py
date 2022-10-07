import gi   # type: ignore[import]
import typing

import factsheet.ui_bricks.ui_abc.text_abc as BTEXTABC

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]  # noqa: E402

StoreUiDisplay = typing.Union[Gtk.Label]
StoreUiTextMarkup = typing.Union[Gtk.EntryBuffer]


class ControlTextMarkupGtk3(
        BTEXTABC.ControlTextAbc[StoreUiTextMarkup]):

    def new_model(self) -> 'ModelTextMarkupGtk3':
        raise NotImplementedError


class ModelTextMarkupGtk3(
        BTEXTABC.ModelTextAbc[StoreUiTextMarkup]):

    def get_external(self) -> str:
        raise NotImplementedError

    def new_control(self) -> ControlTextMarkupGtk3:
        raise NotImplementedError
