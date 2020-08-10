"""
Defines unit tests for classes to display fact value.  See
:mod:`.scene_value`.
"""
import dataclasses as DC
import gi   # type: ignore[import]
import pytest   # type: ignore[import]

from factsheet.model import array as MARRAY
from factsheet.model import element as MELEMENT
from factsheet.model import table as MTABLE
from factsheet.view import scene_value as VVALUE

gi.require_version('Gtk', '3.0')
from gi.repository import Gdk   # type: ignore[import]    # noqa: E402
from gi.repository import GObject as GO  # type: ignore[import]  # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402
from gi.repository import Pango  # type: ignore[import]  # noqa:E402


class TestSceneEvaluate:
    """Unit tests for :class:`.SceneEvaluate`."""

    @pytest.mark.skip(reason='Deferred until complete Facet implementation.')
    def test_init(self):
        """Confirm initialization."""
        # Setup
        # Test
        pass


class TestSceneSynopsis:
    """Unit tests for :class:`.SceneSynopsis`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        # Test
        target = VVALUE.SceneSynopsis()
        assert target.scene_gtk is target._scene_gtk
        assert isinstance(target._scene_gtk, Gtk.ScrolledWindow)
        assert isinstance(target._label_gtk, Gtk.Label)
        viewport = target._scene_gtk.get_child()
        label = viewport.get_child()
        assert target._label_gtk is label
        assert target.SYNOPSIS_DEFAULT == label.get_label()
        assert label.get_halign() is Gtk.Align.START
        assert label.get_valign() is Gtk.Align.START
        assert label.get_width_chars() is target.WIDTH_DEFAULT
        assert label.get_max_width_chars() is target.WIDTH_MAX
        assert label.get_ellipsize() is Pango.EllipsizeMode.MIDDLE
        assert label.get_selectable()

    def test_set_markup(self):
        """Confirm markup change."""
        # Setup
        MARKUP = 'A Norwegian Blue'
        target = VVALUE.SceneSynopsis()
        # Test
        target.set_markup(MARKUP)
        assert MARKUP == target._label_gtk.get_label()


class TestLabelColumn:
    """Unit tests for :class:`.LabelColumn`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        INDEX = 0
        MEMBER = 'x'
        SYMBOL = 'g'
        element = MELEMENT.ElementGeneric[str](
            p_member=MEMBER, p_index=MELEMENT.IndexElement(INDEX))
        ID_STYLE = MELEMENT.IdStyle('Element')
        style = MELEMENT.Style(p_name=ID_STYLE)
        TEXT = element.format(style.name, SYMBOL)
        # Test
        target = VVALUE.LabelColumn(
            p_element=element, p_style=style, p_symbol=SYMBOL)
        assert target._element is element
        assert target._style is style
        assert SYMBOL == target._symbol
        assert isinstance(target._label_gtk, Gtk.Label)
        assert TEXT == target._label_gtk.get_label()
        assert target._label_gtk.get_use_markup()
        assert target._label_gtk.get_visible()

    @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
        ('_label_gtk', 'label_gtk'),
        ])
    def test_property(self, NAME_ATTR, NAME_PROP):
        """Confirm properties are get-only.

        #. Case: get
        #. Case: no set
        #. Case: no delete
        """
        # Setup
        INDEX = 0
        MEMBER = 'x'
        SYMBOL = 'g'
        element = MELEMENT.ElementGeneric[str](
            p_member=MEMBER, p_index=MELEMENT.IndexElement(INDEX))
        ID_STYLE = MELEMENT.IdStyle('Element')
        style = MELEMENT.Style(p_name=ID_STYLE)
        # Test
        target = VVALUE.LabelColumn(
            p_element=element, p_style=style, p_symbol=SYMBOL)
        value_attr = getattr(target, NAME_ATTR)
        target_prop = getattr(VVALUE.LabelColumn, NAME_PROP)
        value_prop = getattr(target, NAME_PROP)
        # Test: read
        assert target_prop.fget is not None
        assert str(value_attr) == str(value_prop)
        # Test: no replace
        assert target_prop.fset is None
        # Test: no delete
        assert target_prop.fdel is None

    def test_refresh(self):
        """Confirm update to label display."""
        INDEX = 0
        MEMBER = 'x'
        SYMBOL = 'g'
        element = MELEMENT.ElementGeneric[str](
            p_member=MEMBER, p_index=MELEMENT.IndexElement(INDEX))
        STYLE_BEFORE = MELEMENT.IdStyle('Plain')
        style = MELEMENT.Style(p_name=STYLE_BEFORE)
        target = VVALUE.LabelColumn(
            p_element=element, p_style=style, p_symbol=SYMBOL)
        STYLE_AFTER = MELEMENT.IdStyle('Element')
        style.name = STYLE_AFTER
        TEXT = element.format(style.name, SYMBOL)
        # Test
        target.refresh()
        assert TEXT == target._label_gtk.get_label()


