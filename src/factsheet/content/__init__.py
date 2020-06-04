"""
Defines topic templates and fact forms for Factsheet content.

.. attribute:: BUILTIN

    Content for topic templates and fact forms outlines.
"""
from factsheet.view import ui as UI
from . import section as XSECTION
from . import sets as XSETS

BUILTIN = UI.FACTORY_SHEET.new_model_outline_templates()
BUILTIN.deepcopy_section_child(XSECTION.BUILTIN)
BUILTIN.deepcopy_section_child(XSETS.BUILTIN)
