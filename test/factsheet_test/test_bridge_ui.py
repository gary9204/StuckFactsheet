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

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_EXPECT', [
        (BUI.TimeEvent, BBASE.TimeEvent),
        (BUI.ChooserOutline, BOUTLINE.ChooserOutline),
        (BUI.FactoryChooserOutline, BOUTLINE.FactoryChooserOutline),
        (BUI.FactoryViewOutline, BOUTLINE.FactoryViewOutline),
        (BUI.LineOutline, BOUTLINE.LineOutline),
        (BUI.ModelOutlineMulti, BOUTLINE.ModelOutlineMulti),
        (BUI.ModelOutlineSingle, BOUTLINE.ModelOutlineSingle),
        (BUI.ViewOutline, BOUTLINE.ViewOutline),
        (BUI.ModelTextMarkup, BTEXT.ModelTextMarkup),
        (BUI.DisplayTextMarkup, BTEXT.DisplayTextMarkup),
        (BUI.FactoryDisplayTextMarkup, BTEXT.FactoryDisplayTextMarkup),
        (BUI.EditorTextMarkup, BTEXT.EditorTextMarkup),
        (BUI.FactoryEditorTextMarkup, BTEXT.FactoryEditorTextMarkup),
        (BUI.ModelTextStyled, BTEXT.ModelTextStyled),
        (BUI.DisplayTextStyled, BTEXT.DisplayTextStyled),
        (BUI.FactoryDisplayTextStyled, BTEXT.FactoryDisplayTextStyled),
        (BUI.EditorTextStyled, BTEXT.EditorTextStyled),
        (BUI.FactoryEditorTextStyled, BTEXT.FactoryEditorTextStyled),
        ])
    def test_types(self, TYPE_TARGET, TYPE_EXPECT):
        """Confirm API definitions.

        :param TYPE_TARGET: type hint under test.
        :param TYPE_EXPECT: type expected.
        """
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_EXPECT


class TestBridgeConstant:
    """Unit tests for definitions of API classes and type hints in
    :mod:`.bridge_ui`.
    """

    def test_constants(self):
        """Confirm constant definitions."""
        # Setup
        # Test
        assert BBASE.TIME_EVENT_CURRENT == BUI.TIME_EVENT_CURRENT
        assert BUI.escape_text_markup is BTEXT.escape_text_markup
