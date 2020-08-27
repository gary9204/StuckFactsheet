"""
Defines application for manually testing view of table value.
"""
import gi   # type: ignore[import]
import sys
import typing

from factsheet.control import control_fact as CFACT
from factsheet.model import fact as MFACT
from factsheet.view.block import block_fact as VFACT

gi.require_version('Gtk', '3.0')
# from gi.repository import Gdk   # type: ignore[import]    # noqa: E402
from gi.repository import Gio   # type: ignore[import]    # noqa: E402
# from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class SampleFact:
    """Sample presenting a Boolean Fact"""

    def __init__(self, p_parent, p_status_check, p_value_check) -> None:
        self.window_gtk = p_parent
        self.status_check = p_status_check
        self.value_check = p_value_check
        self.control = self.make_control()
        self.block_fact = VFACT.BlockFact[typing.Any](self.control)
        self.dialog_gtk = self.make_dialog(self.block_fact.block_gtk)

    def on_check(self, _button) -> None:
        self.block_fact.update(self.status_check, self.value_check)

    def on_clear(self, _button) -> None:
        default = 'You have not checked this fact.'
        self.block_fact.update(MFACT.StatusOfFact.UNCHECKED, default)

    def make_control(self) -> CFACT.ControlFact:
        type_value = type(self.value_check).__name__
        fact: MFACT.Fact = MFACT.Fact(
            p_name='Sample',
            p_summary=('Fact demonstrates {} fact value'
                       ''.format(type_value)),
            p_title='Sample {} Fact'.format(type_value))
        control = CFACT.ControlFact(p_fact=fact)
        return control

    def make_dialog(self, p_block_fact) -> Gtk.Dialog:
        NO_EXPAND = False
        EXPAND = True
        NO_FILL = False
        FILL = True
        PADDING = 0

        box_buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        button = Gtk.Button(label='Check')
        button.connect('clicked', self.on_check)
        box_buttons.pack_start(button, NO_EXPAND, NO_FILL, PADDING)

        button = Gtk.Button(label='Clear')
        button.connect('clicked', self.on_clear)
        box_buttons.pack_start(button, NO_EXPAND, NO_FILL, PADDING)

        dialog = Gtk.Dialog(transient_for=self.window_gtk)
        # dialog.set_transient_for(self.window_gtk)
        # dialog.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        # dialog.set_skip_pager_hint(True)
        _ = dialog.add_button('Close', Gtk.ResponseType.CLOSE)
        dialog.set_skip_taskbar_hint(True)
        content = dialog.get_child()
        content.pack_start(p_block_fact, EXPAND, FILL, PADDING)
        content.pack_start(box_buttons, NO_EXPAND, NO_FILL, PADDING)
        content.show_all()
        return dialog


class WinDispatch:
    """Main window for table view manual test.

    :param p_app: manual test application.
    """

    def __init__(self, p_app: Gtk.Application) -> None:
        self.window_gtk = Gtk.ApplicationWindow(application=p_app)
        NO_EXPAND = False
        EXPAND = True
        NO_FILL = False
        FILL = True
        PADDING = 6
        box_gtk = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.window_gtk.add(box_gtk)

        button = Gtk.Button(label='Demo Boolean Fact')
        box_gtk.pack_start(button, NO_EXPAND, NO_FILL, PADDING)
        sample_bool = SampleFact(p_parent=self.window_gtk,
                                 p_status_check=MFACT.StatusOfFact.DEFINED,
                                 p_value_check=True)
        button.connect('clicked', self.on_clicked, sample_bool)

        button = Gtk.Button(label='Demo Integer Fact')
        box_gtk.pack_start(button, NO_EXPAND, NO_FILL, PADDING)
        sample_int = SampleFact(p_parent=self.window_gtk,
                                p_status_check=MFACT.StatusOfFact.DEFINED,
                                p_value_check=42)
        button.connect('clicked', self.on_clicked, sample_int)

        button = Gtk.Button(label='Demo Text Fact')
        box_gtk.pack_start(button, NO_EXPAND, NO_FILL, PADDING)
        text = (
            'There is a tide in the affairs of men, which taken at the '
            'flood, leads on to fortune.  Omitted, all the voyage of '
            'their lives is bound in shallows and in miseries.\n\n'
            'On such a full sea are we now afloat.  We must take the '
            'current when it serves or lose our ventures.\n\n'
            '-- Cassius from <i>Julius Caeser</i>'
            )
        sample_text = SampleFact(p_parent=self.window_gtk,
                                 p_status_check=MFACT.StatusOfFact.DEFINED,
                                 p_value_check=text)
        button.connect('clicked', self.on_clicked, sample_text)

        filler = Gtk.Label()
        box_gtk.pack_start(filler, EXPAND, FILL, PADDING)

        self.window_gtk.show_all()

    def on_clicked(self, _button, sample) -> None:
        """TBD"""
        _ = sample.dialog_gtk.run()
        sample.dialog_gtk.hide()


class AppBlockFact(Gtk.Application):
    """Application ."""

    def __init__(self) -> None:
        super().__init__(application_id='com.novafolks.manual_block_fact',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self):
        """Create and display a dispatch window."""
        self.window = WinDispatch(p_app=self)

    def do_shutdown(self):
        """Application teardown within GTK. """
        Gtk.Application.do_shutdown(self)

    def do_startup(self):
        """Application setup within GTK. """
        Gtk.Application.do_startup(self)


def run_app():
    """Start application and show dispatch window."""
    print('Start -  fact block check.')
    app = AppBlockFact()
    app.run(sys.argv)
    print('Finish - fact block check.')


if __name__ == '__main__':
    run_app()
