"""
Defines classes to mediate factsheet-level interactions.

:doc:`../guide/devel_notes` explains how application Factsheet is based
on a Model-View-Controller (MVC) design.  Module :mod:`control_sheet`
defines classes representing control components for a factsheet as a
whole.

.. data:: g_control_app

    Application-level collection of open factsheets.

.. data:: IdFactsheet

    Distinct type for unique identifier of a factsheet.

.. data:: IdViewSheet

    Distinct type for unique identifier of a sheet view.
"""
import abc
import enum
# import errno
import logging
from pathlib import Path
import pickle
# import traceback as TB
import typing   # noqa


# import factsheet.control.control_idcore as CIDCORE
import factsheet.model.sheet as MSHEET
# from factsheet.abc_types import abc_sheet as ABC_SHEET
# from factsheet.control import pool as CPOOL
# from factsheet.control import control_topic as CTOPIC
# from factsheet.model import topic as MTOPIC
# from factsheet.model import types_model as MTYPES
# from factsheet.view import types_view as VTYPES
# from factsheet.view import ui as UI

logger = logging.getLogger('Main.CSHEET')


class GoNoGo(enum.Enum):  # TBD - Not tested yet
    """Indicates whether an action should continue or halt.

    .. attribute: GO

        Continue the action.

    .. attribute: NOGO

        Halt the action.
    """
    GO = enum.auto()
    NOGO = enum.auto()


IdFactsheet = typing.NewType('IdFactsheet', int)
IdViewSheet = typing.NewType('IdViewSheet', int)


def id_factsheet(p_control_sheet: 'ControlSheet') -> IdFactsheet:
    """Return unique identifier for a factsheet.

    There is a one-to-one correspondence between factsheets and sheet
    controls.  The identifier is unique during the lifetime of the
    factsheet.  An identifier may be reused if a factsheet view is
    destroyed.

    :param p_control_sheet: sheet control for the factsheet to identify.
    """
    return IdFactsheet(id(p_control_sheet))


def id_view_sheet(p_view_sheet: 'ObserverControlSheet') -> IdViewSheet:
    """Return unique identifier for a sheet view.

    The identifier is unique during the lifetime of the sheet view.  An
    identifier may be reused if a sheet view is destroyed.

    :param p_view_sheet: sheet view to identify.
    """
    return IdViewSheet(id(p_view_sheet))


class ControlApp:
    """Maintains collection of open factsheets.

    A user may open a factsheet by requesting a new, empty factsheet or
    opening a factsheet file.
    """

    def __init__(self) -> None:
        """Initialize empty roster for factsheets."""
        self._roster_sheets: typing.MutableMapping[
            IdFactsheet, 'ControlSheet'] = dict()

    def close_factsheet(self, p_control: 'ControlSheet') -> None:
        """Stop tracking factsheet.

        Log a warning when the control is not in the collection.

        :param p_control: factsheet to close.
        """
        id_control = id_factsheet(p_control)
        try:
            self._roster_sheets.pop(id_control)
        except KeyError:
            logger.warning('Missing control: 0x{:X} ({}.{})'.format(
                id_control, self.__class__.__name__,
                self.close_factsheet.__name__))

    def close_all_factsheets(self) -> None:
        """TBD"""

    def open_factsheet(self, p_path: typing.Optional[Path] = None
                       ) -> typing.Optional['ControlSheet']:
        """Return factsheet for the given path or None if factsheet is
        open already.

        If the path corresponds to an open factsheet, present the sheet
        views to the user and return None.  Otherwise, return factsheet
        with the given path.

        See :meth:`.ControlSheet.open` regarding file load failure.

        :param p_path: location for factsheet file.
        """
        if p_path is not None:
            raise NotImplementedError
        # path_absolute = p_path.resolve()
        # for control in _m_factsheets.values():
        #     if control._path is not None:
        #         if path_absolute == control._path.resolve():
        #             control.present()
        #             return
        control = ControlSheet(p_path)
        id_control = id_factsheet(control)
        self._roster_sheets[id_control] = control
        return control


g_control_app = ControlApp()


