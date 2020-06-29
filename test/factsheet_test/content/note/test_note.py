"""
Unit tests for section template of Factsheet content.  See
:mod:`~.factsheet.content.note`.
"""
from factsheet.adapt_gtk import adapt_sheet as ASHEET
from factsheet.content import note as XNOTE


class TestSection:
    """Unit tests for content initialization."""

    def test_new_templates(self):
        """Confirm template outline initialization."""
        # Setup
        N_HEADINGS = 1
        NAME = 'Note'
        N_CHILDREN = 0
        # Test
        target = XNOTE.new_templates()
        assert isinstance(target, ASHEET.AdaptTreeStoreTemplate)
        model = target._gtk_model
        assert N_HEADINGS == len(model)
        i_first = model.get_iter_first()
        heading = target.get_item(i_first)
        assert isinstance(heading, XNOTE.note_spec.SpecNote)
        assert NAME == heading.name
        assert N_CHILDREN == model.iter_n_children(i_first)
