"""
Encapsulates user interface classes from widget toolkit.  The following
models define the classes.

    * :mod:`.bridge_base`
    * :mod:`.bridge_outline`
    * :mod:`.bridge_text`

Outline Types and Classes
=========================

.. data:: ChooserOutline

    Visual element to choose a line from an outline.  See
    :data:`.bridge_outline.ChooserOutline`.

.. data:: FactoryChooserOutline

    Factory to create :data:`.ChooserOutline` for an outline.
    See :class:`.bridge_outline.FactoryChooserOutline`.

.. data:: FactoryViewOutline

    Factory to create :data:`.ViewOutline` for an outline
    See :class:`.bridge_outline.FactoryViewOutline`.

.. data:: LineOutline

    Storage for a line in an outline.
    See :data:`.bridge_outline.LineOutline`.

.. data:: ModelOutlineMulti

    Storage for multi-line outline.
    See :class:`.bridge_outline.ModelOutlineMulti`.

.. data:: ModelOutlineSingle

    Storage for single-line outline.
    See :class:`.bridge_outline.ModelOutlineSingle`.

.. data:: ViewOutline

    Visual element to view outline in columnar format.
    See :data:`.bridge_outline.ViewOutline`.

Text with Markup Types and Classes
==================================

.. data:: DisplayTextMarkup

    Visual element for view-only markup text.
    See :data:`.bridge_text.DisplayTextMarkup`.

.. data:: EditorTextMarkup

    Visual element to view and edit markup text.
    See :data:`.bridge_text.EditorTextMarkup`.

.. data:: x_b_t_escape_text_markup

    Function returns text with `Pango markup`_ errors escaped.
    See :func:`.bridge_text.x_b_t_escape_text_markup`.

.. _Pango markup:
    https://docs.gtk.org/Pango/pango_markup.html

.. data:: FactoryDisplayTextMarkup

    Factory to create :data:`.DisplayTextMarkup` for markup text.
    See :class:`.bridge_text.FactoryDisplayTextMarkup`.

.. data:: FactoryEditorTextMarkup

    Factory to create :data:`.EditorTextMarkup` for markup text.
    See :class:`.bridge_text.FactoryEditorTextMarkup`.

.. data:: x_b_t_ModelTextMarkup

    Storage for text with `Pango markup`_.
    See :class:`.bridge_text.x_b_t_ModelTextMarkup`.

Text with Styles Types and Classes
==================================

.. data:: DisplayTextStyled

    Visual element for view-only text with tag-based formatting.
    See :data:`.bridge_text.DisplayTextStyled`.

.. data:: EditorTextStyled

    Visual element to view and edit text with tag-based formatting.
    See :data:`.bridge_text.EditorTextStyled`.

.. data:: FactoryDisplayTextStyled

    Factory to create :data:`.DisplayTextStyled` for text with tag-based
    formatting. See :class:`.bridge_text.FactoryDisplayTextStyled`.

.. data:: FactoryEditorTextStyled

    Factory to create :data:`.EditorTextStyled` for text with tag-based
    formatting. See :class:`.bridge_text.FactoryEditorTextStyled`.

.. data:: ModelTextStyled

    Storage for text with tag-based formatting.
    See :class:`.bridge_text.ModelTextStyled`.
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
ModelOutline = BOUTLINE.ModelOutline
ModelOutlineMulti = BOUTLINE.ModelOutlineMulti
ModelOutlineSingle = BOUTLINE.ModelOutlineSingle
ViewOutline = BOUTLINE.ViewOutline

ModelText = BTEXT.ModelText

x_b_t_escape_text_markup = BTEXT.x_b_t_escape_text_markup
x_b_t_ModelTextMarkup = BTEXT.x_b_t_ModelTextMarkup
DisplayTextMarkup = BTEXT.DisplayTextMarkup
FactoryDisplayTextMarkup = BTEXT.FactoryDisplayTextMarkup
EditorTextMarkup = BTEXT.EditorTextMarkup
FactoryEditorTextMarkup = BTEXT.FactoryEditorTextMarkup

ModelTextStyled = BTEXT.ModelTextStyled
DisplayTextStyled = BTEXT.DisplayTextStyled
FactoryDisplayTextStyled = BTEXT.FactoryDisplayTextStyled
EditorTextStyled = BTEXT.EditorTextStyled
FactoryEditorTextStyled = BTEXT.FactoryEditorTextStyled
