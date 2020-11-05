"""
Unit tests for classes that encapsulates user interface classes from
widget toolkit.  See :mod:`~.bridge_ui`.
"""
import gi   # type: ignore[import]
import pytest  # type: ignore[import]
import typing

import factsheet.bridge_gtk.bridge_base as BBASE
import factsheet.bridge_gtk.bridge_outline as BOUTLINE
import factsheet.bridge_gtk.bridge_text as BTEXT
import factsheet.bridge_ui as BUI

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class TestBridgeTypes:
    """Unit tests for definitions of API classes and type hints in
    :mod:`.bridge_ui`.
    """
    # Workaround for Mypy issue with Union.
    # See https://github.com/python/mypy/issues/5354
    ViewOutline: typing.Type[typing.Any] = (
        BUI.ViewOutline)  # type: ignore[misc]

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_SOURCE', [
        (BUI.ModelOpaque, BBASE.ModelOpaque),
        (BUI.ViewOpaque, BBASE.ViewOpaque),
        (BUI.BridgeOutline, BOUTLINE.BridgeOutline),
        (BUI.BridgeOutlineMulti, BOUTLINE.BridgeOutlineMulti),
        (BUI.LineOutline, BOUTLINE.LineOutline),
        (BUI.ModelOutline, BOUTLINE.ModelOutline),
        (ViewOutline.__args__, (Gtk.ComboBox, Gtk.TreeView)),
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
