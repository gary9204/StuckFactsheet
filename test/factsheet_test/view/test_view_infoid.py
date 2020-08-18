"""
Unit tests for class to display page identification information.

See :mod:`.view_infoid`.
"""
import pytest   # type: ignore[import]

from factsheet.adapt_gtk import adapt_infoid as AINOFID
from factsheet.view import view_infoid as VINFOID


class TestInfoId:
    """Unit tests for :class:`.ViewInfoId`."""

    def test_init(self, patch_ui_infoid, patch_args_infoid):
        """Confirm initialization."""
        # Setup
        ARGS = patch_args_infoid
        get_object = patch_ui_infoid
        # Test
        target = VINFOID.ViewInfoId(get_object)
        assert isinstance(target._view_title, AINOFID.AdaptEntry)
        assert ARGS.p_name == target._view_name.get_text()
        assert ARGS.p_summary == (
            AINOFID.str_adapt_textview(target.get_view_summary()))
        assert ARGS.p_title == target._view_title.get_text()

    # def test_init(self, patch_ui_infoid, text_ui_infoid):
    #     """Confirm initialization."""
    #     # Setup
    #     get_object = patch_ui_infoid
    #     # Test
    #     target = VINFOID.ViewInfoId(get_object)
    #     assert isinstance(target._view_title, AINOFID.AdaptEntry)
    #     assert text_ui_infoid['name'] == target._view_name.get_text()
    #     assert text_ui_infoid['summary'] == (
    #         AINOFID.str_adapt_textview(target.get_view_summary()))
    #     assert text_ui_infoid['title'] == target._view_title.get_text()

    @pytest.mark.parametrize('name_method, name_attr', [
        ['get_view_name', '_view_name'],
        ['get_view_summary', '_view_summary'],
        ['get_view_title', '_view_title'],
        ])
    def test_get_view(self, patch_ui_infoid, name_method, name_attr):
        """Confirm return is view display element for each attribute."""
        # Setup
        get_object = patch_ui_infoid
        target = VINFOID.ViewInfoId(get_object)
        method = getattr(target, name_method)
        attr = getattr(target, name_attr)
        # Test
        assert method() is attr

    @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
        ['_view_name', 'name'],
        ['_view_title', 'title'],
        ])
    def test_property_entry(self, patch_ui_infoid, NAME_ATTR, NAME_PROP):
        """Confirm name and title properties are get-only.

        #. Case: get
        #. Case: no set
        #. Case: no delete
        """
        # Setup
        get_object = patch_ui_infoid
        target = VINFOID.ViewInfoId(get_object)
        value_attr = getattr(target, NAME_ATTR)
        target_prop = getattr(VINFOID.ViewInfoId, NAME_PROP)
        value_prop = getattr(target, NAME_PROP)
        # Test: read
        assert target_prop.fget is not None
        assert value_attr.props.text == value_prop
        # Test: no replace
        assert target_prop.fset is None
        # Test: no delete
        assert target_prop.fdel is None

    def test_property_summary(self, patch_ui_infoid, patch_args_infoid):
        """Confirm summary property is get-only.

        #. Case: get
        #. Case: no set
        #. Case: no delete
        """
        # Setup
        ARGS = patch_args_infoid
        text = ARGS.p_summary
        get_object = patch_ui_infoid
        target_prop = getattr(VINFOID.ViewInfoId, 'summary')
        target = VINFOID.ViewInfoId(get_object)
        # Test: read
        assert target_prop.fget is not None
        assert text == target.summary
        # Test: no replace
        assert target_prop.fset is None
        # Test: no delete
        assert target_prop.fdel is None
