"""
Unit tests for GTK-based factory classes.

See :mod:`.adapt_factory`.
"""
from factsheet.adapt_gtk import adapt_factory as AFACTORY
from factsheet.adapt_gtk import adapt_text as ATEXT
from factsheet.adapt_gtk import adapt_view as AVIEW


class TestFactoryInfoId:
    """Unit tests for :class:`~.adapt_factory.FactoryInfoId`."""

    def test_new_title_model(self):
        """Confirm factory produces instance of :mod:`~factsheet.model`
        title.
        """
        # Setup
        factory = AFACTORY.FactoryInfoId()
        text = 'Something completely different'
        # Test
        title_model = factory.new_model_title(p_text=text)
        assert isinstance(title_model, ATEXT.AdaptEntryBuffer)
        assert text == str(title_model)

    def test_new_title_view(self):
        """Confirm factory produces instance of :mod:`~factsheet.view`
        title.
        """
        # Setup
        factory = AFACTORY.FactoryInfoId()
        # Test
        title_view = factory.new_view_title()
        assert isinstance(title_view, AVIEW.AdaptEntry)
