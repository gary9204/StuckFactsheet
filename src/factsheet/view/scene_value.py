"""
Defines classes for displaying fact values.
"""
import typing
import gi   # type: ignore[import]

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


GenericValue = typing.TypeVar('GenericValue')
GenericUI = typing.TypeVar('GenericUI')


class SceneValue(typing.Generic[GenericValue]):
    """Common ancestor for views of fact values.
    """
    def __init__(self, **_kwargs: typing.Mapping[str, typing.Any]) -> None:
        self._scene_gtk = Gtk.ScrolledWindow()

    @property
    def scene_gtk(self):
        return self._scene_gtk


class SceneEvaluate(SceneValue[GenericValue]):
    """View of fact value with interactive format.
    """
    def __init__(self):
        pass


class SceneSynopsis(SceneValue[GenericValue]):
    """View of compact form of fact value.
    """
    def __init__(self, **kwargs: typing.Mapping[str, typing.Any]) -> None:
        super().__init__(**kwargs)
        self._label_gtk = Gtk.Label()
        self._scene_gtk.add(self._label_gtk)


class SceneTableau(SceneValue[GenericValue]):
    """View of fact value in table fromat.
    """
    def __init__(self, **kwargs: typing.Mapping[str, typing.Any]) -> None:
        super().__init__(**kwargs)
        self._treeview_gtk = Gtk.TreeView()
        self._scene_gtk.add(self._treeview_gtk)


class SceneText(SceneValue[GenericValue]):
    """View of fact value in text format.
    """
    def __init__(self, **kwargs: typing.Mapping[str, typing.Any]) -> None:
        super().__init__(**kwargs)
        self._label_gtk = Gtk.Label()
        self._scene_gtk.add(self._label_gtk)
