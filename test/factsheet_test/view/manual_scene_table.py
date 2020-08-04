"""
Defines application for manually testing view of table value.
"""
import gi   # type: ignore[import]
import sys

from factsheet.model import element as MELEMENT
from factsheet.model import setindexed as MSET
from factsheet.model import table as MTABLE
from factsheet.view import scene_value as VVALUE

gi.require_version('Gtk', '3.0')
from gi.repository import Gio   # type: ignore[import]    # noqa: E402
from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


def patch_table():
    """Return sample table for instpection"""
    set_int = MSET.SetIndexed[int]([0, 2, 4, 6, 8])
    set_str = MSET.SetIndexed[str](['a', 'e', 'i', 'o', 'u'])
    list_mix = [MELEMENT.ElementGeneric('x', 0), None,
                MELEMENT.ElementGeneric('y', 1), None,
                MELEMENT.ElementGeneric('z', 2)]
    rows = Gtk.ListStore(GO.TYPE_PYOBJECT, GO.TYPE_PYOBJECT, GO.TYPE_PYOBJECT)
    for e_int, e_str, e_mix in zip(set_int, set_str, list_mix):
        rows.append([e_int, e_str, e_mix])
    info_int = MTABLE.InfoColumn(title='Integers', symbol='i', styles=[
        'Label', 'Element', 'Index', 'Member', 'Plain'])
    info_str = MTABLE.InfoColumn(title='Strings', symbol='s', styles=[
        'Label', 'Element', 'Index', 'Member', 'Plain', 'Oops'])
    info_mix = MTABLE.InfoColumn(title='Mixed', symbol='m', styles=[
        'Label', 'Element', 'Index', 'Member', 'Plain'])
    columns = [info_int, info_str, info_mix]
    return MTABLE.TableElements(rows=rows, columns=columns)


class WinTable:
    """Main window for table view manual test.

    :param p_app: manual test application.
    """

    def __init__(self, p_app: Gtk.Application) -> None:
        self.window_gtk = Gtk.ApplicationWindow(application=p_app)
        table = patch_table()
        scene = VVALUE.SceneTableau(p_value=table)
        self.window_gtk.add(scene.scene_gtk)
        self.window_gtk.show_all()


class AppTable(Gtk.Application):
    """Application body."""

    def __init__(self) -> None:
        super().__init__(application_id='com.novafolks.manual_scene_table',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self):
        """Create and display an application window."""
        self.window = WinTable(p_app=self)

    def do_shutdown(self):
        """Application teardown. """
        Gtk.Application.do_shutdown(self)

    def do_startup(self):
        """Application setup within GTK. """
        Gtk.Application.do_startup(self)


def run_app():
    """Start application and show initial window."""
    app = AppTable()
    app.run(sys.argv)
    print('Done')


if __name__ == '__main__':
    run_app()
