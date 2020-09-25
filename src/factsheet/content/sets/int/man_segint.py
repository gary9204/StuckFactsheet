"""
Defines manifest function for integer subsection of sets section.
See :mod:`~.factsheet.content.sets`.
"""
from pathlib import Path

import factsheet.content.spec as XSPEC
import factsheet.model.types_model as MTYPES
import factsheet.view.block.block_fact as VFACT
import factsheet.view.types_view as VTYPES

from . import segint_facts as XFACTS_SEGINT
from . import segint_spec as XSPEC_SEGINT
from . import segint_topic as XSEGINT
from . import setint_facts as XFACTS_SETINT


def new_templates(p_attach_view_topics: VTYPES.AttachViewTopics
                  ) -> MTYPES.OutlineTemplates:
    """Return outline of integer templates."""
    templates = MTYPES.OutlineTemplates()

    prototopic_segint = XSPEC.ProtoTopic(XSEGINT.SegInt)
    path_segint = str(Path(XSPEC_SEGINT.__file__).parent / 'segint_spec.ui')
    spec_segint = XSPEC_SEGINT.SpecSegInt(
        p_name='Segment',
        p_summary=(
            'Add a topic for an initial segment of natural numbers to '
            'the <i>Topics </i>outline.'
            ),
        p_title='Add Initial Segment of Natural Numbers',
        p_path_assist=XSPEC.StrAssist(path_segint),
        p_attach_view_topics=p_attach_view_topics,
        p_prototopic=prototopic_segint,
        )
    _ = templates.insert_child(spec_segint, None)

    proto = XSPEC.ProtoFact(XFACTS_SETINT.ElementsSetInt, VFACT.BlockFact)
    spec_segint.add_protofact(proto)

#         XFACTS_SETINT.SearchSetInt,
#         XFACTS_SETINT.SizeSet,
#         XFACTS_SEGINT.BoundSegInt

    return templates
