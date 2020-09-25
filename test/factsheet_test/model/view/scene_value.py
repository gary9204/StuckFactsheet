"""
Defines classes to display fact value.
"""
import dataclasses as DC
import gi   # type: ignore[import]
import typing

from factsheet.model import array as MARRAY
from factsheet.model import table as MTABLE

gi.require_version('Gtk', '3.0')
from gi.repository import Gdk   # type: ignore[import]    # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402
from gi.repository import Pango  # type: ignore[import]    # noqa: E402


InterfaceTBD = typing.Any


class SceneValue:
    """Common ancestor for views of fact values."""

    def __init__(self) -> None:
        self._scene_gtk = Gtk.ScrolledWindow()

    def add_content(self, p_content: Gtk.Widget) -> None:
        """Add display object for content of scene.

        :param p_content: display object to add.
        """
        self._scene_gtk.add(p_content)

    @property
    def scene_gtk(self):
        return self._scene_gtk


class SceneEvaluate(SceneValue):
    """Interactive view of fact value."""

    def __init__(self):
        pass


class SceneSynopsis(SceneValue):
    """Compact view of fact value.

    .. attribute:: SYNOPSIS_DEFAULT

    Default markup for fact synopsis.

    .. attribute:: WIDTH_DEFAULT

    Width requested by default for a synopsis field.

    .. attribute:: WIDTH_MAX

    Maximum width for a synopsis field.
    """

    SYNOPSIS_DEFAULT = '<b>Oops! no synopsis.</b>'
    WIDTH_DEFAULT = 30
    WIDTH_MAX = 50

    def __init__(self) -> None:
        label = Gtk.Label(label=self.SYNOPSIS_DEFAULT)
        label.set_halign(Gtk.Align.START)
        label.set_valign(Gtk.Align.START)
        label.set_width_chars(self.WIDTH_DEFAULT)
        label.set_max_width_chars(self.WIDTH_MAX)
        label.set_ellipsize(Pango.EllipsizeMode.MIDDLE)
        label.set_selectable(True)

        super().__init__()
        self._label_gtk = label
        self.add_content(self._label_gtk)

    def set_markup(self, p_markup: str) -> None:
        """Set synopsis text.

        :param p_markup: new text, which may contain Pango markup.
        """
        self._label_gtk.set_label(p_markup)


class LabelColumn:
    """Label for row or column in a :class:`.SceneTableauArray`.

    :param p_element: element for label text.
    :param p_style: style to convert element to text.
    :param p_symbol: symbol for element.
    """

    def __init__(self, p_element: MARRAY.Entry, p_style: MARRAY.Style,
                 p_symbol: str) -> None:
        self._element = p_element
        self._style = p_style
        self._symbol = p_symbol
        self.refresh()
        self._label_gtk.set_use_markup(True)
        self._label_gtk.show()

    @property
    def label_gtk(self) -> Gtk.Label:
        """Return GTK presentation element for column label."""
        return self._label_gtk

    def refresh(self) -> None:
        """Update label to current style."""
        text = self._element.format(self._style.name, self._symbol)
        self._label_gtk = Gtk.Label(label=text)


