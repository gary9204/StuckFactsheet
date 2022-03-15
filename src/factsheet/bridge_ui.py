"""
Encapsulates user interface classes from widget toolkit.  The following
models define the classes.

    * :mod:`.bridge_base`
    * :mod:`.bridge_outline`
    * :mod:`.bridge_text`


.. data:: ChooserOutline

    BOUTLINE.ChooserOutline

.. data:: FactoryChooserOutline

    BOUTLINE.FactoryChooserOutline

.. data:: FactoryViewOutline

    BOUTLINE.FactoryViewOutline

.. data:: LineOutline

    BOUTLINE.LineOutline

.. data:: ModelOutlineMulti

    BOUTLINE.ModelOutlineMulti

.. data:: ModelOutlineSingle

    BOUTLINE.ModelOutlineSingle

.. data:: ViewOutline

    BOUTLINE.ViewOutline


.. data:: escape_text_markup

    BTEXT.escape_text_markup

.. data:: ModelTextMarkup

    BTEXT.ModelTextMarkup

.. data:: DisplayTextMarkup

    BTEXT.DisplayTextMarkup

.. data:: FactoryDisplayTextMarkup

    BTEXT.FactoryDisplayTextMarkup

.. data:: EditorTextMarkup

    BTEXT.EditorTextMarkup

.. data:: FactoryEditorTextMarkup

    BTEXT.FactoryEditorTextMarkup


.. data:: ModelTextStyled

    BTEXT.ModelTextStyled

.. data:: DisplayTextStyled

    BTEXT.DisplayTextStyled

.. data:: FactoryDisplayTextStyled

    BTEXT.FactoryDisplayTextStyled

.. data:: EditorTextStyled

    BTEXT.EditorTextStyled

.. data:: FactoryEditorTextStyled

    BTEXT.FactoryEditorTextStyled

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
