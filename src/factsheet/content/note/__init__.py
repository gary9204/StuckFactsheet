"""
Defines templates for sections to organize a factsheet topic outline.

.. attribute:: BUILTIN

    Content for outline section template.
"""
from pathlib import Path

from factsheet.content import spec as XSPEC
from factsheet.content.note import note_spec as XNOTE_SPEC
from factsheet.content.note import note_topic as XNOTE
from factsheet.view import ui as UI


def new_templates(
       p_new_view_topic: UI.NewViewOutlineTopics) -> UI.OutlineTemplates:
    """Return outline containing note template.

    :param p_new_view_topics: funcion that returns current topics outline.
    """
    templates = UI.FACTORY_SHEET.new_model_outline_templates()

    note_spec = XNOTE_SPEC.SpecNote(
        p_name='Note',
        p_summary=(
            'Adds a note to the topics outline. Also, you may group '
            'topics within the outline by adding a note and then '
            'adding or moving topics underneath it.'
            ),
        p_title='Add note to <i>Topics </i>outline',
        p_class_topic=XNOTE.Note,
        p_path_assist=XSPEC.StrAssist(
            str(Path(XNOTE_SPEC.__file__).parent / 'note_spec.ui')),
        p_new_view_topics=p_new_view_topic
        )

    _ = templates.insert_child(note_spec, None)
    return templates