"""
Unit tests for fact aspect classes.  See :mod:`~.aspect`.
"""
import pytest   # type: ignore[import]

import factsheet.bridge_ui as BUI
import factsheet.model.aspect as MASPECT


@pytest.fixture
def param_plain_with_view():
    """Fixture to return plain text aspect with view."""
    aspect = MASPECT.AspectPlain()
    TEXT = 'The Parrot Sketch'
    aspect.set_presentation(p_subject=TEXT)
    view = aspect.new_view()
    yield aspect, view
    view.destroy()


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
        class PatchAspect(MASPECT.Aspect[str]):
            def __eq__(self, p_other):
                return super().__eq__(p_other)

            def __init__(self):
                self._presentation = 'Presentation defined'

            def clear_presentation(self):
                self._presentation += ', cleared'

            def new_view(self):
                raise NotImplementedError

            def set_presentation(self, p_subject):
                self._presentation += ', set to ' + p_subject

        source = PatchAspect()
        TEXT = 'The Parrot Sketch'
        source.set_presentation(p_subject=TEXT)
        # Test: type difference
        assert not source.__eq__(TEXT)
        # Test: Equivalence
        target = PatchAspect()
        target.set_presentation(p_subject=TEXT)
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
        source = MASPECT.AspectPlain()
        source.set_presentation(p_subject=TEXT)
        # Test: type difference
        assert not source.__eq__(TEXT)
        # Test: text difference
        target = MASPECT.AspectPlain()
        target.set_presentation(p_subject=TEXT_DIFF)
        assert not source.__eq__(target)
        # Test: Equivalence
        target = MASPECT.AspectPlain()
        target.set_presentation(p_subject=TEXT)
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
        """Confirm presentation is blank text."""
        # Setup
        DEFAULT = ''
        target = MASPECT.AspectPlain()
        target._presentation.text = 'Something completely different.'
        # Test
        target.clear_presentation()
        assert DEFAULT == target._presentation.text

    def test_new_view(self, param_plain_with_view):
        """Confirm view returned."""
        # Setup
        target, view = param_plain_with_view
        # Test
        assert isinstance(view, MASPECT.ViewAspectPlain)
        assert target._presentation.text == view.get_text()

    def test_set_presentation(self):
        """Confirm presentation matches attribute."""
        # Setup
        target = MASPECT.AspectPlain()
        TEXT = 'The Parrot Sketch'
        # Test
        target.set_presentation(p_subject=TEXT)
        assert TEXT == target._presentation.text
