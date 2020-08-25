"""
Defines unit tests for type aliases of model components.  See
:mod:`.types_model`.
"""
from factsheet.adapt_gtk import adapt_infoid as AINFOID
from factsheet.adapt_gtk import adapt_outline as AOUTLINE
from factsheet.adapt_gtk import adapt_sheet as ASHEET
from factsheet.adapt_gtk import adapt_topic as ATOPIC
from factsheet.model import types_model as MTYPES
# from factsheet.view import types_view as VTYPES


class TestTypesModel:
    """Unit tests for :mod:`.types_model`."""

    def test_types(self):
        """Confirm alias definitions for type hints."""
        # Setup
        # Test
        assert MTYPES.ModelName is AINFOID.AdaptEntryBuffer
        assert MTYPES.ModelSummary is AINFOID.AdaptTextBuffer
        assert MTYPES.ModelTitle is AINFOID.AdaptEntryBuffer

        assert MTYPES.IndexOutline is AOUTLINE.AdaptIndex

        assert MTYPES.OutlineTemplates is ASHEET.AdaptTreeStoreTemplate
        assert MTYPES.OutlineTopics is ASHEET.AdaptTreeStoreTopic

        assert MTYPES.IdTopic is ATOPIC.IdTopic
        assert MTYPES.OutlineFacts is ATOPIC.AdaptTreeStoreFact
