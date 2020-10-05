"""
Unit tests for identification information abstract classes and
interfaces.

See :mod:`.abc_infoid`.
"""
import pytest   # type: ignore[import]

import factsheet.abc_types.abc_infoid as ABC_INFOID


class TestInterfaceIdentity:
    """Unit tests for :class:`.InterfaceIdentity`."""

    def test_abstract(self):
        """Confirm class is abstract."""
        # No Setup
        # Test
        with pytest.raises(TypeError):
            _target = ABC_INFOID.InterfaceIdentity()

    @pytest.mark.parametrize('NAME_PROP, HAS_SETTER', [
        ('name', False),
        ('summary', False),
        ('tag', False),
        ('title', False),
        ])
    def test_property_abstract(self, NAME_PROP, HAS_SETTER):
        """Confirm access limits of each abstract property."""
        # Setup

        class PatchInterface(ABC_INFOID.InterfaceIdentity):

            @property
            def name(self):
                prop = getattr(ABC_INFOID.InterfaceIdentity, NAME_PROP)
                prop.fget(self)

            @property
            def summary(self):
                prop = getattr(ABC_INFOID.InterfaceIdentity, NAME_PROP)
                prop.fget(self)

            @property
            def tag(self):
                prop = getattr(ABC_INFOID.InterfaceIdentity, NAME_PROP)
                prop.fget(self)

            @property
            def title(self):
                prop = getattr(ABC_INFOID.InterfaceIdentity, NAME_PROP)
                prop.fget(self)

        _target = PatchInterface()  # Confirms abstract method override.
        # Test
        prop = getattr(PatchInterface, NAME_PROP)
        with pytest.raises(NotImplementedError):
            prop.fget(self)
        if HAS_SETTER:
            with pytest.raises(NotImplementedError):
                prop.fset(self, 'Oops!')
        else:
            assert prop.fset is None
        assert prop.fdel is None


class TestTypes:
    """Unit tests for type definitions in :mod:`.abc_infoid`."""

    def test_types(self):
        """Confirm type hint definitions."""
        # Setup
        # Test
        assert ABC_INFOID.IdNameOpaque is not None
        assert ABC_INFOID.IdSummaryOpaque is not None
        assert ABC_INFOID.TagOpaque is not None
        assert ABC_INFOID.IdTitleOpaque is not None
