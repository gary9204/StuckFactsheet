"""
factsheet.app - define Factsheet application and entry point.
"""


import gi   # type: ignore[import]
import sys
import typing   # noqa

from factsheet.view import sheet as VSHEET


gi.require_version('Gtk', '3.0')
from gi.repository import Gio   # type: ignore[import]    # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class Factsheet(Gtk.Application):
    """Factsheet applications
    """

    def __init__(self, *args: typing.Tuple, **kwargs: typing.Dict):
        """Register application with GTK.

        :param args: superclass positional parameters
        :param kwargs: superclass keyword parameters
        """
        super().__init__(application_id='com.novafolks.g2alpha',
                         flags=Gio.ApplicationFlags.FLAGS_NONE,
                         *args, **kwargs)

    def do_activate(self):
        """Create and display an initial factsheet with default content. """
        _ = VSHEET.Sheet.new_factsheet(self)

    def do_shutdown(self):
        """Application teardown. """
        Gtk.Application.do_shutdown(self)
        print('Factsheet application shutdown.')

    def do_startup(self):
        """Application setup within GTK. """
        Gtk.Application.do_startup(self)
        print('Factsheet application startup.')


def run_app():
    """Start application and show initial window."""
    app = Factsheet()
    app.run(sys.argv)


if __name__ == '__main__':
    run_app()
