"""
factsheet_test.control.test_sheet - unit tests for control class Sheet.
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

    @pytest.mark.skip(reason='Pending implementation')
    def test_attach_view(self):
        """Confirm observer addition."""
        # Setup
        # Test

    @pytest.mark.skip(reason='Pending implementation')
    def test_delete(self):
        """Confirm unconditional deletion."""
        # Setup
        # Test

    @pytest.mark.skip(reason='Pending implementation')
    def test_delete_safe(self):
        """Confirm deletion with guard for unsaved changes.
        Case: no unsaved changes
        Case: unsaved changes
        """
        # Setup
        # Test

    @pytest.mark.skip(reason='Pending implementation')
    def test_detach_view(self):
        """Confirm observer deletion."""
        # Setup
        # Test

    def test_detach_view_safe(self):
        """Confirm observer deletion with guard for unsaved changes.
        Case: no unsaved changes
        Case: unsaved changes, multiple views
        Case: unsaved changes, single view
        """
        # Setup
        target = CSHEET.Sheet()
        # Test
        assert target.detach_view_safe(None) is ASHEET.ALLOWED

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
