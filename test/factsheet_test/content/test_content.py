"""
Unit tests for initialization of Factsheet content.  See
:mod:`~.factsheet.content`.
"""
from factsheet import content as XCONTENT
from factsheet.adapt_gtk import adapt_sheet as ASHEET


class TestContent:
    """Unit tests for content initialization."""

    def test_new_templates(self):
        """Confirm templates outline initialization."""
        # Setup
        N_HEADINGS = 2
        # Test
        target = XCONTENT.new_templates()
        assert isinstance(target, ASHEET.AdaptTreeStoreTemplate)
        model = target._gtk_model
        assert N_HEADINGS == len(model)
