"""
Unit tests for GTK-based factory classes.

See :mod:`.adapt_factory`.
"""


from factsheet.adapt_gtk import adapt_factory as AFACTORY
from factsheet.adapt_gtk import adapt_text as ATEXT
from factsheet.adapt_gtk import adapt_view as AVIEW


class TestFactoryHeaderGtk:
    """Unit tests for :class:`.FactoryHeaderGtk`."""

    def test_new_title_model(self):
        """Confirm factory produces model Title instance. """
        # Setup
        factory = AFACTORY.FactoryHeaderGtk()
        text = 'Something completely different'
        # Test
        title_model = factory.new_title_model(p_text=text)
        assert isinstance(title_model, ATEXT.AdaptEntryBuffer)
        assert text == str(title_model)

    def test_new_title_view(self):
        """Confirm factory produces model Title instance. """
        # Setup
        factory = AFACTORY.FactoryHeaderGtk()
        # Test
        title_view = factory.new_title_view()
        assert isinstance(title_view, AVIEW.AdaptEntry)
