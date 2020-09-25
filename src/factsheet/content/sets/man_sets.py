"""
Defines manifest function for sets section of Factsheet content.
See :mod:`~.factsheet.content`.
"""
import factsheet.content.heading as XHEADING
import factsheet.model.types_model as MTYPES
import factsheet.view.types_view as VTYPES

from . int import man_setint as XMAN_SETINT


def new_templates(p_attach_view_topics: VTYPES.AttachViewTopics
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
    section_setint = XMAN_SETINT.new_templates(p_attach_view_topics)
    templates.insert_section(section_setint, px_i_target=i_sets)
    return templates
