"""
Defines manifest function for section templates to organize a factsheet
topic outline.
"""
from pathlib import Path

import factsheet.content.spec as XSPEC
import factsheet.content.note.note_spec as XSPEC_NOTE
import factsheet.content.note.note_topic as XNOTE
import factsheet.model.types_model as MTYPES
import factsheet.view.types_view as VTYPES


def new_templates(p_attach_view_topics: VTYPES.AttachViewTopics
                  ) -> MTYPES.OutlineTemplates:
    """Return outline containing note template.

    :param p_attach_view_topics: funcion that returns current topics
        outline.
    """
    templates = MTYPES.OutlineTemplates()

    note_topic = XSPEC.ProtoTopic(class_topic=XNOTE.Note)

    note_spec = XSPEC_NOTE.SpecNote(
        p_name='Note',
        p_summary=(
            'Adds a note to the topics outline. Also, you may group '
            'topics within the outline by adding a note and then '
            'adding or moving topics underneath it.'
            ),
        p_title='Add note to <i>Topics </i>outline',
        p_path_assist=XSPEC.StrAssist(
            str(Path(XSPEC_NOTE.__file__).parent / 'note_spec.ui')),
        p_attach_view_topics=p_attach_view_topics,
        p_prototopic=note_topic,
        )

    _ = templates.insert_child(note_spec, None)
    return templates
