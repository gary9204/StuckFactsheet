"""
Defines manifest function for topic templates with facts for Factsheet
content.
"""
# from factsheet.view import ui as UI
import factsheet.content.note.man_note as XMAN_NOTE
import factsheet.model.types_model as MTYPES
import factsheet.view.types_view as VTYPES

from . sets import man_sets as XMAN_SETS
from . ops import man_ops as XMAN_OPS


def new_templates(p_attach_view_topics: VTYPES.AttachViewTopics
                  ) -> MTYPES.OutlineTemplates:
    """Return outline of all templates."""
    templates = MTYPES.OutlineTemplates()

    templates.insert_section(XMAN_NOTE.new_templates(p_attach_view_topics))
    templates.insert_section(XMAN_SETS.new_templates(p_attach_view_topics))
    templates.insert_section(XMAN_OPS.new_templates(p_attach_view_topics))
    return templates
