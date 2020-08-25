"""
Unit tests for initialization of Factsheet content.  See
:mod:`~.factsheet.content`.
"""
from factsheet import content as XCONTENT
from factsheet.adapt_gtk import adapt_sheet as ASHEET
# from factsheet.view import ui as UI
from factsheet.view import types_view as VTYPES


class TestContent:
    """Unit tests for content initialization."""

    def test_new_templates(self):
        """Confirm templates outline initialization."""
        # Setup
        VIEW_TOPICS = VTYPES.ViewOutlineTopics()
        N_HEADINGS = 3
        # Test
        target = XCONTENT.new_templates(lambda: VIEW_TOPICS)
        assert isinstance(target, ASHEET.AdaptTreeStoreTemplate)
        model = target._gtk_model
        assert N_HEADINGS == len(model)
