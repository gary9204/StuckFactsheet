"""
Unit tests for GTK-based adapter classes.  See :mod:`.adapt`.
"""
import pytest  # type: ignore[import]
import typing

import factsheet.adapt_gtk.adapt_text as ATEXT
import factsheet.adapt_gtk.adapt_value as AVALUE
import factsheet.adapt_gtk.adapt as ADAPT


class PatchAdaptText(ADAPT.AdaptText[typing.Any, typing.Any]):
    """Class with stub for methods abstract in :class:`.AdaptText`."""

    # def __init__(self): super().__init__()

    def _bind_store(self): super()._bind_store(None)

    def _loose_store(self): super()._loose_store(None)

    def _new_store_gtk(self): super()._new_store_gtk()

    @property
    def text(self):
        prop = getattr(ADAPT.AdaptText, 'text')
        prop.fget(self)

    @text.setter
    def text(self, value):
        prop = getattr(ADAPT.AdaptText, 'text')
        prop.fset(self, value)


class PatchFormatValue(ADAPT.FormatValue[typing.Any, typing.Any]):
    """Class with stub for methods abstract in :class:`.FormatValue`."""

    def __init__(self): pass

    def attach_aspect(self): super().attach_aspect(None)

    def clear(self): super().clear()

    def detach_aspect(self): super().detach_aspect(None)

    def set(self): super().set(None)


class TestAdaptAbstract:
    """Unit tests for abstract methods and properties of adapter classes.

    See the base class for each of the patch classes above.
    """

    @pytest.mark.parametrize('CLASS, ARGS', [
        (ADAPT.AdaptText, dict()),
        (ADAPT.FormatValue, dict(p_value=None)),
        ])
    def test_abstract_class(self, CLASS, ARGS):
        """Confirm the interface class is abstract."""
        # Setup
        # Test
        with pytest.raises(TypeError):
            _ = CLASS(**ARGS)

    @pytest.mark.parametrize('PATCH_CLASS, NAME_METHOD', [
        (PatchAdaptText, '_bind_store'),
        (PatchAdaptText, '_loose_store'),
        (PatchAdaptText, '_new_store_gtk'),
        (PatchFormatValue, 'attach_aspect'),
        (PatchFormatValue, 'detach_aspect'),
        (PatchFormatValue, 'clear'),
        (PatchFormatValue, 'set'),
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
    def test_property_access(self, PATCH_CLASS, NAME_PROP, HAS_SETTER):
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

        (ADAPT.FormatValue, AVALUE.FormatValue),
        (ADAPT.FormatValuePlain, AVALUE.FormatValuePlain),
        (ADAPT.AspectValueOpaque, AVALUE.AspectValueOpaque),
        (ADAPT.AspectValuePlain, AVALUE.AspectValuePlain),
        (ADAPT.ValueOpaque, AVALUE.ValueOpaque),
        ])
    def test_types(self, TYPE_TARGET, TYPE_SOURCE):
        """Confirm API definitions."""
        # Setup
        # Test
        assert TYPE_TARGET == TYPE_SOURCE
