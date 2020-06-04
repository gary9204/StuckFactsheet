"""
Unit tests for sets section of Factsheet content.  See
:mod:`~factsheet.content.sets`.
"""
from factsheet.adapt_gtk import adapt_sheet as ASHEET
from factsheet.content import heading as XHEADING
from factsheet.content import sets as XSET


class TestSets:
    """Unit tests for content initialization."""

    def test_builtin(self):
        """Confirm content initialization."""
        # Setup
        N_HEADINGS = 1
        NAME = '<i>Sets</i>'
        PATH = '0'
        N_CHILDREN = 1
        # Test
        assert isinstance(XSET.BUILTIN, ASHEET.AdaptTreeStoreTemplate)
        model = XSET.BUILTIN._gtk_model
        assert N_HEADINGS == len(model)
        i_first = model.get_iter_first()
        heading = XSET.BUILTIN.get_item(i_first)
        assert isinstance(heading, XHEADING.Heading)
        assert NAME == heading.name
        assert PATH == model.get_string_from_iter(XSET.i_sets)
        assert N_CHILDREN == model.iter_n_children(i_first)
