"""
Defines class to display fact in a topic pane.  See :mod:`.pane_topic`.
"""
import gi   # type: ignore[import]
import logging
import typing

from factsheet.abc_types import abc_fact as ABC_FACT
from factsheet.abc_types import abc_infoid as ABC_INFOID
from factsheet.control import control_fact as CFACT
from factsheet.view import scenes as VSCENES
from factsheet.view import view_infoid as VINFOID
from factsheet.view import ui as UI

gi.require_version('Gtk', '3.0')
from gi.repository import Gio   # type: ignore[import]    # noqa: E402
from gi.repository import GObject as GO  # type: ignore[import] # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402
from gi.repository import Pango  # type: ignore[import]  # noqa:E402

logger = logging.getLogger('Main.block_fact')


Aspect = typing.TypeVar('Aspect')


# class AspectValue:
#     """Common ancestor for fact aspects."""
#
#     def __init__(self) -> None:
#         self._aspect_gtk = Gtk.ScrolledWindow()
#         # self._content_gtk = Gtk.Label()
#
#     # def get_content(self) -> Gtk.Widget:
#     #     """Return presentation element for aspect content."""
#     #     return self._content_gtk
#
#     def set_content(self, p_content: Gtk.Widget) -> None:
#         """Add presentation element for aspect content.
#
#         :param p_content: presetntation element to add.
#         """
#         # self._content_gtk = p_content
#         self._aspect_gtk.add(p_content)
#
#     @property
#     def aspect_gtk(self):
#         """Return presentation element."""
#         return self._aspect_gtk


StatusOfFact = ABC_FACT.StatusOfFact
ValueOfFact = ABC_FACT.ValueOfFact


class BlockFact(ABC_FACT.InterfaceBlockFact[ValueOfFact]):
    """Displays fact and translates user actions.

    Class ``BlockFact`` displays a fact in a component of a topic pane.
    The class displays the content of a fact model and updates the
    display as the model changes.  It translates user actions at the
    display into requests to update the model.

    .. attribute:: NAME_FILE_FACT_UI

       Path to user interface defintion of fact block.

    :param p_control: fact control to mediate access to fact model.
    """
    NAME_FILE_FACT_UI = str(UI.DIR_UI / 'fact.ui')

    def __init__(self, p_control: CFACT.ControlFact) -> None:
        self._value: ValueOfFact = StatusOfFact.BLOCKED
        self._control = p_control

        builder = Gtk.Builder.new_from_file(self.NAME_FILE_FACT_UI)
        get_object = builder.get_object

        self._infoid = VINFOID.ViewInfoId(get_object)

        actions_fact = Gio.SimpleActionGroup()
        self._block_gtk = get_object('ui_block_fact')
        self._block_gtk.insert_action_group('fact', actions_fact)

        aspects_gtk = get_object('ui_aspects_fact')
        self._aspects = VSCENES.Scenes(aspects_gtk)
        self._new_aspect = dict(
            Synopsis=self.synopsis,
            Plain=self.plain
            )

        select_gtk = get_object('ui_select_name')
        model_names = Gtk.ListStore(str)
        select_gtk.set_model(model_names)
        self._names = SelectorName(select_gtk, self.select_aspect)
        for name in self._new_aspect:
            self._names.add_name(name, p_select=False)
#         select_gtk.set_active_id('Synopsis')
#         self._name_default = select_gtk.get_active_id()
        self._name_default = 'Synopsis'
        self._names.select(self._name_default)
