"""
Unit tests for sets section of Factsheet content.  See
:mod:`~factsheet.content.sets`.
"""
from factsheet.adapt_gtk import adapt_sheet as ASHEET
from factsheet.content import heading as XHEADING
from factsheet.content import sets as XSET


class TestSets:
    """Unit tests for content initialization."""

    def test_new_templates(self):
        """Confirm template outline initialization."""
        # Setup
        N_HEADINGS = 1
        NAME = '<i>Sets</i>'
        N_CHILDREN = 1
        # Test
        target = XSET.new_templates()
        assert isinstance(target, ASHEET.AdaptTreeStoreTemplate)
        model = target._gtk_model
        assert N_HEADINGS == len(model)
        i_first = model.get_iter_first()
        heading = target.get_item(i_first)
        assert isinstance(heading, XHEADING.Heading)
        assert NAME == heading.name
        assert N_CHILDREN == model.iter_n_children(i_first)
