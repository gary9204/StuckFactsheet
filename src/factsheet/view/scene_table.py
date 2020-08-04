"""
Specializes :class:`.SceneValue` classes for fact value that is table
of indexed elements.  See :mod:`.scene_value` and :mod:`.element`.
"""
from factsheet.model import table as MTABLE
from factsheet.view import scene_value as VVALUE


class SceneSynopsisTable(VVALUE.SceneSynopsis):
    """Compact view of fact value that is table of indexed elements.

    :param p_value: table of elements.
    """

    def __init__(self, p_value: MTABLE.TableElements) -> None:
        super().__init__()
        markup = 'Table with {} rows and {} columns'.format(
            len(p_value.rows), len(p_value.columns))
        self.set_markup(markup)


class SceneTableauTable(VVALUE.SceneTableau):
    """Tabular view of fact value that is table of indexed elements.

    Not implemented at present. :class:`.SceneTableau` serves as sample
    at present.

    :param p_value: table of elements.
    """

    def __init__(self, p_value: MTABLE.TableElements) -> None:
        pass


class SceneTextTable(VVALUE.SceneText):
    """Plain text view of fact value that is table of indexed elements.

    :param p_value: table of elements.
    """

    def __init__(self, p_value: MTABLE.TableElements) -> None:
        super().__init__()
        text = repr(p_value)
        self.set_text(text)
