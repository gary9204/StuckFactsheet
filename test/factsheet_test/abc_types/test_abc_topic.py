"""
Unit tests for topic abstract interfaces.
"""
import pytest   # type: ignore[import]

import factsheet.abc_types.abc_topic as ABC_TOPIC


class TestInterfaceViewTopic:
    """Unit tests for interface :class:`.InterfaceViewTopic`."""

    def test_abstract_class(self):
        """Confirm the interface class is abstract."""
        # Setup
        # Test
        with pytest.raises(TypeError):
            _ = ABC_TOPIC.InterfaceViewTopic()

    @pytest.mark.parametrize('name_method', [
        'get_infoid',
        ])
    def test_must_override(self, name_method):
        """Confirm each method must be overridden."""
        # Setup
        class PatchViewTopic(ABC_TOPIC.InterfaceViewTopic):
            def get_infoid(self): super().get_infoid()

        target = PatchViewTopic()
        # Test
        with pytest.raises(NotImplementedError):
            method = getattr(target, name_method)
            method()
