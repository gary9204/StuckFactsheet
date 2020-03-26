"""
Unit tests for class to display page identification information.

See :mod:`.view_infoid`.
"""
import pytest   # type: ignore[import]

from factsheet.adapt_gtk import adapt_infoid as AINOFID
from factsheet.view import view_infoid as VINFOID


class TestInfoId:
    """Unit tests for :class:`.ViewInfoId`."""

    def test_init(self, patch_ui_infoid, text_ui_infoid):
        """Confirm initialization."""
        # Setup
        get_object = patch_ui_infoid
        # Test
        target = VINFOID.ViewInfoId(get_object)
        assert isinstance(target._view_title, AINOFID.AdaptEntry)
        assert text_ui_infoid['name'] == target._view_name.get_text()
        assert text_ui_infoid['title'] == target._view_title.get_text()

    @pytest.mark.parametrize('name_method, name_attr', [
        ['get_view_name', '_view_name'],
        ['get_view_title', '_view_title'],
        ])
    def test_get_title(self, patch_ui_infoid, name_method, name_attr):
        """Confirm return is title display element."""
        # Setup
        get_object = patch_ui_infoid
        target = VINFOID.ViewInfoId(get_object)
        method = getattr(target, name_method)
        attr = getattr(target, name_attr)
        # Test
        assert method() is attr

    @pytest.mark.parametrize('name_attr, name_prop', [
        ['_view_name', 'name'],
        ['_view_title', 'title'],
        ])
    def test_property_text(self, patch_ui_infoid, name_attr, name_prop):
        """Confirm properties are get-only.

        #. Case: read
        #. Case: no replace
        #. Case: no delete
        """
        # Setup
        get_object = patch_ui_infoid
        target = VINFOID.ViewInfoId(get_object)
        value_attr = getattr(target, name_attr)
        target_prop = getattr(VINFOID.ViewInfoId, name_prop)
        value_prop = getattr(target, name_prop)
        # Test: read
        assert target_prop.fget is not None
        assert value_attr.props.text == value_prop
        # Test: no replace
        assert target_prop.fset is None
        # Test: no delete
        assert target_prop.fdel is None
