"""
Defines class to track and maintain collection of active factsheets.
"""
import logging
from pathlib import Path
import typing   # noqa

from factsheet.control import sheet as CSHEET   # noqa

logger = logging.getLogger('Main.CPOOL')


class PoolSheets:
    """Represents collection of active factsheets identified by
    :mod:`~factsheet.control` :class:`~.control.sheet.Sheet`.
    """
    def __init__(self) -> None:
        self._controls: typing.Dict[int, CSHEET.Sheet] = dict()

    def add(self, px_control: CSHEET.Sheet) -> None:
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

    def owner_file(self, p_path: Path) -> typing.Optional[CSHEET.Sheet]:
        """Return control with given path or None."""
        for control in self._controls.values():
            assert control.path is not None
            if p_path.resolve() == control.path.resolve():
                return control
        return None

    def remove(self, px_control: CSHEET.Sheet) -> None:
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
