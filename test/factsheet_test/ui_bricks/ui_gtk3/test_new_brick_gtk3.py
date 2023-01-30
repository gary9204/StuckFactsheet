"""
Unit tests for :mod:`.new_brick_gtk3`.
"""
import pytest

import factsheet.ui_bricks.ui_gtk3.markup_gtk3 as BMARKUPGTK3
import factsheet.ui_bricks.ui_gtk3.new_brick_gtk3 as NEWBRICKGTK3


class TestNewBrickGtk3:
    """Unit tests for :class:`.NewBrickGtk3`."""

    @pytest.mark.parametrize('FACTORY, CLASS', [
        ('_markup', BMARKUPGTK3.NewMarkupGtk3),
        ])
    def test_init(self, FACTORY, CLASS):
        """Confirm initialization of each component factory attribute.

        :param FACTORY: name of factory attribute under test.
        :param CLASS: expected class of factory.
        """
        # Setup
        # Test
        target = NEWBRICKGTK3.NewBrickGtk3()
        factory = getattr(target, FACTORY)
        assert isinstance(factory, CLASS)

    @pytest.mark.parametrize('PROP, ATTR', [
        ('markup', '_markup'),
        ])
    def test_property_access(self, PROP, ATTR):
        """Confirm access limits of each property.

        :param PROP: name of property under test.
        :param ATTR: name of attribute for property.
        """
        # Setup
        CLASS = NEWBRICKGTK3.NewBrickGtk3
        target = CLASS()
        attr = getattr(target, ATTR)
        target_prop = getattr(CLASS, PROP)
        # Test
        assert target_prop.fget is not None
        assert attr == target_prop.fget(target)
        assert target_prop.fset is None
        assert target_prop.fdel is None
