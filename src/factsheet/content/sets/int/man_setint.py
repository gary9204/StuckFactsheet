"""
Defines manifest function for integer subsection of sets section.
See :mod:`~.factsheet.content.sets`.
"""
# from pathlib import Path

import factsheet.content.heading as XHEADING
# import factsheet.content.spec as XSPEC
import factsheet.model.types_model as MTYPES
import factsheet.view.types_view as VTYPES

from . import man_segint as XMAN_SEGINT
# from . import segint_spec as XSPEC_SEGINT
# from . import segint_topic as XSEGINT


def new_templates(p_attach_view_topics: VTYPES.AttachViewTopics
                  ) -> MTYPES.OutlineTemplates:
    """Return outline of integer templates."""
    templates = MTYPES.OutlineTemplates()

    heading_int = XHEADING.Heading(
        p_name='<i>Integer</i>',
        p_summary=(
            'Integer includes templates for initial segments of natural '
            'numbers, finite arithmetic sequences, and multiplicative '
            'units.'
            ),
        p_title='Sets of Integers'
        )

    i_heading = templates.insert_child(heading_int, None)

    spec_segint = XMAN_SEGINT.new_templates(
        p_attach_view_topics=p_attach_view_topics)

    templates.insert_section(spec_segint, px_i_target=i_heading)

    # prototopic_segint = XSPEC.ProtoTopic(XSEGINT.SegInt)
    # path_segint = str(Path(XSPEC_SEGINT.__file__).parent / 'segint_spec.ui')
    # spec_segint = XSPEC_SEGINT.SpecSegInt(
    #     p_name='Segment',
    #     p_summary=(
    #         'Add a topic for an initial segment of natural numbers to '
    #         'the <i>Topics </i>outline.'
    #         ),
    #     p_title='Add Initial Segment of Natural Numbers',
    #     p_path_assist=XSPEC.StrAssist(path_segint),
    #     p_attach_view_topics=p_attach_view_topics,
    #     p_prototopic=prototopic_segint,
    #     )

    return templates
