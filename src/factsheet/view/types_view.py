"""
Defines type aliases for view components paired with model components.
"""
import typing

from factsheet.adapt_gtk import adapt_sheet as ASHEET
from factsheet.adapt_gtk import adapt_topic as ATOPIC

from factsheet.abc_types.abc_topic import TagTopic  # noqa (non-local use)

ViewOutlineTemplates = ASHEET.AdaptTreeViewTemplate
ViewOutlineTopics = ASHEET.AdaptTreeViewTopic
AttachViewTopics = typing.Callable[[ViewOutlineTopics], None]

ViewOutlineFacts = ATOPIC.AdaptTreeViewFact
