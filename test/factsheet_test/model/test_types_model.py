"""
Defines unit tests for type aliases of model components.  See
:mod:`.types_model`.
"""
import factsheet.adapt_gtk.adapt_infoid as AINFOID
# import factsheet.adapt_gtk.adapt_sheet as ASHEET
# import factsheet.adapt_gtk.adapt_topic as ATOPIC
import factsheet.model.types_model as MTYPES

# from factsheet.abc_types.abc_fact import TagFact
# from factsheet.abc_types.abc_topic import TagTopic


class TestTypesModel:
    """Unit tests for :mod:`.types_model`."""

    def test_types(self):
        """Confirm alias definitions for type hints."""
        # Setup
        # Test
        # assert MTYPES.ModelName is AINFOID.AdaptEntryBuffer
        # assert MTYPES.ModelSummary is AINFOID.AdaptTextBuffer
        # assert MTYPES.ModelTitle is AINFOID.AdaptEntryBuffer

        # assert MTYPES.IndexTemplate is ASHEET.IndexTemplate
        # assert MTYPES.OutlineTemplates is ASHEET.AdaptTreeStoreTemplate
        # assert MTYPES.IndexTopic is ASHEET.IndexTopic
        # assert MTYPES.OutlineTopics is ASHEET.AdaptTreeStoreTopic
        # assert MTYPES.TagTopic is TagTopic

        # assert MTYPES.IndexFact is ATOPIC.IndexFact
        # assert MTYPES.OutlineFacts is ATOPIC.AdaptTreeStoreFact
        # assert MTYPES.TagFact is TagFact

        assert MTYPES.IdName is AINFOID.AdaptTextMarkup
        assert MTYPES.IdNameStatic is AINFOID.AdaptTextStatic
        assert MTYPES.IdSummary is AINFOID.AdaptTextFormat
        assert MTYPES.IdSummaryStatic is AINFOID.AdaptTextStatic
        assert MTYPES.IdTitle is AINFOID.AdaptTextMarkup
        assert MTYPES.IdTitleStatic is AINFOID.AdaptTextStatic

        assert MTYPES.ViewIdName is AINFOID.ViewTextMarkup
        assert MTYPES.ViewIdNameStatic is AINFOID.ViewTextStatic
        assert MTYPES.ViewIdSummary is AINFOID.ViewTextFormat
        assert MTYPES.ViewIdSummaryStatic is AINFOID.ViewTextStatic
        assert MTYPES.ViewIdTitle is AINFOID.ViewTextMarkup
        assert MTYPES.ViewIdTitleStatic is AINFOID.ViewTextStatic