#         self.select_aspect(self._name_default)

        self._block_gtk.show_all()
        self._control.attach_block(self)

        # Fact Menu
        UI.new_action_active_dialog(actions_fact, 'show-help-fact',
                                    self.on_show_dialog, UI.HELP_FACT)

        # Fact Display Menu
        UI.new_action_active_dialog(actions_fact, 'show-help-fact-display',
                                    self.on_show_dialog, UI.HELP_FACT_DISPLAY)

        context_s = get_object('ui_context_summary')
        button_s = get_object('ui_flip_summary')
        _binding = button_s.bind_property(
            'active', context_s, 'visible', GO.BindingFlags.BIDIRECTIONAL)

        context_v = get_object('ui_context_value')
        button_v = get_object('ui_flip_value')
        _binding = button_v.bind_property(
            'active', context_v, 'visible', GO.BindingFlags.BIDIRECTIONAL)

        context_n = get_object('ui_context_notes')
        assert context_n
        button_n = get_object('ui_flip_notes')
        _binding = button_n.bind_property(
            'active', context_n, 'visible', GO.BindingFlags.BIDIRECTIONAL)

        context_r = get_object('ui_context_related')
        button_r = get_object('ui_flip_related')
        _binding = button_r.bind_property(
            'active', context_r, 'visible', GO.BindingFlags.BIDIRECTIONAL)

    @property
    def block_gtk(self) -> Gtk.Box:
        """Return GTK presentation element for fact block."""
        return self._block_gtk

    def get_infoid(self) -> ABC_INFOID.InterfaceViewInfoId:
        """Return view of fact identification information."""
        return self._infoid

    def on_show_dialog(self):
        """Display informational dialog.

        :param px_dialog: informational dialog.

        .. note:: **Enhancement opportunity**

           Method ``on_show_dialog`` includes a top-level window check
           as per `Gtk.Widget.get_toplevel <GtkWidget.get_toplevel_>`_.
           During normal operation, this check should always confirm the
           topic pane is in a top-level window.

           The method silently patches a failure.  Consider adding a
           log message to the method to document abnormal behavior.

        .. _GtkWidget.get_toplevel: https://lazka.github.io/pgi-docs/
           #Gtk-3.0/classes/Widget.html#Gtk.Widget.get_toplevel
        """
        raise NotImplementedError

    def plain(self) -> Aspect:
        """Return unformatted text of fact value."""
        label = Gtk.Label()
        label.set_halign(Gtk.Align.START)
        label.set_valign(Gtk.Align.START)
        label.set_line_wrap(True)
        label.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)
        label.set_selectable(True)
        label.set_label(str(self._value))
        label.show()

        aspect = Gtk.ScrolledWindow()
        aspect.add(label)
        return aspect

    def select_aspect(self, p_name_aspect: str) -> None:
        """Show aspect, adding it to scenes if necessary.

        :param p_name_aspect: aspect to show
        """
        name_visible = self._aspects.show_scene(p_name_aspect)
        if name_visible == p_name_aspect:
            return

        try:
            aspect = self._new_aspect[p_name_aspect]()
        except KeyError:
            logger.warning('Unsupported aspect: \'{}\' ({}.{})'
                           ''.format(p_name_aspect, self.__class__.__name__,
                                     self.select_aspect.__name__))
            return

        self._aspects.add_scene(aspect, p_name_aspect)
        _ = self._aspects.show_scene(p_name_aspect)

    def synopsis(self) -> Aspect:
        """Return formatted text summary of fact value."""
        WIDTH_DEFAULT = 30
        WIDTH_MAX = 50

        label = Gtk.Label()
        label.set_xalign(0.0)
        label.set_yalign(0.0)
        label.set_width_chars(WIDTH_DEFAULT)
        label.set_max_width_chars(WIDTH_MAX)
        label.set_ellipsize(Pango.EllipsizeMode.MIDDLE)
        label.set_selectable(True)
        if isinstance(self._value, ABC_FACT.StatusOfFact):
            text = self._value.name
        else:
            text = str(self._value)
        label.set_markup(text)
        label.show()

        aspect = Gtk.ScrolledWindow()
        aspect.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        aspect.add(label)
        return aspect

    def update_value(self, p_value: ValueOfFact) -> None:
        """Update value and clear aspects then change to synopsis aspect.

        :param p_value: new fact falue
        """
        self._value = p_value
        self._aspects.clear()
        if self._name_default == self._names.get_name():
            self.select_aspect(self._name_default)
        else:
            self._names.select(self._name_default)


class SelectorName:
    """Selects name from list of names.

    :param p_view: presents selected name and selection mechanism.
    :param p_on_select: callback to invoke when user selects a name.
    """

    def __init__(self, p_view: Gtk.ComboBox, p_on_select:
                 typing.Callable[[str], None]) -> None:
        self._selector_gtk = p_view
        self._selector_gtk.connect(
            'changed', lambda sel_gtk: p_on_select(sel_gtk.get_active_id()))

    def __iter__(self) -> typing.Iterator:
        """Return iterator over names."""
        C_NAME = 0
        model = self._selector_gtk.get_model()
        for row in model:
            yield row[C_NAME]

    def add_name(self, p_name: str, p_select: bool = True) -> None:
        """Add name to end of list of names.

        Log warning if name already in list.

        :param p_name: name to add.
        :param p_select: True selects the new name while False leaves
            the selection unchanged.

        """
        model = self._selector_gtk.get_model()
        id_column = self._selector_gtk.get_id_column()
        for row in model:
            if p_name == row[id_column]:
                logger.warning('Duplicate name: {} ({}.{})'.format(
                    p_name, self.__class__.__name__, self.add_name.__name__))
                return
        i_new = model.append([p_name])
        if p_select:
            self._selector_gtk.set_active_iter(i_new)

    def get_name(self) -> typing.Optional[str]:
        """Return name that is selected."""
        return self._selector_gtk.get_active_id()

    def remove_name(self, p_name: str) -> None:
        """Remove name from list of names.

        :param p_name: name to remove.
        """
        model = self._selector_gtk.get_model()
        id_column = self._selector_gtk.get_id_column()
        index = model.get_iter_first()
        while index is not None:
            if p_name == model[index][id_column]:
                _ = model.remove(index)
                return

            index = model.iter_next(index)
        logger.warning('Missing name: {} ({}.{})'.format(
            p_name, self.__class__.__name__, self.remove_name.__name__))

    def select(self, p_name: str) -> None:
        """Select name from list of names.

        If name is not in list or is None, method has no effect.

        :param p_name: name to select.
        """
        if p_name is not None:
            self._selector_gtk.set_active_id(p_name)
