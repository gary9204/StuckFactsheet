"""
Unit tests common to abstract interfaces.

There are test to confirm a class is abstract and to confirm definitions
of abstract methods and propreties.
"""
import pytest   # type: ignore[import]

import factsheet.abc_types.abc_fact as ABC_FACT
import factsheet.abc_types.abc_infoid as ABC_INFOID
import factsheet.abc_types.abc_stalefile as ABC_STALE
import factsheet.adapt_gtk.adapt_text as ATEXT


class PatchInterfaceAdaptText(ATEXT.AdaptText):
    """Abstract method and property overrides for :class:`.AdaptText`."""

    def attach_view(self): super().attach_view(None)

    def detach_view(self): super().detach_view(None)

    @property
    def text(self):
        prop = getattr(ATEXT.AdaptText, 'text')
        prop.fget(self)

    @text.setter
    def text(self, value):
        prop = getattr(ATEXT.AdaptText, 'text')
        prop.fset(self, value)

    # InterfaceStaleFile
    def is_fresh(self): pass

    def is_stale(self): pass

    def set_fresh(self): pass

    def set_stale(self): pass


class PatchInterfaceBlockFact(ABC_FACT.InterfaceBlockFact):
    """Abstract method overrides for :class:`.InterfaceBlockFact`."""

    def update(self): super().update(None, None)


class PatchInterfaceFact(ABC_FACT.InterfaceFact):
    """Abstract method and property overrides for :class:`.InterfaceFact`."""

    def check(self): return super().check()

    def clear(self): super().clear()

    @property
    def note(self):
        prop = getattr(ABC_FACT.InterfaceFact, 'note')
        prop.fget(self)

    @property
    def status(self):
        prop = getattr(ABC_FACT.InterfaceFact, 'status')
        prop.fget(self)

    @property
    def value(self):
        prop = getattr(ABC_FACT.InterfaceFact, 'value')
        prop.fget(self)

    # InterfaceIdentity
    @property
    def name(self): pass

    @property
    def summary(self): pass

    @property
    def tag(self): pass

    @property
    def title(self): pass

    # InterfaceStaleFile
    def is_fresh(self): pass

    def is_stale(self): pass

    def set_fresh(self): pass

    def set_stale(self): pass


class PatchInterfaceIdentity(ABC_INFOID.InterfaceIdentity):
    """Abstract property overrides for :class:`.InterfaceIdentity`."""

    @property
    def name(self):
        prop = getattr(ABC_INFOID.InterfaceIdentity, 'name')
        prop.fget(self)

    @property
    def summary(self):
        prop = getattr(ABC_INFOID.InterfaceIdentity, 'summary')
        prop.fget(self)

    @property
    def tag(self):
        prop = getattr(ABC_INFOID.InterfaceIdentity, 'tag')
        prop.fget(self)

    @property
    def title(self):
        prop = getattr(ABC_INFOID.InterfaceIdentity, 'title')
        prop.fget(self)


class PatchInterfaceStalefile(ABC_STALE.InterfaceStaleFile):
    """Abstract method overrides for :class:`.InterfaceStaleFile`."""

    def is_fresh(self): super().is_fresh()

    def is_stale(self): super().is_stale()

    def set_fresh(self): super().set_fresh()

    def set_stale(self): super().set_stale()


class TestInterface:
    """Unit tests for abstract interfaces.

    See the base class for each of the patch classes above.
    """

    @pytest.mark.parametrize('CLASS', [
        ABC_FACT.InterfaceBlockFact,
        ABC_FACT.InterfaceFact,
        ABC_INFOID.InterfaceIdentity,
        ABC_STALE.InterfaceStaleFile,
        ATEXT.AdaptText,
        ])
    def test_abstract_class(self, CLASS):
        """Confirm the interface class is abstract."""
        # Setup
        # Test
        with pytest.raises(TypeError):
            _ = CLASS()

    @pytest.mark.parametrize('PATCH_CLASS, NAME_METHOD', [
        (PatchInterfaceAdaptText, 'attach_view'),
        (PatchInterfaceAdaptText, 'detach_view'),
        (PatchInterfaceBlockFact, 'update'),
        (PatchInterfaceFact, 'check'),
        (PatchInterfaceFact, 'clear'),
        (PatchInterfaceStalefile, 'is_fresh'),
        (PatchInterfaceStalefile, 'is_stale'),
        (PatchInterfaceStalefile, 'set_fresh'),
        (PatchInterfaceStalefile, 'set_stale'),
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
        (PatchInterfaceAdaptText, 'text', True),
        (PatchInterfaceFact, 'note', False),
        (PatchInterfaceFact, 'status', False),
        (PatchInterfaceFact, 'value', False),
        (PatchInterfaceIdentity, 'name', False),
        (PatchInterfaceIdentity, 'summary', False),
        (PatchInterfaceIdentity, 'tag', False),
        (PatchInterfaceIdentity, 'title', False),
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
