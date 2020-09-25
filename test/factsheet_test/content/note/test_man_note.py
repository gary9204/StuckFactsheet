"""
Unit tests for manifest function of section template.  See
:mod:`.man_note`.
"""
import factsheet.adapt_gtk.adapt_sheet as ASHEET
import factsheet.content.note.man_note as XMAN_NOTE
import factsheet.content.note.note_spec as XSPEC_NOTE
import factsheet.view.types_view as VTYPES


class TestSection:
    """Unit tests for content initialization."""

    def test_new_templates(self):
        """Confirm template outline initialization."""
        # Setup
        VIEW_TOPICS = VTYPES.ViewOutlineTopics()
        N_HEADINGS = 1
        NAME = 'Note'
        N_CHILDREN = 0
        # Test
        target = XMAN_NOTE.new_templates(lambda: VIEW_TOPICS)
        assert isinstance(target, ASHEET.AdaptTreeStoreTemplate)
        model = target._gtk_model
        assert N_HEADINGS == len(model)
        i_first = model.get_iter_first()
        heading = target.get_item(i_first)
        assert isinstance(heading, XSPEC_NOTE.SpecNote)
        assert NAME == heading.name
        assert N_CHILDREN == model.iter_n_children(i_first)
