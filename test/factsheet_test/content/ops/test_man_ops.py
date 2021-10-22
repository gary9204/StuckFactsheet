"""
Unit tests for manifest function of operations section of Factsheet
content.  See :mod:`.man_ops`.
"""
import factsheet.content.heading as XHEADING
import factsheet.content.ops.man_ops as XMAN_OPS
import factsheet.view.types_view as VTYPES


class TestOps:
    """Unit tests for content initialization."""

    def test_new_templates(self):
        """Confirm template outline initialization."""
        # Setup
        VIEW_TOPICS = VTYPES.ViewOutlineTopics()
        N_HEADINGS = 1
        NAME = '<i>Operations</i>'
        N_CHILDREN = 1
        # Test
        target = XMAN_OPS.new_templates(lambda: VIEW_TOPICS)
        assert isinstance(target, ASHEET.AdaptTreeStoreTemplate)
        model = target._ui_model
        assert N_HEADINGS == len(model)
        i_first = model.get_iter_first()
        heading = target.get_item(i_first)
        assert isinstance(heading, XHEADING.Heading)
        assert NAME == heading.name
        assert N_CHILDREN == model.iter_n_children(i_first)