class TestLabelArray:
    """Unit tests for :class:`.LabelArray`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        TITLE = 'Cheeses'
        STYLES = [MELEMENT.Style('Cheddar'), MELEMENT.Style('Gouda'),
                  MELEMENT.Style('Munster'), MELEMENT.Style('Stilton'),
                  MELEMENT.Style('Provolone'), MELEMENT.Style('Oops!'),
                  ]
        I_ROW_DEFAULT = 0
        style = STYLES[I_ROW_DEFAULT]
        names = [s.name for s in STYLES]
        FIELD_NAME = 0
        I_CELL = 0
        # Test
        target = VVALUE.LabelArray(
            p_title=TITLE, p_style=style, p_styles=STYLES)
        assert isinstance(target._clients, list)
        assert not target._clients
        assert target._style is style
        assert TITLE == target._title
        assert isinstance(target._label_gtk, Gtk.ComboBox)
        target_gtk = target._label_gtk
        target_store = target_gtk.get_model()
        assert names == [row[FIELD_NAME] for row in target_store]

        render = target_gtk.get_cells()[I_CELL]
        assert isinstance(render, Gtk.CellRendererText)
        assert target_gtk.get_halign() is Gtk.Align.START
        assert VVALUE.LabelArray.FIELD_NAME == target_gtk.get_id_column()
        assert I_ROW_DEFAULT == target_gtk.get_active()
        assert not target_gtk.get_popup_fixed_width()
        assert target_gtk.get_visible()

    @pytest.mark.parametrize(
        'NAME_SIGNAL, NAME_ATTRIBUTE, ORIGIN, N_DEFAULT', [
            ('changed', '_label_gtk', Gtk.ComboBox, 0),
            ])
    def test_init_signals(
            self, NAME_SIGNAL, NAME_ATTRIBUTE, ORIGIN, N_DEFAULT):
        """Confirm initialization of signal connections."""
        # Setup
        TITLE = 'Cheeses'
        STYLES = [MELEMENT.Style('Cheddar'), MELEMENT.Style('Gouda'),
                  MELEMENT.Style('Munster'), MELEMENT.Style('Stilton'),
                  MELEMENT.Style('Provolone'), MELEMENT.Style('Oops!'),
                  ]
        I_STYLE = 0
        style = STYLES[I_STYLE]
        origin_gtype = GO.type_from_name(GO.type_name(ORIGIN))
        signal = GO.signal_lookup(NAME_SIGNAL, origin_gtype)
        # Test
        target = VVALUE.LabelArray(
            p_title=TITLE, p_style=style, p_styles=STYLES)
        attribute = getattr(target, NAME_ATTRIBUTE)
        n_handlers = 0
        while True:
            id_signal = GO.signal_handler_find(
                attribute, GO.SignalMatchType.ID, signal,
                0, None, None, None)
            if 0 == id_signal:
                break

            n_handlers += 1
            GO.signal_handler_disconnect(attribute, id_signal)

        assert N_DEFAULT + 1 == n_handlers

    @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
        ('_label_gtk', 'label_gtk'),
        ])
    def test_property(self, NAME_ATTR, NAME_PROP):
        """Confirm properties are get-only.

        #. Case: get
        #. Case: no set
        #. Case: no delete
        """
        # Setup
        TITLE = 'Cheeses'
        STYLES = [MELEMENT.Style('Cheddar'), MELEMENT.Style('Gouda'),
                  MELEMENT.Style('Munster'), MELEMENT.Style('Stilton'),
                  MELEMENT.Style('Provolone'), MELEMENT.Style('Oops!'),
                  ]
        I_STYLE = 0
        style = STYLES[I_STYLE]
        target = VVALUE.LabelArray(
            p_title=TITLE, p_style=style, p_styles=STYLES)
        value_attr = getattr(target, NAME_ATTR)
        target_prop = getattr(VVALUE.LabelArray, NAME_PROP)
        value_prop = getattr(target, NAME_PROP)
        # Test: read
        assert target_prop.fget is not None
        assert str(value_attr) == str(value_prop)
        # Test: no replace
        assert target_prop.fset is None
        # Test: no delete
        assert target_prop.fdel is None

    def test_attach_client(self):
        """Confirm client added."""
        # Setup
        TITLE = 'Cheeses'
        STYLES = [MELEMENT.Style('Cheddar'), MELEMENT.Style('Gouda'),
                  MELEMENT.Style('Munster'), MELEMENT.Style('Stilton'),
                  MELEMENT.Style('Provolone'), MELEMENT.Style('Oops!'),
                  ]
        I_STYLE = 0
        style = STYLES[I_STYLE]
        target = VVALUE.LabelArray(
            p_title=TITLE, p_style=style, p_styles=STYLES)
        ELEMENT = MELEMENT.ElementGeneric[str](p_member='x', p_index=0)
        style = target._style
        SYMBOL = 'g'
        N_CLIENTS = 5
        clients = [VVALUE.LabelColumn(ELEMENT, style, SYMBOL)
                   for _ in range(N_CLIENTS)]
        # Test
        for c in clients:
            target.attach_client(c)
        assert clients == target._clients

    @pytest.mark.parametrize('SHOWN, TEXT', [
        (False, 'Cheeses'),
        (True, 'Munster'),
        ])
    def test_fill_label_gtk(self, SHOWN, TEXT):
        """Confirm cell data function updates label text."""
        # Setup
        TITLE = 'Cheeses'
        STYLES = [MELEMENT.Style('Cheddar'), MELEMENT.Style('Gouda'),
                  MELEMENT.Style('Munster'), MELEMENT.Style('Stilton'),
                  MELEMENT.Style('Provolone'), MELEMENT.Style('Oops!'),
                  ]
        I_STYLE = 0
        style = STYLES[I_STYLE]
        target = VVALUE.LabelArray(
            p_title=TITLE, p_style=style, p_styles=STYLES)
        target_gtk = target._label_gtk
        I_CELL = 0
        render = target_gtk.get_cells()[I_CELL]
        store = target_gtk.get_model()
        I_ROW = 2
        win = Gtk.Window()
        win.add(target_gtk)
        win.show_all()
        if SHOWN:
            target_gtk.popup()
        # Test
        target._fill_label_gtk(target_gtk, render, store, I_ROW)
        assert TEXT == render.get_property('text')

    def test_on_changed(self):
        """Confirm header calls column refresh."""
        # Setup
        class PatchRefresh:
            def __init__(self):
                self.called = False

            def refresh(self):
                self.called = True

        TITLE = 'Cheeses'
        STYLES = [MELEMENT.Style('Cheddar'), MELEMENT.Style('Gouda'),
                  MELEMENT.Style('Munster'), MELEMENT.Style('Stilton'),
                  MELEMENT.Style('Provolone'), MELEMENT.Style('Oops!'),
                  ]
        I_STYLE = 0
        style = STYLES[I_STYLE]
        target = VVALUE.LabelArray(
            p_title=TITLE, p_style=style, p_styles=STYLES)
        N_CLIENTS = 5
        clients = []
        for _ in range(N_CLIENTS):
            client = PatchRefresh()
            clients.append(client)
            target.attach_client(client)
        ID_ACTIVE = 'Gouda'
        target._label_gtk.set_active_id(ID_ACTIVE)
        # Test
        target.on_changed(target._label_gtk)
        assert ID_ACTIVE == target._style.name
        for c in clients:
            assert c.called


class TestColumnEntryArray:
    """Unit tests for :class:`.ColumnEntryArray`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        FIELD = 2
        TITLE = MARRAY.Entry(p_member=42, p_index=6)
        SYMBOL_TITLE = 'c'
        STYLE_TITLE = MARRAY.Style('Label')
        SYMBOL_ENTRY = 'e'
        STYLE_ENTRY = MARRAY.Style('Entry')
        I_CELL = 0
        # Test
        target = VVALUE.ColumnEntryArray(
            p_field=FIELD, p_title=TITLE, p_symbol_title=SYMBOL_TITLE,
            p_style_title=STYLE_TITLE, p_symbol_entry=SYMBOL_ENTRY,
            p_style_entry=STYLE_ENTRY)
        assert FIELD == target._field
        assert SYMBOL_ENTRY == target._symbol_entry
        assert STYLE_ENTRY == target._style_entry
        assert isinstance(target._column_gtk, Gtk.TreeViewColumn)
        target_gtk = target._column_gtk
        target_render = target_gtk.get_cells()[I_CELL]
        assert isinstance(target_render, Gtk.CellRendererText)
        assert isinstance(target_gtk.get_widget(), Gtk.Label)

        assert target_gtk.get_clickable()
        assert target_gtk.get_resizable()
        assert target_gtk.get_reorderable()
        assert target.WIDTH_MIN == target_gtk.get_min_width()

    @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
        ('_column_gtk', 'column_gtk'),
        ])
    def test_property(self, NAME_ATTR, NAME_PROP):
        """Confirm properties are get-only.

        #. Case: get
        #. Case: no set
        #. Case: no delete
        """
        # Setup
        FIELD = 2
        TITLE = MARRAY.Entry(p_member=42, p_index=6)
        SYMBOL_TITLE = 'c'
        STYLE_TITLE = MARRAY.Style('Label')
        SYMBOL_ENTRY = 'e'
        STYLE_ENTRY = MARRAY.Style('Entry')
        target = VVALUE.ColumnEntryArray(
            p_field=FIELD, p_title=TITLE, p_symbol_title=SYMBOL_TITLE,
            p_style_title=STYLE_TITLE, p_symbol_entry=SYMBOL_ENTRY,
            p_style_entry=STYLE_ENTRY)
        value_attr = getattr(target, NAME_ATTR)
        target_prop = getattr(VVALUE.ColumnEntryArray, NAME_PROP)
        value_prop = getattr(target, NAME_PROP)
        # Test: read
        assert target_prop.fget is not None
        assert str(value_attr) == str(value_prop)
        # Test: no replace
        assert target_prop.fset is None
        # Test: no delete
        assert target_prop.fdel is None

    def test_fill_column_gtk(self, patch_args_array):
        """Confirm cell data function updates column text."""
        # Setup
        FIELD = 2
        TITLE = MARRAY.Entry(p_member=42, p_index=6)
        ARGS = patch_args_array
        symbol_title = ARGS.p_symbol_col
        STYLE_TITLE = MARRAY.Style('Label')
        symbol_entry = ARGS.p_symbol_entry
        STYLE_ENTRY = MARRAY.Style('Entry')
        target = VVALUE.ColumnEntryArray(
            p_field=FIELD, p_title=TITLE, p_symbol_title=symbol_title,
            p_style_title=STYLE_TITLE, p_symbol_entry=symbol_entry,
            p_style_entry=STYLE_ENTRY)
        I_STYLE = 4
        STYLE_ENTRY.name = ARGS.p_styles[I_STYLE].name
        target_gtk = target._column_gtk
        I_CELL = 0
        render = target_gtk.get_cells()[I_CELL]
        array = ARGS.p_rows
        for row in array:
            print([(e.member, e.index) for e in row])
        I_ROW = 2
        TEXT = '{}: 11'.format(FIELD-1)
        # Test
        target._fill_column_gtk(target_gtk, render, array, I_ROW, STYLE_ENTRY)
        assert TEXT == render.get_property('text')

    def test_fill_column_gtk_none(self, patch_args_array):
        """Confirm cell data function updates column text."""
        # Setup
        FIELD = 2
        TITLE = MARRAY.Entry(p_member=42, p_index=6)
        ARGS = patch_args_array
        symbol_title = ARGS.p_symbol_col
        STYLE_TITLE = MARRAY.Style('Label')
        symbol_entry = ARGS.p_symbol_entry
        STYLE_ENTRY = MARRAY.Style('Entry')
        target = VVALUE.ColumnEntryArray(
            p_field=FIELD, p_title=TITLE, p_symbol_title=symbol_title,
            p_style_title=STYLE_TITLE, p_symbol_entry=symbol_entry,
            p_style_entry=STYLE_ENTRY)
        I_STYLE = 4
        STYLE_ENTRY.name = ARGS.p_styles[I_STYLE].name
        target_gtk = target._column_gtk
        I_CELL = 0
        render = target_gtk.get_cells()[I_CELL]
        array = ARGS.p_rows
        I_ROW = 0
        array[I_ROW][FIELD] = None
        TEXT = '---'
        # Test
        target._fill_column_gtk(target_gtk, render, array, I_ROW, STYLE_ENTRY)
        assert TEXT == render.get_property('text')

    def test_refresh(self, monkeypatch, patch_args_array):
        """Confirm style change and display update."""
        # Setup
        class PatchVisible:
            def __init__(self):
                self.args = []

            def set_visible(self, p_visible):
                self.args.append(p_visible)

        FIELD = 2
        TITLE = MARRAY.Entry(p_member=42, p_index=6)
        ARGS = patch_args_array
        symbol_title = ARGS.p_symbol_col
        STYLE_TITLE = MARRAY.Style('Label')
        symbol_entry = ARGS.p_symbol_entry
        STYLE_ENTRY = MARRAY.Style('Entry')
        target = VVALUE.ColumnEntryArray(
            p_field=FIELD, p_title=TITLE, p_symbol_title=symbol_title,
            p_style_title=STYLE_TITLE, p_symbol_entry=symbol_entry,
            p_style_entry=STYLE_ENTRY)
        I_STYLE = 4
        STYLE_ENTRY.name = ARGS.p_styles[I_STYLE].name

        patch = PatchVisible()
        monkeypatch.setattr(
            Gtk.TreeViewColumn, "set_visible", patch.set_visible)
        ARGS_VISIBLE = [False, True]
        # Test
        target.refresh()
        assert ARGS_VISIBLE == patch.args


