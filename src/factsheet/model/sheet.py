"""
Defines :mod:`~factsheet.model` for a Factsheet document.
"""
import logging
import typing   # noqa

from factsheet.abc_types import abc_infoid as ABC_INFOID
from factsheet.model import infoid as MINFOID
# from factsheet.view import page_sheet as VSHEET
from factsheet.abc_types import abc_sheet as ABC_SHEET

logger = logging.getLogger('Main.model.sheet')


class Sheet(ABC_INFOID.InterfaceStaleFile):
    """Factsheet document :mod:`~factsheet.model`.

    `Sheet` represents an entire Factsheet document.  A model factsheet
    consists of a hierarchy of topics along with identification
    information (see :mod:`~factsheet.model` class :class:`.InfoId`.)
    Each topic represents a collection of facts about a specific
    subject.

    :param p_title: title of factsheet.
    """
    #: Identifies role of model component.
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

    def __init__(self, *, p_title: str = '') -> None:
        self._infoid = MINFOID.InfoId(
            p_aspect=self.ASPECT, p_title=p_title)
        self._state_transient()

    def __setstate__(self, px_state: typing.Dict) -> None:
        """Reconstruct factsheet model from state pickle loads.

        Reconstructed attribute is marked fresh and has views.

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
            self._detach_page_views(page)
            page.close_page()

    def detach_page(self, pm_page: ABC_SHEET.InterfacePageSheet) -> None:
        """Remove one page from sheet.

        Log warning when requested page is not attached.

        :param px_observer: page to remove.
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

        self._detach_page_views(pm_page)

    def _detach_page_views(
            self, pm_page: ABC_SHEET.InterfacePageSheet) -> None:
        """For each sheet component, remove the view for the component.

        :param pm_page: page with views to remove.
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

    def set_fresh(self) -> None:
        """Mark factsheet in memory consistent with file contents."""
        self._stale = False
        self._infoid.set_fresh()

    def set_stale(self) -> None:
        """Mark factsheet in memory changed from file contents."""
        self._stale = True
