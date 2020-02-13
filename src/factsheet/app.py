"""
factsheet.app - Factsheet application entry point.
"""


import gi   # type: ignore[import]
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


def run_app():
    """Start application and show initial window."""
    win = Gtk.ApplicationWindow()
    win.connect('destroy', Gtk.main_quit)
    win.show_all()
    Gtk.main()


if __name__ == '__main__':
    run_app()
