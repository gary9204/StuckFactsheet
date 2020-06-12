"""
Defines integer subsection of sets content.
See :mod:`~.factsheet.content.sets`.

.. attribute:: BUILTIN

    Content for integer topic templates and integer fact forms.
"""
from factsheet.content import heading as XHEADING
from factsheet.view import ui as UI


def new_templates() -> UI.OutlineTemplates:
    # def new_templates() -> ABC_OUTLINE.AbstractOutline:
    """Return outline of integer templates."""
    templates = UI.FACTORY_SHEET.new_model_outline_templates()

    heading_integer = XHEADING.Heading(
        p_name='<i>Integer</i>',
        p_summary=(
            'Integer includes templates for initial segments of natural '
            'numbers, finite arithmetic sequences, and multiplicative '
            'units.'
            ),
        p_title='Sets of Integers'
        )

    _ = templates.insert_child(heading_integer, None)
    return templates
