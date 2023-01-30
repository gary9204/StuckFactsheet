"""
Unit tests common to abstract interfaces.

There are test to confirm a class is abstract and to confirm definitions
of abstract methods and propreties.
"""
import pytest

import factsheet.abc_types.abc_stalefile as ABC_STALE


class PatchInterfaceStalefile(ABC_STALE.InterfaceStaleFile):
    """Abstract method overrides for :class:`.InterfaceStaleFile`."""

    def has_not_changed(self): super().has_not_changed()

    def is_stale(self): super().is_stale()

    def set_fresh(self): super().set_fresh()

    def set_stale(self): super().set_stale()


class TestInterface:
    """Unit tests for abstract interfaces.

    See the base class for each of the patch classes above.
    """

    @pytest.mark.parametrize('CLASS', [
        ABC_STALE.InterfaceStaleFile,
        ])
    def test_abstract_class(self, CLASS):
        """Confirm the interface class is abstract."""
        # Setup
        # Test
        with pytest.raises(TypeError):
            _ = CLASS()

    @pytest.mark.parametrize('PATCH_CLASS, NAME_METHOD', [
        (PatchInterfaceStalefile, 'has_not_changed'),
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
