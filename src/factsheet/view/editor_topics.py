"""
Defines class to display and edit topics outline of a Factsheet.

Types and Type Aliases
----------------------

.. data:: UiEditorTopics

    TBD
"""
import gi   # type: ignore[import]
import typing
from pathlib import Path

import factsheet.bridge_ui as BUI
import factsheet.control.control_sheet as CSHEET

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


UiEditorTopics = typing.Union[Gtk.Frame]


class EditorTopics:
    """TBD"""

    def __init__(self, p_control_sheet: CSHEET.ControlSheet) -> None:
        """TBD"""
        self._control_sheet = p_control_sheet
        path_string = str(Path(__file__).with_suffix('.ui'))
        builder = Gtk.Builder.new_from_file(path_string)
        self._ui_view = builder.get_object('ui_editor_topics')

    @property
    def ui_view(self) -> UiEditorTopics:
        """Return user interface element of topics editor."""
        return self._ui_view
