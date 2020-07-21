"""
Unit tests for integer subsection of sets content.  See
:mod:`~.factsheet.content.sets.int`.
"""
from factsheet.adapt_gtk import adapt_sheet as ASHEET
from factsheet.content import heading as XHEADING
from factsheet.content.sets import int as XINTEGER
from factsheet.view import ui as UI


class TestInteger:
    """Unit tests for content initialization."""

    def test_new_templates(self):
        """Confirm template outline initialization."""
        # Setup
        VIEW_TOPICS = UI.FACTORY_SHEET.new_view_outline_topics()
        N_HEADINGS = 1
        NAME = '<i>Integer</i>'
        N_CHILDREN = 1
        # Test
        target = XINTEGER.new_templates(lambda: VIEW_TOPICS)
        assert isinstance(target, ASHEET.AdaptTreeStoreTemplate)
        model = target._gtk_model
        assert N_HEADINGS == len(model)
        i_first = model.get_iter_first()
        heading = target.get_item(i_first)
        assert isinstance(heading, XHEADING.Heading)
        assert NAME == heading.name
        assert N_CHILDREN == model.iter_n_children(i_first)
