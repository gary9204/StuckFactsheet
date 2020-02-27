"""
Unit tests for header abstract data type classes.
"""

import pytest   # type: ignore[import]

from factsheet.abc_types import abc_header as AHEADER


class TestAbstractTextModel:
    """Unit tests for interfaces common to model text attributes."""

    def test_abstract(self):
        """Confirm class is abstract."""
        # No Setup
        # Test
        with pytest.raises(TypeError):
            _target = AHEADER.AbstractTextModel()

    def test_eq(self):
        """Confirm equivalence comparison.

        #. Case: different type
        #. Case: different text
        #. Case: same text
        #. Case: confirm not-equal defined
        """
        # Setup
        class PatchTextModel(AHEADER.AbstractTextModel):
            def __init__(self, p_text): self.text = p_text

            def __str__(self): return self.text

            def attach_view(self, _v): pass

            def detach_view(self, _v): pass

            def is_fresh(self): super().is_fresh()

            def is_stale(self): super().is_stale()

            def set_fresh(self): super().set_fresh()

            def set_stale(self): super().set_stale()

        text = 'The Spanish Inquisition'
        source = PatchTextModel(text)
        # Test: different type
        target = text
        assert not source.__eq__(target)
        # Test: different text
        target = PatchTextModel('Something completely different')
        assert not source.__eq__(target)
        # Test: same text
        target = PatchTextModel(text)
        assert source.__eq__(target)
        # Test: confirm not-equal defined
        assert not source.__ne__(target)

    @pytest.mark.parametrize('name_method', [
        '__str__',
        'attach_view',
        'detach_view',
        ])
    def test_must_override(self, name_method):
        """Confirm each method must be overridden."""
        # Setup
        class PatchTextModel(AHEADER.AbstractTextModel):
            def __eq__(self, _o): return False

            def __str__(self): super().__str__()

            def attach_view(self): super().attach_view(None)

            def detach_view(self): super().detach_view(None)

            def is_fresh(self): super().is_fresh()

            def is_stale(self): super().is_stale()

            def set_fresh(self): super().set_fresh()

            def set_stale(self): super().set_stale()

        target = PatchTextModel()
        # Test
        with pytest.raises(NotImplementedError):
            method = getattr(target, name_method)
            method()


class TestFactoryHeader:
    """Unit tests for abstract Header factory. """

    def test_abstract_class(self):
        """Confirm the interface class is abstract."""
        # Setup
        # Test
        with pytest.raises(TypeError):
            _ = AHEADER.FactoryHeader()

    @pytest.mark.parametrize('name_method', [
        'new_title_model',
        'new_title_view',
        ])
    def test_must_override(self, name_method):
        """Confirm each method must be overridden."""
        # Setup
        class PatchFactory(AHEADER.FactoryHeader):
            def new_title_model(self): super().new_title_model()

            def new_title_view(self): super().new_title_view()

        target = PatchFactory()
        # Test
        with pytest.raises(NotImplementedError):
            method = getattr(target, name_method)
            method()


class TestInterfaceStaleFile:
    """Unit tests for interfaces to detect out-of-date model."""

    def test_abstract_class(self):
        """Confirm the interface class is abstract."""
        # Setup
        # Test
        with pytest.raises(TypeError):
            _ = AHEADER.InterfaceStaleFile()

    @pytest.mark.parametrize('name_method', [
        'is_fresh',
        'is_stale',
        'set_fresh',
        'set_stale',
        ])
    def test_must_override(self, name_method):
        """Confirm each method must be overridden."""
        # Setup
        class PatchInterface(AHEADER.InterfaceStaleFile):
            def is_fresh(self): super().is_fresh()

            def is_stale(self): super().is_stale()

            def set_fresh(self): super().set_fresh()

            def set_stale(self): super().set_stale()

        target = PatchInterface()
        # Test
        with pytest.raises(NotImplementedError):
            method = getattr(target, name_method)
            method()
