"""
Defines type aliases for view components paired with model components.
"""
import typing

from factsheet.adapt_gtk import adapt_sheet as ASHEET
from factsheet.adapt_gtk import adapt_topic as ATOPIC


ViewOutlineTemplates = ASHEET.AdaptTreeViewTemplate
ViewOutlineTopics = ASHEET.AdaptTreeViewTopic
NewViewOutlineTopics = typing.Callable[[], ViewOutlineTopics]

IdTopic = ATOPIC.IdTopic
ViewOutlineFacts = ATOPIC.AdaptTreeViewFact
