"""
Encapsulates user interface classes from widget toolkit.
"""
import typing

import factsheet.bridge_gtk.bridge_base as BBASE
import factsheet.bridge_gtk.bridge_outline as BOUTLINE
import factsheet.bridge_gtk.bridge_text as BTEXT

Bridge = BBASE.BridgeBase
ModelOpaque = typing.Union[BBASE.ModelOpaque]
ViewAny = BBASE.ViewAny
ViewOpaque = typing.Union[BBASE.ViewOpaque]

BridgeOutlineColumnar = BOUTLINE.BridgeOutlineColumnar
BridgeOutlineMultiColumnar = BOUTLINE.BridgeOutlineMultiColumnar
BridgeOutlineMultiSelect = BOUTLINE.BridgeOutlineMultiSelect
BridgeOutlineSelect = BOUTLINE.BridgeOutlineSelect
LineOutline = BOUTLINE.LineOutline
ViewOutlineColumnar = BOUTLINE.ViewOutlineColumnar
ViewOutlineSelect = BOUTLINE.ViewOutlineSelect

BridgeText = BTEXT.BridgeText
BridgeTextMarkup = BTEXT.BridgeTextMarkup
BridgeTextTagged = BTEXT.BridgeTextTagged
ViewTextDisplay = BTEXT.ViewTextDisplay
ViewTextMarkup = BTEXT.ViewTextMarkup
ViewTextTagged = BTEXT.ViewTextTagged
