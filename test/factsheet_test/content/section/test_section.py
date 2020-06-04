"""
Unit tests for section template of Factsheet content.  See
:mod:`~.factsheet.content.section`.
"""
from factsheet.adapt_gtk import adapt_sheet as ASHEET
from factsheet.content import section as XSECTION
from factsheet.content.section import section_spec as XSPEC


class TestSection:
    """Unit tests for content initialization."""

    def test_builtin(self):
        """Confirm content initialization."""
        # Setup
        N_ITEMS = 1
        NAME = 'Section'
        PATH = '0'
        N_CHILDREN = 0
        # Test
        assert isinstance(XSECTION.BUILTIN, ASHEET.AdaptTreeStoreTemplate)
        model = XSECTION.BUILTIN._gtk_model
        assert N_ITEMS == len(model)
        i_first = model.get_iter_first()
        item = XSECTION.BUILTIN.get_item(i_first)
        assert isinstance(item, XSPEC.Section)
        assert NAME == item.name
        assert PATH == model.get_string_from_iter(XSECTION.i_sets)
        assert N_CHILDREN == model.iter_n_children(i_first)
