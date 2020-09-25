"""
Unit tests for manifest function of integer operations subsection of
operations section.  See :mod:`~.factsheet.content.ops.int`.
"""
import factsheet.adapt_gtk.adapt_sheet as ASHEET
import factsheet.content.heading as XHEADING
import factsheet.content.ops.int.man_opint as XMAN_OPINT
import factsheet.view.types_view as VTYPES


class TestOpInteger:
    """Unit tests for content initialization."""

    def test_new_templates(self):
        """Confirm template outline initialization."""
        # Setup
        # VIEW_TOPICS = UI.FACTORY_SHEET.new_view_outline_topics()
        VIEW_TOPICS = VTYPES.ViewOutlineTopics()
        N_HEADINGS = 1
        NAME = '<i>Integer</i>'
        N_CHILDREN = 1
        # Test
        target = XMAN_OPINT.new_templates(lambda: VIEW_TOPICS)
        assert isinstance(target, ASHEET.AdaptTreeStoreTemplate)
        model = target._gtk_model
        assert N_HEADINGS == len(model)
        i_first = model.get_iter_first()
        heading = target.get_item(i_first)
        assert isinstance(heading, XHEADING.Heading)
        assert NAME == heading.name
        assert N_CHILDREN == model.iter_n_children(i_first)
