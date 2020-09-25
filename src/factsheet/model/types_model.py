"""
Defines type aliases for model components that depend on GTK.
"""
import factsheet.adapt_gtk.adapt_infoid as AINFOID
import factsheet.adapt_gtk.adapt_outline as AOUTLINE
import factsheet.adapt_gtk.adapt_sheet as ASHEET
import factsheet.adapt_gtk.adapt_topic as ATOPIC

from factsheet.adapt_gtk.adapt_topic import IndexFact  # noqa (non-local use)
from factsheet.abc_types.abc_topic import TagTopic  # noqa (non-local use)

ModelName = AINFOID.AdaptEntryBuffer
ModelSummary = AINFOID.AdaptTextBuffer
ModelTitle = AINFOID.AdaptEntryBuffer

IndexOutline = AOUTLINE.IndexGtk

OutlineTemplates = ASHEET.AdaptTreeStoreTemplate
OutlineTopics = ASHEET.AdaptTreeStoreTopic

OutlineFacts = ATOPIC.AdaptTreeStoreFact
