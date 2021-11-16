"""
Defines class to display topic in a factsheet window pane.
"""
import gi   # type: ignore[import]
import typing   # noqa

from factsheet.control import control_topic as CTOPIC
from factsheet.view import ui as UI

gi.require_version('Gtk', '3.0')
from gi.repository import Gio   # type: ignore[import]    # noqa: E402
from gi.repository import GLib   # type: ignore[import]    # noqa: E402
from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class FormTopic(ABC_TOPIC.InterfaceFormTopic):
    """Display topic and translate user actions.

    Class ``FormTopic`` maintains presentation of a topic in a pane of a
    Factsheet window.  The class displays the content of a topic model.
    It translates a user's actions at the user interface into requests
    to update the model and its presentation.

    .. attribute:: NAME_FILE_TOPIC_UI

       Path to user interface defintion of topic pane.
    """
    NAME_FILE_TOPIC_UI = str(UI.DIR_UI / 'topic.ui')

    def __init__(self, *, p_control: CTOPIC.ControlTopic) -> None:
        self._control = p_control
        builder = Gtk.Builder.new_from_file(self.NAME_FILE_TOPIC_UI)
        get_object = builder.get_object

        # Components
        actions_topic = Gio.SimpleActionGroup()
        self._gtk_pane = get_object('ui_form_topic')
        self._gtk_pane.insert_action_group('topic', actions_topic)
        self._context_name = get_object('ui_context_name')

        self._name_former: typing.Optional[str] = None
        self._infoid = VINFOID.ViewInfoId(get_object)

        self._gtk_pane.show_all()
        self._control.attach_form(self)

        # Signals
        view_name = self._infoid.get_view_name()
        _id = view_name.connect(
            'activate', lambda _entry: self._context_name.popdown())

        # Topic Menu
        UI.new_action_active_dialog(
            actions_topic, 'show-help-topic', self.on_show_dialog,
            UI.HELP_TOPIC)

        # Topic Display Menu
        UI.new_action_active(
            actions_topic, 'popup-name', self.on_popup_name)
        UI.new_action_active(
            actions_topic, 'reset-name', self.on_reset_name)
#         UI.new_action_active(
#             actions_topic, 'flip-summary', self.on_flip_summary)
        UI.new_action_active_dialog(
            actions_topic, 'show-help-topic-display', self.on_show_dialog,
            UI.HELP_TOPIC_DISPLAY)

        button_name = get_object('ui_flip_name')
        _binding = button_name.bind_property(
            'active', self._context_name, 'visible',
            GO.BindingFlags.BIDIRECTIONAL)

        exp_topic_summary = get_object('ui_exp_topic_summary')
        button_summary = get_object('ui_flip_summary')
        _binding = button_summary.bind_property(
            'active', exp_topic_summary, 'visible',
            GO.BindingFlags.BIDIRECTIONAL)

        exp_facts = get_object('ui_exp_facts')
        button_facts = get_object('ui_flip_facts')
        _binding = button_facts.bind_property(
            'active', exp_facts, 'visible',
            GO.BindingFlags.BIDIRECTIONAL)

        exp_current_fact = get_object('ui_exp_current_fact')
        button_current_fact = get_object('ui_flip_current_fact')
        _binding = button_current_fact.bind_property(
            'active', exp_current_fact, 'visible',
            GO.BindingFlags.BIDIRECTIONAL)

        exp_related_topics = get_object('ui_exp_related_topics')
        button_related_topics = get_object('ui_flip_related_topics')
        _binding = button_related_topics.bind_property(
            'active', exp_related_topics, 'visible',
            GO.BindingFlags.BIDIRECTIONAL)

    def _init_flip(self, p_get: 'gi.FunctionInfo', p_id_button: str,
                   p_id_view: str) -> None:
        """Initialize menu button to flip visibility of view.

        :param p_get:
        """
        pass

    def get_infoid(self) -> VINFOID.ViewInfoId:
        """Return view of topic identification information."""
        return self._infoid

#     def on_flip_summary(self, _action: Gio.SimpleAction,
#                         _target: GLib.Variant) -> None:
#         """Flip visibility of summary pane."""
#         new_state = not self._context_summary.get_visible()
#         self._context_summary.set_visible(new_state)

    @property
    def gtk_pane(self) -> Gtk.Box:
        """Return underlying presentation element."""
        return self._gtk_pane

    def on_popup_name(self, _action: Gio.SimpleAction,
                      _target: GLib.Variant) -> None:
        """Show factsheet name popover and save former name."""
        self._context_name.popup()
        self._name_former = self._infoid.name

    def on_reset_name(self, _action: Gio.SimpleAction,
                      _target: GLib.Variant) -> None:
        """Reset name to value at start of name change."""
        view_name = self._infoid.get_view_name()
        view_name.set_text(self._name_former)

    def on_show_dialog(self, _action: Gio.SimpleAction,
                       _target: GLib.Variant, p_dialog: Gtk.Dialog
                       ) -> None:
        """Display informational dialog.

        :param p_dialog: informational dialog.

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
        p_dialog.set_transient_for(None)
        window_top = self._gtk_pane.get_toplevel()
        if isinstance(window_top, Gtk.Window):
            if window_top.get_window_type() is Gtk.WindowType.TOPLEVEL:
                p_dialog.set_transient_for(window_top)
        _ = p_dialog.run()
        p_dialog.hide()