class LabelArray:
    """Label for array in a :class:`.SceneTableauArray`..

    :param p_title: text of column title.
    :param p_style: style to convert element to text.
    :param p_styles: styles array elements support.

    .. attribute:: FIELD_NAME

        Model field that contains names of supported styles.
    """

    FIELD_NAME = 0

    def __init__(self, p_title: str, p_style: MARRAY.Style,
                 p_styles: typing.Iterable[MARRAY.Style]) -> None:
        self._clients: typing.List[InterfaceTBD] = list()
        self._style = p_style
        self._title = p_title
        store = Gtk.ListStore(str)
        for style in p_styles:
            store.append([style.name])

        self._label_gtk = Gtk.ComboBox(model=store)
        render = Gtk.CellRendererText()
        self._label_gtk.set_cell_data_func(render, self._fill_label_gtk)
        self._label_gtk.pack_start(render, expand=False)

        self._label_gtk.connect('changed', self.on_changed)
        self._label_gtk.set_halign(Gtk.Align.START)
        self._label_gtk.set_id_column(self.FIELD_NAME)
        I_ROW_ACTIVE = 0
        self._label_gtk.set_active(I_ROW_ACTIVE)
        self._label_gtk.set_popup_fixed_width(False)
        self._label_gtk.show()

    def attach_client(self, p_client: InterfaceTBD) -> None:
        """Add client to notify when active style change."""
        self._clients.append(p_client)

    def _fill_label_gtk(
            self, p_label_gtk: Gtk.CellLayout, p_render: Gtk.CellRenderer,
            p_store_styles: Gtk.TreeModel, p_i_row: Gtk.TreeIter) -> None:
        """Set array label contents to element style or title.

        The array label is a selection popup.  When the popup pops
        down, this method populates it with element styles.  When the popup
        pops up, this method populates it with the array title.

        :param p_label_gtk: contains popup cell.
        :param p_render: renders popup cell.
        :param p_store_styles: contains style ids.
        :param p_i_row: index of current row in store.
        """
        text = self._title
        if p_label_gtk.get_property('popup_shown'):
            text = p_store_styles[p_i_row][self.FIELD_NAME]
        p_render.set_property('markup', text)

    @property
    def label_gtk(self) -> Gtk.ComboBox:
        """Return GTK presentation element for array label."""
        return self._label_gtk

    def on_changed(self, p_label_gtk: Gtk.ComboBox) -> None:
        """Change style and notify clients when user changes selection.

        :param p_label_gtk: contains popup cell.
        """
        self._style.name = p_label_gtk.get_active_id()
        for client in self._clients:
            client.refresh()


class ColumnEntryArray:
    """Column that contains entries of an array.

    .. note:: The GTK widgit for a GtkTreeViewColumn is a child of a
        GtkButton.  It is necessary to pass window events through the
        button to the widget. `Stack Overflow button passthrough example`_
        presents one option in its last answer.

    .. _`Stack Overflow button passthrough example`:
        https://stackoverflow.com/questions/5223705/
        pygtk-entry-widget-in-treeviewcolumn-header

    .. attribute:: WIDTH_MIN

        Minimum width of column.

    :param p_field: model field that contains elements for column.
    :param p_title: element for title of column.
    :param p_style_title: style to convert title element to text.
    :param p_symbol_title: symbol for converting title element to text.
    :param p_style_entry: style to convert entry element to text.
    :param p_symbol_entry: symbol for converting entry elements to text.
    """

    WIDTH_MIN = 12

    def __init__(self, p_field: int, p_title: MARRAY.Entry,
                 p_style_title: MARRAY.Style, p_symbol_title: str,
                 p_style_entry: MARRAY.Style, p_symbol_entry: str) -> None:
        self._field = p_field
        self._style_entry = p_style_entry
        self._symbol_entry = p_symbol_entry

        self._column_gtk = Gtk.TreeViewColumn()
        render = Gtk.CellRendererText()
        self._column_gtk.pack_start(render, expand=True)
        self._column_gtk.set_cell_data_func(
            render, self._fill_column_gtk, p_style_entry)

        label = LabelColumn(p_element=p_title, p_style=p_style_title,
                            p_symbol=p_symbol_title)
        self._column_gtk.set_widget(label.label_gtk)

        self._column_gtk.set_clickable(True)
        self._column_gtk.set_resizable(True)
        self._column_gtk.set_reorderable(True)
        self._column_gtk.set_min_width(self.WIDTH_MIN)

    @property
    def column_gtk(self) -> Gtk.ComboBox:
        """Return GTK presentation element for column."""
        return self._column_gtk

    def _fill_column_gtk(self, _column: Gtk.TreeViewColumn,
                         p_render: Gtk.CellRenderer, p_array: Gtk.TreeModel,
                         p_i_row: Gtk.TreeIter, p_style: MARRAY.Style
                         ) -> None:
        """Set element cell contents to text of element from table.

        :param _column: column to contain the text (unused).
        :param p_render: renders text.
        :param p_array: array that contains row label elements.
        :param p_i_row: index of table row for current cell.
        :param p_style: style to convert element to text.
        """
        text = '---'
        element = p_array[p_i_row][self._field]
        if element is not None:
            text = element.format(p_style.name, self._symbol_entry)
        p_render.set_property('markup', text)

    def refresh(self) -> None:
        """Update display."""
        self._column_gtk.set_visible(False)
        self._column_gtk.set_visible(True)


