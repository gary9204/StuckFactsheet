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
        (MASPECT.Aspect, 'clear_presentation'),
        (MASPECT.Aspect, 'new_view'),
        (MASPECT.Aspect, 'set_presentation'),
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

            def __init__(self):
                self._presentation = 'Presentation defined'

            def clear_presentation(self):
                self._presentation += ', cleared'

            def new_view(self):
                raise NotImplementedError

            def set_presentation(self, p_value):
                self._presentation += ', set to ' + p_value

        source = PatchAspect()
        TEXT = 'The Parrot Sketch'
        source.set_presentation(p_value=TEXT)
        # Test: type difference
        assert not source.__eq__(TEXT)
        # Test: Equivalence
        target = PatchAspect()
        target.set_presentation(p_value=TEXT)
        assert source.__eq__(target)


# class TestAspectBridge:
#     """ Unit tests for :class:`~.AspectBridge`."""
#
#     @pytest.mark.skip(reason='Switch basis to value.')
#     def test_eq(self):
#         """Confirm equivalence operator.
#
#         #. Case: type difference.
#         #. Case: content difference.
#         #. Case: equivalent.
#         """
#         # Setup
#         AspectBridge = MASPECT.AspectBridge[BUI.ViewTextMarkup]
#         TEXT = 'The Parrot Sketch'
#         basis = BUI.BridgeTextMarkup()
#         basis.text = TEXT
#         source = AspectBridge(p_value=basis)
#         TEXT_DIFF = 'Something completely different'
#         basis_diff = BUI.BridgeTextMarkup()
#         basis_diff.text = TEXT_DIFF
#         # Test: type difference
#         assert not source.__eq__(TEXT)
#         # Test: content difference
#         target = AspectBridge(p_value=basis_diff)
#         assert not source.__eq__(target)
#         # Test: Equivalence
#         target = AspectBridge(p_value=basis)
#         assert source.__eq__(target)
#
#     @pytest.mark.skip(reason='Switch basis to value.')
#     def test_init(self):
#         """Confirm initialization."""
#         # Setup
#         TEXT = 'The Parrot Sketch'
#         basis = BUI.BridgeTextMarkup()
#         basis.text = TEXT
#         # Test
#         target = MASPECT.AspectBridge[BUI.ViewTextMarkup](p_value=basis)
#         assert target._basis is basis
#
#     @pytest.mark.skip(reason='Switch basis to value.')
#     def test_new_view(self):
#         """Confirm view returned."""
#         # Setup
#         TEXT = 'The Parrot Sketch'
#         basis = BUI.BridgeTextMarkup()
#         basis.text = TEXT
#         target = MASPECT.AspectBridge[BUI.ViewTextMarkup](p_value=basis)
#         # Test
#         view = target.new_view()
#         assert isinstance(view, BUI.ViewTextMarkup)
#         assert target._basis.text == view.get_text()
#         # Teardown
#         view.destroy()
#
#     @pytest.mark.skip(reason='Switch basis to value.')
#     def test_refresh(self):
#         """Confirm removal of fact information."""
#         # Setup
#         TEXT = 'The Parrot Sketch'
#         basis = BUI.BridgeTextMarkup()
#         basis.text = TEXT
#         target = MASPECT.AspectBridge[BUI.ViewTextMarkup](p_value=basis)
#         # Test
#         target.set_presentation()
#         # Method is no-op. Hnece, test passes if call succeeds.


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
        source = MASPECT.AspectPlain()
        source.set_presentation(p_value=TEXT)
        # Test: type difference
        assert not source.__eq__(TEXT)
        # Test: text difference
        target = MASPECT.AspectPlain()
        target.set_presentation(p_value=TEXT_DIFF)
        assert not source.__eq__(target)
        # Test: Equivalence
        target = MASPECT.AspectPlain()
        target.set_presentation(p_value=TEXT)
        assert source.__eq__(target)

    def test_init(self):
        """Confirm initialization."""
        # Setup
        DEFAULT = ''
        # Test
        target = MASPECT.AspectPlain()
        assert isinstance(target._presentation, BUI.BridgeTextStatic)
        assert DEFAULT == target._presentation.text

    def test_clear_presentation(self):
        """Confirm presentation is default."""
        # Setup
        DEFAULT = ''
        target = MASPECT.AspectPlain()
        target._presentation.text = 'Something completely different.'
        # Test
        target.clear_presentation()
        assert DEFAULT == target._presentation.text

    def test_new_view(self):
        """Confirm view returned."""
        # Setup
        target = MASPECT.AspectPlain()
        TEXT = 'The Parrot Sketch'
        target.set_presentation(p_value=TEXT)
        # Test
        view = target.new_view()
        assert isinstance(view, MASPECT.ViewAspectPlain)
        assert target._presentation.text == view.get_text()
        # Teardown
        view.destroy()

    def test_set_presentation(self):
        """Confirm presentation matches fact value."""
        # Setup
        target = MASPECT.AspectPlain()
        TEXT = 'The Parrot Sketch'
        # Test
        target.set_presentation(p_value=TEXT)
        assert TEXT == target._presentation.text
