"""
Defines constants, functions, and objects for user interface elements.

Factsheet-level Definitions
===========================
Supporting deinitions for user interface elements for application and
Factsheets.

.. _delete-event:
   https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Widget.html
   #Gtk.Widget.signals.delete_event

.. data:: DIR_UI

   Path to directory that contains user interface definition files.

Exceptions
----------

.. exception:: ExceptionUi

    Bases: :exc:`.Exception`

    Base class for exceptions acessing user interface elements.

.. exception:: UiDescriptionError

    Bases: :exc:`.ExceptionUi`

    Raise when user interface description is not accessible.

.. exception:: UiObjectNotFoundError

    Bases: :exc:`.ExceptionUi`

    Raise when no object found for a given user interface ID.

Sheet Dialogs
-------------
All factsheet pages share guidance dialogs.

.. data:: ABOUT_APP

   Application About dialog.

.. data:: HELP_APP

   Application Help dialog.

.. data:: INTRO_APP

   Application Introduction dialog.

.. data:: HELP_SHEET

    Factsheet Help dialog.

.. data:: HELP_SHEET_DISPLAY

    Factsheet Display Menu Help dialog.

.. data:: HELP_SHEET_FILE

    Factsheet File Menu Help dialog.

.. data:: HELP_SHEET_TOPICS

    Factsheet Topics Menu Help dialog.

Sheet Types
-----------
Factsheet models and views use type aliases to minimize
implementation-specific details.

.. data:: IndexOutline

    Type hint for index to item in an outline in a :class:`.Sheet` or
    :class:`.Topic`.

.. data:: NewViewOutlineTopics

    Type hint for signature of constructor for a topic.

.. data:: OutlineTemplates

    Type hint for :class:`.Sheet`'s outline of templates.

.. data:: OutlineTopics

    Type hint for :class:`.Sheet`'s outline of topics.

.. data:: ViewOutlineTemplates

    Type hint for presentation element of an outline of templates.

.. data:: ViewOutlineTopics

    Type hint for presentation element of an outline of topics.

Topic-level Definitions
===========================
Supporting deinitions for user interface elements for topics.

.. data:: FACTORY_TOPIC

    Factory to produce factsheet components for classes :class:`.Topic`
    and :class:`.PaneTopic`.   See :mod:`.abc_factory`.

Topic Dialogs
-------------
All topic forms share guidance dialogs.

.. data:: HELP_TOPIC

    Topic Help dialog.

.. data:: HELP_TOPIC_DISPLAY

    Topic Display Menu Help dialog.

Topic Types
-----------
Topic models and views use type aliases to minimize
implementation-specific details.

.. data:: IdTopic

    Type hint for unique identifier of a topic.

.. data:: OutlineFacts

    Type hint for :class:`.Topic`'s outline of facts.

.. data:: ViewOutlineFacts

    Type hint for presentation element of an outline of facts.

Fact-level Definitions
===========================
Supporting deinitions for user interface elements for topics.

.. data:: FACTORY_FACT

    Factory to produce factsheet components for classes :class:`.Fact`
    and :class:`.BlockFact`.   See :mod:`.abc_factory`.

Fact Dialogs
-------------
All fact blocks share guidance dialogs.

.. data:: HELP_FACT

    Fact Help dialog.

.. data:: HELP_FACT_DISPLAY

    Fact Display Menu help.

.. data:: HELP_FACT_VALUE

    Help dialog for fact value.  See :class:`AspectValue`.

Fact Types
-----------
Factsheet models and views use type aliases to minimize
implementation-specific details.

.. note:: No fact type aliases yet.

"""
import abc
import logging
import typing

from pathlib import Path

import factsheet as FS

import gi   # type: ignore[import]
gi.require_version('Gtk', '3.0')
from gi.repository import Gio   # type: ignore[import]    # noqa: E402
from gi.repository import GLib   # type: ignore[import]    # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402

logger = logging.getLogger('Main.UI')


