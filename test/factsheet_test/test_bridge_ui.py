"""
Unit tests for classes that encapsulates user interface classes from
widget toolkit.  See :mod:`~.bridge_ui`.
"""
import pytest  # type: ignore[import]

import factsheet.bridge_gtk.bridge_base as BBASE
import factsheet.bridge_gtk.bridge_outline as BOUTLINE
import factsheet.bridge_gtk.bridge_text as BTEXT
import factsheet.bridge_ui as BUI


class TestBridgeTypes:
    """Unit tests for definitions of API classes and type hints in
    :mod:`.bridge_ui`.
    """

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_SOURCE', [
        (BUI.ModelOpaque, BBASE.ModelOpaque),
        (BUI.ViewOpaque, BBASE.ViewOpaque),
        (BUI.BridgeOutlineColumnar, BOUTLINE.BridgeOutlineColumnar),
        (BUI.BridgeOutlineMultiColumnar, BOUTLINE.BridgeOutlineMultiColumnar),
        (BUI.BridgeOutlineMultiSelect, BOUTLINE.BridgeOutlineMultiSelect),
        (BUI.BridgeOutlineSelect, BOUTLINE.BridgeOutlineSelect),
        (BUI.LineOutline, BOUTLINE.LineOutline),
        (BUI.BridgeTextFormat, BTEXT.BridgeTextFormat),
        (BUI.BridgeTextMarkup, BTEXT.BridgeTextMarkup),
        (BUI.BridgeTextStatic, BTEXT.BridgeTextStatic),
        (BUI.ViewTextFormat, BTEXT.ViewTextFormat),
        (BUI.ViewTextMarkup, BTEXT.ViewTextMarkup),
        (BUI.ViewTextStatic, BTEXT.ViewTextStatic),
        ])
    def test_types(self, TYPE_TARGET, TYPE_SOURCE):
        """Confirm API definitions."""
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_SOURCE
