"""
Unit tests for :mod:`.text_markup_gtk3`.
"""
import pytest

import factsheet.ui_bricks.ui_gtk3.text_markup.text_markup_gtk3 as BMARKUPGTK3


class TestControlMarkupGtk3:
    """Unit tests for :class:`.ControlTextMarkupGtk3`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        MODEL = BMARKUPGTK3.ModelTextMarkupGtk3()
        # Test
        target = BMARKUPGTK3.ControlTextMarkupGtk3(p_model=MODEL)
        assert target._model is MODEL
        assert isinstance(target._changed, bool)
        assert not target._changed

    def test_new_model(self):
        """Confirm model construction."""
        # Setup
        target = BMARKUPGTK3.ControlTextMarkupGtk3()
        # Test
        assert isinstance(target._model, BMARKUPGTK3.ModelTextMarkupGtk3)
        assert target._model._control is target


class TestModelMarkupGtk3:
    """Unit tests for :class:`.ModelTextMarkupGtk3`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        CONTROL = BMARKUPGTK3.ControlTextMarkupGtk3()
        # Test
        target = BMARKUPGTK3.ModelTextMarkupGtk3(p_control=CONTROL)
        assert target._control is CONTROL

    def test_new_store_ui(self):
        """Confirm storage object construction."""
        # Setup
        target = BMARKUPGTK3.ModelTextMarkupGtk3()
        # Test
        assert isinstance(target._store_ui, BMARKUPGTK3.StoreUiTextMarkup)

    def test_new_control(self):
        """Confirm control construction."""
        # Setup
        target = BMARKUPGTK3.ModelTextMarkupGtk3()
        # Test
        assert isinstance(target._control, BMARKUPGTK3.ControlTextMarkupGtk3)
        assert target._control._model is target
