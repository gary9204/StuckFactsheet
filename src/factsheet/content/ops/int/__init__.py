"""
Defines integer subsection of operations content.
See :mod:`~.factsheet.content.ops`.
"""
from pathlib import Path

from factsheet.content import spec as XSPEC
from factsheet.content import heading as XHEADING
# from factsheet.view import ui as UI
from factsheet.model import types_model as MTYPES
from factsheet.view import types_view as VTYPES
from . import plusmodn_spec as XSPEC_PLUS_N
from . import plusmodn_topic as XPLUS_N


def new_templates(p_new_view_topic: VTYPES.NewViewOutlineTopics
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

    spec_plusmodn = XSPEC_PLUS_N.SpecPlusModN(
        p_name='Plus mod n',
        p_summary=(
            'Add a topic for modular addition the <i>Topics </i>outline.'
            ''
            ),
        p_title='Modular Addition',
        p_class_topic=XPLUS_N.PlusModN,
        p_path_assist=XSPEC.StrAssist(
            str(Path(XSPEC_PLUS_N.__file__).parent / 'plusmodn_spec.ui')),
        p_new_view_topics=p_new_view_topic
        )

    _ = templates.insert_child(spec_plusmodn, i_int)

    return templates
