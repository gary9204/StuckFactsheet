"""
Defines unit tests for type aliases of model components.  See
:mod:`.types_model`.
"""
import factsheet.adapt_gtk.adapt_infoid as AINFOID
import factsheet.adapt_gtk.adapt_outline as AOUTLINE
import factsheet.adapt_gtk.adapt_sheet as ASHEET
import factsheet.adapt_gtk.adapt_topic as ATOPIC
import factsheet.model.types_model as MTYPES
# from factsheet.view import types_view as VTYPES

from factsheet.abc_types.abc_topic import TagTopic


class TestTypesModel:
    """Unit tests for :mod:`.types_model`."""

    def test_types(self):
        """Confirm alias definitions for type hints."""
        # Setup
        # Test
        assert MTYPES.ModelName is AINFOID.AdaptEntryBuffer
        assert MTYPES.ModelSummary is AINFOID.AdaptTextBuffer
        assert MTYPES.ModelTitle is AINFOID.AdaptEntryBuffer

        assert MTYPES.IndexOutline is AOUTLINE.IndexGtk

        assert MTYPES.OutlineTemplates is ASHEET.AdaptTreeStoreTemplate
        assert MTYPES.OutlineTopics is ASHEET.AdaptTreeStoreTopic

        assert MTYPES.IndexFact is ATOPIC.IndexFact
        assert MTYPES.OutlineFacts is ATOPIC.AdaptTreeStoreFact
        assert MTYPES.TagTopic is TagTopic
