"""
Defines application for manually testing view of table value.
"""
import gi   # type: ignore[import]
import sys

from factsheet.model import array as MARRAY
from factsheet.model import element as MELEMENT
from factsheet.model import setindexed as MSET
from factsheet.model import table as MTABLE
from factsheet.view import scene_value as VVALUE

gi.require_version('Gtk', '3.0')
from gi.repository import Gio   # type: ignore[import]    # noqa: E402
from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


def patch_array():
    """Return sample array for inspection"""
    Set = MSET.SetIndexed[int]
    Element = MELEMENT.ElementGeneric[int]
    N_ROWS = 3
    N_COLUMNS = 4
    size = N_ROWS * N_COLUMNS
    range_r = range(0, size, N_COLUMNS)
    range_c = range(0, size, N_ROWS)
    ROWS = Gtk.ListStore(*[GO.TYPE_PYOBJECT]*(1+N_COLUMNS))
    for i, r in enumerate(range_r):
        row = [Element(p_member=r, p_index=i)]
        entries = []
        for j, c in enumerate(range_c):
            entry = Element(p_member=((r+c) % size), p_index=i*N_COLUMNS + j)
            entries.append(entry)
        # entries = Set([(r+c) % size for c in range_c])
        row.extend(entries)
        ROWS.append(row)
    set_cols = Set(range_c)
    COLS = list(set_cols)
    STYLES = [MELEMENT.Style('Label'), MELEMENT.Style('Element'),
              MELEMENT.Style('Index'), MELEMENT.Style('Member'),
              MELEMENT.Style('Plain'), MELEMENT.Style('Oops!'),
              ]
    TITLE = 'A'
    SYMBOL_ROW = 'r'
    SYMBOL_COL = 'c'
    SYMBOL_ENTRY = 'a'
    return MARRAY.Array(p_rows=ROWS, p_cols=COLS, p_styles=STYLES,
                        p_title=TITLE, p_symbol_row=SYMBOL_ROW,
                        p_symbol_col=SYMBOL_COL, p_symbol_entry=SYMBOL_ENTRY)


def patch_table():
    """Return sample table for inspection"""
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
        EXPAND = True
        FILL = True
        PADDING = 6
        box_gtk = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.window_gtk.add(box_gtk)

        table = patch_table()
        scene_table = VVALUE.SceneTableau(p_value=table)
        box_gtk.pack_start(scene_table.scene_gtk, EXPAND, FILL, PADDING)

        array = patch_array()
        scene_array = VVALUE.SceneTableauArray(p_value=array)
        box_gtk.pack_start(scene_array.scene_gtk, EXPAND, FILL, PADDING)

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
    print('Done.')


if __name__ == '__main__':
    run_app()