class ColumnLabelArray:
    """Column that contains row labels of an array.

    .. note:: The GTK widgit for a GtkTreeViewColumn is a child of a
        GtkButton.  It is necessary to pass window events through the
        button to the widget. `Stack Overflow button passthrough example`_
        presents one option in its last answer.

    .. _`Stack Overflow button passthrough example`:
        https://stackoverflow.com/questions/5223705/
        pygtk-entry-widget-in-treeviewcolumn-header

    .. attribute:: COLOR_NAME

        Background color for row labels.

    .. attribute:: WIDTH_MIN

        Minimum width of column.

    :param p_field: model field that contains elements for row labels.
    :param p_title: title for column.
    :param p_symbol: symbol for converting row label elements to text.
    :param p_style: style to convert element to text.
    :param p_styles: styles row elements support.
    """

    COLOR_NAME = 'Light Green'
    WIDTH_MIN = 12

    def __init__(self, p_field: int, p_title: str, p_symbol: str,
                 p_style: MARRAY.Style,
                 p_styles: typing.Iterable[MARRAY.Style]) -> None:
        self._field = p_field
        self._symbol = p_symbol

        self._column_gtk = Gtk.TreeViewColumn()
        render = Gtk.CellRendererText()
        self._column_gtk.pack_start(render, expand=True)
        self._column_gtk.set_cell_data_func(
            render, self._fill_column_gtk, p_style)
        color = Gdk.RGBA()
        _ = color.parse(self.COLOR_NAME)
        render.set_property('background-rgba', color)

        label = LabelArray(
            p_title=p_title, p_style=p_style, p_styles=p_styles)
        self._column_gtk.set_widget(label.label_gtk)
        button = self._column_gtk.get_button()
        button.connect('realize',
                       lambda b: b.get_event_window().set_pass_through(True))
        label.attach_client(self)

        self._column_gtk.set_clickable(True)
        self._column_gtk.set_resizable(True)
        self._column_gtk.set_reorderable(True)
        self._column_gtk.set_min_width(self.WIDTH_MIN)

    @property
    def column_gtk(self) -> Gtk.ComboBox:
        """Return GTK presentation element for column."""
        return self._column_gtk

    def _fill_column_gtk(self, _column: Gtk.TreeViewColumn,
                         p_render: Gtk.CellRenderer, p_array: Gtk.TreeModel,
                         p_i_row: Gtk.TreeIter, p_style: MARRAY.Style
                         ) -> None:
        """Set element cell contents to text of element from table.

        :param _column: column to contain the text (unused).
        :param p_render: renders text.
        :param p_array: array that contains row label elements.
        :param p_i_row: index of table row for current cell.
        :param p_style: style to convert element to text.
        """
        text = '---'
        element = p_array[p_i_row][self._field]
        if element is not None:
            text = element.format(p_style.name, self._symbol)
        p_render.set_property('markup', text)

    def refresh(self) -> None:
        """Update display."""
        self._column_gtk.set_visible(False)
        self._column_gtk.set_visible(True)


