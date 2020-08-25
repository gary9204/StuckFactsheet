"""
Defines operations section of Factsheet content.
See :mod:`~.factsheet.content`.
"""
from factsheet.content import heading as XHEADING
# from factsheet.view import ui as UI
from factsheet.model import types_model as MTYPES
from factsheet.view import types_view as VTYPES
from . import int as XINT


def new_templates(p_new_view_topic: VTYPES.NewViewOutlineTopics
                  ) -> MTYPES.OutlineTemplates:
    """Return outline of operation templates."""
    templates = MTYPES.OutlineTemplates()

    heading_sets = XHEADING.Heading(
        p_name='<i>Operations</i>',
        p_summary=(
            'Operations includes templates for operations on sets on '
            'products of sets.  It includes a template to define an '
            'operation by entering the effect on pairs of elements '
            'from the set.'
            ),
        p_title='Representations of Binary Operations'
        )

    i_ops = templates.insert_child(heading_sets, None)
    templates.insert_section(
        XINT.new_templates(p_new_view_topic), px_i_target=i_ops)
    return templates
