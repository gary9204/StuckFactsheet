"""
Unit tests for fact abstract interfaces.  See :mod:`.abc_fact`.
"""
import enum
import pytest   # type: ignore[import]

import factsheet.abc_types.abc_fact as ABC_FACT


class TestAbstractFact:
    """Unit tests for interface :class:`.AbstractFact`."""

    def test_abstract_class(self):
        """Confirm the interface class is abstract."""
        # Setup
        # Test
        with pytest.raises(TypeError):
            _ = ABC_FACT.AbstractFact()

    @pytest.mark.parametrize('NAME_METHOD', [
        # 'attach_block',
        'check',
        'clear',
        # 'detach_block',
        'name',
        'status',
        'summary',
        'tag',
        'title',
        ])
    def test_must_override(self, NAME_METHOD):
        """Confirm each method must be overridden."""
        # Setup
        class PatchFact(ABC_FACT.AbstractFact):
            # def attach_block(self): return super().attach_block(None)

            def check(self): return super().check()

            def clear(self): return super().clear()

            # def detach_block(self): return super().detach_block(None)

            def name(self): return super().name

            def status(self): return super().status

            def summary(self): return super().summary

            def tag(self): return super().tag

            def title(self): return super().title

            def init_identity(self): return super().init_identity()

            def is_fresh(self): super().is_fresh()

            def is_stale(self): super().is_stale()

            def set_fresh(self): super().set_fresh()

            def set_stale(self): super().set_stale()

        target = PatchFact()
        # Test
        with pytest.raises(NotImplementedError):
            method = getattr(target, NAME_METHOD)
            method()


class TestInterfaceBlockFact:
    """Unit tests for interface :class:`.InterfaceBlockFact`."""

    def test_abstract_class(self):
        """Confirm the interface class is abstract."""
        # Setup
        # Test
        with pytest.raises(TypeError):
            _ = ABC_FACT.InterfaceBlockFact()

    @pytest.mark.parametrize('NAME_METHOD', [
        'update',
        'get_infoid',
        ])
    def test_must_override(self, NAME_METHOD):
        """Confirm each method must be overridden."""
        # Setup
        class PatchBlockFact(ABC_FACT.InterfaceBlockFact):
            def update(self): super().update(None, None)

            def get_infoid(self): super().get_infoid()

        target = PatchBlockFact()
        # Test
        with pytest.raises(NotImplementedError):
            method = getattr(target, NAME_METHOD)
            method()


class TestTypes:
    """Unit tests for type definitions in :mod:`.abc_fact`."""

    def test_types(self):
        """Confirm types defined."""
        # Setup
        # Test
        assert ABC_FACT.TagFact
        assert ABC_FACT.NameScene
        Status = ABC_FACT.StatusOfFact
        assert issubclass(Status, enum.Enum)
        assert Status.BLOCKED
        assert Status.DEFINED
        assert Status.UNCHECKED
        assert Status.UNDEFINED
        assert ABC_FACT.TopicOpaque
        assert ABC_FACT.ValueOpaque
