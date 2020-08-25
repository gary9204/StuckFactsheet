"""
Defines sets section of Factsheet content.
See :mod:`~.factsheet.content`.
"""
from factsheet.content import heading as XHEADING
# from factsheet.view import ui as UI
from factsheet.model import types_model as MTYPES
from factsheet.view import types_view as VTYPES
from . import int as XINT


def new_templates(p_new_view_topic: VTYPES.NewViewOutlineTopics
                  ) -> MTYPES.OutlineTemplates:
    """Return outline of set templates."""
    templates = MTYPES.OutlineTemplates()

    heading_sets = XHEADING.Heading(
        p_name='<i>Sets</i>',
        p_summary=(
            'Sets includes templates for sets of integers, subsets, and '
            'product sets.  It includes a template to define a set by '
            'entering the elements of the set.'
            ),
        p_title='Representations of Mathematical Sets'
        )

    i_sets = templates.insert_child(heading_sets, None)
    templates.insert_section(
        XINT.new_templates(p_new_view_topic), px_i_target=i_sets)
    return templates
