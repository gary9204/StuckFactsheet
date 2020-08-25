"""
Defines topic templates and fact forms for Factsheet content.
"""
# from factsheet.view import ui as UI
from factsheet.content import note as XSECTION
from factsheet.model import types_model as MTYPES
from factsheet.view import types_view as VTYPES
from . import sets as XSETS
from . import ops as XOPS


def new_templates(p_new_view_topic: VTYPES.NewViewOutlineTopics
                  ) -> MTYPES.OutlineTemplates:
    """Return outline of all templates."""
    templates = MTYPES.OutlineTemplates()

    templates.insert_section(XSECTION.new_templates(p_new_view_topic))
    templates.insert_section(XSETS.new_templates(p_new_view_topic))
    templates.insert_section(XOPS.new_templates(p_new_view_topic))
    return templates
