"""
Defines classes to mediate factsheet-level interactions.

:doc:`../guide/devel_notes` explains how application Factsheet is based
on a Model-View-Controller (MVC) design.  Module :mod:`control_sheet`
defines classes representing control components for a factsheet as a
whole.

Exceptions
----------

.. exception:: BackupFileError

    Bases: :exc:`.FactsheetError`

    Raise for errors when making backup copy of file during save
    operation.

.. exception:: DumpFileError

    Bases: :exc:`.FactsheetError`

    Raise for errors dumping sheet to a file.

.. exception:: FactsheetError

    Bases: :exc:`.Exception`

    Base class for Factsheet exceptions.

.. exception:: NoFileError

    Bases: :exc:`.FactsheetError`

    Raise for file operations when when factsheet has no file path.

.. exception:: OpenFileError

    Bases: :exc:`.FactsheetError`

    Raise for errors when opening a factsheet file.

Global Variables
----------------

.. data:: g_control_app

    Application-level collection of open factsheets.

Types and Type Aliases
----------------------

.. data:: DisplayName

    Type alias for user interface element to display Factsheet
    :data:`~.sheet.Name`.  See :class:`~.control_sheet.FactoryDisplayName`.

.. data:: DisplaySummary

    Type alias for user interface element to display Factsheet
    :data:`~.sheet.Summary`.  See
    :class:`~.control_sheet.FactoryDisplaySummary`.

.. data:: DisplayTitle

    Type alias for user interface element to display Factsheet
    :data:`~.sheet.Title`.  See :class:`~.control_sheet.FactoryDisplayTitle`.

.. data:: EditorName

    Type alias for user interface element to edit Factsheet
    :data:`~.sheet.Name`.  See :class:`~.control_sheet.FactoryEditorName`.

.. data:: EditorSummary

    Type alias for user interface element to edit Factsheet
    :data:`~.sheet.Summary`.  See
    :class:`~.control_sheet.FactoryEditorSummary`.

.. data:: EditorTitle

    Type alias for user interface element to edit Factsheet
    :data:`~.sheet.Title`.  See
    :class:`~.control_sheet.FactoryEditorTitle`.

.. class:: FactoryDisplayName(p_name: Name)

    Type alias of factory for user interface elements.

    A call to the factory takes no arguments and returns a
    :data:`~.control_sheet.DisplayName` for the Factsheet
    :data:`~.sheet.Name`.

    :param p_name: name of Factsheet.
    :type p_name: :data:`~.sheet.Name`

.. class:: FactoryDisplaySummary(p_summary: Summary)

    Type alias of factory for user interface elements.

    A call to the factory takes no arguments and returns a
    :data:`~.control_sheet.DisplaySummary` for the Factsheet
    :data:`~.sheet.Summary`.

    :param p_summary: summary of Factsheet.
    :type p_summary: :data:`~.sheet.Summary`

.. class:: FactoryDisplayTitle(p_title: Title)

    Type alias of factory for user interface elements.

    A call to the factory takes no arguments and returns a
    :data:`~.control_sheet.DisplayTitle` for the Factsheet
    :data:`~.sheet.Title`.

    :param p_title: title of Factsheet.
    :type p_title: :data:`~.sheet.Title`

.. class:: FactoryEditorName(p_name: Name)

    Type alias of factory for user interface elements.

    A call to the factory takes no arguments and returns a
    :data:`~.control_sheet.EditorName` for the Factsheet
    :data:`~.sheet.Name`.

    :param p_name: name of Factsheet.
    :type p_name: :data:`~.sheet.Name`

.. class:: FactoryEditorSummary(p_summary: Summary)

    Type alias of factory for user interface elements.

    A call to the factory takes no arguments and returns a
    :data:`~.control_sheet.EditorSummary` for the Factsheet
    :data:`~.sheet.Summary`.

    :param p_summary: summary of Factsheet.
    :type p_summary: :data:`~.sheet.Summary`

.. class:: FactoryEditorTitle(p_title: Title)

    Type alias of factory for user interface elements.

    A call to the factory takes no arguments and returns a
    :data:`~.control_sheet.EditorTitle` for the Factsheet
    :data:`~.sheet.Title`.

    :param p_title: title of Factsheet.
    :type p_title: :data:`~.sheet.Title`

.. class:: FactoryViewTopics(p_topics: Topics)

    Type alias of factory for user interface elements.

    A call to the factory takes no arguments and returns a
    :data:`~.control_sheet.ViewTopics` for the Factsheet
    :data:`~.sheet.Topics`.

    :param p_topics: topics outline of Factsheet.
    :type p_topics: :data:`~.sheet.Topics`

.. data:: IdViewSheet

    Distinct type for unique identifier of a sheet view. See
    :func:`.id_view_sheet`.

.. data:: ViewTopics

    Type alias for user interface element to view outline of
    :data:`~.sheet.Topics`.  See
    :class:`~.control_sheet.FactoryViewTopics`.


Classes
-------
"""
import abc
import logging
from pathlib import Path
import pickle
import traceback as TB
import typing   # noqa


