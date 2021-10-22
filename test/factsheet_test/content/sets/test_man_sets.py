"""
Unit tests fanifest function of sets section of Factsheet content.  See
:mod:`~.man_sets`.
"""
import factsheet.content.heading as XHEADING
import factsheet.content.sets.man_sets as XMAN_SET
import factsheet.view.types_view as VTYPES


class TestSets:
    """Unit tests for content initialization."""

    def test_new_templates(self):
        """Confirm template outline initialization."""
        # Setup
        VIEW_TOPICS = VTYPES.ViewOutlineTopics()
        N_HEADINGS = 1
        NAME = '<i>Sets</i>'
        N_CHILDREN = 1
        # Test
        target = XMAN_SET.new_templates(lambda: VIEW_TOPICS)
        assert isinstance(target, ASHEET.AdaptTreeStoreTemplate)
        model = target._ui_model
        assert N_HEADINGS == len(model)
        i_first = model.get_iter_first()
        heading = target.get_item(i_first)
        assert isinstance(heading, XHEADING.Heading)
        assert NAME == heading.name
        assert N_CHILDREN == model.iter_n_children(i_first)
