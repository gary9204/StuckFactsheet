"""
Defines class to track and maintain collection of active factsheets.
"""
import logging
from pathlib import Path
import typing   # noqa

from factsheet.abc_types import abc_sheet as ABC_SHEET

logger = logging.getLogger('Main.CPOOL')


class PoolSheets:
    """Represents collection of active factsheets identified by
    control :class:`~.control.sheet.Sheet`.
    """
    def __init__(self) -> None:
        self._controls: typing.Dict[int, ABC_SHEET.InterfaceControlSheet] = (
            dict())

    def add(self, px_control: ABC_SHEET.InterfaceControlSheet) -> None:
        """Add control to collection.

        Log a warning when the control is in the collection already.
        """
        id_control = id(px_control)
        if id_control in self._controls.keys():
            logger.warning('Duplicate control: {} ({}.{})'.format(
                hex(id_control), self.__class__.__name__,
                self.add.__name__))
            return
        self._controls[id_control] = px_control

    def owner_file(self, p_path: Path
                   ) -> typing.Optional[ABC_SHEET.InterfaceControlSheet]:
        """Return control with given path or None."""
        path_absolute = p_path.resolve()
        for control in self._controls.values():
            if control.path is None:
                continue
            if path_absolute == control.path.resolve():
                return control
        return None

    def remove(self, px_control: ABC_SHEET.InterfaceControlSheet) -> None:
        """Remove control from collection.

        Log a warning when the control is not in the collection.
        """
        id_control = id(px_control)
        try:
            self._controls.pop(id_control)
        except KeyError:
            logger.warning('Missing control: {} ({}.{})'.format(
                hex(id_control), self.__class__.__name__,
                self.remove.__name__))
