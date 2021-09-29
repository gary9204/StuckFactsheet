"""
Unit tests for manifext function of Factsheet content.  See
:mod:`.man_content`.
"""
import factsheet.content.man_content as XMAN_CONTENT
import factsheet.adapt_gtk.adapt_sheet as ASHEET
import factsheet.view.types_view as VTYPES


class TestContent:
    """Unit tests for content initialization."""

    def test_new_templates(self):
        """Confirm templates outline initialization."""
        # Setup
        VIEW_TOPICS = VTYPES.ViewOutlineTopics()
        N_HEADINGS = 3
        # Test
        target = XMAN_CONTENT.new_templates(lambda: VIEW_TOPICS)
        assert isinstance(target, ASHEET.AdaptTreeStoreTemplate)
        model = target._ui_model
        assert N_HEADINGS == len(model)
