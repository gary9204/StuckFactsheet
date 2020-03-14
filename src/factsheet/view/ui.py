"""
Defines constants, functions, and objects for user interface elements.

.. data:: ABOUT_APP

   Factsheet About dialog.

.. data:: CANCEL_GTK

   Value to cancel processing of a GtkWidget `delete-event`_ signal.

.. data:: CLOSE_GTK

   Value to continue processing of a GtkWidget `delete-event`_ signal.

.. _delete-event:
   https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Widget.html
   #Gtk.Widget.signals.delete_event

.. data:: DIR_UI

   Path to directory that contains user interface definition files.

.. data:: FACTORY_INFOID

    Factory to produce :class:`.Head` components. See :mod:`.abc_factory`.

.. data:: HELP_APP

   Factsheet Help dialog.

.. data:: INTRO_APP

   Factsheet Introduction dialog.

"""
import typing

from pathlib import Path

import factsheet as FS
from factsheet.adapt_gtk import adapt_factory as AFACTORY

import gi   # type: ignore[import]
gi.require_version('Gtk', '3.0')
from gi.repository import Gio   # type: ignore[import]    # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


CLOSE_GTK = False
CANCEL_GTK = not CLOSE_GTK

DIR_UI = Path(__file__).parent / 'ui'

FACTORY_INFOID = AFACTORY.FactoryInfoId()

# Application/Sheet-level guidance dialogs
NAME_FILE_GUIDE_SHEET_UI = str(DIR_UI / 'guide_sheet.ui')
builder_guide_sheet = Gtk.Builder.new_from_file(NAME_FILE_GUIDE_SHEET_UI)
get_object_guide_sheet = builder_guide_sheet.get_object

ABOUT_APP = get_object_guide_sheet('ui_about_app')
ABOUT_APP.set_version(FS.__version__)
HELP_APP = get_object_guide_sheet('ui_help_app')
INTRO_APP = get_object_guide_sheet('ui_intro_app')

HELP_SHEET = get_object_guide_sheet('ui_help_sheet')
HELP_SHEET_DISPLAY = get_object_guide_sheet('ui_help_sheet_display')
HELP_SHEET_FILE = get_object_guide_sheet('ui_help_sheet_file')

del builder_guide_sheet
del get_object_guide_sheet

# # Data Loss Warning dialog
# # This section works aroung limitations in Glade and Python bindings for
# # GTK.  Glade does not recognize use-header-bar property of GtkDialog.
# # Gtk.Dialog() does not recognize flag Gtk.DialogFlags.USE_HEADER_BAR.
# #
# # Manually add the following to GtkDialog section of dialog_data_loss.ui:
# #        <property name="use-header-bar">1</property>
#
# NAME_FILE_DIALOG_DATA_LOSS_UI = str(DIR_UI / 'dialog_data_loss.ui')
# builder_dialog_data_loss = Gtk.Builder.new_from_file(
#     NAME_FILE_DIALOG_DATA_LOSS_UI)
# get_object_dialog_data_loss = builder_dialog_data_loss.get_object
#
# DIALOG_DATA_LOSS = get_object_dialog_data_loss('ui_dialog_data_loss')
# DIALOG_DATA_LOSS.add_button('Cancel', Gtk.ResponseType.CANCEL)
# button = DIALOG_DATA_LOSS.get_widget_for_response(Gtk.ResponseType.CANCEL)
# button.get_style_context().add_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)
# DIALOG_DATA_LOSS.add_button('Discard', Gtk.ResponseType.APPLY)
# button = DIALOG_DATA_LOSS.get_widget_for_response(Gtk.ResponseType.APPLY)
# button.get_style_context().add_class(Gtk.STYLE_CLASS_DESTRUCTIVE_ACTION)
# WARNING_DATA_LOSS = get_object_dialog_data_loss('ui_warning_data_loss')
#
# del builder_dialog_data_loss
# del get_object_dialog_data_loss


def new_action_active(pm_group: Gio.SimpleActionGroup, p_name: str,
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


def new_action_active_dialog(pm_group: Gio.SimpleActionGroup,
                             p_name: str, px_handler: typing.Callable,
                             px_dialog: Gtk.Dialog) -> None:
    """Construct action, add to group, and connect to 'activate' signal
    handler with dialog parameter.

    :param pm_group: action group to contain new action.
    :param p_name: name of new action.
    :param px_handler: 'activate' signal handler for new action.
    :param px_dialog: dialog passed to handler.
    """
    action = Gio.SimpleAction.new(p_name, None)
    pm_group.add_action(action)
    action.connect('activate', px_handler, px_dialog)
