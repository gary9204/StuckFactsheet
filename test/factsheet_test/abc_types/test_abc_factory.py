"""
Unit tests for abstract factory classes.

See :mod:`.abc_factory`.
"""

import pytest   # type: ignore[import]

from factsheet.abc_types import abc_factory as ABC_FACTORY


class TestFactoryHeader:
    """Unit tests for abstract Header factory :class:`.FactoryHeaderGtk`."""

    def test_abstract_class(self):
        """Confirm the factory class is abstract."""
        # Setup
        # Test
        with pytest.raises(TypeError):
            _ = ABC_FACTORY.FactoryHead()

    @pytest.mark.parametrize('name_method', [
        'new_title_model',
        'new_title_view',
        ])
    def test_must_override(self, name_method):
        """Confirm each method must be overridden."""
        # Setup
        class PatchFactory(ABC_FACTORY.FactoryHead):
            def new_title_model(self): super().new_title_model()

            def new_title_view(self): super().new_title_view()

        target = PatchFactory()
        # Test
        with pytest.raises(NotImplementedError):
            method = getattr(target, name_method)
            method()
