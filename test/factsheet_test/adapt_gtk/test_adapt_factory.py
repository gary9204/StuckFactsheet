"""
Unit tests for GTK-based factory classes.

See :mod:`.adapt_factory`.
"""
import pytest   # type: ignore[import]

from factsheet.adapt_gtk import adapt_factory as AFACTORY
from factsheet.adapt_gtk import adapt_infoid as AINFOID


class TestFactoryInfoId:
    """Unit tests for :class:`~.adapt_factory.FactoryInfoId`."""

    @pytest.mark.parametrize('name_method, class_attr', [
        ('new_model_name', AINFOID.AdaptEntryBuffer),
        ('new_model_title', AINFOID.AdaptEntryBuffer),
        ])
    def test_new_attr_model(self, name_method, class_attr):
        """Confirm factory produces instance of :mod:`~factsheet.model`
        attribute.
        """
        # Setup
        factory = AFACTORY.FactoryInfoId()
        text = 'Something completely different'
        target = getattr(factory, name_method)
        # Test
        attr_model = target(p_text=text)
        assert isinstance(attr_model, class_attr)
        assert text == str(attr_model)

    @pytest.mark.parametrize('name_method, class_attr', [
        ('new_view_name', AINFOID.AdaptEntry),
        ('new_view_title', AINFOID.AdaptEntry),
        ])
    def test_new_attr_view(self, name_method, class_attr):
        """Confirm factory produces instance of :mod:`~factsheet.view`
        attribute.
        """
        # Setup
        factory = AFACTORY.FactoryInfoId()
        target = getattr(factory, name_method)
        # Test
        attr_view = target()
        assert isinstance(attr_view, class_attr)
