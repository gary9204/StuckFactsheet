"""
Defines integer subsection of sets content.
See :mod:`~.factsheet.content.sets`.

.. attribute:: BUILTIN

    Content for integer topic templates and integer fact forms.
"""
from pathlib import Path

from factsheet.content import heading as XHEADING
from factsheet.content import spec as XSPEC
from factsheet.view import ui as UI
from . import segint_spec as XSPEC_SEGINT
from . import segint_topic as XSEGINT


def new_templates(
       p_new_view_topic: UI.NewViewOutlineTopics) -> UI.OutlineTemplates:
    """Return outline of integer templates."""
    templates = UI.FACTORY_SHEET.new_model_outline_templates()

    heading_int = XHEADING.Heading(
        p_name='<i>Integer</i>',
        p_summary=(
            'Integer includes templates for initial segments of natural '
            'numbers, finite arithmetic sequences, and multiplicative '
            'units.'
            ),
        p_title='Sets of Integers'
        )

    i_int = templates.insert_child(heading_int, None)

    spec_segint = XSPEC_SEGINT.SpecSegInt(
        p_name='Segment',
        p_summary=(
            'Add a topic for an initial segment of natural numbers to '
            'the <i>Topics </i>outline.'
            ),
        p_title='Add Initial Segment of Natural Numbers',
        p_class_topic=XSEGINT.SegInt,
        p_path_assist=XSPEC.StrAssist(
            str(Path(XSPEC_SEGINT.__file__).parent / 'segint_spec.ui')),
        p_new_view_topics=p_new_view_topic
        )

    _ = templates.insert_child(spec_segint, i_int)

    return templates
