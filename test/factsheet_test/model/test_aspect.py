"""
Unit tests for fact aspect classes.  See :mod:`~.bridge_aspect`.
"""
import pytest   # type: ignore[import]

import factsheet.bridge_ui as BUI
import factsheet.model.aspect as MASPECT


class TestAspect:
    """ Unit tests for :class:`~.Aspect`."""

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (MASPECT.Aspect, '__init__'),
        (MASPECT.Aspect, 'new_view'),
        (MASPECT.Aspect, 'clear'),
        ])
    def test_method_abstract(self, CLASS, NAME_METHOD):
        """Confirm each abstract method is specified."""
        # Setup
        # Test
        assert hasattr(CLASS, '__abstractmethods__')
        assert NAME_METHOD in CLASS.__abstractmethods__


class TestAspectPlain:
    """ Unit tests for :class:`~.AspectPlain`."""

    def test_init(self):
        # Setup
        BASIS = 'The Parrot Sketch'
        # Test
        target = MASPECT.AspectPlain(BASIS)
        assert isinstance(target._aspect, BUI.BridgeTextStatic)
        assert BASIS == target._aspect.text

    def test_clear(self):
        # Setup
        BASIS = 'The Parrot Sketch'
        CLEAR = ''
        target = MASPECT.AspectPlain(BASIS)
        # Test
        target.clear()
        assert CLEAR == target._aspect.text

    def test_new_view(self):
        # Setup
        BASIS = 'The Parrot Sketch'
        target = MASPECT.AspectPlain(BASIS)
        # Test
        view = target.new_view()
        assert isinstance(view, MASPECT.ViewAspectPlain)
        assert BASIS == view.get_text()
        # Teardown
        view.destroy()