import factsheet.bridge_ui as BUI
import factsheet.control.control_topic as CTOPIC
import factsheet.model.sheet as MSHEET
import factsheet.model.topic as MTOPIC

logger = logging.getLogger('Main.CSHEET')


class FactsheetError(Exception):
    pass


class BackupFileError(FactsheetError):
    pass


class DumpFileError(FactsheetError):
    pass


class NoFileError(FactsheetError):
    pass


class OpenFileError(FactsheetError):
    pass


DisplayName = BUI.DisplayTextMarkup
DisplaySummary = BUI.DisplayTextStyled
DisplayTitle = BUI.DisplayTextMarkup

EditorName = BUI.EditorTextMarkup
EditorSummary = BUI.EditorTextStyled
EditorTitle = BUI.EditorTextMarkup

FactoryDisplayName = BUI.FactoryDisplayTextMarkup
FactoryDisplaySummary = BUI.FactoryDisplayTextStyled
FactoryDisplayTitle = BUI.FactoryDisplayTextMarkup

FactoryEditorName = BUI.FactoryEditorTextMarkup
FactoryEditorSummary = BUI.FactoryEditorTextStyled
FactoryEditorTitle = BUI.FactoryEditorTextMarkup

FactoryViewTopics = BUI.FactoryViewOutline[BUI.ViewOutline, MTOPIC.Topic]

IdViewSheet = typing.NewType('IdViewSheet', int)

TagTopic = MTOPIC.TagTopic

ViewTopics = BUI.ViewOutline


class ControlApp:
    """Maintains collection of open factsheets.

    A user may open a factsheet by requesting a new, empty factsheet or
    opening a factsheet file.
    """

    def __init__(self) -> None:
        """Initialize empty roster for factsheets."""
        self._roster_sheets: typing.MutableMapping[
            MSHEET.TagSheet, 'ControlSheet'] = dict()

    def close_all_factsheets(self) -> None:
        """TBD"""
        pass

    def close_factsheet(self, p_control: 'ControlSheet') -> None:
        """Close all views of the given factsheet.

        :param p_control: factsheet whose views to close.
        """
        p_control.remove_all_views()

    def open_factsheet(
            self, p_path: typing.Optional[Path], p_time: BUI.TimeEvent
            ) -> typing.Optional['ControlSheet']:
        """Return factsheet for the given path or None if factsheet is
        open already.

        If the path corresponds to an open factsheet, present the sheet
        views to the user and return None.  Otherwise, return factsheet
        with the given path.

        See :meth:`.ControlSheet.open` regarding file load failure.

        :param p_path: location for factsheet file.
        :param p_time: timestamp to order open requests.
        """
        if p_path is not None:
            path_absolute = p_path.resolve()
            for control in self._roster_sheets.values():
                if control._path is not None:
                    if path_absolute == control._path.resolve():
                        control.present_views(p_time)
                        return None
        control = ControlSheet(p_path)
        self._roster_sheets[control.tag] = control
        return control

    def remove_factsheet(self, p_control: 'ControlSheet') -> None:
        """Remove factsheet from collection of open factsheets.

        Log a warning when the control is not in the collection.

        :param p_control: factsheet to remove.
        """
        try:
            _ = self._roster_sheets.pop(p_control.tag)
        except KeyError:
            logger.warning('Missing control: 0x{:X} ({}.{})'.format(
                p_control.tag, self.__class__.__name__,
                self.remove_factsheet.__name__))


g_control_app = ControlApp()