class TestColumnLabelArray:
    """Unit tests for :class:`.ColumnLabelArray`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        FIELD_ROW_LABELS = 0
        TITLE = 'Cheeses'
        SYMBOL = 'r'
        STYLES = [MELEMENT.Style('Cheddar'), MELEMENT.Style('Gouda'),
                  MELEMENT.Style('Munster'), MELEMENT.Style('Stilton'),
                  MELEMENT.Style('Provolone'), MELEMENT.Style('Oops!'),
                  ]
        style = MARRAY.Style('Oops!')
        I_CELL = 0
        # Test
        target = VVALUE.ColumnLabelArray(
            p_field=FIELD_ROW_LABELS, p_title=TITLE, p_symbol=SYMBOL,
            p_style=style, p_styles=STYLES)
        assert FIELD_ROW_LABELS == target._field
        assert SYMBOL == target._symbol
        assert isinstance(target._column_gtk, Gtk.TreeViewColumn)
        target_gtk = target._column_gtk
        assert isinstance(target_gtk.get_widget(), Gtk.ComboBox)
        target_render = target_gtk.get_cells()[I_CELL]
        assert isinstance(target_render, Gtk.CellRendererText)
        assert target_render.get_property('background-set')
        color_rgba = Gdk.RGBA()
        _ = color_rgba.parse(target.COLOR_NAME)
        assert target_render.get_property('background-rgba').equal(color_rgba)

        assert target_gtk.get_clickable()
        assert target_gtk.get_resizable()
        assert target_gtk.get_reorderable()
        assert target.WIDTH_MIN == target_gtk.get_min_width()

    @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
        ('_column_gtk', 'column_gtk'),
        ])
    def test_property(self, NAME_ATTR, NAME_PROP):
        """Confirm properties are get-only.

        #. Case: get
        #. Case: no set
        #. Case: no delete
        """
        # Setup
        FIELD_ROW_LABELS = 0
        TITLE = 'Cheeses'
        SYMBOL = 'r'
        STYLES = [MELEMENT.Style('Cheddar'), MELEMENT.Style('Gouda'),
                  MELEMENT.Style('Munster'), MELEMENT.Style('Stilton'),
                  MELEMENT.Style('Provolone'), MELEMENT.Style('Oops!'),
                  ]
        style = MARRAY.Style('Oops!')
        target = VVALUE.ColumnLabelArray(
            p_field=FIELD_ROW_LABELS, p_title=TITLE, p_symbol=SYMBOL,
            p_style=style, p_styles=STYLES)
        I_STYLE = 0
        style.name = STYLES[I_STYLE].name
        value_attr = getattr(target, NAME_ATTR)
        target_prop = getattr(VVALUE.ColumnLabelArray, NAME_PROP)
        value_prop = getattr(target, NAME_PROP)
        # Test: read
        assert target_prop.fget is not None
        assert str(value_attr) == str(value_prop)
        # Test: no replace
        assert target_prop.fset is None
        # Test: no delete
        assert target_prop.fdel is None

    def test_fill_column_gtk(self, patch_args_array):
        """Confirm cell data function updates column text."""
        # Setup
        FIELD_ROW_LABELS = 0
        ARGS = patch_args_array
        style = MARRAY.Style('Oops!')
        target = VVALUE.ColumnLabelArray(
            p_field=FIELD_ROW_LABELS, p_title=ARGS.p_title,
            p_symbol=ARGS.p_symbol_row, p_style=style, p_styles=ARGS.p_styles)
        I_STYLE = 4
        style.name = ARGS.p_styles[I_STYLE].name
        target_gtk = target._column_gtk
        I_CELL = 0
        render = target_gtk.get_cells()[I_CELL]
        array = ARGS.p_rows
        I_ROW = 2
        TEXT = '2: 8'
        # Test
        target._fill_column_gtk(target_gtk, render, array, I_ROW, style)
        assert TEXT == render.get_property('text')

    def test_fill_column_gtk_none(self, patch_args_array):
        """Confirm cell data function updates column text."""
        # Setup
        ARGS = patch_args_array
        FIELD_ROW_LABELS = 0
        style = MARRAY.Style('Oops!')
        target = VVALUE.ColumnLabelArray(
            p_field=FIELD_ROW_LABELS, p_title=ARGS.p_title,
            p_symbol=ARGS.p_symbol_row, p_style=style, p_styles=ARGS.p_styles)
        I_STYLE = 4
        style.name = ARGS.p_styles[I_STYLE].name
        target_gtk = target._column_gtk
        I_CELL = 0
        render = target_gtk.get_cells()[I_CELL]
        array = ARGS.p_rows
        I_ROW = 1
        array[I_ROW][FIELD_ROW_LABELS] = None
        TEXT = '---'
        # Test
        target._fill_column_gtk(target_gtk, render, array, I_ROW, style)
        assert TEXT == render.get_property('text')

    def test_refresh(self, monkeypatch, patch_args_array):
        """Confirm style change and display update."""
        # Setup
        class PatchVisible:
            def __init__(self):
                self.args = []

            def set_visible(self, p_visible):
                self.args.append(p_visible)

        FIELD_ROW_LABELS = 0
        ARGS = patch_args_array
        style = MARRAY.Style('Oops!')
        target = VVALUE.ColumnLabelArray(
            p_field=FIELD_ROW_LABELS, p_title=ARGS.p_title,
            p_symbol=ARGS.p_symbol_row, p_style=style, p_styles=ARGS.p_styles)
        I_STYLE = 4
        style.name = ARGS.p_styles[I_STYLE].name

        patch = PatchVisible()
        monkeypatch.setattr(
            Gtk.TreeViewColumn, "set_visible", patch.set_visible)
        ARGS_VISIBLE = [False, True]
        # Test
        target.refresh()
        assert ARGS_VISIBLE == patch.args


class TestSceneTableauArray:
    """Unit tests for :class:`.SceneTableauArray`."""

    def test_init(self, patch_args_array):
        """| Confirm initialization.
        | Case: explicit agruments.
        """
        # Setup
        ARGS = patch_args_array
        TABLE = MARRAY.Array(
            p_rows=ARGS.p_rows, p_cols=ARGS.p_cols, p_styles=ARGS.p_styles,
            p_title=ARGS.p_title, p_symbol_row=ARGS.p_symbol_row,
            p_symbol_col=ARGS.p_symbol_col, p_symbol_entry=ARGS.p_symbol_entry)
        FIELD_LABEL = 0
        # Test
        target = VVALUE.SceneTableauArray(p_value=TABLE)
        assert target.scene_gtk is target._scene_gtk
        assert isinstance(target._scene_gtk, Gtk.ScrolledWindow)
        target_gtk = target._scene_gtk.get_child()
        assert isinstance(target_gtk, Gtk.TreeView)
        assert target_gtk.get_model() is ARGS.p_rows
        target_column_label = target_gtk.get_column(FIELD_LABEL)
        assert isinstance(target_column_label.get_widget(), Gtk.ComboBox)
        assert len(ARGS.p_cols)+1 == target_gtk.get_n_columns()
        assert target_gtk.get_reorderable()

    def test_init_default(self, patch_args_array):
        """| Confirm initialization.
        | Case: default arguments.
        """
        # Setup
        ARGS = patch_args_array
        TABLE = MARRAY.Array(
            p_rows=ARGS.p_rows, p_cols=ARGS.p_cols, p_styles=ARGS.p_styles)
        # Test
        target = VVALUE.SceneTableauArray(p_value=TABLE)
        # target_gtk = target._scene_gtk.get_child()
        # assert isinstance(target_gtk, Gtk.TreeView)
        # assert target_gtk.get_model() is ARGS.rows
        # assert len(ARGS.columns) == target_gtk.get_n_columns()
        # assert target_gtk.get_reorderable()


class TestHeaderColumn:
    """Unit tests for :class:`.HeaderColumn`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        TITLE = 'Cheeses'
        IDS_STYLE = ['Cheddar', 'Gouda', 'Munster', 'Stilton']

        def REFRESH(p_id_style): pass
        I_ROW_DEFAULT = 0
        I_CELL = 0
        # Test
        target = VVALUE.HeaderColumn(p_title=TITLE, p_ids_style=IDS_STYLE,
                                     p_refresh=REFRESH)
        assert isinstance(target._header_gtk, Gtk.ComboBox)
        assert TITLE == target._title
        model = target._header_gtk.get_model()
        assert IDS_STYLE == [row[0] for row in model]
        assert target._refresh is REFRESH

        target_gtk = target.header_gtk
        render = target_gtk.get_cells()[I_CELL]
        assert isinstance(render, Gtk.CellRendererText)
        assert target_gtk.get_halign() is Gtk.Align.START
        assert I_ROW_DEFAULT == target_gtk.get_active()
        assert VVALUE.HeaderColumn.FIELD_ID == target_gtk.get_id_column()
        assert not target_gtk.get_popup_fixed_width()
        assert target_gtk.get_visible()

    @pytest.mark.parametrize(
        'NAME_SIGNAL, NAME_ATTRIBUTE, ORIGIN, N_DEFAULT', [
            ('changed', '_header_gtk', Gtk.ComboBox, 0),
            ])
    def test_init_signals(
            self, NAME_SIGNAL, NAME_ATTRIBUTE, ORIGIN, N_DEFAULT):
        """Confirm initialization of signal connections."""
        # Setup
        TITLE = "Cheeses"
        IDS_STYLE = ['Cheddar', 'Gouda', 'Munster', 'Stilton']

        def REFRESH(p_id_style): pass
        origin_gtype = GO.type_from_name(GO.type_name(ORIGIN))
        signal = GO.signal_lookup(NAME_SIGNAL, origin_gtype)
        # Test
        target = VVALUE.HeaderColumn(p_title=TITLE, p_ids_style=IDS_STYLE,
                                     p_refresh=REFRESH)
        attribute = getattr(target, NAME_ATTRIBUTE)
        n_handlers = 0
        while True:
            id_signal = GO.signal_handler_find(
                attribute, GO.SignalMatchType.ID, signal,
                0, None, None, None)
            if 0 == id_signal:
                break

            n_handlers += 1
            GO.signal_handler_disconnect(attribute, id_signal)

        assert N_DEFAULT + 1 == n_handlers

    @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
        ('_header_gtk', 'header_gtk'),
        ])
    def test_property(self, NAME_ATTR, NAME_PROP):
        """Confirm properties are get-only.

        #. Case: get
        #. Case: no set
        #. Case: no delete
        """
        # Setup
        TITLE = "Cheeses"
        IDS_STYLE = ['Cheddar', 'Gouda', 'Munster', 'Stilton']

        def REFRESH(p_id_style): pass
        target = VVALUE.HeaderColumn(p_title=TITLE, p_ids_style=IDS_STYLE,
                                     p_refresh=REFRESH)
        value_attr = getattr(target, NAME_ATTR)
        target_prop = getattr(VVALUE.HeaderColumn, NAME_PROP)
        value_prop = getattr(target, NAME_PROP)
        # Test: read
        assert target_prop.fget is not None
        assert str(value_attr) == str(value_prop)
        # Test: no replace
        assert target_prop.fset is None
        # Test: no delete
        assert target_prop.fdel is None

    @pytest.mark.parametrize('SHOWN, TEXT', [
        (False, 'Cheeses'),
        (True, 'Munster'),
        ])
    def test_fill_header_gtk(self, SHOWN, TEXT):
        """Confirm cell data function updates header text."""
        # Setup
        TITLE = 'Cheeses'
        IDS_STYLE = ['Cheddar', 'Gouda', 'Munster', 'Stilton']

        def REFRESH(p_id_style): pass
        target = VVALUE.HeaderColumn(p_title=TITLE, p_ids_style=IDS_STYLE,
                                     p_refresh=REFRESH)
        target_gtk = target._header_gtk
        I_CELL = 0
        render = target_gtk.get_cells()[I_CELL]
        model = target_gtk.get_model()
        I_ROW = 2
        win = Gtk.Window()
        win.add(target_gtk)
        win.show_all()
        if SHOWN:
            target_gtk.popup()
        # Test
        target._fill_header_gtk(target_gtk, render, model, I_ROW)
        assert TEXT == render.get_property('text')

    def test_on_changed(self):
        """Confirm header calls column refresh."""
        # Setup
        class PatchRefresh:
            def __init__(self):
                self.called = False
                self.id_style = ''

            def refresh(self, p_id_style):
                self.called = True
                self.id_style = p_id_style

        patch = PatchRefresh()
        TITLE = "Cheeses"
        IDS_STYLE = ['Cheddar', 'Gouda', 'Munster', 'Stilton']
        ID_ACTIVE = 'Gouda'
        target = VVALUE.HeaderColumn(p_title=TITLE, p_ids_style=IDS_STYLE,
                                     p_refresh=patch.refresh)
        target.header_gtk.set_active_id(ID_ACTIVE)
        # Test
        target.on_changed(target.header_gtk)
        assert patch.called
        assert ID_ACTIVE == patch.id_style


