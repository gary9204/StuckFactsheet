"""
Defines base classes for topic specification.
"""
import gi   # type: ignore[import]
import logging
from pathlib import Path
import typing

import factsheet.bridge_ui as BUI

gi.require_version('Gtk', '3.0')
from gi.repository import GLib   # type: ignore[import]    # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402

logger = logging.getLogger('Main.SBASE')

SUFFIX_SPEC = '.py'
SUFFIX_ASSIST = '.ui'

PageAssist = typing.Union[Gtk.Box]


class ExceptionSpec(Exception):
    """Base class for specification exceptions."""

    pass


class SpecFileError(ExceptionSpec):
    """Raise for when specification file is inaccessible."""

    pass


class UiDescriptionError(ExceptionSpec):
    """Raise for when user interface description in accessible."""

    pass


class UiObjectNotFoundError(ExceptionSpec):
    """Raise for when no object found for a given user interface ID."""

    pass


class GetUiObject:
    """Get user interface object while supplementing failure information.

    `Gtk.Builder`_ aborts if there is an error opening a user interface
    description file or parsing the description.
    `Gtk.Builder.get_object()`_ returns None when the method cannot find
    the object for a given ID.  Class :class:`GetUiObject` augments
    `Gtk.Builder`_ to provide more information when failures occur.

    .. _`Gtk.Builder`:
        https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Builder.html

    .. _`Gtk.Builder.get_object()`:
        https://lazka.github.io/pgi-docs/#Gtk-3.0/classes/
        Builder.html#Gtk.Builder.get_object
    """

    def __init__(self, *, p_path: Path = None, p_string: str = None) -> None:
        """Initialize underlying builder and log source of description.

        The caller can provide the user interface description in a file
        or a string.  If the caller provides both, the method uses the
        file.  If the caller provides neither, the method raises an
        exception.

        :param p_path: location of user interface description file.
        :param p_string: string containing user interface description.
        :raises UiDescriptionError: when user interface description is
            missing.
        """
        if p_path is None and p_string is None:
            raise UiDescriptionError(
                'No user interface description provided.')

        ALL = -1
        if p_path is not None:
            logger.debug(
                'Building UI description from {}.'.format(str(p_path)))
            try:    # Reduce potential for new_from_file() abort.
                with p_path.open() as _io_none:
                    pass
            except Exception as err_access:
                MESSAGE = ('Could not access description file "{}".'
                           ''.format(p_path.name))
                raise UiDescriptionError(MESSAGE) from err_access
            self._builder = Gtk.Builder.new_from_file(str(p_path))
        else:
            logger.debug('Building UI description from string.')
            self._builder = Gtk.Builder.new_from_string(p_string, ALL)

    def __call__(self, p_id: str) -> typing.Any:
        """Return object with given ID.

        :param p_id: ID of desired object.
        :raises UiObjectNotFoundError: when no objecte matches ID.
        """
        ui_object = self._builder.get_object(p_id)
        if ui_object is None:
            MESSAGE = 'No object found for ID {}.'.format(p_id)
            raise UiObjectNotFoundError(MESSAGE)
        return ui_object


class Base:
    """Base spec for Factsheet topics.

    A spec provides a user the means to create a class of topics.  A
    spec embodies a template for the class.  It queries the user to
    complete the template for a specific topic.  The spec also queries
    the user of the location of the new topic in the Factsheet's
    outline of topics.
    """

    def __init__(self, *, p_name: str) -> None:
        """Initialize spec identity and topic identity including location.

        :param p_name: name of specification.
        """
        self._name_spec = BUI.ModelTextMarkup(p_text=p_name)

        self._init_name_topic()

    def _init_name_topic(self) -> None:
        """ Initialize"""
        self._name_topic = BUI.ModelTextMarkup(p_text='')
        self._new_display_name_topic = (
            BUI.FactoryDisplayTextMarkup(p_model=self._name_topic))
        self._new_editor_name_topic = (
            BUI.FactoryEditorTextMarkup(p_model=self._name_topic))

    def __call__(self):
        """TBD"""
        # assist = self.new_assistant()
        # self.add_pages(p_assist=assist)
        # run assistant
        # construct topic (or exit)
        # place topic (or exit)
        pass

    def add_pages(self, p_assist: Gtk.Assistant) -> None:
        """TBD"""
        pass

    def add_page_confirm(self, p_assist: Gtk.Assistant) -> None:
        """TBD"""
        pass

    def add_page_identify(self, p_assist: Gtk.Assistant) -> None:
        """TBD"""
        pass

    def add_page_intro(self, p_assist: Gtk.Assistant) -> None:
        """Construct an introduction page and add it to assistant.

        :param p_assist: add introduction to this assistant.
        """
        pass

    def add_page_locate(self, p_assist: Gtk.Assistant) -> None:
        """TBD"""
        pass

    def name(self) -> str:
        """TBD"""
        pass

    def new_assistant(self) -> typing.Optional[Gtk.Assistant]:
        """Return an assistant from user interface definition."""
        path_assist = Path(__file__).with_suffix('.ui')
        get_ui_object = GetUiObject(p_path=path_assist)
        assist = get_ui_object('ui_assistant')
        return assist

    def on_apply(self, p_assistant) -> None:
        """TBD"""
        pass

    def on_cancel(self, p_assistant) -> None:
        """TBD"""
        pass

    def on_prepare(self, p_assistant, p_page) -> None:
        """TBD"""
        pass

    def summary(self) -> str:
        """TBD"""
        pass

    def title(self) -> str:
        """TBD"""
        pass
