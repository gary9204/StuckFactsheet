"""
Unit tests for class that mediates from :mod:`~factsheet.view` to
:mod:`~factsheet.model` of a factsheet
"""
import pytest   # type: ignore[import]

from factsheet.abc_types import abc_sheet as ABC_SHEET
from factsheet.control import sheet as CSHEET
from factsheet.model import sheet as MSHEET


@pytest.fixture
def patch_model_safe():
    class PatchSafe(MSHEET.Sheet):
        def __init__(self, p_stale, p_n_pages):
            super().__init__()
            self._stale = p_stale
            self._n_pages = p_n_pages
#             self.n_delete = 0
            self.n_detach = 0

        def n_pages(self) -> int:
            return self._n_pages

#         def delete(self):
#             self.n_delete += 1

        def detach_page(self, _view):
            self.n_detach += 1

    return PatchSafe


class TestControlSheet:
    """Unit tests for control class Sheet."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        # Test
        target = CSHEET.Sheet()
        assert target._model is None

    def test_attach_page(self, monkeypatch):
        """Confirm page addition."""
        # Setup
        class PatchModel:
            def __init__(self): self.called = False

            def attach_page(self, _page): self.called = True

        patch_model = PatchModel()
        monkeypatch.setattr(
            MSHEET.Sheet, 'attach_page', patch_model.attach_page)

        target = CSHEET.Sheet.new()
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

        target = CSHEET.Sheet.new()
        # Test
        target.delete_force()
        assert patch_model.called

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

        target = CSHEET.Sheet.new()
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

        target = CSHEET.Sheet.new()
        # Test
        response = target.delete_safe()
        assert not patch_model.called
        assert response is ABC_SHEET.EffectSafe.NO_EFFECT

    def test_detach_page_force(self, patch_model_safe):
        """Confirm page removed unconditionally."""
        # Setup
        patch_model = patch_model_safe(p_stale=True, p_n_pages=1)
        target = CSHEET.Sheet()
        target._model = patch_model
        N_DETACH = 1
        # Test
        target.detach_page_force(None)
        assert N_DETACH == patch_model.n_detach

    def test_detach_page_safe_fresh(self, patch_model_safe):
        """Confirm page removal with guard for unsaved changes.
        Case: no unsaved changes
        """
        # Setup
        patch_model = patch_model_safe(p_stale=False, p_n_pages=1)
        target = CSHEET.Sheet()
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
        target = CSHEET.Sheet()
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
        target = CSHEET.Sheet()
        target._model = patch_model
        N_DETACH = 0
        # Test
        assert target.detach_page_safe(None) is (
            ABC_SHEET.EffectSafe.NO_EFFECT)
        assert N_DETACH == patch_model.n_detach

    @pytest.mark.skip(reason='Pending implementation')
    def test_load(self):
        """Confirm control creation from file."""
        # Setup
        # Test

    def test_new(self):
        """Confirm control creation with default model."""
        # Setup
        # Test
        target = CSHEET.Sheet.new()
        assert isinstance(target, CSHEET.Sheet)
        assert isinstance(target._model, MSHEET.Sheet)
