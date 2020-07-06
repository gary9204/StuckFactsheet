"""
Defines helper function to access GTK widget content.

Multiple specification classes need to get content from a Gtk.TextBuffer
in a Gtk.Assistant.  Function ``textbuffer_get_text`` simplifies reading
the entire contents of a buffer.

.. note::
    The implementation of specification classes is in its early stages
    at present (2020-07-01).  It is not clear whether a base class
    between :class:`.AbstractTemplate` and specification classes is
    needed. If it is, perhaps ``textbuffer_get_text`` should be a class
    method.
"""
import gi   # type: ignore[import]

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


def textbuffer_get_text(
        p_buffer: Gtk.TextBuffer, p_hidden: bool = True) -> str:
    """Return contents of GTK text buffer."""
    begin, end = p_buffer.get_bounds()
    text = p_buffer.get_text(begin, end, p_hidden)
    return text
