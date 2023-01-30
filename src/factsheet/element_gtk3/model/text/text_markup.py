"""
Define facade class for text storage element supporting `Pango markup`_

.. _Pango markup:
    https://docs.gtk.org/Pango/pango_markup.html

Type Aliases
------------

.. data:: UiModelTextMarkup

    Type alias for element to store text formatted with `Pango markup`_.
    See `Gtk.EntryBuffer`_.

.. _Gtk.EntryBuffer:
   https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/EntryBuffer.html

Classes
-------
"""
import gi  # type: ignore[import]
import typing

import factsheet.element_gtk3.model.text.text_abc as EMTEXT

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]  # noqa: E402

UiModelTextMarkup = typing.Union[Gtk.EntryBuffer]


class TextMarkup(EMTEXT.TextAbc[UiModelTextMarkup]):
    """Text storage eleemnt with support for editing and `Pango markup`_."""

    def to_external(self) -> EMTEXT.ExternalText:
        """Return external representation of text storage element."""
        return self._ui_model.get_text()

    def new_ui_model(self) -> UiModelTextMarkup:
        """Return a user interface text storage element."""
        return UiModelTextMarkup()

    def set_internal(self, p_external: EMTEXT.ExternalText) -> None:
        """Set text storage element from external representation.

        :param p_external: external representation of desired content.
        """
        ALL = -1
        self._ui_model.set_text(p_external, ALL)
