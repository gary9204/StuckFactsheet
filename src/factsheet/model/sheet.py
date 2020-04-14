"""
Defines factsheet-level model.

:doc:`../guide/devel_notes` explains how application Factsheet is based
on a Model-View-Controller (MVC) design.  The design is partitioned into
factsheet, topic, and fact layers.  Module ``sheet`` defines
class representing the model of a factsheet.
"""
import logging
import typing   # noqa

from factsheet.abc_types import abc_stalefile as ABC_STALE
from factsheet.model import infoid as MINFOID
from factsheet.abc_types import abc_sheet as ABC_SHEET

logger = logging.getLogger('Main.model.sheet')


class Sheet(ABC_STALE.InterfaceStaleFile):
    """Factsheet document :mod:`~factsheet.model`.

    Class ``Sheet`` represents an entire Factsheet document.  A model
    factsheet consists of a hierarchy of topics along with
    identification information (see :class:`.InfoId`.) Each topic
    represents a collection of facts about a specific subject.

    :param p_name: name of factsheet.
    :param p_summary: summary of factsheet.
    :param p_title: title of factsheet.

    .. attribute:: ASPECT

       Identifies role of model component.
    """
    ASPECT = 'factsheet'

    def __eq__(self, px_other: typing.Any) -> bool:
        """Return True when px_other has same identification information.

        :param px_other: object to compare with self.
        """
        if not isinstance(px_other, Sheet):
            return False

        if self._infoid != px_other._infoid:
            return False

        return True

    def __getstate__(self) -> typing.Dict:
        """Return factsheet model in form pickle can persist.

        Persistent form of factsheet excludes run-time information .
        """
        state = self.__dict__.copy()
        del state['_pages']
        del state['_stale']
        return state

    def __init__(self, *, p_name: str = 'Unnamed', p_summary: str = '',
                 p_title: str = '') -> None:
        self._infoid = MINFOID.InfoId(p_aspect=self.ASPECT, p_name=p_name,
                                      p_summary=p_summary, p_title=p_title)
        self._state_transient()

    def __setstate__(self, px_state: typing.Dict) -> None:
        """Reconstruct factsheet model from state pickle loads.

        Reconstructed attribute is marked fresh and has no views.

        :param px_state: unpickled state of stored factsheet model.
        """
        self.__dict__.update(px_state)
        self._state_transient()

    def _state_transient(self) -> None:
        """Helper ensures __init__ and __setstate__ are consistent."""
        self._stale = False
        self._pages: typing.Dict[int, ABC_SHEET.InterfacePageSheet] = dict()

    def attach_page(self, pm_page: ABC_SHEET.InterfacePageSheet) -> None:
        """Add page to update display when sheet changes.

        Log warning when requested page is already attached.

        :param pm_page: page to add.
        """
        id_page = id(pm_page)
        if id_page in self._pages.keys():
            logger.warning(
                'Duplicate page: {} ({}.{})'.format(
                    hex(id_page),
                    self.__class__.__name__, self.attach_page.__name__))
            return

        self._infoid.attach_view(pm_page.get_infoid())
        self._pages[id(pm_page)] = pm_page

    def detach_all(self) -> None:
        """Detach all pages from sheet."""
        while self._pages:
            _id_page, page = self._pages.popitem()
            self._detach_attribute_views(page)
            page.close_page()

    def detach_page(self, pm_page: ABC_SHEET.InterfacePageSheet) -> None:
        """Remove one page from sheet.

        Log warning when requested page is not attached.

        :param px_view: page to remove.
        """
        id_page = id(pm_page)
        try:
            self._pages.pop(id_page)
        except KeyError:
            logger.warning(
                'Missing page: {} ({}.{})'.format(
                    hex(id_page),
                    self.__class__.__name__, self.detach_page.__name__))
            return

        self._detach_attribute_views(pm_page)

    def _detach_attribute_views(
            self, pm_page: ABC_SHEET.InterfacePageSheet) -> None:
        """For each sheet attribute with a distinct view, remove the
        view for the attribute.

        :param pm_page: page for factsheet as a whole.
        """
        self._infoid.detach_view(pm_page.get_infoid())

    def is_fresh(self) -> bool:
        """Return True when there are no unsaved changes to factsheet."""
        if self._stale:
            return False

        if self._infoid.is_stale():
            self._stale = True
            return False

        return True

    def is_stale(self) -> bool:
        """Return True when there is at least one unsaved change to
        factsheet.
        """
        if self._stale:
            return True

        if self._infoid.is_stale():
            self._stale = True
            return True

        return False

    def n_pages(self) -> int:
        """Return number of pages attached to factsheet."""
        return len(self._pages)

    def present_pages(self, p_time: int) -> None:
        """Notify all pages to make them visible to user.

        :param p_time: timestamp of event requesting presentation.
        """
        for page in self._pages.values():
            page.present(p_time)

    def set_fresh(self) -> None:
        """Mark factsheet in memory consistent with file contents."""
        self._stale = False
        self._infoid.set_fresh()

    def set_stale(self) -> None:
        """Mark factsheet in memory changed from file contents."""
        self._stale = True

    def update_titles(self, p_subtitle_base: str) -> None:
        """Notify each page to update titles in page's window.

        Each page receives a subtitle that identifies both the factsheet
        and page.

        :param p_subtitle_base: common part of all subtitles.
        """
        id_model = self._infoid.id_model
        text_model = hex(id_model)[-3:].upper()
        for id_page, page in self._pages.items():
            text_page = hex(id_page)[-3:].upper()
            subtitle = '{} ({}:{})'.format(
                p_subtitle_base, text_model, text_page)
            page.set_titles(subtitle)
