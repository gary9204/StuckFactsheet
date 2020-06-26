"""
Defines topic templates and fact forms for Factsheet content.

.. attribute:: BUILTIN

    Content for topic templates and fact forms outlines.
"""
from factsheet.view import ui as UI
from factsheet.content import note as XSECTION
from . import sets as XSETS


def new_templates() -> UI.OutlineTemplates:
    """Return outline of all templates."""
    templates = UI.FACTORY_SHEET.new_model_outline_templates()

    # UNRESOLVED: Issue #108
    templates.insert_section(XSECTION.new_templates())
    templates.insert_section(XSETS.new_templates())
    return templates
