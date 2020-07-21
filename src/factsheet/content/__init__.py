"""
Defines topic templates and fact forms for Factsheet content.
"""
from factsheet.view import ui as UI
from factsheet.content import note as XSECTION
from . import sets as XSETS
from . import ops as XOPS


def new_templates(
       p_new_view_topic: UI.NewViewOutlineTopics) -> UI.OutlineTemplates:
    """Return outline of all templates."""
    templates = UI.FACTORY_SHEET.new_model_outline_templates()

    # UNRESOLVED: Issue #108
    templates.insert_section(XSECTION.new_templates(p_new_view_topic))
    templates.insert_section(XSETS.new_templates(p_new_view_topic))
    templates.insert_section(XOPS.new_templates(p_new_view_topic))
    return templates
