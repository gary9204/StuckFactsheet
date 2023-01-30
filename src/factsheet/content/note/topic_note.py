"""
Defines topic class for user to record notes.  See :class:`.Topic`.
"""
import typing   # noqa

from factsheet.model import topic as MTOPIC


class Note(MTOPIC.Topic):
    """Defines topic for user to record notes.

    A note topic has no content other than identification information.
    A user can record notes in the summary field and label the notes
    with a name and title.  Also, a user may group topics within the
    topics outline by adding or moving the topics underneath a note.
    """

    pass
