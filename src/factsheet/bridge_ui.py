"""
Encapsulates user interface classes from widget toolkit.
"""

import factsheet.bridge_gtk.bridge_base as BBASE
# import factsheet.bridge_gtk.bridge_outline as BOUTLINE
import factsheet.bridge_gtk.bridge_text as BTEXT

TimeEvent = BBASE.TimeEvent
TIME_EVENT_CURRENT = BBASE.TIME_EVENT_CURRENT

# BridgeOutlineColumnar = BOUTLINE.BridgeOutlineColumnar
# BridgeOutlineMultiColumnar = BOUTLINE.BridgeOutlineMultiColumnar
# BridgeOutlineMultiSelect = BOUTLINE.BridgeOutlineMultiSelect
# BridgeOutlineSelect = BOUTLINE.BridgeOutlineSelect
# LineOutline = BOUTLINE.LineOutline
# ViewOutlineColumnar = BOUTLINE.ViewOutlineColumnar
# ViewOutlineSelect = BOUTLINE.ViewOutlineSelect

escape_text_markup = BTEXT.escape_text_markup
ModelTextMarkup = BTEXT.ModelTextMarkup
DisplayTextMarkup = BTEXT.DisplayTextMarkup
FactoryDisplayTextMarkup = BTEXT.FactoryDisplayTextMarkup
EditorTextMarkup = BTEXT.EditorTextMarkup
FactoryEditorTextMarkup = BTEXT.FactoryEditorTextMarkup

ModelTextStyled = BTEXT.ModelTextStyled
DisplayTextStyled = BTEXT.DisplayTextStyled
FactoryDisplayTextStyled = BTEXT.FactoryDisplayTextStyled
EditorTextStyled = BTEXT.EditorTextStyled
FactoryEditorTextStyled = BTEXT.FactoryEditorTextStyled
