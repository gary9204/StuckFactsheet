"""
Encapsulates user interface classes from widget toolkit.
"""
import typing

import factsheet.bridge_gtk.bridge_base as BBASE
import factsheet.bridge_gtk.bridge_outline as BOUTLINE
import factsheet.bridge_gtk.bridge_text as BTEXT

ModelOpaque = typing.Union[BBASE.ModelOpaque]
ViewOpaque = typing.Union[BBASE.ViewOpaque]

BridgeOutlineColumnar = BOUTLINE.BridgeOutlineColumnar
BridgeOutlineMultiColumnar = BOUTLINE.BridgeOutlineMultiColumnar
BridgeOutlineMultiSelect = BOUTLINE.BridgeOutlineMultiSelect
BridgeOutlineSelect = BOUTLINE.BridgeOutlineSelect
LineOutline = BOUTLINE.LineOutline

BridgeTextFormat = BTEXT.BridgeTextFormat
BridgeTextMarkup = BTEXT.BridgeTextMarkup
BridgeTextStatic = BTEXT.BridgeTextStatic
ViewTextFormat = BTEXT.ViewTextFormat
ViewTextMarkup = BTEXT.ViewTextMarkup
ViewTextStatic = BTEXT.ViewTextStatic