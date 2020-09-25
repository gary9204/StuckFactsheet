"""
Defines manifest function for integer operations subsection of
operations section.  See :mod:`~.factsheet.content.ops`.
"""
from pathlib import Path

import factsheet.content.spec as XSPEC
import factsheet.content.heading as XHEADING
import factsheet.model.types_model as MTYPES
import factsheet.view.types_view as VTYPES

from . import plusmodn_spec as XSPEC_PLUS_N
from . import plusmodn_topic as XPLUS_N


def new_templates(p_attach_view_topics: VTYPES.AttachViewTopics
                  ) -> MTYPES.OutlineTemplates:
    """Return outline of integer operation templates."""
    templates = MTYPES.OutlineTemplates()

    heading_int = XHEADING.Heading(
        p_name='<i>Integer</i>',
        p_summary=(
            'Integer includes templates for modular addition and '
            'multilication.'
            ),
        p_title='Binary Operations on Sets of Integers'
        )

    i_int = templates.insert_child(heading_int, None)

    prototopic_plusn = XSPEC.ProtoTopic(XPLUS_N.PlusModN)
    path_plusn = XSPEC.StrAssist(
        str(Path(XSPEC_PLUS_N.__file__).parent / 'plusmodn_spec.ui'))
    spec_plusmodn = XSPEC_PLUS_N.SpecPlusModN(
        p_name='Plus mod n',
        p_summary=(
            'Add a topic for modular addition the <i>Topics </i>outline.'
            ''
            ),
        p_title='Modular Addition',
        p_path_assist=path_plusn,
        p_attach_view_topics=p_attach_view_topics,
        p_prototopic=prototopic_plusn
        )

    _ = templates.insert_child(spec_plusmodn, i_int)

    return templates
