"""
Defines sets section of Factsheet content.
See :mod:`~.factsheet.content`.

.. attribute:: BUILTIN

    Content for set topic templates and set fact forms.
"""
from factsheet.content import heading as XHEADING
from factsheet.view import ui as UI
from . import integer as XINTEGER

heading_sets = XHEADING.Heading(
    p_name='<i>Sets</i>',
    p_summary=(
        'Sets includes templates for sets of integers, subsets, and '
        'product sets.  It includes a template to define a set by '
        'entering the elements of the set.'
        ),
    p_title='Representations of Mathematical Sets'
    )

BUILTIN = UI.FACTORY_SHEET.new_model_outline_templates()
i_sets = BUILTIN.insert_child(heading_sets, None)
BUILTIN.deepcopy_section_child(XINTEGER.BUILTIN, px_i_target=i_sets)
