"""
Unit tests for identity fields enumeration.  See :mod:`.id`.
"""
import factsheet.view.id as VID


class TestFieldsId:
    """Unit tests for :class:`.FieldsId`."""

    def test_members(self):
        """Confirm member definitions."""
        # Setup
        # Test
        assert not bool(VID.FieldsId.VOID)
        assert VID.FieldsId.NAME
        assert VID.FieldsId.SUMMARY
        assert VID.FieldsId.TITLE
