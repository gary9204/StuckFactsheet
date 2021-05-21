"""
Module in transition.  Preparing to move content to
:mod:`~factsheet.control.sheet`.
"""
import logging
from pathlib import Path
import typing   # noqa

# from factsheet.abc_types import abc_sheet as ABC_SHEET


logger = logging.getLogger('Main.CPOOL')

_m_factsheets: typing.MutableMapping[int, 'ControlSheet'] = dict()


def open_factsheet(p_path: typing.Optional[Path] = None
                   ) -> 'ControlSheet':
    """Return and track a new factsheet or return and present an
    existing factsheet.

    Functions :func:`open_factsheet` and :func:`close_factsheet`
    maintain a collection of open factsheets as a singleton.

    :param p_path: location of factsheet in filesystem.  If there is no
        file at the given location, create and return a new factsheet.
    """
    if p_path is None:
        control = ControlSheet.open(None)
        _m_factsheets[id(control)] = control
        return control
    raise NotImplementedError
    path_absolute = p_path.resolve()
    for control in _m_factsheets.values():
        if control._path is not None:
            if path_absolute == control._path.resolve():
                control.present()
                return


def close_factsheet(p_control: 'ControlSheet') -> None:
    """Close and stop tracking factsheet.

    Log a warning when the control is not in the collection.
    Functions :func:`open_factsheet` and :func:`close_factsheet`
    maintain a collection of open factsheets as a singleton.

    :param p_control: factsheet to close.
    """
    raise NotImplementedError
    # id_control = id(px_control)
    # try:
    #     self._controls.pop(id_control)
    # except KeyError:
    #     logger.warning('Missing control: {} ({}.{})'.format(
    #         hex(id_control), self.__class__.__name__,
    #         self.remove.__name__))


class ControlSheet:
    """Temporary placeholder"""
    def __init__(self):
        self._path = None
        self.present_called = False

    @classmethod
    def open(cls, p_path: typing.Optional[Path] = None) -> 'ControlSheet':
        control = ControlSheet()
        control._path = p_path
        return control

    def present(self):
        self.present_called = True
