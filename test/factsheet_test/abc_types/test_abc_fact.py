"""
Unit tests for fact abstract interfaces.  See :mod:`.abc_fact`.
"""
import pytest   # type: ignore[import]

import factsheet.abc_types.abc_fact as ABC_FACT


class TestTypes:
    """Unit tests for type definitions in :mod:`.abc_fact`."""

    def test_types(self):
        """Confirm types defined."""
        # Setup
        # Test
        assert ABC_FACT.IdFact is not None


class TestAbstractFact:
    """Unit tests for interface :class:`.AbstractFact`."""

    def test_abstract_class(self):
        """Confirm the interface class is abstract."""
        # Setup
        # Test
        with pytest.raises(TypeError):
            _ = ABC_FACT.AbstractFact()

    @pytest.mark.parametrize('name_method', [
        'id_fact',
        'name',
        'summary',
        'title',
        ])
    def test_must_override(self, name_method):
        """Confirm each method must be overridden."""
        # Setup
        class PatchFact(ABC_FACT.AbstractFact):
            def id_fact(self): return super().id_fact

            def name(self): return super().name

            def summary(self): return super().summary

            def title(self): return super().title

            def is_fresh(self): super().is_fresh()

            def is_stale(self): super().is_stale()

            def set_fresh(self): super().set_fresh()

            def set_stale(self): super().set_stale()

        target = PatchFact()
        # Test
        with pytest.raises(NotImplementedError):
            method = getattr(target, name_method)
            method()


class TestInterfacePaneFact:
    """Unit tests for interface :class:`.InterfacePaneFact`."""

    def test_abstract_class(self):
        """Confirm the interface class is abstract."""
        # Setup
        # Test
        with pytest.raises(TypeError):
            _ = ABC_FACT.InterfacePaneFact()

    @pytest.mark.parametrize('name_method', [
        'get_infoid',
        ])
    def test_must_override(self, name_method):
        """Confirm each method must be overridden."""
        # Setup
        class PatchPaneFact(ABC_FACT.InterfacePaneFact):
            def get_infoid(self): super().get_infoid()

            def get_view_facts(self): super().get_view_facts()

        target = PatchPaneFact()
        # Test
        with pytest.raises(NotImplementedError):
            method = getattr(target, name_method)
            method()
