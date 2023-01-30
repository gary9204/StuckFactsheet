"""
Defines manifest function for operations section of Factsheet content.
See :mod:`~.factsheet.content`.
"""
import factsheet.content.heading as XHEADING
import factsheet.model.types_model as MTYPES
import factsheet.view.types_view as VTYPES

from . int import man_opint as XMAN_OPINT


def new_templates(p_attach_view_topics: VTYPES.AttachViewTopics
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
    section_opint = XMAN_OPINT.new_templates(p_attach_view_topics)
    templates.insert_section(section_opint, px_i_target=i_ops)
    return templates
