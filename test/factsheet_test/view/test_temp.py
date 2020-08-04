"""
Temporary test to visualize tableau.
"""
import gi   # type: ignore[import]
import sys
import typing

from factsheet.model import element as MELEMENT
from factsheet.model import setindexed as MSET

gi.require_version('Gtk', '3.0')
from gi.repository import Gio   # type: ignore[import]    # noqa: E402
from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class WinTemp:
    """Application main window."""

    def __init__(self, p_app: Gtk.Application) -> None:
        super().__init__()
        self.window_gtk = Gtk.ApplicationWindow(application=p_app)

        self.apply_style = {
            'Label': self.style_label,
            'Element': self.style_element,
            'Index': self.style_index,
            'Member': self.style_member,
            'Plain': self.style_plain,
            }
        self.current = 'Label'

        store_combo = Gtk.ListStore(str)
        # store_combo = Gtk.ListStore(str, str)
        for style in self.apply_style:
            store_combo.append([style])
            # style_markup = ''.join(
            #     ['<span weight="normal">', style, '</span>'])
            # store_combo.append([style, style_markup])

        combo = Gtk.ComboBox.new_with_model(store_combo)
        combo.set_halign(Gtk.Align.START)
        combo.set_active(0)
        combo.set_popup_fixed_width(False)
        combo.set_id_column(0)
        combo.show()
        render = Gtk.CellRendererText()
        combo.pack_start(render, expand=False)
        combo.add_attribute(render, 'markup', 0)
        combo.set_cell_data_func(render, self.fill_cell, combo, 0)

        # render_title = Gtk.CellRendererText()
        # combo.pack_start(render_title, expand=False)
        # # combo.add_attribute(render_title, 'markup', 0)
        # combo.set_cell_data_func(
        #     render_title, lambda *_a: render_title.set_property(
        #         'text', 'Element'))
        # # combo.set_cell_data_func(
        # #     render_title, lambda *_a: render_title.set_property(
        # #         'markup', '<i>Elements</i>'))
        # # combo.set_cell_data_func(render_title, self.title_data)
        # combo.bind_property('popup_shown', render_title, 'visible',
        #                     GO.BindingFlags.INVERT_BOOLEAN)

        # render_format = Gtk.CellRendererText()
        # render_format.set_property('visible', False)
        # combo.pack_start(cell=render_format, expand=False)
        # combo.add_attribute(render_format, 'text', 0)
        # # combo.add_attribute(render_format, 'markup', 1)
        # combo.bind_property('popup_shown', render_format, 'visible',
        #                     GO.BindingFlags.DEFAULT)

        vbox_combo = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=6)
        # vbox_combo.pack_start(
        #     combo, expand=False, fill=False, padding=0)
        vbox_combo.pack_start(
            Gtk.Label(label='Filler'), expand=False, fill=True, padding=0)

        store_tableau = Gtk.ListStore(GO.TYPE_PYOBJECT)
        sample_set = MSET.SetIndexed[int]([2, 4, 8, 16, 32, 64, 128])
        for e in sample_set:
            store_tableau.append([e])
        store_tableau.append([None])

        render_element = Gtk.CellRendererText()
        column_element = Gtk.TreeViewColumn(title='Elements')
        column_element.pack_start(render_element, False)
        column_element.set_cell_data_func(render_element, self.element_data, 0)
        column_element.set_clickable(True)
        column_element.set_widget(combo)
        combo.connect('changed', self.on_changed, column_element)
        # https://stackoverflow.com/questions/5223705/pygtk-entry-widget-in-treeviewcolumn-header
        button = column_element.get_button()
        button.connect('realize', lambda *_a: button.get_event_window(
            ).set_pass_through(True))
        tableau = Gtk.TreeView(model=store_tableau)
        tableau.append_column(column_element)

        win_tableau = Gtk.ScrolledWindow()
        win_tableau.add(tableau)

        vbox_tableau = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox_tableau.pack_start(
            Gtk.Label(label='Filler'), expand=False, fill=True, padding=0)
        vbox_tableau.pack_start(
            win_tableau, expand=True, fill=True, padding=0)
        vbox_tableau.pack_start(
            Gtk.Label(label='Filler'), expand=False, fill=True, padding=0)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        hbox.pack_start(
            vbox_combo, expand=False, fill=True, padding=0)
        hbox.pack_start(
            vbox_tableau, expand=True, fill=True, padding=0)

        self.window_gtk.add(hbox)
        self.window_gtk.show_all()

    def fill_cell(self, _layout, p_cell, p_model, p_iter, p_combo,
                  p_column) -> None:
        if p_combo.get_property('popup_shown'):
            option = p_model[p_iter][p_column]
            p_cell.set_property('markup', option)
        else:
            p_cell.set_property('markup', '<i>X</i>')

    def element_data(self, _column, p_render, p_store, p_index, p_offset
                     ) -> None:
        element = p_store[p_index][p_offset]
        p_render.set_property(
            'markup', self.apply_style[self.current](element))

    def on_changed(self, p_combo: Gtk.ComboBox, p_column: Gtk.TreeViewColumn
                   ) -> None:
        # model = p_combo.get_model()
        # i_active = p_combo.get_active_iter()
        # active = model[i_active][0]
        self.current = p_combo.get_active_id()
        p_column.set_visible(False)
        p_column.set_visible(True)

    def style_index(self, p_element: typing.Optional[
            MELEMENT.ElementGeneric[int]]) -> str:
        text = '--'
        if p_element is not None:
            text = str(p_element.index)
        return text

    def style_plain(self, p_element: MELEMENT.ElementGeneric[int]) -> str:
        text = '--'
        if p_element is not None:
            text = ''.join(
                [str(p_element.index), ': ', str(p_element.member)])
        return text

    def style_label(self, p_element: MELEMENT.ElementGeneric[int]) -> str:
        text = '--'
        if p_element is not None:
            text = ''.join(
                ['<i>a</i><sub>', str(p_element.index), '</sub>'])
        return text

    def style_element(self, p_element: MELEMENT.ElementGeneric[int]) -> str:
        text = '--'
        if p_element is not None:
            text = ''.join(['<i>a</i><sub>', str(p_element.index),
                           '</sub> = ', str(p_element.member)])
        return text

    def style_member(self, p_element: MELEMENT.ElementGeneric[int]) -> str:
        text = '--'
        if p_element is not None:
            text = str(p_element.member)
        return text

    # def title_data(self, _layout, p_cell, _model, _iter) -> None:
    #     p_cell.set_property('markup', '<i>Elements</i>')


class AppTemp(Gtk.Application):
    """Application body."""

    def __init__(self) -> None:
        super().__init__(application_id='com.novafolks.temp_tableau',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self):
        """Create and display an application window."""
        self.window = WinTemp(p_app=self)

    def do_shutdown(self):
        """Application teardown. """
        Gtk.Application.do_shutdown(self)

    def do_startup(self):
        """Application setup within GTK. """
        Gtk.Application.do_startup(self)


def run_app():
    """Start application and show initial window."""
    app = AppTemp()
    app.run(sys.argv)
    print('Done')


if __name__ == '__main__':
    run_app()