class SceneTableauArray(SceneValue):
    """Tabular view of array fact value.

    :param p_value: array of elements.
    """

    FIELD_LABEL = 0

    def __init__(self, p_value: MARRAY.Array) -> None:
        super().__init__()
        array_gtk = Gtk.TreeView(model=p_value.rows)
        self._scene_gtk.add(array_gtk)
        style_row = MARRAY.Style(MARRAY.IdStyle('Label'))
        style_col = style_row
        style_entry = style_row
        column_label = ColumnLabelArray(
            p_field=self.FIELD_LABEL,
            p_title=p_value.title,
            p_symbol=p_value.symbol_row,
            p_style=style_row,
            p_styles=p_value.styles
            )
        array_gtk.append_column(column_label.column_gtk)
        for i_col, label_col in enumerate(p_value.cols):
            i_field = i_col + 1
            column_entry = ColumnEntryArray(
                p_field=i_field,
                p_title=label_col,
                p_symbol_title=p_value.symbol_col,
                p_style_title=style_col,
                p_symbol_entry=p_value.symbol_entry,
                p_style_entry=style_entry
                )
            array_gtk.append_column(column_entry.column_gtk)
        array_gtk.set_reorderable(True)


class HeaderColumn:
    """View of column header in a tableau scene.

    :param p_title: text of column title.
    :param p_ids_style: IDs of styles column elements support.
    :param p_refresh: function to refresh parent column view.

    .. attribute:: FIELD_ID

        Model field that contains IDs of supported styles.
    """

    FIELD_ID = 0

    def __init__(self, p_title: str, p_ids_style: typing.Iterable[str],
                 p_refresh: typing.Callable[[str], None]
                 ) -> None:
        self._title = p_title
        ids_style = Gtk.ListStore(str)
        for id_style in p_ids_style:
            ids_style.append([id_style])
        self._refresh = p_refresh

        self._header_gtk = Gtk.ComboBox(model=ids_style)
        self._header_gtk.connect('changed', self.on_changed)
        self._header_gtk.set_halign(Gtk.Align.START)
        I_ROW_ACTIVE = 0
        self._header_gtk.set_active(I_ROW_ACTIVE)
        self._header_gtk.set_id_column(self.FIELD_ID)
        self._header_gtk.set_popup_fixed_width(False)
        self._header_gtk.show()

        render = Gtk.CellRendererText()
        self._header_gtk.set_cell_data_func(render, self._fill_header_gtk)
        self._header_gtk.pack_start(render, expand=False)

    def _fill_header_gtk(
            self, p_header_gtk: Gtk.CellLayout, p_render: Gtk.CellRenderer,
            p_store_ids: Gtk.TreeModel, p_i_row: Gtk.TreeIter) -> None:
        """Set header view contents to element style ids or title.

        The column header is a selection popup.  When the popup pops
        down, this method populates it with style ids.  When the popup
        pops up, this method populates it with the column title.

        :param p_header_gtk: contains the popup cell.
        :param p_render: renders popup cell.
        :param p_store_ids: store that contains style ids.
        :param p_i_row: index of current row in store.
        """
        text = self._title
        if p_header_gtk.get_property('popup_shown'):
            text = p_store_ids[p_i_row][self.FIELD_ID]
        p_render.set_property('markup', text)

    @property
    def header_gtk(self) -> Gtk.ComboBox:
        """Return GTK presentation element for header column."""
        return self._header_gtk

    def on_changed(self, p_header_gtk: Gtk.ComboBox) -> None:
        """Refresh column display when user changes selection in header.

        :param p_header_gtk: column header.
        """
        self._refresh(p_header_gtk.get_active_id())


