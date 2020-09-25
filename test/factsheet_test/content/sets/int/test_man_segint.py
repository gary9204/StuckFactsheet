"""
Unit tests for manifest function of initial segment of natural numbers
topic.  See :mod:`.man_segint`.
"""
import factsheet.adapt_gtk.adapt_sheet as ASHEET
import factsheet.content.sets.int.man_segint as XMAN_SEGINT
import factsheet.content.sets.int.segint_spec as XSPEC_SEGINT
import factsheet.view.types_view as VTYPES


class TestInteger:
    """Unit tests for content initialization."""

    def test_new_templates(self):
        """Confirm template outline initialization."""
        # Setup
        VIEW_TOPICS = VTYPES.ViewOutlineTopics()
        N_TOPICS = 1
        NAME = 'Segment'
        N_CLASSES_FACT = 4
        # Test
        target = XMAN_SEGINT.new_templates(lambda: VIEW_TOPICS)
        assert isinstance(target, ASHEET.AdaptTreeStoreTemplate)
        model = target._gtk_model
        assert N_TOPICS == len(model)
        i_first = model.get_iter_first()
        spec = target.get_item(i_first)
        assert isinstance(spec, XSPEC_SEGINT.SpecSegInt)
        assert NAME == spec.name
        assert N_CLASSES_FACT == len(spec._protofacts)
