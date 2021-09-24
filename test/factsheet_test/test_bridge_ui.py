"""
Unit tests for classes that encapsulates user interface classes from
widget toolkit.  See :mod:`~.bridge_ui`.
"""
import pytest  # type: ignore[import]

import factsheet.bridge_gtk.bridge_base as BBASE
# import factsheet.bridge_gtk.bridge_outline as BOUTLINE
# import factsheet.bridge_gtk.bridge_text as BTEXT
import factsheet.bridge_ui as BUI


class TestBridgeTypes:
    """Unit tests for definitions of API classes and type hints in
    :mod:`.bridge_ui`.
    """

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_SOURCE', [
        # (BUI.Bridge, BBASE.BridgeBase),
        # (BUI.ModelOpaque, BBASE.ModelGtkOpaque),
        (BUI.TimeEvent, BBASE.TimeEvent),
        # (BUI.ViewAny, BBASE.ViewAny),
        # (BUI.ViewOpaque, BBASE.ViewGtkOpaque),
        # (BUI.BridgeOutlineColumnar, BOUTLINE.BridgeOutlineColumnar),
        # (BUI.BridgeOutlineMultiColumnar, BOUTLINE.BridgeOutlineMultiColumnar),
        # (BUI.BridgeOutlineMultiSelect, BOUTLINE.BridgeOutlineMultiSelect),
        # (BUI.BridgeOutlineSelect, BOUTLINE.BridgeOutlineSelect),
        # (BUI.LineOutline, BOUTLINE.LineOutline),
        # (BUI.ViewOutlineColumnar, BOUTLINE.ViewOutlineColumnar),
        # (BUI.ViewOutlineSelect, BOUTLINE.ViewOutlineSelect),
        # (BUI.BridgeText, BTEXT.BridgeText),
        # (BUI.BridgeTextMarkup, BTEXT.BridgeTextMarkup),
        # (BUI.BridgeTextTagged, BTEXT.BridgeTextTagged),
        # (BUI.ViewTextDisplay, BTEXT.ViewTextDisplay),
        # (BUI.ViewTextMarkup, BTEXT.ViewTextMarkup),
        # (BUI.ViewTextTagged, BTEXT.ViewTextTagged),
        ])
    def test_types(self, TYPE_TARGET, TYPE_SOURCE):
        """Confirm API definitions."""
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_SOURCE


class TestBridgeConstant:
    """Unit tests for definitions of API classes and type hints in
    :mod:`.bridge_ui`.
    """

    def test_time_current(self):
        """Confirm constant definitions."""
        # Setup
        # Test
        assert BBASE.TIME_EVENT_CURRENT == BUI.TIME_EVENT_CURRENT
        # assert BUI.filter_user_markup is BTEXT.filter_user_markup
