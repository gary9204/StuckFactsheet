"""
Defines constants, functions, and objects for user interface elements.

.. data:: ABOUT_APP

   Glade definition for application About dialog.

.. data:: CANCEL_GTK

   Value to cancel processing of a GTK signal.  For example, see
   GtkWidget `delete-event`_ signal.

.. data:: HELP_APP

   Glade definition for application Help dialog.

..     data:: INTRO_APP

   Glade definition for application Introduction dialog.

.. data:: UI_DIR

   Path to directory that contains user interface definition files.

.. _delete-event:
   https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Widget.html
   #Gtk.Widget.signals.delete_event
"""


import os.path
import typing

from factsheet.adapt_gtk import adapt_factory as AFACTORY

import gi   # type: ignore[import]
gi.require_version('Gtk', '3.0')
from gi.repository import Gio   # type: ignore[import]    # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


#: Factory to produce :class:`Head` components. See :class:`.abc_factory`.
FACTORY_HEAD = AFACTORY.FactoryHead()


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


def new_activate_action(pm_group: Gio.SimpleActionGroup, p_name: str,
                        px_handler: typing.Callable) -> None:
    """Construct action, add to group, and connect to 'activate' signal
    handler.

    :param pm_group: action group to contain new action
    :param p_name: name of new action
    :param px_handler: 'activate' signal handler for new action
    """
    action = Gio.SimpleAction.new(p_name, None)
    pm_group.add_action(action)
    action.connect('activate', px_handler)
