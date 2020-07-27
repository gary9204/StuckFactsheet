"""
Defines classes for displaying fact values.
"""
import gi   # type: ignore[import]

from factsheet.view import ui as UI  # noqa - only for type hints.

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402
from gi.repository import Pango  # type: ignore[import]    # noqa: E402


class SceneValue:
    """Common ancestor for views of fact values."""

    def __init__(self, **_kwargs: UI.KWArgs) -> None:
        self._scene_gtk = Gtk.ScrolledWindow()

    def add_content(self, p_content: Gtk.Widget) -> None:
        """Add display object for content of scene.

        :param p_content: display object to add.
        """
        self._scene_gtk.add(p_content)

    @property
    def scene_gtk(self):
        return self._scene_gtk


class SceneEvaluate(SceneValue):
    """View of fact value with interactive format."""

    def __init__(self):
        pass


class SceneSynopsis(SceneValue):
    """View of compact form of fact value.

    :param kwargs: keyword arguments for superclass.

    .. attribute:: SYNOPSIS_DEFAULT

    Default markup for fact synopsis.

    .. attribute:: WIDTH_DEFAULT

    Width requested by default for a synopsis field.

    .. attribute:: WIDTH_MAX

    Maximum width for a synopsis field.
    """

    SYNOPSIS_DEFAULT = '<b>Oops! no synopsis.</b>'
    WIDTH_DEFAULT = 30
    WIDTH_MAX = 50

    def __init__(self, **kwargs: UI.KWArgs) -> None:
        label = Gtk.Label(label=self.SYNOPSIS_DEFAULT)
        label.set_halign(Gtk.Align.START)
        label.set_valign(Gtk.Align.START)
        label.set_width_chars(self.WIDTH_DEFAULT)
        label.set_max_width_chars(self.WIDTH_MAX)
        label.set_ellipsize(Pango.EllipsizeMode.MIDDLE)
        label.set_selectable(True)

        super().__init__(**kwargs)
        self._label_gtk = label
        self.add_content(self._label_gtk)

    def set_markup(self, p_markup: str) -> None:
        """Set synopsis text.

        :param p_markup: new text, which may contain Pango markup.
        """
        self._label_gtk.set_label(p_markup)


class SceneTableau(SceneValue):
    """View of fact value in table fromat.

    :param kwargs: keyword arguments for superclass.
    """

    def __init__(self, **kwargs: UI.KWArgs) -> None:
        super().__init__(**kwargs)
        self._treeview_gtk = Gtk.TreeView()
        self._scene_gtk.add(self._treeview_gtk)


class SceneText(SceneValue):
    """View of fact value in plain text format.

    :param kwargs: keyword arguments for superclass.

    .. attribute:: TEXT_DEFAULT

    Default plain text for fact.
    """

    TEXT_DEFAULT = '<b>Oops! no fact text.</b>'

    def __init__(self, **kwargs: UI.KWArgs) -> None:
        label = Gtk.Label(label=self.TEXT_DEFAULT)
        label.set_halign(Gtk.Align.START)
        label.set_valign(Gtk.Align.START)
        label.set_line_wrap(True)
        label.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)
        label.set_selectable(True)

        super().__init__(**kwargs)
        self._label_gtk = label
        self.add_content(self._label_gtk)

    def set_text(self, p_text: str) -> None:
        """Set plain text for fact.

        :param p_markup: new plain text.
        """
        self._label_gtk.set_text(p_text)
