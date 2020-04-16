"""
Unit tests for topic abstract interfaces.
"""
import pytest   # type: ignore[import]

import factsheet.abc_types.abc_topic as ABC_TOPIC


class TestInterfacePaneTopic:
    """Unit tests for interface :class:`.InterfacePaneTopic`."""

    def test_abstract_class(self):
        """Confirm the interface class is abstract."""
        # Setup
        # Test
        with pytest.raises(TypeError):
            _ = ABC_TOPIC.InterfacePaneTopic()

    @pytest.mark.parametrize('name_method', [
        'get_infoid',
        ])
    def test_must_override(self, name_method):
        """Confirm each method must be overridden."""
        # Setup
        class PatchPaneTopic(ABC_TOPIC.InterfacePaneTopic):
            def get_infoid(self): super().get_infoid()

        target = PatchPaneTopic()
        # Test
        with pytest.raises(NotImplementedError):
            method = getattr(target, name_method)
            method()
