"""
Defines templates for sections to organize a factsheet topic outline.

.. attribute:: BUILTIN

    Content for outline section template.
"""
from pathlib import Path

from factsheet.content.section import section_topic as XSECTION
from factsheet.content.section import section_spec as XSPEC
from factsheet.view import ui as UI


def new_templates() -> UI.OutlineTemplates:
    """Return outline of set templates."""
    templates = UI.FACTORY_SHEET.new_model_outline_templates()

    section_spec = XSPEC.Section(
        p_name='Section',
        p_summary=(
            'You may group topics in the topics outline into sections. '
            'Template Section creates a section heading in the outline '
            'where you may place or move topics.'
            ),
        p_title='Section in Topics Outline',
        p_path_assist=str(Path(XSPEC.__file__).parent / 'section_spec.ui'),
        p_model=XSECTION.Topic
        )

    _ = templates.insert_child(section_spec, None)
    return templates
