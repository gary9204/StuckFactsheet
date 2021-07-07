"""
Unit tests for class that tracks and maintains pool of active
factsheets.  See :mod:`.pool`.
"""
import logging
from pathlib import Path
import pytest   # type: ignore[import]

from factsheet.control import pool as CPOOL


class TestOpenFactsheet:
    """Unit tests for :class:`.PoolSheets`."""

    def test_open_factsheet_none(self):
        """| Confirm factsheet open and return.
        | Case: new factsheet without path
        """
        # Setup
        CPOOL._m_factsheets.clear()
        # Test
        target = CPOOL.open_factsheet()
        assert isinstance(target, CPOOL.StubControlSheet)
        assert target is CPOOL._m_factsheets[id(target)]

    def test_open_factsheet_new(self, tmp_path):
        """| Confirm factsheet open and return.
        | Case: new factsheet with path
        """
        # Setup
        CPOOL._m_factsheets.clear()
        N_CONTROLS = 5
        PATH_BASE = Path(tmp_path)
        for i in range(N_CONTROLS):
            control = CPOOL.open_factsheet()
            path = PATH_BASE / '/factsheet{}.fsg'.format(i)
            control._path = path
        PATH_DIFF = PATH_BASE / '/scd.fsg'
        # Test
        target = CPOOL.open_factsheet(PATH_DIFF)
        assert isinstance(target, CPOOL.StubControlSheet)
        assert PATH_DIFF == target._path
        assert N_CONTROLS + 1 == len(CPOOL._m_factsheets)
        assert target is CPOOL._m_factsheets[id(target)]

    def test_open_factsheet_existing(self, tmp_path):
        """| Confirm factsheet open and return.
        | Case: existing factsheet file at path
        """
        # Setup
        CPOOL._m_factsheets.clear()
        N_CONTROLS = 5
        I_MATCH = 4
        PATH_BASE = Path(tmp_path)
        for i in range(N_CONTROLS):
            control = CPOOL.open_factsheet()
            path = PATH_BASE / '/factsheet{}.fsg'.format(i)
            control._path = path
            if i == I_MATCH:
                path_match = path
                control_match = control
        # Test
        target = CPOOL.open_factsheet(path_match)
        assert isinstance(target, CPOOL.StubControlSheet)
        assert target is control_match
        assert N_CONTROLS == len(CPOOL._m_factsheets)
        assert target is CPOOL._m_factsheets[id(target)]

    @pytest.mark.skip
    def test_open_factsheet_except(self):
        """| Confirm factsheet open and return.
        | Case: file at path cannot be read
        """
        # # Setup
        # N_CONTROLS = 3
        # controls = [patch_sheet() for _ in range(N_CONTROLS)]
        # # Test
        # for control in controls:
        #     target.add(control)
        # assert len(controls) == len(target._controls)
        # for control in controls:
        #     assert target._controls[id(control)] is control

    @pytest.mark.skip
    def test_open_factsheet_multiple(self):
        """| Confirm factsheet open and return.
        | Case: file at path cannot be read
        """
        # # Setup
        # N_CONTROLS = 3
        # controls = [patch_sheet() for _ in range(N_CONTROLS)]
        # # Test
        # for control in controls:
        #     target.add(control)
        # assert len(controls) == len(target._controls)
        # for control in controls:
        #     assert target._controls[id(control)] is control


class TestCloseFactsheet:
    """Unit tests for :class:`.PoolSheets`."""

    @pytest.mark.skip
    def test_close_factsheet(self):
        """| Confirm factsheet close.
        | Case: existing control
        """
        # # Setup
        # N_CONTROLS = 3
        # controls = [patch_sheet() for _ in range(N_CONTROLS)]
        # for control in controls:
        #     target.add(control)
        # assert len(controls) == len(target._controls)
        #
        # I_REMOVE = 1
        # removed = controls.pop(I_REMOVE)
        # # Test
        # target.remove(removed)
        # assert id(removed) not in target._controls.keys()
        # assert len(controls) == len(target._controls)
        # for control in controls:
        #     assert target._controls[id(control)] is control

    @pytest.mark.skip
    def test_close_factsheet_warn(self, PatchLogger, monkeypatch):
        """| Confirm factsheet close.
        | Case: control not found
        """
        # # Setup
        # N_CONTROLS = 3
        # controls = [patch_sheet() for _ in range(N_CONTROLS)]
        # for control in controls:
        #     target.add(control)
        # assert len(controls) == len(target._controls)
        #
        # I_REMOVED = 1
        # removed = controls.pop(I_REMOVED)
        # target.remove(removed)
        # assert id(removed) not in target._controls.keys()
        #
        # patch_logger = PatchLogger()
        # monkeypatch.setattr(
        #     logging.Logger, 'warning', patch_logger.warning)
        # log_message = (
        #     'Missing control: {} (PoolSheets.remove)'
        #     ''.format(hex(id(removed))))
        # # Test
        # target.remove(removed)
        # assert id(removed) not in target._controls.keys()
        # assert len(controls) == len(target._controls)
        # for control in controls:
        #     assert target._controls[id(control)] is control
        # assert patch_logger.called
        # assert PatchLogger.T_WARNING == patch_logger.level
        # assert log_message == patch_logger.message
