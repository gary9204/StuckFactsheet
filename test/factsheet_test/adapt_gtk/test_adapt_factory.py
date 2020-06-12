"""
Unit tests for GTK-based factories.

See :mod:`.adapt_factory`.
"""
import pytest   # type: ignore[import]

from factsheet.adapt_gtk import adapt_factory as AFACTORY
from factsheet.adapt_gtk import adapt_infoid as AINFOID
from factsheet.adapt_gtk import adapt_outline as AOUTLINE
from factsheet.adapt_gtk import adapt_sheet as ASHEET


class TestFactoryInfoId:
    """Unit tests for :class:`~.adapt_factory.FactoryInfoId`."""

    @pytest.mark.parametrize('name_method, class_attr', [
        ('new_model_name', AINFOID.AdaptEntryBuffer),
        ('new_model_summary', AINFOID.AdaptTextBuffer),
        ('new_model_title', AINFOID.AdaptEntryBuffer),
        ])
    def test_new_attr_model(self, name_method, class_attr):
        """Confirm factory produces instance of each
        :mod:`~factsheet.model` attribute.
        """
        # Setup
        factory = AFACTORY.FactoryInfoId()
        TEXT = 'Something completely different'
        target = getattr(factory, name_method)
        # Test
        attr_model = target(p_text=TEXT)
        assert isinstance(attr_model, class_attr)
        assert TEXT == str(attr_model)

    @pytest.mark.parametrize('name_method, class_attr', [
        ('new_view_name', AINFOID.AdaptEntry),
        ('new_view_summary', AINFOID.AdaptTextView),
        ('new_view_title', AINFOID.AdaptEntry),
        ])
    def test_new_attr_view(self, name_method, class_attr):
        """Confirm factory produces instance of each
        :mod:`~factsheet.view` attribute.
        """
        # Setup
        factory = AFACTORY.FactoryInfoId()
        target = getattr(factory, name_method)
        # Test
        attr_view = target()
        assert isinstance(attr_view, class_attr)


class TestFactorySheet:
    """Unit tests for :class:`~.adapt_factory.FactorySheet`."""

    @pytest.mark.parametrize('name_method, class_attr', [
        ('new_model_outline_templates', ASHEET.AdaptTreeStoreTemplate),
        ('new_view_outline_templates', ASHEET.AdaptTreeViewTemplate),
        ('new_model_outline_topics', ASHEET.AdaptTreeStoreTopic),
        ('new_view_outline_topics', ASHEET.AdaptTreeViewTopic),
        ])
    def test_new_attr(self, name_method, class_attr):
        """Confirm factory produces instance of each
        :mod:`~factsheet.model` and each :mod:`~factsheet.view`
        attribute.
        """
        # Setup
        factory = AFACTORY.FactorySheet()
        target = getattr(factory, name_method)
        # Test
        attr_model = target()
        assert isinstance(attr_model, class_attr)

    def test_types(self):
        """Confirm alias definitions for type hints."""
        # Setup
        # Test
        assert AFACTORY.IndexOutline is AOUTLINE.AdaptIndex
        assert AFACTORY.OutlineTemplates is ASHEET.AdaptTreeStoreTemplate
        assert AFACTORY.OutlineTopics is ASHEET.AdaptTreeStoreTopic
