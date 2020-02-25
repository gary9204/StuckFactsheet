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

.. data:: ABOUT_APP

   Glade definition for application About dialog.

.. data:: HELP_APP

   Glade definition for application Help dialog.

.. data:: INTRO_APP

   Glade definition for application Introduction dialog.
"""


import os.path

import gi   # type: ignore[import]
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402

CANCEL_GTK = True

UI_DIR = os.path.abspath(os.path.dirname(__file__)) + '/ui/'

# Application/Sheet-level guidance dialogs
builder_guide_sheet = Gtk.Builder.new_from_file(UI_DIR + 'guide_sheet.ui')
get_object_guide_sheet = builder_guide_sheet.get_object

ABOUT_APP = get_object_guide_sheet('ui_about_app')
HELP_APP = get_object_guide_sheet('ui_help_app')
INTRO_APP = get_object_guide_sheet('ui_intro_app')

del builder_guide_sheet
del get_object_guide_sheet
