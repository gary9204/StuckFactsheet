"""
Unit tests for GTK-based adapter classes.  See :mod:`.adapt`.
"""
import pytest  # type: ignore[import]
import typing

import factsheet.adapt_gtk.adapt_text as ATEXT
import factsheet.adapt_gtk.adapt_value as AVALUE
import factsheet.adapt_gtk.adapt as ADAPT


class PatchAdaptText(ADAPT.AdaptText[typing.Any]):
    """Class with stub for methods abstract in :class:`.AdaptText`."""

    def __init__(self): super().__init__()

    def attach_view(self): super().attach_view(None)

    def detach_view(self): super().detach_view(None)

    @property
    def text(self):
        prop = getattr(ADAPT.AdaptText, 'text')
        prop.fget(self)

    @text.setter
    def text(self, value):
        prop = getattr(ADAPT.AdaptText, 'text')
        prop.fset(self, value)


class PatchAdaptValue(ADAPT.AdaptValue[typing.Any]):
    """Class with stub for methods abstract in :class:`.AdaptValue`."""

    def __init__(self): super().__init__()

    def attach_aspect(self): super().attach_aspect(None)

    def detach_aspect(self): super().detach_aspect(None)


class TestAdaptAbstract:
    """Unit tests for abstract methods and properties of adapter classes.

    See the base class for each of the patch classes above.
    """

    @pytest.mark.parametrize('CLASS, ARGS', [
        (ADAPT.AdaptText, dict()),
        (ADAPT.AdaptValue, dict(p_value=None)),
        ])
    def test_abstract_class(self, CLASS, ARGS):
        """Confirm the interface class is abstract."""
        # Setup
        # Test
        with pytest.raises(TypeError):
            _ = CLASS(**ARGS)

    @pytest.mark.parametrize('PATCH_CLASS, NAME_METHOD', [
        (PatchAdaptText, 'attach_view'),
        (PatchAdaptText, 'detach_view'),
        (PatchAdaptValue, 'attach_aspect'),
        (PatchAdaptValue, 'detach_aspect'),
        ])
    def test_method_abstract(self, PATCH_CLASS, NAME_METHOD):
        """Confirm each abstract method is defined."""
        # Setup
        target = PATCH_CLASS()
        method = getattr(target, NAME_METHOD)
        # Test
        with pytest.raises(NotImplementedError):
            method()

    @pytest.mark.parametrize('PATCH_CLASS, NAME_PROP, HAS_SETTER', [
        (PatchAdaptText, 'text', True),
        ])
    def test_property_abstract(self, PATCH_CLASS, NAME_PROP, HAS_SETTER):
        """Confirm access limits of each abstract property."""
        # Setup
        _ = PATCH_CLASS()  # Confirms abstract method override.
        # Test
        target = getattr(PATCH_CLASS, NAME_PROP)
        with pytest.raises(NotImplementedError):
            target.fget(self)
        if HAS_SETTER:
            with pytest.raises(NotImplementedError):
                target.fset(self, 'Oops!')
        else:
            assert target.fset is None
        assert target.fdel is None


class TestAdaptTypes:
    """Unit tests for definitions of API classes and type hints in
    :mod:`.adapt`.
    """

    @pytest.mark.parametrize('TYPE_TARGET, TYPE_SOURCE', [
        (ADAPT.AdaptText, ATEXT.AdaptText),
        (ADAPT.AdaptTextFormat, ATEXT.AdaptTextFormat),
        (ADAPT.AdaptTextMarkup, ATEXT.AdaptTextMarkup),
        (ADAPT.AdaptTextStatic, ATEXT.AdaptTextStatic),
        (ADAPT.ViewTextFormat, ATEXT.ViewTextFormat),
        (ADAPT.ViewTextMarkup, ATEXT.ViewTextMarkup),
        (ADAPT.ViewTextStatic, ATEXT.ViewTextStatic),

        (ADAPT.AdaptValue, AVALUE.AdaptValue),
        (ADAPT.AspectValueOpaque, AVALUE.AspectValueOpaque),
        (ADAPT.AspectValueText, AVALUE.AspectValueText),
        (ADAPT.ValueOpaque, AVALUE.ValueOpaque),
        ])
    def test_types(self, TYPE_TARGET, TYPE_SOURCE):
        """Confirm API definitions."""
        # Setup
        # Test
        assert TYPE_TARGET is TYPE_SOURCE
