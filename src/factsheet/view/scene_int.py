"""
Specializes :class:`.SceneValue` classes for fact value that is an
integer.  See :mod:`.scene_value`.
"""
from factsheet.view import scene_value as VVALUE


class SceneSynopsisInt(VVALUE.SceneSynopsis):
    """Compact view of fact value that is an integer.

    :param p_value: integer fact value.
    """

    def __init__(self, p_value: int) -> None:
        super().__init__()
        markup = str(p_value)
        self.set_markup(markup)


class SceneTextInt(VVALUE.SceneText):
    """Plain text view of fact value that is an integer.

    :param p_value: integer fact value.
    """

    def __init__(self, p_value: int) -> None:
        super().__init__()
        text = repr(p_value)
        self.set_text(text)
