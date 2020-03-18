"""
Defines class to mediates from :mod:`~factsheet.view` to
:mod:`~factsheet.model` of a factsheet.
"""
import errno
import logging
from pathlib import Path
import pickle
import typing   # noqa

from factsheet.abc_types import abc_sheet as ABC_SHEET
from factsheet.model import sheet as MSHEET

logger = logging.getLogger('Main.CSHEET')


class Sheet(object):
    """Mediates user actions at view to model updates for a factsheet.

    Class 'Sheet` translates user requests in a factsheet page
    into changes in the factsheet model (such as save or delete) or in
    the collection of factsheet views (such as add or close a view).
    """

    def __init__(self) -> None:
        self._model: typing.Optional[MSHEET.Sheet] = None
        self._path: typing.Optional[Path] = None

    def attach_page(self, pm_page: ABC_SHEET.InterfacePageSheet) -> None:
        """Add page to model."""
        assert self._model is not None
        self._model.attach_page(pm_page)

    def delete_force(self) -> None:
        """Delete factsheet unconditionally."""
        assert self._model is not None
        self._model.detach_all()

    def delete_safe(self) -> ABC_SHEET.EffectSafe:
        """Delete factsheet provided no changes will be lost."""
        assert self._model is not None
        if self._model.is_stale():
            return ABC_SHEET.EffectSafe.NO_EFFECT

        self._model.detach_all()
        return ABC_SHEET.EffectSafe.COMPLETED

    def detach_page_force(self, pm_page) -> None:
        """Remove page unconditionally."""
        assert self._model is not None
        self._model.detach_page(pm_page)

    def detach_page_safe(self, pm_page) -> ABC_SHEET.EffectSafe:
        """Remove page provided no changes will be lost."""
        assert self._model is not None
        if self._model.is_fresh():
            self.detach_page_force(pm_page)
            return ABC_SHEET.EffectSafe.COMPLETED

        if 1 < self._model.n_pages():
            self.detach_page_force(pm_page)
            return ABC_SHEET.EffectSafe.COMPLETED

        return ABC_SHEET.EffectSafe.NO_EFFECT

    def save(self) -> None:
        """Save factsheet contents to file.

        Log a warning when control has no file path.
        """
        assert self._model is not None
        if self._path is None:
            logger.warning('No file path ({}.{})'.format(
                self.__class__.__name__, self.save.__name__))
            return

        self._model.set_fresh()
        with self._open_guard() as io_out:
            pickle.dump(self._model, io_out)

    def _open_guard(self) -> typing.BinaryIO:
        """Backup existing file when opening for save.

        Backup provides (minimal) guard against inadvertent overwrite.
        Backup and open are combined to minimize risk of race condition.
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

    def save_as(self, p_path: Path) -> None:
        """Save factsheet contents to file at given path.

        :param path: file system path to file.
        """
        self._path = p_path
        self.save()

    @classmethod
    def open(cls, p_path: Path) -> 'Sheet':
        """Create control with model from file."""
        control = Sheet()
        try:
            with p_path.open(mode='rb') as io_in:
                model = pickle.load(io_in)
        except Exception:
            # err = TB.format_exc()
            title = 'Error opening file \'{}\''.format(p_path)
            # Reminder: deecopy default factsheet and set attributes
            control._model = MSHEET.Sheet(p_title=title)
        else:
            control._model = model
            control._path = p_path

        return control

    @classmethod
    def new(cls) -> 'Sheet':
        """Create control with default model."""
        control = Sheet()
        control._model = MSHEET.Sheet()
        return control

    @property
    def path(self) -> typing.Optional[Path]:
        """Return path to file containing factsheet contents."""
        return self._path
