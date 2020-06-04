"""
Unit tests for integer subsection of sets content.  See
:mod:`~.factsheet.content.sets.integer`.
"""
from factsheet.adapt_gtk import adapt_sheet as ASHEET
from factsheet.content import heading as XHEADING
from factsheet.content.sets import integer as XINTEGER


class TestInteger:
    """Unit tests for content initialization."""

    def test_builtin(self):
        """Confirm content initialization."""
        # Setup
        N_HEADINGS = 1
        NAME = '<i>Integer</i>'
        PATH = '0'
        N_CHILDREN = 0
        # Test
        assert isinstance(XINTEGER.BUILTIN, ASHEET.AdaptTreeStoreTemplate)
        model = XINTEGER.BUILTIN._gtk_model
        assert N_HEADINGS == len(model)
        i_first = model.get_iter_first()
        heading = XINTEGER.BUILTIN.get_item(i_first)
        assert isinstance(heading, XHEADING.Heading)
        assert NAME == heading.name
        assert PATH == model.get_string_from_iter(XINTEGER.i_integer)
        assert N_CHILDREN == model.iter_n_children(i_first)
