"""
Encapsulates user interface classes from widget toolkit.
"""
import typing

import factsheet.bridge_gtk.bridge_base as BBASE
import factsheet.bridge_gtk.bridge_outline as BOUTLINE

ModelOpaque = typing.Union[BBASE.ModelOpaque]
ViewOpaque = typing.Union[BBASE.ViewOpaque]

BridgeOutline = BOUTLINE.BridgeOutline
BridgeOutlineMulti = BOUTLINE.BridgeOutlineMulti
LineOutline = BOUTLINE.LineOutline
ModelOutline = BOUTLINE.ModelOutline
ViewOutline = BOUTLINE.ViewOutline
