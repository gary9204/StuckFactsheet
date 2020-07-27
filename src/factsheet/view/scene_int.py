"""
Specializes :class:`.SceneValue` classes for integer fact values.  See
:mod:`.scene_value`.
"""
from factsheet.view import scene_value as VVALUE
from factsheet.view import ui as UI  # noqa - only for type hints.


class SceneSynopsisInt(VVALUE.SceneSynopsis):
    """View of compact form of fact value.

    :param p_value: integer fact value.
    :param kwargs: keyword arguments for superclass.
    """

    def __init__(self, p_value: int, **kwargs: UI.KWArgs) -> None:
        super().__init__(**kwargs)
        markup = str(p_value)
        self.set_markup(markup)


class SceneTextInt(VVALUE.SceneText):
    """View of fact value in plain text form.

    :param p_value: integer fact value.
    :param kwargs: keyword arguments for superclass.
    """

    def __init__(self, p_value: int, **kwargs: UI.KWArgs) -> None:
        super().__init__(**kwargs)
        text = repr(p_value)
        self.set_text(text)
