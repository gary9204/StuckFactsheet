"""
Unit tests for topic abstract interfaces.  See :mod:`.abc_topic`.
"""
import pytest   # type: ignore[import]

import factsheet.abc_types.abc_topic as ABC_TOPIC


class TestTypes:
    """Unit tests for type definitions in :mod:`.abc_topic`."""

    def test_types(self):
        """Confirm types defined."""
        # Setup
        # Test
        assert ABC_TOPIC.IdTopic is not None


class TestAbstractTopic:
    """Unit tests for :class:`.AbstractTopic`."""

    def test_abstract_class(self):
        """Confirm the interface class is abstract."""
        # Setup
        # Test
        with pytest.raises(TypeError):
            _ = ABC_TOPIC.AbstractTopic()

    @pytest.mark.parametrize('name_method', [
        'id_topic',
        'name',
        'summary',
        'title',
        ])
    def test_must_override(self, name_method):
        """Confirm each method must be overridden."""
        # Setup
        class PatchTopic(ABC_TOPIC.AbstractTopic):
            def id_topic(self): return super().id_topic

            def name(self): return super().name

            def summary(self): return super().summary

            def title(self): return super().title

            def is_fresh(self): super().is_fresh()

            def is_stale(self): super().is_stale()

            def set_fresh(self): super().set_fresh()

            def set_stale(self): super().set_stale()

        target = PatchTopic()
        # Test
        with pytest.raises(NotImplementedError):
            method = getattr(target, name_method)
            method()


class TestInterfaceFormTopic:
    """Unit tests for :class:`.InterfaceFormTopic`."""

    def test_abstract_class(self):
        """Confirm the interface class is abstract."""
        # Setup
        # Test
        with pytest.raises(TypeError):
            _ = ABC_TOPIC.InterfaceFormTopic()

    @pytest.mark.parametrize('name_method', [
        'get_infoid',
        # 'get_view_facts',
        ])
    def test_must_override(self, name_method):
        """Confirm each method must be overridden."""
        # Setup
        class PatchPaneTopic(ABC_TOPIC.InterfaceFormTopic):
            def get_infoid(self): super().get_infoid()

            def get_view_facts(self): super().get_view_facts()

        target = PatchPaneTopic()
        # Test
        with pytest.raises(NotImplementedError):
            method = getattr(target, name_method)
            method()
