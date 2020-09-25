"""
Defines unit tests for type aliases of view components.  See
:mod:`.types_view`.
"""
import factsheet.abc_types.abc_topic as ABC_TOPIC
from factsheet.adapt_gtk import adapt_sheet as ASHEET
from factsheet.adapt_gtk import adapt_topic as ATOPIC
from factsheet.view import types_view as VTYPES


class TestTypesView:
    """Unit tests for :mod:`.types_view`."""

    def test_types(self):
        """Confirm alias definitions for type hints."""
        # Setup
        # Test
        assert VTYPES.ViewOutlineTemplates is ASHEET.AdaptTreeViewTemplate
        assert VTYPES.ViewOutlineTopics is ASHEET.AdaptTreeViewTopic

        assert VTYPES.TagTopic is ABC_TOPIC.TagTopic
        assert VTYPES.ViewOutlineFacts is ATOPIC.AdaptTreeViewFact

        # assert VTYPES.AttachViewTopics is not None  # Not testable
        #     at runtime [misc]
