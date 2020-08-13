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

    Factory to produce :class:`.InfoId` components. See :mod:`.abc_factory`.

.. data:: HELP_APP

   Factsheet Help dialog.

.. data:: IndexOutline

    Type hint for index to item in an outline.

.. data:: INTRO_APP

   Factsheet Introduction dialog.

.. data:: OutlineTemplates

    Type hint for outline containing templates.

.. data:: OutlineTopics

    Type hint for outline containing topics.
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
FACTORY_SHEET = AFACTORY.FactorySheet()
FACTORY_FACT = AFACTORY.FactoryFact()

KWArgs = typing.Mapping[str, typing.Any]
IdTopic = AFACTORY.IdTopic
IndexOutline = AFACTORY.IndexOutline
OutlineTemplates = AFACTORY.OutlineTemplates
OutlineTopics = AFACTORY.OutlineTopics
ViewOutlineTemplates = AFACTORY.ViewOutlineTemplates
ViewOutlineTopics = AFACTORY.ViewOutlineTopics
NewViewOutlineTopics = typing.Callable[[], ViewOutlineTopics]

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
HELP_SHEET_TOPICS = get_object_guide_sheet('ui_help_sheet_topics')

del builder_guide_sheet
del get_object_guide_sheet


# Topic-level guidance dialogs
NAME_FILE_GUIDE_TOPIC_UI = str(DIR_UI / 'guide_topic.ui')
builder_guide_topic = Gtk.Builder.new_from_file(NAME_FILE_GUIDE_TOPIC_UI)
get_object_guide_topic = builder_guide_topic.get_object

HELP_TOPIC = get_object_guide_topic('ui_help_topic')
HELP_TOPIC_DISPLAY = get_object_guide_topic('ui_help_topic_display')

del builder_guide_topic
del get_object_guide_topic


# Fact-level guidance dialogs
NAME_FILE_GUIDE_FACT_UI = str(DIR_UI / 'guide_fact.ui')
builder_guide_fact = Gtk.Builder.new_from_file(NAME_FILE_GUIDE_FACT_UI)
get_object_guide_fact = builder_guide_fact.get_object

HELP_FACT = get_object_guide_fact('ui_help_fact')
HELP_FACT_DISPLAY = get_object_guide_fact('ui_help_fact_display')
HELP_FACT_VALUE = get_object_guide_fact('ui_help_fact_value')

del builder_guide_fact
del get_object_guide_fact


def new_action_active(pm_group: Gio.SimpleActionGroup, p_name: str,
                      px_handler: typing.Callable) -> None:
    """Construct action, add to group, and connect to
    `activate <GioSimpleActionActivate_>`_ signal handler.

    :param pm_group: action group to contain new action.
    :param p_name: name of new action.
    :param px_handler: `activate <GioSimpleActionActivate_>`_ signal
       handler for new action.

    .. _GioSimpleActionActivate: https://lazka.github.io/pgi-docs/
       #Gio-2.0/classes/SimpleAction.html#Gio.SimpleAction.signals
       .activate
    """
    action = Gio.SimpleAction.new(p_name, None)
    pm_group.add_action(action)
    action.connect('activate', px_handler)


def new_action_active_dialog(pm_group: Gio.SimpleActionGroup,
                             p_name: str, px_handler: typing.Callable,
                             px_dialog: Gtk.Dialog) -> None:
    """Construct action, add to group, and connect to
    `activate <GioSimpleActionActivate_>`_ signal handler with dialog
    parameter.

    :param pm_group: action group to contain new action.
    :param p_name: name of new action.
    :param px_handler: `activate <GioSimpleActionActivate_>`_ signal
       handler for new action.
    :param px_dialog: dialog passed to handler.
    """
    action = Gio.SimpleAction.new(p_name, None)
    pm_group.add_action(action)
    action.connect('activate', px_handler, px_dialog)
