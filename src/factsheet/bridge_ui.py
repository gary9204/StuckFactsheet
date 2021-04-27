"""
Encapsulates user interface classes from widget toolkit.
"""
import typing

import factsheet.bridge_gtk.bridge_aspect as BASPECT
import factsheet.bridge_gtk.bridge_base as BBASE
import factsheet.bridge_gtk.bridge_outline as BOUTLINE
import factsheet.bridge_gtk.bridge_text as BTEXT

BridgeAspect = BASPECT.BridgeAspect
BridgeAspectPlain = BASPECT.BridgeAspectPlain
PersistAspectPlain = BASPECT.PersistAspectPlain
ViewAspectAny = BASPECT.ViewAspectAny
ViewAspectMissing = BASPECT.ViewAspectMissing
ViewAspectPlain = BASPECT.ViewAspectPlain

Bridge = BBASE.BridgeBase
ModelOpaque = typing.Union[BBASE.ModelOpaque]
ViewOpaque = typing.Union[BBASE.ViewOpaque]

BridgeOutlineColumnar = BOUTLINE.BridgeOutlineColumnar
BridgeOutlineMultiColumnar = BOUTLINE.BridgeOutlineMultiColumnar
BridgeOutlineMultiSelect = BOUTLINE.BridgeOutlineMultiSelect
BridgeOutlineSelect = BOUTLINE.BridgeOutlineSelect
LineOutline = BOUTLINE.LineOutline
ViewOutlineColumnar = BOUTLINE.ViewOutlineColumnar
ViewOutlineSelect = BOUTLINE.ViewOutlineSelect

BridgeText = BTEXT.BridgeText
BridgeTextFormat = BTEXT.BridgeTextFormat
BridgeTextMarkup = BTEXT.BridgeTextMarkup
BridgeTextStatic = BTEXT.BridgeTextStatic
ViewTextFormat = BTEXT.ViewTextFormat
ViewTextMarkup = BTEXT.ViewTextMarkup
ViewTextStatic = BTEXT.ViewTextStatic
