"""
Defines class to display topic view in a Factsheet window pane.
"""
import gi   # type: ignore[import]
import typing   # noqa

import factsheet.control.control_topic as CTOPIC
import factsheet.view.ui as UI
import factsheet.view.view_markup as VMARKUP

gi.require_version('Gtk', '3.0')
from gi.repository import Gio   # noqa: E402
from gi.repository import GLib   # noqa: E402
from gi.repository import GObject as GO  # noqa: E402
from gi.repository import Gtk   # noqa: E402


class ViewTopic:
    """Display topic and translate user actions.

    Class :class:`.ViewTopic` maintains presentation of a topic in a
    pane of a Factsheet window.  The class displays the content of a
    topic model. It translates a user's actions at the user interface
    into requests to update the model and its presentation.

    .. attribute:: NAME_FILE_TOPIC_UI

       Path to user interface defintion of topic pane.
    """
    NAME_FILE_TOPIC_UI = str(UI.DIR_UI / 'topic.ui')

    def __init__(self, *, p_control: CTOPIC.ControlTopic) -> None:
        """
        :param p_control: control for topic the view presents.
        """
        self._control = p_control
        builder = Gtk.Builder.new_from_file(self.NAME_FILE_TOPIC_UI)
        get_object = builder.get_object

        # Components
        self._ui_view = get_object('ui_view_topic')
        self._init_name_topic(get_object)
        self._init_summary_topic(get_object)
        self._init_title_topic(get_object)
        self._init_menu_display(p_get_object=get_object)
        self._ui_view.show_all()

        # Dialogs
        dialogs = [('show-help-topic', UI.HELP_TOPIC),
                   ('show-help-topic-display', UI.HELP_TOPIC_DISPLAY),
                   ]
        actions_topic = Gio.SimpleActionGroup()
        self._ui_view.insert_action_group('topic', actions_topic)
        for name, dialog in dialogs:
            UI.new_action_active_dialog(
                actions_topic, name, self.on_show_dialog, dialog)

    def _init_menu_display(self, p_get_object: 'gi.FunctionInfo') -> None:
        """Bind display menu buttons to topic components.

        :param p_get_object: method to get topic user interface elements.
        """
        SYNC = GO.BindingFlags.BIDIRECTIONAL | GO.BindingFlags.SYNC_CREATE
        SYNC_ALL = GO.BindingFlags.SYNC_CREATE
        button_all = p_get_object('ui_show_all')
        names_ui = [
            ('ui_show_summary', 'ui_expander_summary'),
            ('ui_show_facts', 'ui_expander_facts'),
            ('ui_show_fact_current', 'ui_expander_fact_current'),
            ('ui_show_topics_related', 'ui_expander_topics_related'),
            ]
        for name_button, name_expander in names_ui:
            button = p_get_object(name_button)
            expander = p_get_object(name_expander)
            _ = button.bind_property('active', expander, 'visible', SYNC)
            _ = button_all.bind_property('active', button, 'active', SYNC_ALL)

    def _init_name_topic(self, p_get_object: 'gi.FunctionInfo') -> None:
        """Initialize view for topic name.

        :param p_get_object: method to get topic user interface elements.
        """
        EXPAND_OKAY = True
        FILL_OKAY = True
        N_PADDING = 6

        display_name = self._control.new_display_name()
        editor_name = self._control.new_editor_name()
        view_name = VMARKUP.ViewMarkup(display_name, editor_name, 'Name')
        site_name_sheet = p_get_object('ui_site_name_topic')
        site_name_sheet.pack_start(
            view_name.ui_view, EXPAND_OKAY, FILL_OKAY, N_PADDING)

    def _init_summary_topic(self, p_get_object: 'gi.FunctionInfo') -> None:
        """Initialize view for topic summary.

        :param p_get_object: method to get topic user interface elements.
        """
        editor_summary = self._control.new_editor_summary()
        site_summary_topic = p_get_object('ui_site_summary')
        site_summary_topic.add(editor_summary)

    def _init_title_topic(self, p_get_object: 'gi.FunctionInfo') -> None:
        """Initialize view for topic title.

        :param p_get_object: method to get topic user interface elements.
        """
        EXPAND_OKAY = True
        FILL_OKAY = True
        N_PADDING = 6

        display_title = self._control.new_display_title()
        editor_title = self._control.new_editor_title()
        view_title = VMARKUP.ViewMarkup(display_title, editor_title, 'Title')
        site_title_sheet = p_get_object('ui_site_title_topic')
        site_title_sheet.pack_start(
            view_title.ui_view, EXPAND_OKAY, FILL_OKAY, N_PADDING)

    @property
    def ui_view(self) -> Gtk.Box:
        """Return underlying presentation element.

        This is a stub method. It is untested.
        """
        return self._ui_view

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
        window_top = self._ui_view.get_toplevel()
        if isinstance(window_top, Gtk.Window):
            if window_top.get_window_type() is Gtk.WindowType.TOPLEVEL:
                p_dialog.set_transient_for(window_top)
        _ = p_dialog.run()
        p_dialog.hide()
