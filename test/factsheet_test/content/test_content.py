"""
Unit tests for initialization of Factsheet content.  See
:mod:`~.factsheet.content`.
"""
from factsheet import content as XCONTENT
from factsheet.adapt_gtk import adapt_sheet as ASHEET


class TestContent:
    """Unit tests for content initialization."""

    def test_builtin(self):
        """Confirm content initialization."""
        # Setup
        N_ITEMS = 2
        # Test
        assert isinstance(XCONTENT.BUILTIN, ASHEET.AdaptTreeStoreTemplate)
        model = XCONTENT.BUILTIN._gtk_model
        assert N_ITEMS == len(model)
