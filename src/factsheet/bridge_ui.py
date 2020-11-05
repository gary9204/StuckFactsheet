"""
Encapsulates user interface classes from widget toolkit.
"""
import typing

import factsheet.bridge_gtk.bridge_base as BBASE
import factsheet.bridge_gtk.bridge_outline as BOUTLINE
import factsheet.bridge_gtk.bridge_text as BTEXT

ModelOpaque = typing.Union[BBASE.ModelOpaque]
ViewOpaque = typing.Union[BBASE.ViewOpaque]

BridgeOutline = BOUTLINE.BridgeOutline
BridgeOutlineMulti = BOUTLINE.BridgeOutlineMulti
LineOutline = BOUTLINE.LineOutline
ModelOutline = BOUTLINE.ModelOutline
ViewOutline = BOUTLINE.ViewOutline

ModelTextFormat = BTEXT.ModelTextFormat
ModelTextMarkup = BTEXT.ModelTextMarkup
ModelTextStatic = BTEXT.ModelTextStatic
PersistText = BTEXT.PersistText
ViewTextFormat = BTEXT.ViewTextFormat
ViewTextMarkup = BTEXT.ViewTextMarkup
ViewTextStatic = BTEXT.ViewTextStatic
