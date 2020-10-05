"""
Unit tests for topic abstract interfaces.  See :mod:`.abc_topic`.
"""
import pytest   # type: ignore[import]

import factsheet.abc_types.abc_outline as ABC_OUTLINE
import factsheet.abc_types.abc_topic as ABC_TOPIC


class TestAbstractTopic:
    """Unit tests for :class:`.AbstractTopic`."""

    def test_abstract_class(self):
        """Confirm the interface class is abstract."""
        # Setup
        # Test
        with pytest.raises(TypeError):
            _ = ABC_TOPIC.AbstractTopic()

    @pytest.mark.parametrize('name_method', [
        'attach_form',
        'check_fact',
        'clear_all',
        'clear_fact',
        'detach_form',
        ])
    def test_must_override(self, name_method):
        """Confirm each method must be overridden."""
        # Setup
        class PatchTopic(ABC_TOPIC.AbstractTopic):
            def attach_form(self): return super().attach_form(None)

            def check_fact(self): return super().check_fact(None)

            def clear_all(self): return super().clear_all()

            def clear_fact(self): return super().clear_fact(None)

            def detach_form(self): return super().detach_form(None)

            def init_identity(self): return super().init_identity()

            def name(self): return super().name

            def summary(self): return super().summary

            def tag(self): return super().id_topic

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
        'get_view_facts',
        ])
    def test_must_override(self, name_method):
        """Confirm each method must be overridden."""
        # Setup
        class PatchFormTopic(ABC_TOPIC.InterfaceFormTopic):
            def get_infoid(self): super().get_infoid()

            def get_view_facts(self): super().get_view_facts()

        target = PatchFormTopic()
        # Test
        with pytest.raises(NotImplementedError):
            method = getattr(target, name_method)
            method()


class TestTypes:
    """Unit tests for type definitions in :mod:`.abc_topic`."""

    def test_types(self):
        """Confirm types defined."""
        # Setup
        # Test
        assert ABC_TOPIC.IndexOpaque is ABC_OUTLINE.IndexOpaque
        assert ABC_TOPIC.TagTopic is not None
