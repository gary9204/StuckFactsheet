"""
Defines class that mediates factsheet-level interaction from
:mod:`~factsheet.view` to :mod:`~factsheet.model`.

:doc:`../guide/devel_notes` explains how application Factsheet is based
on a Model-View-Controller (MVC) design.  Module ``control_sheet``
defines classes representing control components for a factsheet as a
whole.
"""
import errno
import logging
from pathlib import Path
import pickle
import traceback as TB
import typing   # noqa

from factsheet.abc_types import abc_sheet as ABC_SHEET
from factsheet.control import pool as CPOOL
from factsheet.control import control_topic as CTOPIC
from factsheet.model import sheet as MSHEET
from factsheet.model import topic as MTOPIC
from factsheet.view import ui as UI

logger = logging.getLogger('Main.CSHEET')


class ControlSheet(ABC_SHEET.InterfaceControlSheet):
    """Mediates user actions at view to model updates for a factsheet.

    Class ``ControlSheet`` translates user requests in a factsheet page
    into changes in the factsheet model (such as save or delete) or in
    the collection of factsheet views (such as add or close a view).

    :param pm_sheets_active: collection of open factsheet documents.
    """

    def __init__(self, pm_sheets_active: CPOOL.PoolSheets) -> None:
        self._model: typing.Optional[MSHEET.Sheet] = None
        self._path: typing.Optional[Path] = None
        self._sheets_active = pm_sheets_active
        self._sheets_active.add(self)
        self._controls_topic: typing.Dict[
            UI.IdTopic, CTOPIC.ControlTopic] = dict()

    def _add_new_control_topic(self, px_topic: MTOPIC.Topic
                               ) -> CTOPIC.ControlTopic:
        """Return a new topic control after adding it to the collection.

        :param px_topic: topic model for new control.
        """
        control_new = CTOPIC.ControlTopic(px_topic)
        id_topic = px_topic.id_topic
        self._controls_topic[id_topic] = control_new
        return control_new

    def attach_page(self, pm_page: ABC_SHEET.InterfacePageSheet) -> None:
        """Add page to model.

        :param pm_page: page to add.
        """
        assert self._model is not None
        self._model.attach_page(pm_page)
        self.new_name()

    def clear(self) -> None:
        """Requests topics outline to remove all topics."""
        assert self._model is not None
        self._model.clear()

    def delete_force(self) -> None:
        """Delete factsheet unconditionally."""
        assert self._model is not None
        self._model.detach_all()
        self._sheets_active.remove(self)

    def delete_safe(self) -> ABC_SHEET.EffectSafe:
        """Delete factsheet provided no changes will be lost.

        :returns: Whether delete request completed.
        """
        assert self._model is not None
        if self._model.is_stale():
            return ABC_SHEET.EffectSafe.NO_EFFECT

        self.delete_force()
        return ABC_SHEET.EffectSafe.COMPLETED

    def detach_page_force(self, pm_page: ABC_SHEET.InterfacePageSheet
                          ) -> None:
        """Remove page unconditionally.

        :param pm_page: page to remove.
        """
        assert self._model is not None
        self._model.detach_page(pm_page)
        if 0 == self._model.n_pages():
            self._sheets_active.remove(self)

    def detach_page_safe(self, pm_page: ABC_SHEET.InterfacePageSheet
                         ) -> ABC_SHEET.EffectSafe:
        """Remove page provided no changes will be lost.

        :param pm_page: page to remove.
        :returns: Whether remove request completed.
        """
        assert self._model is not None
        if self._model.is_fresh():
            self.detach_page_force(pm_page)
            return ABC_SHEET.EffectSafe.COMPLETED

        if 1 < self._model.n_pages():
            self.detach_page_force(pm_page)
            return ABC_SHEET.EffectSafe.COMPLETED

        return ABC_SHEET.EffectSafe.NO_EFFECT

    def extract_topic(self, px_i: UI.IndexOutline) -> None:
        """Requests topics outline to remove topic and all descendants.

        :param px_i: index of parent topic to remove along with all
            descendants.  If index is None, remove no topics.
        """
        assert self._model is not None
        self._model.extract_topic(px_i)

    def get_control_topic(self, px_topic: MTOPIC.Topic
                          ) -> typing.Optional[CTOPIC.ControlTopic]:
        """Return topic control for given topic or None when no control.

        :param px_topic: topic corresponding to desired control.
        """
        id_control = px_topic.id_topic
        try:
            return self._controls_topic[id_control]
        except KeyError:
            return None

    def insert_topic_after(
            self, px_topic: MTOPIC.Topic, px_i: UI.IndexOutline
            ) -> typing.Tuple[CTOPIC.ControlTopic, UI.IndexOutline]:
        """Requests topics outline add topic after topic at given index.

        See :meth:`~.model.sheet.Sheet.insert_topic_after`.

        :param px_topic: new topic to add.
        :param px_i: index of topic to precede new topic.
        :returns: index of newly-added topic.
        """
        assert self._model is not None
        index_new = self._model.insert_topic_after(px_topic, px_i)
        control_new = self._add_new_control_topic(px_topic)
        return index_new, control_new

    def insert_topic_before(
            self, px_topic: MTOPIC.Topic, px_i: UI.IndexOutline
            ) -> typing.Tuple[CTOPIC.ControlTopic, UI.IndexOutline]:
        """Requests topics outline add topic before topic at given index.

        See :meth:`~.model.sheet.Sheet.insert_topic_before`.

        :param px_topic: new topic to add.
        :param px_i: index of topic to follow new topic.
        :returns: index of newly-added topic.
        """
        assert self._model is not None
        index_new = self._model.insert_topic_before(px_topic, px_i)
        control_new = self._add_new_control_topic(px_topic)
        return index_new, control_new

    def insert_topic_child(
            self, px_topic: MTOPIC.Topic, px_i: UI.IndexOutline
            ) -> typing.Tuple[CTOPIC.ControlTopic, UI.IndexOutline]:
        """Requests topics outline add topic as child of topic at given
        index.

        See :meth:`~.model.sheet.Sheet.insert_topic_child`.

        :param px_topic: new topic to add.
        :param px_i: index of parent topic for new topic.
        :returns: index of newly-added topic.
        """
        assert self._model is not None
        index_new = self._model.insert_topic_child(px_topic, px_i)
        control_new = self._add_new_control_topic(px_topic)
        return index_new, control_new

    @classmethod
    def new(cls, pm_sheets_active: CPOOL.PoolSheets) -> 'ControlSheet':
        """Create and return control with default model.

        :param pm_sheets_active: collection of open factsheet documents.
        :returns: Newly created control.
        """
        control = ControlSheet(pm_sheets_active)
        control._model = MSHEET.Sheet()
        return control

    def new_name(self) -> None:
        """Notify model a page changed factsheet name."""
        if self._path is None:
            subtitle_base = 'Unsaved'
        else:
            subtitle_base = self._path.name
        assert self._model is not None
        self._model.update_titles(subtitle_base)

    @classmethod
    def open(cls, pm_sheets_active: CPOOL.PoolSheets, p_path: Path
             ) -> 'ControlSheet':
        """Create and return control with model from file.

        :param pm_sheets_active: collection of open factsheet documents.
        :param p_path: location of file containing factsheet model.
        :returns: Newly created control.
        """
        control = ControlSheet(pm_sheets_active)
        try:
            with p_path.open(mode='rb') as io_in:
                model = pickle.load(io_in)
        except Exception:
            name = 'OPEN ERROR'
            summary = TB.format_exc()
            title = 'Error opening file \'{}\''.format(p_path)
            control._model = MSHEET.Sheet(
                p_name=name, p_summary=summary, p_title=title)
        else:
            control._model = model
            control._path = p_path

        return control

    def _open_guard(self) -> typing.BinaryIO:
        """Backup existing file when opening for save.

        Backup provides (minimal) guard against inadvertent overwrite.
        Backup and open are combined to minimize risk of race condition.

        :raises OSError: When control cannot open file at control's
           path.
        :returns: Open file object at control's path.
        """
        assert self._path is not None
        try:
            io_out = self._path.open(mode='xb')
        except OSError as err:
            if errno.EEXIST == err.errno:
                self._path.replace(str(self._path) + '~')
                io_out = self._path.open(mode='xb')
            else:
                raise
        return io_out

    @property
    def path(self) -> typing.Optional[Path]:
        """Return path to file containing factsheet contents."""
        return self._path

    def present_factsheet(self, p_time: int) -> None:
        """Make all factsheet pages visible to user.

        :param p_time: timestamp of event requesting presentation.
        """
        assert self._model is not None
        self._model.present_pages(p_time)

    def save(self) -> None:
        """Save factsheet contents to file.

        Log a warning when control has no file path.

        :raises OSError: when control cannot open file at path.
        """
        assert self._model is not None
        if self._path is None:
            logger.warning('No file path ({}.{})'.format(
                self.__class__.__name__, self.save.__name__))
            return

        self._model.set_fresh()
        with self._open_guard() as io_out:
            pickle.dump(self._model, io_out)

    def save_as(self, p_path: Path) -> None:
        """Save factsheet contents to file at given path.

        :param p_path: file system path to file.
        :raises OSError: when control cannot open file at path.
        """
        self._path = p_path
        subtitle_base = self._path.name
        assert self._model is not None
        self._model.update_titles(subtitle_base)
        self.save()

    @property
    def sheets_active(self) -> CPOOL.PoolSheets:
        """Return collection of active factsheets."""
        return self._sheets_active