class ExceptionUi(Exception):
    pass


class UiDescriptionError(ExceptionUi):
    pass


class UiObjectNotFoundError(ExceptionUi):
    pass

# Factshet-level Definitions
# CLOSE_GTK = False
# CANCEL_GTK = not CLOSE_GTK
DIR_UI = Path(__file__).parent / 'ui'

# Application/Sheet dialogs
NAME_FILE_GUIDE_SHEET_UI = str(DIR_UI / 'guide_sheet.ui')
builder_guide_sheet = Gtk.Builder.new_from_file(NAME_FILE_GUIDE_SHEET_UI)
get_object_guide_sheet = builder_guide_sheet.get_object

ABOUT_APP = get_object_guide_sheet('ui_about_app')
ABOUT_APP.set_version(FS.__version__)
HELP_APP = get_object_guide_sheet('ui_help_app')
INTRO_APP = get_object_guide_sheet('ui_intro_app')

HELP_SHEET = get_object_guide_sheet('ui_help_sheet')
# HELP_SHEET_DISPLAY = get_object_guide_sheet('ui_help_sheet_display')
# HELP_SHEET_FILE = get_object_guide_sheet('ui_help_sheet_file')
# HELP_SHEET_TOPICS = get_object_guide_sheet('ui_help_sheet_topics')

del get_object_guide_sheet
del builder_guide_sheet

# Topic-level definitions

# Topic-level guidance dialogs
NAME_FILE_GUIDE_TOPIC_UI = str(DIR_UI / 'guide_topic.ui')
builder_guide_topic = Gtk.Builder.new_from_file(NAME_FILE_GUIDE_TOPIC_UI)
get_object_guide_topic = builder_guide_topic.get_object

HELP_TOPIC = get_object_guide_topic('ui_help_topic')
HELP_TOPIC_DISPLAY = get_object_guide_topic('ui_help_topic_display')

del get_object_guide_topic
del builder_guide_topic


# Fact-level definitions

# # Fact dialogs
# NAME_FILE_GUIDE_FACT_UI = str(DIR_UI / 'guide_fact.ui')
# builder_guide_fact = Gtk.Builder.new_from_file(NAME_FILE_GUIDE_FACT_UI)
# get_object_guide_fact = builder_guide_fact.get_object
#
# HELP_FACT = get_object_guide_fact('ui_help_fact')
# HELP_FACT_DISPLAY = get_object_guide_fact('ui_help_fact_display')
# HELP_FACT_VALUE = get_object_guide_fact('ui_help_fact_value')
#
# del builder_guide_fact
# del get_object_guide_fact

# Fact Types
# Not defined yet.


def new_action_active(p_group: Gio.SimpleActionGroup, p_name: str,
                      p_handler: typing.Callable) -> None:
    """Construct action, add to group, and connect to
    `activate <GioSimpleActionActivate_>`_ signal handler.

    :param p_group: action group to contain new action.
    :param p_name: name of new action.
    :param p_handler: `activate <GioSimpleActionActivate_>`_ signal
       handler for new action.

    .. _GioSimpleActionActivate: https://lazka.github.io/pgi-docs/
       #Gio-2.0/classes/SimpleAction.html#Gio.SimpleAction.signals
       .activate
    """
    action = Gio.SimpleAction.new(p_name, None)
    p_group.add_action(action)
    action.connect('activate', p_handler)


def new_action_active_dialog(p_group: Gio.SimpleActionGroup,
                             p_name: str, p_handler: typing.Callable,
                             p_dialog: Gtk.Dialog) -> None:
    """Construct action, add to group, and connect to
    `activate <GioSimpleActionActivate_>`_ signal handler with dialog
    parameter.

    :param p_group: action group to contain new action.
    :param p_name: name of new action.
    :param p_handler: `activate <GioSimpleActionActivate_>`_ signal
       handler for new action.
    :param p_dialog: dialog passed to handler.
    """
    action = Gio.SimpleAction.new(p_name, None)
    p_group.add_action(action)
    action.connect('activate', p_handler, p_dialog)