class ControlSheet:
    """Mediates between user actions at factsheet view and factsheet model.

    Class :class:`ControlSheet` maintains a collection of active views
    of a factsheet. The class translates user requests in a factsheet
    view into changes in the factsheet model (such as save or delete) or
    in the collection of factsheet views (such as add or remove a view).
    """

    def __init__(self, p_path: Path = None) -> None:
        """Initialize instance from given file or with default attributes.

        :param p_path: location of file for factsheet model.
        """
        self._path = p_path
        self._model = self._model_from_path(p_path)

        self._factory_display_name = FactoryDisplayName(self._model.name)
        self._factory_display_summary = (
            FactoryDisplaySummary(self._model.summary))
        self._factory_display_title = FactoryDisplayTitle(self._model.title)

        self._factory_editor_name = FactoryEditorName(self._model.name)
        self._factory_editor_summary = (
            FactoryEditorSummary(self._model.summary))
        self._factory_editor_title = FactoryEditorTitle(self._model.title)

        self._factory_view_topics = (
            FactoryViewTopics(self._model.outline_topics))

        self._roster_views: typing.MutableMapping[
            IdViewSheet, ObserverControlSheet] = dict()
        self._roster_topics: typing.MutableMapping[
            TagTopic, CTOPIC.ControlTopic] = dict()
        # Untested fix for issue #256
        for topic in self._model.topics():
            control_new = CTOPIC.ControlTopic(p_model=topic)
            self._insert_topic_control(p_control=control_new)
        # Issue #253
        self._stub_topics()

    def _stub_topics(self):
        """Stub topics outline and roster for development.  See Issue #253.
        """
        N_TOP_TOPICS = 4
        N_DEPTH_TOPICS = 2
        for i in range(N_TOP_TOPICS):
            name = 'Name: Topic {}'.format(i)
            title = 'Title: Topic {}'.format(i)
            topic = MTOPIC.Topic(p_name=name, p_summary='', p_title=title)
            result = self.insert_topic_before(topic, None)
            if 0 == i:
                parent = result
        for j in range(N_DEPTH_TOPICS):
            name = '\t'*(j+1) + 'Name: Topic {}'.format(j + N_TOP_TOPICS)
            title = '\t'*(j+1) + 'Title: Topic {}'.format(j + N_TOP_TOPICS)
            topic = MTOPIC.Topic(p_name=name, p_summary='', p_title=title)
            parent = self.insert_topic_child(topic, parent)
        self._model.set_fresh()

    def add_view(self, p_view: 'ObserverControlSheet') -> None:
        """Add given view to collection of active views.

        Log a warning for a duplicate addition.

        :param p_view: view to add.
        """
        id_view = id_view_sheet(p_view_sheet=p_view)
        if id_view in self._roster_views:
            logger.warning('Duplicate: sheet 0x{:X} add view 0x{:X}  '
                           '({}.{})'.format(self.tag, id_view,
                                            self.__class__.__name__,
                                            self.add_view.__name__))
        self._roster_views[id_view_sheet(p_view)] = p_view

    def clear(self) -> None:
        """Remove contents of topics roster and topics outline."""
        self._roster_topics.clear()
        self._model.clear()

    def get_control_topic(self, p_line: BUI.LineOutline
                          ) -> typing.Optional[CTOPIC.ControlTopic]:
        """Return contents of topics outline at given line.

        :param p_line: line corresponding to desired control.
        """
        tag = self._model.get_tag(p_line)
        return self._roster_topics.get(tag, None)

    def insert_topic_after(self, p_topic: MTOPIC.Topic,
                           p_line: BUI.LineOutline) -> BUI.LineOutline:
        """Add topic to topics outline and roster of topics.

        Add topic to topics outline after topic at given index.  Create
        corresponding :class:`.ControlTopic` for roster of topics.

        :param p_topic: new topic to add.
        :param p_line: line of topic to precede new topic.
        :returns: line containing new topic.
        """
        control_new = CTOPIC.ControlTopic(p_model=p_topic)
        self._insert_topic_control(p_control=control_new)
        return self._model.insert_topic_after(p_topic, p_line)

    def insert_topic_before(self, p_topic: MTOPIC.Topic,
                            p_line: BUI.LineOutline) -> BUI.LineOutline:
        """Add topic to topics outline and roster of topics.

        Add topic to topics outline before topic at given index.  Create
        corresponding :class:`.ControlTopic` for roster of topics.

        :param p_topic: new topic to add.
        :param p_line: line of topic to follow new topic.
        :returns: line containing new topic.
        """
        control_new = CTOPIC.ControlTopic(p_model=p_topic)
        self._insert_topic_control(p_control=control_new)
        return self._model.insert_topic_before(p_topic, p_line)

    def insert_topic_child(self, p_topic: MTOPIC.Topic,
                           p_line: BUI.LineOutline) -> BUI.LineOutline:
        """Add topic to topics outline and roster of topics.

        Add topic to topics outline as child of topic at given index.
        Create corresponding :class:`.ControlTopic` for roster of topics.

        :param p_topic: new topic to add.
        :param p_line: line of parent topic for new topic.
        :returns: line containing new topic.
        """
        control_new = CTOPIC.ControlTopic(p_model=p_topic)
        self._insert_topic_control(p_control=control_new)
        return self._model.insert_topic_child(p_topic, p_line)

    def _insert_topic_control(self, p_control: CTOPIC.ControlTopic) -> None:
        """Add topic to roster of topics.

        :param p_control: topic control to add.
        """
        self._roster_topics[p_control.tag] = p_control

    def is_fresh(self) -> bool:
        """Return True when there are no unsaved changes to factsheet."""
        return self._model.is_fresh()

    def is_stale(self) -> bool:
        """Return True when there is at least one unsaved change to
        factsheet.
        """
        return self._model.is_stale()

    def _model_from_error(
            self, p_err: Exception, p_message: str) -> MSHEET.Sheet:
        """Return sheet model containing error information and log details.

        :param p_err: error to record.
        :param p_message: text for error sheet summary.
        """
        logger.error(p_message)
        for line in TB.format_exception(
                type(p_err), p_err, p_err.__traceback__):
            logger.error(line.rstrip('\n'))
        name = 'OPEN ERROR'
        source = 'Error source is {}: {}'.format(type(p_err).__name__, p_err)
        path = 'Path: {}'.format(str(self._path))
        summary = '\n'.join([p_message, source, path])
        title = 'Factsheet not opened.'
        model = MSHEET.Sheet(p_name=name, p_summary=summary, p_title=title)
        return model

    def _model_from_path(self, p_path: typing.Optional[Path]) -> MSHEET.Sheet:
        """Return sheet model from file at given location or a new model.

        Return a new, empty sheet model when path is None or when there
        is no file at given path. When model cannot be loaded from file
        at given path, return a sheet model containing error
        information.

        :param p_path: location of file for factsheet model.
        """
        if p_path is None:
            model = MSHEET.Sheet()
            return model

        try:
            with p_path.open(mode='rb') as io_in:
                try:
                    model = pickle.load(io_in)
                except Exception as err:
                    message = 'Factsheet not open! could not read file.'
                    model = self._model_from_error(err, message)
        except FileNotFoundError:
            model = MSHEET.Sheet()
        except Exception as err:
            message = 'Factsheet not open! could not open file.'
            model = self._model_from_error(err, message)
        return model

    @property
    def name(self) -> str:
        """Return sheet name without markup errors."""
        name = BUI.escape_text_markup(self._model.name.text)
        return name

    @property
    def new_display_name(self) -> DisplayName:
        """Return factory for displays of sheet name."""
        return self._factory_display_name

    @property
    def new_display_summary(self) -> DisplaySummary:
        """Return factory for displays of sheet summary."""
        return self._factory_display_summary

    @property
    def new_display_title(self) -> DisplayTitle:
        """Return factory for displays of sheet title."""
        return self._factory_display_title

    @property
    def new_editor_name(self) -> EditorName:
        """Return factory for editors of sheet name."""
        return self._factory_editor_name

    @property
    def new_editor_summary(self) -> EditorSummary:
        """Return factory for editors of sheet summary."""
        return self._factory_editor_summary

    @property
    def new_editor_title(self) -> EditorTitle:
        """Return factory for editors of sheet title."""
        return self._factory_editor_title

    @property
    def new_view_topics(self) -> ViewTopics:
        """Return factory for editors of sheet title."""
        return self._factory_view_topics

    def _open_file_save(self) -> typing.BinaryIO:
        """Return an open file object after backing up any existing file.

        Backup provides (minimal) guard against inadvertent overwrite.

        :raises FactsheetError: see :meth:`~.ControlSheet.save`.
        :returns: Open file object at control's path.
        """
        if self._path is None:
            raise NoFileError('Save: cannot open path None.')
        try:
            io_out = self._path.open(mode='xb')
        except FileExistsError:
            try:
                self._path.replace(str(self._path) + '~')
            except Exception as err_replace:
                raise BackupFileError from err_replace
            try:
                io_out = self._path.open(mode='xb')
            except Exception as err_reopen:
                raise OpenFileError from err_reopen
        except Exception as err_open:
            raise OpenFileError from err_open
        return io_out

    @property
    def path(self) -> typing.Optional[Path]:
        """Return path to file containing factsheet contents."""
        return self._path

    def present_views(self, p_time: BUI.TimeEvent) -> None:
        """Make visible to user all views of the factsheet.

        :param p_time: timestamp of event requesting presentation.
        """
        for view in self._roster_views.values():
            view.present(p_time)

    def remove_all_views(self) -> None:
        """Remove all views of the collection of active views."""
        views = self._roster_views.values()
        while views:
            view = next(iter(views))
            view.erase()
            self.remove_view(p_view=view)

    def remove_topic(self, p_line: BUI.LineOutline) -> None:
        """Remove topic from roster of topic and from topics outline.

        :param p_line: line of topic to remove along with all its
            descendants.  If line is None, remove no topics.
        """
        if p_line is not None:
            for topic in self._model.topics(p_line):
                _ = self._roster_topics.pop(topic.tag)
            self._model.remove_topic(p_line)

    def remove_view(self, p_view: 'ObserverControlSheet') -> None:
        """Remove given view from collection of active views.

        Log a warning for a missing view.

        If the collection of active views is empty, remove the factsheet
        from the collection of open factsheets.

        :param p_view: view to remove.
        """
        id_view = id_view_sheet(p_view_sheet=p_view)
        try:
            self._roster_views.pop(id_view)
        except KeyError:
            logger.warning('Missing: sheet 0x{:X} remove view 0x{:X}  '
                           '({}.{})'.format(self.tag, id_view,
                                            self.__class__.__name__,
                                            self.remove_view.__name__))
            return

        if not self._roster_views:
            global g_control_app
            g_control_app.remove_factsheet(p_control=self)

    def remove_view_is_safe(self) -> bool:
        """Return True when the control can safely remove a view.

        A factsheet closes when it has no views.  A sheet control may
        safely remove a sheet view when:

        * The factsheet contains no unsaved changes or
        * The factsheet has more than one view or
        * The user approves closing the factsheet.
        """
        if (self.is_stale()
                and 1 == len(self._roster_views)):
            return False

        return True

    def save(self, p_path: typing.Optional[Path] = None) -> None:
        """Save factsheet contents to file at factsheet's path.

        :param p_path: path to replace factsheet's path.

        :raises BackupFileError: when backup fails.
        :raises DumpFileError: when factsheet cannot be written to file.
        :raises OpenFileError: for all other errors.
        :raises NoFileError: when path to save file is None.
        """
        if p_path is not None:
            self._path = p_path
        with self._open_file_save() as io_out:
            try:
                pickle.dump(self._model, io_out)
            except Exception as err_dump:
                raise DumpFileError from err_dump
        self._model.set_fresh()

    @property
    def tag(self) -> MSHEET.TagSheet:
        """Return unique identifier of sheet."""
        return self._model.tag

    def topics(self) -> typing.Iterator[CTOPIC.ControlTopic]:
        """Return iterator over topic controls in factsheet."""
        for control in self._roster_topics.values():
            yield control


def id_view_sheet(p_view_sheet: 'ObserverControlSheet') -> IdViewSheet:
    """Return unique identifier for a sheet view.

    The identifier is unique during the lifetime of the sheet view.  An
    identifier may be reused if a sheet view is destroyed.

    :param p_view_sheet: sheet view to identify.
    """
    return IdViewSheet(id(p_view_sheet))


class ObserverControlSheet(abc.ABC):
    """Define interface for sheet control to notify a sheet view.

    In general, a sheet view requests services from its sheet control.
    For a few exceptions, a sheet view acts as an observer of its sheet
    control.  A sheet control notifies its views when to present to the
    user and when to erase.
    """

    @abc.abstractmethod
    def erase(self) -> None:
        """Destroy visible portion of sheet view."""
        raise NotImplementedError

    @abc.abstractmethod
    def present(self, p_time: BUI.TimeEvent) -> None:
        """Make sheet view visible to user.

        :param p_time: time stamp to order multiple requests.
        """
        raise NotImplementedError
