"""
Unit tests for class that tracks and maintains pool of active
factsheets.

See :mod:`.pool`.
"""
import logging
from pathlib import Path
import pytest   # type: ignore[import]

from factsheet.control import pool as CPOOL


@pytest.fixture
def patch_sheet():
    class Sheet:
        def __init__(self): pass

    return Sheet


class TestPoolSheets:
    """Unit tests for :class:`.PoolSheets`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        # Test
        target = CPOOL.PoolSheets()
        assert isinstance(target._controls, dict)
        assert not target._controls

    def test_add(self, patch_sheet):
        """Confirm addition of control.
        Case: control not in collection initially
        """
        # Setup
        N_CONTROLS = 3
        controls = [patch_sheet() for _ in range(N_CONTROLS)]
        target = CPOOL.PoolSheets()
        # Test
        for control in controls:
            target.add(control)
        assert len(controls) == len(target._controls)
        for control in controls:
            assert target._controls[id(control)] is control

    def test_add_warn(self, patch_sheet, PatchLogger, monkeypatch):
        """Confirm addition of control.
        Case: control in collection initially
        """
        # Setup
        N_CONTROLS = 3
        controls = [patch_sheet() for _ in range(N_CONTROLS)]
        target = CPOOL.PoolSheets()
        for control in controls:
            target.add(control)
        assert len(controls) == len(target._controls)

        I_DUP = 1
        duplicate = controls[I_DUP]

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = (
            'Duplicate control: {} (PoolSheets.add)'
            ''.format(hex(id(duplicate))))
        # Test
        target.add(duplicate)
        assert len(controls) == len(target._controls)
        for control in controls:
            assert target._controls[id(control)] is control
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message

    def test_owner_file(self, patch_sheet, tmp_path):
        """Confirm result of owner search.
        Case: owner not found
        """
        # Setup
        target = CPOOL.PoolSheets()
        N_CONTROLS = 3
        controls = list()
        for i in range(N_CONTROLS):
            control = patch_sheet()
            control.path = Path(tmp_path / ('file ' + str(i)))
            controls.append(control)
            target.add(control)
        assert len(controls) == len(target._controls)

        path_missing = Path(tmp_path / 'banana')
        # Test
        assert target.owner_file(path_missing) is None

    def test_owner_file_found(self, patch_sheet, tmp_path):
        """Confirm result of owner search.
        Case: owner found
        """
        # Setup
        target = CPOOL.PoolSheets()
        N_CONTROLS = 4
        controls = list()
        for i in range(N_CONTROLS):
            control = patch_sheet()
            control.path = Path(tmp_path / ('file ' + str(i)))
            controls.append(control)
            target.add(control)
        assert len(controls) == len(target._controls)

        I_NO_PATH = 1
        controls[I_NO_PATH].path = None

        I_OWNER = 2
        owner = controls[I_OWNER]
        path_owner = owner.path
        # Test
        assert target.owner_file(path_owner) is owner

    def test_remove(self, patch_sheet):
        """Confirm removal of control.
        Case: control in collection
        """
        # Setup
        N_CONTROLS = 3
        controls = [patch_sheet() for _ in range(N_CONTROLS)]
        target = CPOOL.PoolSheets()
        for control in controls:
            target.add(control)
        assert len(controls) == len(target._controls)

        I_REMOVE = 1
        removed = controls.pop(I_REMOVE)
        # Test
        target.remove(removed)
        assert id(removed) not in target._controls.keys()
        assert len(controls) == len(target._controls)
        for control in controls:
            assert target._controls[id(control)] is control

    def test_remove_warn(self, patch_sheet, PatchLogger, monkeypatch):
        """Confirm removal of control.
        Case: control not in collection
        """
        # Setup
        N_CONTROLS = 3
        controls = [patch_sheet() for _ in range(N_CONTROLS)]
        target = CPOOL.PoolSheets()
        for control in controls:
            target.add(control)
        assert len(controls) == len(target._controls)

        I_REMOVED = 1
        removed = controls.pop(I_REMOVED)
        target.remove(removed)
        assert id(removed) not in target._controls.keys()

        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = (
            'Missing control: {} (PoolSheets.remove)'
            ''.format(hex(id(removed))))
        # Test
        target.remove(removed)
        assert id(removed) not in target._controls.keys()
        assert len(controls) == len(target._controls)
        for control in controls:
            assert target._controls[id(control)] is control
        assert patch_logger.called
        assert PatchLogger.T_WARNING == patch_logger.level
        assert log_message == patch_logger.message