class GetUiElement(abc.ABC):
    """Get user interface element with supplemental failure information.

    `Gtk.Builder`_ aborts if there is an error opening a user interface
    description file or parsing a description.
    `Gtk.Builder.get_object()`_ returns None when the method cannot find
    the object for a given ID.  Class :class:`GetUiElement` augments
    `Gtk.Builder`_ to provide more information when a failure occurs.

    .. _`Gtk.Builder`:
        https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Builder.html

    .. _`Gtk.Builder.get_object()`:
        https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/
        Builder.html#Gtk.Builder.get_object
    """
    _builder: Gtk.Builder

    @abc.abstractmethod
    def __init__(self, **_kwargs) -> None:
        """Log start of user interface construction.

        Each subclass must extend this method by initializing the
        underlying builder attribute (`_builder`).
        """
        logger.debug('Building UI description ...')

    def __call__(self, p_id_ui: str) -> typing.Any:
        """Return user interface element with given ID.

        :param p_id_ui: ID of desired element.
        :raises UiObjectNotFoundError: when no element matches ID.
        """
        ui_element = self._builder.get_object(p_id_ui)
        if ui_element is None:
            MESSAGE = 'No element found for ID {}.'.format(p_id_ui)
            raise UiObjectNotFoundError(MESSAGE)
        return ui_element


class GetUiElementByPath(GetUiElement):
    """Extend :class:`.GetUiElement` with `Gtk.Builder`_ from file."""

    def __init__(self, *, p_path_ui: Path, **kwargs) -> None:
        """Initialize underlying builder and log source of description.

        :param p_path_ui: location of user interface description file.
        :raises UiDescriptionError: when user interface description is
            missing or inaccessible.
        """
        super().__init__(**kwargs)
        logger.debug('... from file {}.'.format(str(p_path_ui)))
        try:    # Reduce potential for new_from_file() abort.
            with p_path_ui.open() as _io_none:
                pass
        except Exception as err_access:
            MESSAGE = ('Could not access description file "{}".'
                       ''.format(p_path_ui.name))
            raise UiDescriptionError(MESSAGE) from err_access
        self._builder = Gtk.Builder.new_from_file(str(p_path_ui))


class GetUiElementByStr(GetUiElement):
    """Extend :class:`.GetUiElement` with `Gtk.Builder`_ from string."""

    def __init__(self, *, p_string_ui: str, **kwargs) -> None:
        """Initialize underlying builder and log source of description.

        :param p_string_ui: string containing user interface description.
        :param kwargs: superclass keyword parameters.
        """
        super().__init__(**kwargs)
        logger.debug('... from string.')
        ALL = -1
        self._builder = Gtk.Builder.new_from_string(p_string_ui, ALL)

    def __call__(self, p_id: str) -> typing.Any:
        """Return object with given ID.

        :param p_id: ID of desired object.
        :raises UiObjectNotFoundError: when no object matches ID.
        """
        ui_object = self._builder.get_object(p_id)
        if ui_object is None:
            MESSAGE = 'No object found for ID {}.'.format(p_id)
            raise UiObjectNotFoundError(MESSAGE)
        return ui_object


def new_column_stock(p_title: str, p_data_func  # : 'Gtk.TreeCellDataFunc'
                     ) -> Gtk.TreeViewColumn:
    """Return column with stock properties.

    :param p_title: title for column.
    :param p_cell_data_func: function to format column contents.
    """
    column = Gtk.TreeViewColumn(title=p_title)
    render = Gtk.CellRendererText()
    column.pack_start(render, expand=True)
    column.set_cell_data_func(render, p_data_func)
    column.set_clickable(True)
    WIDTH_MIN = 12
    column.set_min_width(WIDTH_MIN)
    column.set_reorderable(True)
    column.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
    return column
