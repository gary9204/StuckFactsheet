"""
Unit tests for fact aspect classes.  See :mod:`~.bridge_aspect`.
"""
import pytest   # type: ignore[import]

import factsheet.bridge_ui as BUI
import factsheet.model.aspect as MASPECT


class TestAspect:
    """ Unit tests for :class:`~.Aspect`."""

    @pytest.mark.parametrize('CLASS, NAME_METHOD', [
        (MASPECT.Aspect, '__eq__'),
        (MASPECT.Aspect, '__init__'),
        (MASPECT.Aspect, 'new_view'),
        (MASPECT.Aspect, 'refresh'),
        ])
    def test_method_abstract(self, CLASS, NAME_METHOD):
        """Confirm each abstract method is specified."""
        # Setup
        # Test
        assert hasattr(CLASS, '__abstractmethods__')
        assert NAME_METHOD in CLASS.__abstractmethods__

    def test_eq(self):
        """Confirm equivalence operator.

        #. Case: type difference.
        #. Case: equivalent.
        """
        # Setup
        class PatchAspect(MASPECT.Aspect[str, str]):
            def __eq__(self, p_other):
                return super().__eq__(p_other)

            def __init__(self, p_basis):
                self._basis = p_basis
                self._bridge = 'Defined'

            def new_view(self):
                raise NotImplementedError

            def refresh(self):
                self._bridge += 'Refreshed'

        TEXT = 'The Parrot Sketch'
        source = PatchAspect(p_basis=TEXT)
        # Test: type difference
        assert not source.__eq__(TEXT)
        # Test: Equivalence
        target = PatchAspect(p_basis=TEXT)
        assert source.__eq__(target)


class TestAspectPlain:
    """ Unit tests for :class:`~.AspectPlain`."""

    def test_eq(self):
        """Confirm equivalence operator.

        #. Case: type difference.
        #. Case: text difference.
        #. Case: equivalent.
        """
        # Setup
        TEXT = 'The Parrot Sketch'
        TEXT_DIFF = 'Something completely different'
        source = MASPECT.AspectPlain(p_basis=TEXT)
        # Test: type difference
        assert not source.__eq__(TEXT)
        # Test: text difference
        target = MASPECT.AspectPlain(p_basis=TEXT_DIFF)
        assert not source.__eq__(target)
        # Test: Equivalence
        target = MASPECT.AspectPlain(p_basis=TEXT)
        assert source.__eq__(target)

    def test_init(self):
        """Confirm initialization."""
        # Setup
        TEXT = 'The Parrot Sketch'
        # Test
        target = MASPECT.AspectPlain(p_basis=TEXT)
        assert TEXT == target._basis
        assert isinstance(target._bridge, BUI.BridgeTextStatic)
        assert target._basis == target._bridge.text

    def test_new_view(self):
        """Confirm view returned."""
        # Setup
        BASIS = 'The Parrot Sketch'
        target = MASPECT.AspectPlain(p_basis=BASIS)
        # Test
        view = target.new_view()
        assert isinstance(view, MASPECT.ViewAspectPlain)
        assert target._basis == view.get_text()
        # Teardown
        view.destroy()

    def test_refresh(self):
        """Confirm removal of fact information."""
        # Setup
        BASIS = 'The Parrot Sketch'
        target = MASPECT.AspectPlain(p_basis=BASIS)
        TEXT = 'Something completely different'
        target._basis = TEXT
        # Test
        target.refresh()
        assert TEXT == target._bridge.text
