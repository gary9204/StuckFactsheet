"""
Unit tests for class that mediates from :mod:`~factsheet.view` to
:mod:`~factsheet.model` of a factsheet
"""
import logging
from pathlib import Path
import pickle
import pytest   # type: ignore[import]

from factsheet.abc_types import abc_sheet as ABC_SHEET
from factsheet.control import sheet as CSHEET
from factsheet.control import pool as CPOOL
from factsheet.model import sheet as MSHEET


@pytest.fixture
def patch_model_safe():
    class PatchSafe(MSHEET.Sheet):
        def __init__(self, p_stale, p_n_pages):
            super().__init__()
            self._stale = p_stale
            self._n_pages = p_n_pages
            self.n_detach = 0

        def n_pages(self) -> int:
            return self._n_pages

        def detach_page(self, _view):
            self.n_detach += 1

    return PatchSafe


class TestControlSheet:
    """Unit tests for control class Sheet."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        sheets_active = CPOOL.PoolSheets()
        # Test
        target = CSHEET.Sheet(sheets_active)
        assert target._model is None
        assert target._path is None
        assert target._sheets_active is sheets_active
        assert sheets_active._controls[id(target)] is target

    def test_attach_page(self, monkeypatch):
        """Confirm page addition."""
        # Setup
        class PatchModel:
            def __init__(self): self.called = False

            def attach_page(self, _page): self.called = True

        patch_model = PatchModel()
        monkeypatch.setattr(
            MSHEET.Sheet, 'attach_page', patch_model.attach_page)

        sheets_active = CPOOL.PoolSheets()
        target = CSHEET.Sheet.new(sheets_active)
        # Test
        target.attach_page(None)
        assert patch_model.called

    def test_delete_force(self, monkeypatch):
        """Confirm unconditional deletion."""
        # Setup
        class PatchModel:
            def __init__(self): self.called = False

            def detach_all(self): self.called = True

        patch_model = PatchModel()
        monkeypatch.setattr(
            MSHEET.Sheet, 'detach_all', patch_model.detach_all)

        sheets_active = CPOOL.PoolSheets()
        target = CSHEET.Sheet.new(sheets_active)
        assert sheets_active._controls[id(target)] is target
        # Test
        target.delete_force()
        assert patch_model.called
        assert id(target) not in sheets_active._controls.keys()

    def test_delete_safe_fresh(self, monkeypatch):
        """Confirm deletion with guard for unsaved changes.
        Case: no unsaved changes
        """
        # Setup
        class PatchModel:
            def __init__(self): self.called = False

            def detach_all(self): self.called = True

        patch_model = PatchModel()
        monkeypatch.setattr(
            MSHEET.Sheet, 'detach_all', patch_model.detach_all)
        monkeypatch.setattr(
            MSHEET.Sheet, 'is_stale', lambda _s: False)

        sheets_active = CPOOL.PoolSheets()
        target = CSHEET.Sheet.new(sheets_active)
        # Test
        response = target.delete_safe()
        assert patch_model.called
        assert response is ABC_SHEET.EffectSafe.COMPLETED

    def test_delete_safe_stale(self, monkeypatch):
        """Confirm deletion with guard for unsaved changes.
        Case: unsaved changes
        """
        # Setup
        class PatchModel:
            def __init__(self): self.called = False

            def detach_all(self): self.called = True

        patch_model = PatchModel()
        monkeypatch.setattr(
            MSHEET.Sheet, 'detach_all', patch_model.detach_all)
        monkeypatch.setattr(
            MSHEET.Sheet, 'is_stale', lambda _s: True)

        sheets_active = CPOOL.PoolSheets()
        target = CSHEET.Sheet.new(sheets_active)
        # Test
        response = target.delete_safe()
        assert not patch_model.called
        assert response is ABC_SHEET.EffectSafe.NO_EFFECT

    def test_detach_page_force(self, patch_model_safe):
        """Confirm page removed unconditionally."""
        # Setup
        patch_model = patch_model_safe(p_stale=True, p_n_pages=1)
        sheets_active = CPOOL.PoolSheets()
        target = CSHEET.Sheet(sheets_active)
        target._model = patch_model
        assert sheets_active._controls[id(target)] is target
        N_DETACH = 1
        # Test
        target.detach_page_force(None)
        assert N_DETACH == patch_model.n_detach
        assert id(target) in sheets_active._controls.keys()

    def test_detach_page_force_last(self, patch_model_safe):
        """Confirm page removed unconditionally."""
        # Setup
        patch_model = patch_model_safe(p_stale=True, p_n_pages=0)
        sheets_active = CPOOL.PoolSheets()
        target = CSHEET.Sheet(sheets_active)
        target._model = patch_model
        assert sheets_active._controls[id(target)] is target
        N_DETACH = 1
        # Test
        target.detach_page_force(None)
        assert N_DETACH == patch_model.n_detach
        assert id(target) not in sheets_active._controls.keys()

    def test_detach_page_safe_fresh(self, patch_model_safe):
        """Confirm page removal with guard for unsaved changes.
        Case: no unsaved changes
        """
        # Setup
        patch_model = patch_model_safe(p_stale=False, p_n_pages=1)
        sheets_active = CPOOL.PoolSheets()
        target = CSHEET.Sheet(sheets_active)
        target._model = patch_model
        N_DETACH = 1
        # Test
        assert target.detach_page_safe(None) is (
            ABC_SHEET.EffectSafe.COMPLETED)
        assert N_DETACH == patch_model.n_detach

    def test_detach_page_safe_stale_multiple(self, patch_model_safe):
        """Confirm page removal with guard for unsaved changes.
        Case: unsaved changes, multiple pages
        """
        # Setup
        patch_model = patch_model_safe(p_stale=True, p_n_pages=2)
        sheets_active = CPOOL.PoolSheets()
        target = CSHEET.Sheet(sheets_active)
        target._model = patch_model
        N_DETACH = 1
        # Test
        assert target.detach_page_safe(None) is (
            ABC_SHEET.EffectSafe.COMPLETED)
        assert N_DETACH == patch_model.n_detach

    def test_detach_page_safe_stale_single(self, patch_model_safe):
        """Confirm page removal with guard for unsaved changes.
        Case: unsaved changes, single page
        """
        # Setup
        patch_model = patch_model_safe(p_stale=True, p_n_pages=1)
        sheets_active = CPOOL.PoolSheets()
        target = CSHEET.Sheet(sheets_active)
        target._model = patch_model
        N_DETACH = 0
        # Test
        assert target.detach_page_safe(None) is (
            ABC_SHEET.EffectSafe.NO_EFFECT)
        assert N_DETACH == patch_model.n_detach

    def test_new(self):
        """Confirm control creation with default model."""
        # Setup
        sheets_active = CPOOL.PoolSheets()
        # Test
        target = CSHEET.Sheet.new(sheets_active)
        assert isinstance(target, CSHEET.Sheet)
        assert isinstance(target._model, MSHEET.Sheet)

    def test_open(self, tmp_path):
        """Confirm control creation from file.
        Case: path to file with model contents
        """
        # Setup
        PATH = Path(tmp_path / 'saved_factsheet.fsg')
        TITLE = 'Parrot Sketch'
        model = MSHEET.Sheet(p_title=TITLE)
        model.set_stale()
        sheets_active = CPOOL.PoolSheets()
        source = CSHEET.Sheet(sheets_active)
        source._model = model
        source._path = PATH
        assert not PATH.exists()
        source.save()
        # Test
        target = CSHEET.Sheet.open(sheets_active, PATH)
        assert source._model == target._model
        assert target._model.is_fresh()

    def test_open_empty(self, tmp_path):
        """Confirm control creation from file.
        Case: path not to a file
        """
        # Setup
        PATH = Path(tmp_path / 'saved_factsheet.fsg')
        TITLE = 'Error opening file \'{}\''.format(PATH)
        MODEL = MSHEET.Sheet(p_title=TITLE)
        assert not PATH.exists()
        sheets_active = CPOOL.PoolSheets()
        # Test
        target = CSHEET.Sheet.open(sheets_active, PATH)
        assert target._model is not None
        assert MODEL == target._model
        assert target._path is None

    def test_open_except(self, tmp_path):
        """Confirm control creation from file.
        Case: path to file with unloadable contents
        """
        # Setup
        PATH = Path(tmp_path / 'saved_factsheet.fsg')
        BYTES = b'Something completely different'
        with PATH.open(mode='wb') as io_out:
            io_out.write(BYTES)
        assert PATH.exists()
        TITLE = 'Error opening file \'{}\''.format(PATH)
        MODEL = MSHEET.Sheet(p_title=TITLE)
        sheets_active = CPOOL.PoolSheets()
        # Test
        target = CSHEET.Sheet.open(sheets_active, PATH)
        assert target._model is not None
        assert MODEL == target._model
        assert target._path is None

    @pytest.mark.parametrize('name_attr, name_prop', [
        ['_path', 'path'],
        ['_sheets_active', 'sheets_active'],
        ])
    def test_property(self, tmp_path, name_attr, name_prop):
        """Confirm properties are get-only.

        #. Case: read
        #. Case: no replace
        #. Case: no delete
        """
        # Setup
        sheets_active = CPOOL.PoolSheets()
        target = CSHEET.Sheet(sheets_active)
        PATH = Path(tmp_path / 'path_factsheet.fsg')
        target._path = PATH
        value_attr = getattr(target, name_attr)
        target_prop = getattr(CSHEET.Sheet, name_prop)
        value_prop = getattr(target, name_prop)
        # Test: read
        assert target_prop.fget is not None
        assert str(value_attr) == str(value_prop)
        # Test: no replace
        assert target_prop.fset is None
        # Test: no delete
        assert target_prop.fdel is None

    def test_present_factsheet(self, monkeypatch):
        """Confirm factsheet presentation."""
        # Setup
        class PatchPresentPages:
            def __init__(self): self.called = False

            def present_pages(self, _time): self.called = True

        patch_present = PatchPresentPages()
        monkeypatch.setattr(
            MSHEET.Sheet, 'present_pages', patch_present.present_pages)
        TITLE = 'Parrot Sketch'
        model = MSHEET.Sheet(p_title=TITLE)
        model.set_stale()
        sheets_active = CPOOL.PoolSheets()
        target = CSHEET.Sheet(sheets_active)
        target._model = model
        NO_TIME = 0
        # Test
        target.present_factsheet(NO_TIME)
        assert patch_present.called

    def test_save(self, tmp_path):
        """Confirm write to file.
        Case: file does not exist.
        """
        # Setup
        PATH = Path(tmp_path / 'saved_factsheet.fsg')
        TITLE = 'Parrot Sketch'
        model = MSHEET.Sheet(p_title=TITLE)
        model.set_stale()
        sheets_active = CPOOL.PoolSheets()
        source = CSHEET.Sheet(sheets_active)
        source._model = model
        source._path = PATH
        assert not PATH.exists()
        # Test
        source.save()
        assert PATH.exists()
        assert source._model.is_fresh()

        with PATH.open(mode='rb') as io_in:
            target = pickle.load(io_in)
        assert target is not None
        assert TITLE == target._infoid.title

    def test_save_as(self, tmp_path):
        """Confirm write to file at new path."""
        # Setup
        TITLE = 'Parrot Sketch'
        model = MSHEET.Sheet(p_title=TITLE)
        model.set_stale()
        sheets_active = CPOOL.PoolSheets()
        source = CSHEET.Sheet(sheets_active)
        source._model = model
        PATH = Path(tmp_path / 'saved_factsheet.fsg')
        assert not PATH.exists()
        # Test
        source.save_as(PATH)
        assert PATH == source._path
        assert PATH.exists()
        assert source._model.is_fresh()

        with PATH.open(mode='rb') as io_in:
            target = pickle.load(io_in)
        assert target is not None
        assert TITLE == target._infoid.title

    def test_save_no_path(self, PatchLogger, monkeypatch):
        """Confirm write to file.
        Case: no file path.
        """
        # Setup
        patch_logger = PatchLogger()
        monkeypatch.setattr(
            logging.Logger, 'warning', patch_logger.warning)
        log_message = ('No file path (Sheet.save)')
        TITLE = 'Parrot Sketch'
        model = MSHEET.Sheet(p_title=TITLE)
        sheets_active = CPOOL.PoolSheets()
        source = CSHEET.Sheet(sheets_active)
        source._model = model
        source._path = None
        # Test
        source.save()
        assert patch_logger.called
        assert log_message == patch_logger.message

    def test_save_exists(self, tmp_path):
        """Confirm write to file.
        Case: file exists.
        """
        # Setup
        PATH = Path(tmp_path / 'saved_factsheet.fsg')
        TEXT = 'Existing content'
        with PATH.open(mode='w') as io_out:
            io_out.write(TEXT)
        TITLE = 'Parrot Sketch'
        model = MSHEET.Sheet(p_title=TITLE)
        model.set_stale()
        sheets_active = CPOOL.PoolSheets()
        source = CSHEET.Sheet(sheets_active)
        source._model = model
        source._path = PATH
        assert PATH.exists()
        BACKUP = PATH.with_name(PATH.name + '~')
        assert not BACKUP.exists()
        # Test
        source.save()
        assert PATH.exists()
        assert source._model.is_fresh()

        with PATH.open(mode='rb') as io_in:
            target = pickle.load(io_in)
        assert target is not None

        assert BACKUP.exists()
        with BACKUP.open(mode='r') as io_in:
            backup_text = io_in.read()
        assert TEXT == backup_text
