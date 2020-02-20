"""
factsheet.view.ui - defines constants and objects for user interface
elements.

.. data:: CANCEL_GTK

   Value to cancel processing of a GTK signal.  For example, see
   GtkWidget `delete-event`_ signal.

.. _delete-event:
   https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Widget.html
   #Gtk.Widget.signals.delete_event

.. data:: UI_DIR

   Path to directory that contains user interface definition files.
"""


import os.path

import gi   # type: ignore[import]
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402

CANCEL_GTK = True

UI_DIR = os.path.abspath(os.path.dirname(__file__)) + '/ui/'
