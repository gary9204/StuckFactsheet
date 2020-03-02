"""
Defines GTK-based View classes that implement abstract View classes.

See :class:`.AbstractTextModel`.

.. data:: AdaptEntry

   Adapts `Gtk.Entry`_ widget to display a text attribute.

.. _Gtk.Entry:
   https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/
   Entry.html#Gtk.Entry

.. data:: AdaptTextView

   Adapts `Gtk.TextView`_ widget to display a text attribute.    # type: ignore

.. _Gtk.TextView:
   https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/
   TextView.html#Gtk.TextView
"""

import gi   # type: ignore[import]


gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


AdaptEntry = Gtk.Entry
AdaptTextView = Gtk.TextView