class TestColumnTableau:
    """Unit tests for :class:`.ColumnTableau`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        I_COLUMN = 0
        TITLE = "Cheeses"
        SYMBOL = 'c'
        IDS_STYLE = ['Cheddar', 'Gouda', 'Munster', 'Stilton']
        ID_STYLE = 0
        info_column = MTABLE.InfoColumn(
            title=TITLE, symbol=SYMBOL, styles=IDS_STYLE)
        I_CELL = 0
        # Test
        target = VVALUE.ColumnTableau(I_COLUMN, *DC.astuple(info_column))
        assert I_COLUMN == target._i_column
        assert SYMBOL == target._symbol
        assert IDS_STYLE[ID_STYLE] == target._id_style
        assert isinstance(target._column_gtk, Gtk.TreeViewColumn)
        target_gtk = target._column_gtk
        assert target_gtk.get_clickable()
        assert target_gtk.get_resizable()
        assert target_gtk.get_reorderable()
        assert target.WIDTH_MIN == target_gtk.get_min_width()

        render = target_gtk.get_cells()[I_CELL]
        assert isinstance(render, Gtk.CellRendererText)

        assert isinstance(target_gtk.get_widget(), Gtk.ComboBox)

    @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
        ('_column_gtk', 'column_gtk'),
        ])
    def test_property(self, patch_args_table, NAME_ATTR, NAME_PROP):
        """Confirm properties are get-only.

        #. Case: get
        #. Case: no set
        #. Case: no delete
        """
        # Setup
        I_COLUMN = 0
        ARGS = patch_args_table
        info_column = ARGS.columns[I_COLUMN]
        target = VVALUE.ColumnTableau(I_COLUMN, *DC.astuple(info_column))
        value_attr = getattr(target, NAME_ATTR)
        target_prop = getattr(VVALUE.ColumnTableau, NAME_PROP)
        value_prop = getattr(target, NAME_PROP)
        # Test: read
        assert target_prop.fget is not None
        assert str(value_attr) == str(value_prop)
        # Test: no replace
        assert target_prop.fset is None
        # Test: no delete
        assert target_prop.fdel is None

    @pytest.mark.parametrize('I_ROW, I_COLUMN, ID_STYLE, TEXT', [
        (1, 2, 'Plain', '---'),
        (3, 1, 'Oops!', '3: o'),
        ])
    def test_fill_column_gtk(
            self, patch_args_table, I_ROW, I_COLUMN, ID_STYLE, TEXT):
        """Confirm cell data function updates column text."""
        # Setup
        ARGS = patch_args_table
        info_column = ARGS.columns[I_COLUMN]
        target = VVALUE.ColumnTableau(I_COLUMN, *DC.astuple(info_column))
        target._id_style = ID_STYLE
        target_gtk = target._column_gtk
        I_CELL = 0
        render = target_gtk.get_cells()[I_CELL]
        table = ARGS.rows
        EXTRA = None
        # Test
        target._fill_column_gtk(target_gtk, render, table, I_ROW, EXTRA)
        assert TEXT == render.get_property('text')

    def test_refresh(self, monkeypatch):
        """Confirm style change and display update."""
        # Setup
        class PatchVisible:
            def __init__(self):
                self.args = []

            def set_visible(self, p_visible):
                self.args.append(p_visible)

        I_COLUMN = 0
        TITLE = "Cheeses"
        SYMBOL = 'c'
        IDS_STYLE = ['Cheddar', 'Gouda', 'Munster', 'Stilton']
        target = VVALUE.ColumnTableau(
            I_COLUMN, p_title=TITLE, p_symbol=SYMBOL, p_ids_styles=IDS_STYLE)

        patch = PatchVisible()
        monkeypatch.setattr(
            Gtk.TreeViewColumn, "set_visible", patch.set_visible)
        ID_STYLE_NEW = 'Stilton'
        ARGS = [False, True]
        # Test
        target.refresh(ID_STYLE_NEW)
        assert ID_STYLE_NEW == target._id_style
        assert ARGS == patch.args


class TestSceneTableau:
    """Unit tests for :class:`.SceneTableau`."""

    def test_init(self, patch_args_table):
        """| Confirm initialization.
        | Case: general attributes.
        """
        # Setup
        ARGS = patch_args_table
        TABLE = MTABLE.TableElements(rows=ARGS.rows, columns=ARGS.columns)
        # Test
        target = VVALUE.SceneTableau(p_value=TABLE)
        assert target.scene_gtk is target._scene_gtk
        assert isinstance(target._scene_gtk, Gtk.ScrolledWindow)
        # assert target._rows is TABLE.rows
        # assert isinstance(target._treeview_gtk, Gtk.TreeView)
        target_gtk = target._scene_gtk.get_child()
        assert isinstance(target_gtk, Gtk.TreeView)
        assert target_gtk.get_model() is ARGS.rows
        assert len(ARGS.columns) == target_gtk.get_n_columns()
        assert target_gtk.get_reorderable()


class TestSceneText:
    """Unit tests for :class:`.SceneText`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        # Test
        target = VVALUE.SceneText()
        assert target.scene_gtk is target._scene_gtk
        assert isinstance(target._scene_gtk, Gtk.ScrolledWindow)
        assert isinstance(target._label_gtk, Gtk.Label)
        viewport = target._scene_gtk.get_child()
        label = viewport.get_child()
        assert target._label_gtk is label
        assert target.TEXT_DEFAULT == label.get_label()
        assert label.get_halign() is Gtk.Align.START
        assert label.get_valign() is Gtk.Align.START
        assert label.get_line_wrap()
        assert label.get_line_wrap_mode() is Pango.WrapMode.WORD_CHAR
        assert label.get_selectable()

    def test_set_markup(self):
        """Confirm text change."""
        # Setup
        TEXT = 'A Norwegian Blue'
        target = VVALUE.SceneText()
        # Test
        target.set_text(TEXT)
        assert TEXT == target._label_gtk.get_label()


class TestSceneValue:
    """Unit tests for :class:`.SceneValue`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        # Test
        target = VVALUE.SceneValue()
        assert isinstance(target._scene_gtk, Gtk.ScrolledWindow)

    def test_add_content(self):
        """Confirm content added to scene."""
        # Setup
        CONTENT = Gtk.TreeView()
        target = VVALUE.SceneValue()
        # Test
        target.add_content(CONTENT)
        assert target._scene_gtk.get_child() is CONTENT

    @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
        ('_scene_gtk', 'scene_gtk'),
        ])
    def test_property(self, NAME_ATTR, NAME_PROP):
        """Confirm properties are get-only.

        #. Case: get
        #. Case: no set
        #. Case: no delete
        """
        # Setup
        target = VVALUE.SceneValue()
        value_attr = getattr(target, NAME_ATTR)
        target_prop = getattr(VVALUE.SceneValue, NAME_PROP)
        value_prop = getattr(target, NAME_PROP)
        # Test: read
        assert target_prop.fget is not None
        assert str(value_attr) == str(value_prop)
        # Test: no replace
        assert target_prop.fset is None
        # Test: no delete
        assert target_prop.fdel is None