class ControlSheet:
    """Mediates user actions at view to model updates for a factsheet.

    Class :class:`ControlSheet` translates user requests in a factsheet
    view into changes in the factsheet model (such as save or delete) or
    in the collection of factsheet views (such as add or close a view).
    """

    def __init__(self, p_path: Path = None) -> None:
        """Initialize instance with given attributes and no topics."""
        self._path = p_path
        self._model = self._model_from_path(p_path)
        self._roster_views: typing.MutableMapping[
            IdViewSheet, ObserverControlSheet] = dict()
        self._is_closing = False
        # self._controls_topic: typing.Dict[
        #     MTYPES.TagTopic, CTOPIC.ControlTopic] = dict()

    def add_view(self, p_view: 'ObserverControlSheet') -> None:
        """Track given sheet view but warn of duplicates."""
        id_view = id_view_sheet(p_view_sheet=p_view)
        if id_view in self._roster_views:
            logger.warning('Duplicate: sheet 0x{:X} add view 0x{:X}  '
                           '({}.{})'.format(id_view, id_factsheet(self),
                                            self.__class__.__name__,
                                            self.add_view.__name__))
        self._roster_views[id_view_sheet(p_view)] = p_view

    def _model_from_path(self, p_path: typing.Optional[Path]) -> MSHEET.Sheet:
        """Return sheet model from file at given location or a new model.

        Return a new, empty sheet model when path is None or when there
        is no file at given path. When model cannot be loaded from file
        at given path, return, as heet model containing error
        information.

        :param p_path: location of file for factsheet model.
        """
        if p_path is None:
            model = MSHEET.Sheet()
            return model

        try:
            with p_path.open(mode='rb') as io_in:
                raise NotImplementedError
                model = pickle.load(io_in)
        except FileNotFoundError:
            model = MSHEET.Sheet()
        except Exception:
            raise NotImplementedError
            # name = 'OPEN ERROR'
            # summary = TB.format_exc()
            # title = 'Error opening file \'{}\''.format(p_path)
            # model = MSHEET.Sheet(
            #     p_name=name, p_summary=summary, p_title=title)
        return model

    def remove_view(self, p_view: 'ObserverControlSheet') -> None:
        """Stop tracking given sheet view but warn of missing view."""
        id_view = id_view_sheet(p_view_sheet=p_view)
        try:
            self._roster_views.pop(id_view)
        except KeyError:
            logger.warning('Missing: sheet 0x{:X} remove view 0x{:X}  '
                           '({}.{})'.format(id_view, id_factsheet(self),
                                            self.__class__.__name__,
                                            self.remove_view.__name__))
            return

        if not self._roster_views:
            global g_control_app
            g_control_app.close_factsheet(p_control=self)

    def remove_view_is_safe(self) -> bool:
        """Return True when the control can safely close a sheet view.

        A factsheet closes when it has no views.  A sheet control may
        safely close a sheet view when:

        * The factsheet contains no unsaved changes or
        * The factsheet has more than one view or
        * The user approves closing the factsheet.
        """
        if (self.is_stale()
                and not self._is_closing
                and 1 == len(self._roster_views)):
            return False

        return True

    # def _add_new_control_topic(self, px_topic: MTOPIC.Topic
    #                            ) -> CTOPIC.ControlTopic:
    #     """Return a new topic control after adding it to the collection.
    #
    #     :param px_topic: topic model for new control.
    #     """
    #     control_new = CTOPIC.ControlTopic(px_topic)
    #     id_topic = px_topic.tag
    #     self._controls_topic[id_topic] = control_new
    #     return control_new

    # def attach_view_topics(self, p_view: VTYPES.ViewOutlineTopics) -> None:
    #     """Add view of topics outline to model.
    #
    #     :param p_view: topics outline view to add.
    #     """
    #     assert self._model is not None
    #     self._model.attach_view_topics(p_view)

    def clear(self) -> None:
        """Requests topics outline to remove all topics."""
        raise NotImplementedError
        # assert self._model is not None
        # self._model.clear()

    def close_all_views(self) -> GoNoGo:
        """Close the factsheet along with all its sheet views.

        A factsheet may contain unsaved changes.  If closing the
        factsheet would discard unsaved changes, method
        :meth:`.close_all_views` confirms the user approves before
        closing any views.  If no changes would be lost, the method
        closes the factsheet unconditionally.

        :return: GO if there are no unsaved changes or the user
            approves discarding changes.  Otherwise, return NOGO.
        """
        logger.error('close_all_views: stub always returns GO.')
        return GoNoGo.GO

    def delete_force(self) -> None:
        """Delete factsheet unconditionally."""
        raise NotImplementedError
        # assert self._model is not None
        # self._model.detach_all()
        # self._sheets_active.remove(self)

    # def delete_safe(self) -> ABC_SHEET.EffectSafe:
    #     """Delete factsheet provided no changes will be lost.
    #
    #     :returns: Whether delete request completed.
    #     """
    #     assert self._model is not None
    #     if self._model.is_stale():
    #         return ABC_SHEET.EffectSafe.NO_EFFECT
    #
    #     self.delete_force()
    #     return ABC_SHEET.EffectSafe.COMPLETED

    # def detach_page_force(self, pm_page: ABC_SHEET.InterfacePageSheet
    #                       ) -> None:
    #     """Remove page unconditionally.
    #
    #     :param pm_page: page to remove.
    #     """
    #     assert self._model is not None
    #     self._model.detach_page(pm_page)
    #     if 0 == self._model.n_pages():
    #         self._sheets_active.remove(self)

    # def detach_page_safe(self, pm_page: ABC_SHEET.InterfacePageSheet
    #                      ) -> ABC_SHEET.EffectSafe:
    #     """Remove page provided no changes will be lost.
    #
    #     :param pm_page: page to remove.
    #     :returns: Whether remove request completed.
    #     """
    #     assert self._model is not None
    #     if self._model.is_fresh():
    #         self.detach_page_force(pm_page)
    #         return ABC_SHEET.EffectSafe.COMPLETED
    #
    #     if 1 < self._model.n_pages():
    #         self.detach_page_force(pm_page)
    #         return ABC_SHEET.EffectSafe.COMPLETED
    #
    #     return ABC_SHEET.EffectSafe.NO_EFFECT

    # def detach_view_topics(self, p_view: VTYPES.ViewOutlineTopics) -> None:
    #     """Remove view of topics outline from model.
    #
    #     :param p_view: topics outline view to remove.
    #     """
    #     assert self._model is not None
    #     self._model.detach_view_topics(p_view)

    # def extract_topic(self, px_i: MTYPES.IndexTopic) -> None:
    #     """Requests topics outline to remove topic and all descendants.
    #
    #     :param px_i: index of parent topic to remove along with all
    #         descendants.  If index is None, remove no topics.
    #     """
    #     assert self._model is not None
    #     self._model.extract_topic(px_i)

    # def get_control_topic(self, px_topic: MTOPIC.Topic
    #                       ) -> typing.Optional[CTOPIC.ControlTopic]:
    #     """Return topic control for given topic or None when no control.
    #
    #     :param px_topic: topic corresponding to desired control.
    #     """
    #     id_control = px_topic.tag
    #     try:
    #         return self._controls_topic[id_control]
    #     except KeyError:
    #         return None

    # def insert_topic_after(
    #         self, px_topic: MTOPIC.Topic, px_i: MTYPES.IndexTopic
    #         ) -> typing.Tuple[MTYPES.IndexTopic, CTOPIC.ControlTopic]:
    #     """Request topics outline add topic after topic at given index.
    #
    #     See :meth:`.Sheet.insert_topic_after`.
    #
    #     :param px_topic: new topic to add.
    #     :param px_i: index of topic to precede new topic.
    #     :returns: index of and control for newly-added topic.
    #     """
    #     assert self._model is not None
    #     index_new = self._model.insert_topic_after(px_topic, px_i)
    #     control_new = self._add_new_control_topic(px_topic)
    #     return index_new, control_new

    # def insert_topic_before(
    #         self, px_topic: MTOPIC.Topic, px_i: MTYPES.IndexTopic
    #         ) -> typing.Tuple[MTYPES.IndexTopic, CTOPIC.ControlTopic]:
    #     """Request topics outline add topic before topic at given index.
    #
    #     See :meth:`.Sheet.insert_topic_before`.
    #
    #     :param px_topic: new topic to add.
    #     :param px_i: index of topic to follow new topic.
    #     :returns: index of and control for newly-added topic.
    #     """
    #     assert self._model is not None
    #     index_new = self._model.insert_topic_before(px_topic, px_i)
    #     control_new = self._add_new_control_topic(px_topic)
    #     return index_new, control_new

    # def insert_topic_child(
    #         self, px_topic: MTOPIC.Topic, px_i: MTYPES.IndexTopic
    #         ) -> typing.Tuple[MTYPES.IndexTopic, CTOPIC.ControlTopic]:
    #     """Request topics outline add topic as child of topic at given
    #     index.
    #
    #     See :meth:`.Sheet.insert_topic_child`.
    #
    #     :param px_topic: new topic to add.
    #     :param px_i: index of parent topic for new topic.
    #     :returns: index of and control for newly-added topic.
    #     """
    #     assert self._model is not None
    #     index_new = self._model.insert_topic_child(px_topic, px_i)
    #     control_new = self._add_new_control_topic(px_topic)
    #     return index_new, control_new

    def is_fresh(self) -> bool:
        """Return True when there are no unsaved changes to factsheet."""
        return self._model.is_fresh()

    def is_stale(self) -> bool:
        """Return True when there is at least one unsaved change to
        factsheet.
        """
        return self._model.is_stale()

    @property
    def model(self) -> MSHEET.Sheet:
        """Return sheet model."""
        return self._model

    # @classmethod
    # def new(cls, pm_sheets_active: CPOOL.PoolSheets) -> 'ControlSheet':
    #     """Create and return control with default model.
    #
    #     :param pm_sheets_active: collection of open factsheet documents.
    #     :returns: Newly created control.
    #     """
    #     control = ControlSheet(pm_sheets_active)
    #     control._model = MSHEET.Sheet()
    #     return control

    # def new_view_name_active(self) -> MSHEET.ViewNameSheetActive:
    #     """Return editable view of name."""
    #     return self._model.new_view_name_active()
    #
    # def new_view_name_passive(self) -> MSHEET.ViewNameSheetPassive:
    #     """Return display-only view of name."""
    #     return self._model.new_view_name_passive()
    #
    # def new_view_summary_active(self) -> MSHEET.ViewSummarySheetActive:
    #     """Return editable view of summary."""
    #     return self._model.new_view_summary_active()
    #
    # def new_view_summary_passive(self) -> MSHEET.ViewSummarySheetPassive:
    #     """Return display-only view of summary."""
    #     return self._model.new_view_summary_passive()
    #
    # def new_view_title_active(self) -> MSHEET.ViewTitleSheetActive:
    #     """Return editable view of title."""
    #     return self._model.new_view_title_active()
    #
    # def new_view_title_passive(self) -> MSHEET.ViewTitleSheetPassive:
    #     """Return display-only view of title."""
    #     return self._model.new_view_title_passive()

    @classmethod
    def open(cls, p_path: typing.Optional[Path] = None) -> 'ControlSheet':
        """Create and return control with model.

        If given path is None or there is no file at the path location,
        then return control with a new, empty model.  If a file at the
        path location does not contain a factsheet, then return control
        with a new model containing a warning message.  Otherwise,
        return control with model from the factsheet file.

        :param p_path: location of file for factsheet model.
        :returns: Newly created control.
        """
        raise NotImplementedError
        # if p_path is None:
        #     model = MSHEET.Sheet()
        # else:
        #     try:
        #         # with p_path.open(mode='rb') as io_in:
        #         #     model = pickle.load(io_in)
        #         raise NotImplementedError
        #     except Exception:
        #         raise
        #         # name = 'OPEN ERROR'
        #         # summary = TB.format_exc()
        #         # title = 'Error opening file \'{}\''.format(p_path)
        #         # model = MSHEET.Sheet(
        #         #     p_name=name, p_summary=summary, p_title=title)
        # control = ControlSheet(p_path=p_path)
        # return control

    def _open_guard(self) -> typing.BinaryIO:
        """Backup existing file when opening for save.

        Backup provides (minimal) guard against inadvertent overwrite.
        Backup and open are combined to minimize risk of race condition.

        :raises OSError: When control cannot open file at control's
           path.
        :returns: Open file object at control's path.
        """
        raise NotImplementedError
        # assert self._path is not None
        # try:
        #     io_out = self._path.open(mode='xb')
        # except OSError as err:
        #     if errno.EEXIST == err.errno:
        #         self._path.replace(str(self._path) + '~')
        #         io_out = self._path.open(mode='xb')
        #     else:
        #         raise
        # return io_out

    @property
    def path(self) -> typing.Optional[Path]:
        """Return path to file containing factsheet contents."""
        return self._path

    def present_views(self, p_time: int) -> None:
        """Make all sheet views visible to user.

        :param p_time: time stamp of event requesting presentation.
        """
        raise NotImplementedError
        # assert self._model is not None
        # self._model.present_pages(p_time)

    def save(self) -> None:
        """Save factsheet contents to file.

        Log a warning when control has no file path.

        :raises OSError: when control cannot open file at path.
        """
        raise NotImplementedError
        # assert self._model is not None
        # if self._path is None:
        #     logger.warning('No file path ({}.{})'.format(
        #         self.__class__.__name__, self.save.__name__))
        #     return
        #
        # self._model.set_fresh()
        # with self._open_guard() as io_out:
        #     pickle.dump(self._model, io_out)

    def save_as(self, p_path: Path) -> None:
        """Save factsheet contents to file at given path.

        :param p_path: file system path to file.
        :raises OSError: when control cannot open file at path.
        """
        raise NotImplementedError
        # self._path = p_path
        # subtitle_base = self._path.name
        # assert self._model is not None
        # self._model.update_titles(subtitle_base)
        # self.save()

    # @property
    # def sheets_active(self) -> CPOOL.PoolSheets:
    #     """Return collection of active factsheets."""
    #     return self._sheets_active


class ObserverControlSheet(abc.ABC):
    """Define interface for sheet control to notify a sheet view observer.

    In general, a sheet view requests services from its sheet control.
    For a few exceptions, a sheet view acts as an observer of its sheet
    control.  A sheet control notifies its views when to present to the
    user and when to close.
    """

    @abc.abstractmethod
    def close(self) -> None:
        """Close sheet view."""
        raise NotImplementedError

    @abc.abstractmethod
    def present(self, p_time: int) -> None:
        """Present sheet view to user.

        :param time: time stamp to order multiple, independent requests.
        """
        raise NotImplementedError
