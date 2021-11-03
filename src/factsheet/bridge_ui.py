"""
Encapsulates user interface classes from widget toolkit.  The following
models define the classes.

    * :mod:`.bridge_base`
    * :mod:`.bridge_outline`
    * :mod:`.bridge_text`
"""

import factsheet.bridge_gtk.bridge_base as BBASE
import factsheet.bridge_gtk.bridge_outline as BOUTLINE
import factsheet.bridge_gtk.bridge_text as BTEXT

TimeEvent = BBASE.TimeEvent
TIME_EVENT_CURRENT = BBASE.TIME_EVENT_CURRENT

ChooserOutline = BOUTLINE.ChooserOutline
FactoryChooserOutline = BOUTLINE.FactoryChooserOutline
FactoryViewOutline = BOUTLINE.FactoryViewOutline
LineOutline = BOUTLINE.LineOutline
ModelOutlineMulti = BOUTLINE.ModelOutlineMulti
ModelOutlineSingle = BOUTLINE.ModelOutlineSingle
ViewOutline = BOUTLINE.ViewOutline

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
