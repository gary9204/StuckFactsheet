"""
Unit tests for class that mediates from :mod:`~factsheet.view` to
:mod:`~factsheet.model` of a factsheet
"""
import pytest   # type: ignore[import]

from factsheet.abc_types import abc_sheet as ASHEET
from factsheet.control import sheet as CSHEET
from factsheet.model import sheet as MSHEET


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

            def delete(self): self.called = True

        patch_model = PatchModel()
        monkeypatch.setattr(
            MSHEET.Sheet, 'delete', patch_model.delete)

        target = CSHEET.Sheet.new()
        # Test
        target.delete_force()
        assert patch_model.called

    @pytest.mark.skip(reason='Pending implementation')
    def test_delete_safe(self, monkeypatch):
        """Confirm deletion with guard for unsaved changes.
        Case: no unsaved changes
        Case: unsaved changes
        """
        # Setup
        class PatchModel:
            def __init__(self): self.called = False

            def delete(self): self.called = True

        patch_model = PatchModel()
        monkeypatch.setattr(
            MSHEET.Sheet, 'delete', patch_model.delete)
        monkeypatch.setattr(
            MSHEET.Sheet, 'is_stale', lambda: False)

        target = CSHEET.Sheet.new()
        response = target.delete_safe()
        assert ASHEET.ALLOWED
        assert patch_model.called

    @pytest.mark.skip(reason='Pending implementation')
    def test_detach_page(self):
        """Confirm observer deletion."""
        # Setup
        # Test

    def test_detach_page_safe(self):
        """Confirm observer deletion with guard for unsaved changes.
        Case: no unsaved changes
        Case: unsaved changes, multiple pages
        Case: unsaved changes, single page
        """
        # Setup
        target = CSHEET.Sheet()
        # Test
        assert target.detach_page_safe(None) is ASHEET.ALLOWED

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