class ColumnTableau:
    """View of column in a tableau scene.

    .. note:: The GTK widgit for a GtkTreeViewColumn is a child of a
        GtkButton.  It is necessary to pass window events through the
        button to the widget. `Stack Overflow button passthrough example`_
        presents one option in its last answer.

    .. _`Stack Overflow button passthrough example`:
        https://stackoverflow.com/questions/5223705/
        pygtk-entry-widget-in-treeviewcolumn-header

    .. attribute:: WIDTH_MIN

        Minimum width of columns.

    :param p_i_column: index of model column for view.
    :param p_title: title for column.
    :param p_symbol: symbol for element display.
    :param p_ids_style: IDs of styles column elements support.
    """

    WIDTH_MIN = 12

    def __init__(self, p_i_column: int, p_title: str, p_symbol: str,
                 p_ids_styles: typing.Sequence[str]) -> None:
        self._i_column = p_i_column
        self._symbol = p_symbol
        ID_DEFAULT = 0

        self._column_gtk = Gtk.TreeViewColumn()
        self._column_gtk.set_clickable(True)
        self._column_gtk.set_resizable(True)
        self._column_gtk.set_reorderable(True)
        self._column_gtk.set_min_width(self.WIDTH_MIN)

        render = Gtk.CellRendererText()
        self._column_gtk.pack_start(render, expand=True)
        self._column_gtk.set_cell_data_func(render, self._fill_column_gtk)

        header = HeaderColumn(p_title=p_title, p_ids_style=p_ids_styles,
                              p_refresh=self.refresh)
        self._column_gtk.set_widget(header.header_gtk)
        button = self._column_gtk.get_button()
        button.connect('realize',
                       lambda b: b.get_event_window().set_pass_through(True))
        self.refresh(p_ids_styles[ID_DEFAULT])

    @property
    def column_gtk(self) -> Gtk.ComboBox:
        """Return GTK presentation element for tableau column."""
        return self._column_gtk

    def _fill_column_gtk(
            self, _column: Gtk.TreeViewColumn, p_render: Gtk.CellRenderer,
            p_table: Gtk.TreeModel, p_i_row: Gtk.TreeIter, _extra: typing.Any
            ) -> None:
        """Set element cell contents to element text from table.

        :param _column: view column that contains the cell (unused).
        :param p_render: renders cell.
        :param p_table: table that contains elements.
        :param p_i_row: index of table row for current cell.
        :param _extra: extra data for renderer (unused)
        """
        text = '---'
        element = p_table[p_i_row][self._i_column]
        if element is not None:
            text = element.format(self._id_style, self._symbol)
        p_render.set_property('markup', text)

    def refresh(self, p_id_style: str) -> None:
        """Change style ID and update display.

        :param p_id_style: ID of new style.
        """
        self._id_style = p_id_style
        self._column_gtk.set_visible(False)
        self._column_gtk.set_visible(True)


class SceneTableau(SceneValue):
    """Tabular view of table fact value.

    :param p_value: table of elements.
    """

    def __init__(self, p_value: MTABLE.TableElements) -> None:
        super().__init__()
        # self._rows = p_value.rows
        treeview_gtk = Gtk.TreeView(model=p_value.rows)
        for i_col, info_col in enumerate(p_value.columns):
            column = ColumnTableau(i_col, *DC.astuple(info_col))
            treeview_gtk.append_column(column.column_gtk)
        treeview_gtk.set_reorderable(True)
        self._scene_gtk.add(treeview_gtk)


class SceneText(SceneValue):
    """Plain text view of fact value.

    .. attribute:: TEXT_DEFAULT

    Default plain text for fact.
    """

    TEXT_DEFAULT = '<b>Oops! no fact text.</b>'

    def __init__(self) -> None:
        label = Gtk.Label(label=self.TEXT_DEFAULT)
        label.set_halign(Gtk.Align.START)
        label.set_valign(Gtk.Align.START)
        label.set_line_wrap(True)
        label.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)
        label.set_selectable(True)

        super().__init__()
        self._label_gtk = label
        self.add_content(self._label_gtk)

    def set_text(self, p_text: str) -> None:
        """Set plain text for fact.

        :param p_markup: new plain text.
        """
        self._label_gtk.set_text(p_text)
