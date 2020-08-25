"""
Defines type aliases for model components that depend on GTK.
"""
from factsheet.adapt_gtk import adapt_infoid as AINFOID
from factsheet.adapt_gtk import adapt_outline as AOUTLINE
from factsheet.adapt_gtk import adapt_sheet as ASHEET
from factsheet.adapt_gtk import adapt_topic as ATOPIC


ModelName = AINFOID.AdaptEntryBuffer
ModelSummary = AINFOID.AdaptTextBuffer
ModelTitle = AINFOID.AdaptEntryBuffer

IndexOutline = AOUTLINE.AdaptIndex

OutlineTemplates = ASHEET.AdaptTreeStoreTemplate
OutlineTopics = ASHEET.AdaptTreeStoreTopic

IdTopic = ATOPIC.IdTopic
OutlineFacts = ATOPIC.AdaptTreeStoreFact
