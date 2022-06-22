"""
Defines classes for visual elements of outline contining items with
identity information.

.. data:: FactoryDisplaySummary

    Factory class for display of item summary.

.. data:: ModelSummary

    Type for model of item summary.

.. data:: UiButtonFind

    Type for button to show and hide search of item outline.

.. data:: UiButtonSearchScope

    Type for button to change scope of search.

.. data:: UiChooserItem

    Type for visual element of :class:`SelectorItem`.

.. data:: UiViewOutline

    Type for view of outline of items.
"""
import gi   # type: ignore[import]
from gi.repository import Gio   # type: ignore[import]
from gi.repository import GLib
from gi.repository import GObject as GO
import logging
from pathlib import Path
import typing

import factsheet.bridge_ui as BUI
import factsheet.view.id as VID
import factsheet.view.ui as UI

import factsheet.model.idcore as MIDCORE

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk   # noqa: E402


logger = logging.getLogger('Main.VSELECT_ITEM')


DisplaySummary = BUI.DisplayTextStyled
FactoryDisplaySummary = BUI.FactoryDisplayTextStyled
ModelSummary = BUI.ModelTextStyled
UiActionsOutlineId = typing.Union[Gio.SimpleActionGroup]
UiDisplayOutlineId = typing.Union[Gtk.TreeView]
UiSearchOutlineId = typing.Union[Gtk.SearchBar]


# TODO: Prune types when updating SelectorItem.
ModelOutline = BUI.ModelOutlineMulti[MIDCORE.IdCore]
UiButtonFind = typing.Union[Gtk.ToggleButton]
UiButtonSearchScope = typing.Union[Gtk.ToggleButton]
UiSelectorItem = typing.Union[Gtk.Box]
UiViewOutline = BUI.ViewOutline


class InitColumnsOutlineId:
    """Initialize identity item outline with name and title columns."""

    def __init__(self, p_ui_view_outline: UiDisplayOutlineId,
                 p_action_group: UiActionsOutlineId = None) -> None:
        """Initialize columns in visual element of outline.

        Each column supports `Pango markup`_.  Optional action cycles
        through showing name column, title column, or both columns.

    .. _Pango markup:
        https://developer.gnome.org/pygtk/stable/pango-markup-language.html

        :param p_ui_view_outline: visual element of outline.
        :param p_action_group: add column switch action to this group
            (optional).
        """
        self._column_name = UI.new_column_stock('Name', self._markup_cell_name)
        p_ui_view_outline.append_column(self._column_name)
        self._column_title = UI.new_column_stock(
            'Title', self._markup_cell_title)
        p_ui_view_outline.append_column(self._column_title)
        if p_action_group is not None:
            UI.new_action_active(
                p_action_group, 'cycle-columns', self.cycle_columns)

    def _markup_cell_name(
            self, _column: Gtk.TreeViewColumn, p_render: Gtk.CellRenderer,
            p_ui_model: Gtk.TreeModel, p_line: BUI.LineOutline, _data) -> None:
        """Set markup for name cell in the outline's visual element.

        :param _column: column of cell to format (unused).
        :param p_render: renders formatted cell contents.
        :param p_ui_model: contains cell content.
        :param p_line: line of cell to format.
        :param _data: user data (unused).
        """
        item_id = BUI.ModelOutline.get_item_direct(p_ui_model, p_line)
        name = 'Missing'
        if item_id is not None:
            name = item_id.name.text
        p_render.set_property('markup', name)

    def _markup_cell_title(
            self, _column: Gtk.TreeViewColumn, p_render: Gtk.CellRenderer,
            p_ui_model: Gtk.TreeModel, p_line: BUI.LineOutline, _data) -> None:
        """Set markup for title cell in the outline visual element.

        :param _column: column of cell to format (unused).
        :param p_render: renders formatted cell contents.
        :param p_ui_model: contains cell content.
        :param p_line: line of cell to format.
        :param _data: user data (unused).
        """
        item_id = BUI.ModelOutline.get_item_direct(p_ui_model, p_line)
        title = 'Missing'
        if item_id is not None:
            title = item_id.title.text
        p_render.set_property('markup', title)

    def cycle_columns(
            self, _action: Gio.SimpleAction, _target: GLib.Variant) -> None:
        """Switch between showing name column, title column, and both.

        :param _action: user activated this action (unused).
        :param _target: parameter GTK provides with activation (unused).
        """
        if not self._column_name.get_visible():
            self._column_name.set_visible(True)
        elif self._column_title.get_visible():
            self._column_title.set_visible(False)
        else:
            self._column_name.set_visible(False)
            self._column_title.set_visible(True)


class InitMotionOutlineId:
    """Initialize actions to move selection through identity item outline"""

    def __init__(self, p_ui_view_outline: UiDisplayOutlineId,
                 p_action_group: UiActionsOutlineId) -> None:
        """Initialize motion actions: expand, collapse, go first, and last.

        :param p_ui_view_outline: visual element of outline.
        :param p_action_group: add motion actions to this group.
        """
        self._ui_view_outline = p_ui_view_outline
        handlers = {'collapse': self.change_depth,
                    'expand': self.change_depth,
                    'go-first': self.go_first_item,
                    'go-last': self.go_last_item,
                    }
        for name, handler in handlers.items():
            UI.new_action_active(
                p_group=p_action_group, p_name=name, p_handler=handler)

    def change_depth(
            self, p_action: Gio.SimpleAction, _target: GLib.Variant) -> None:
        """Expand or collapse outline.

        :param p_action: user activated this action.
        :param _target: target of action (unused).
        """
        name = p_action.get_name()
        if 'collapse' == name:
            self._ui_view_outline.collapse_all()
        elif 'expand' == name:
            self._ui_view_outline.expand_all()
        else:
            self._ui_view_outline.expand_all()

    def go_first_item(
            self, _action: Gio.SimpleAction, _target: GLib.Variant) -> None:
        """Make the first item in the outline the selected item.

        :param _action: user activated this action (unused).
        :param _target: parameter GTK provides with activation (unused).
        """
        model = self._ui_view_outline.get_model()
        line_first = model.get_iter_first()
        if line_first is not None:
            self._ui_view_outline.get_selection().select_iter(line_first)

    def go_last_item(
            self, _action: Gio.SimpleAction, _target: GLib.Variant) -> None:
        """Make the last item in the outline the selected item.

        :param _action: user activated this action (unused).
        :param _target: parameter GTK provides with activation (unused).
        """
        model = self._ui_view_outline.get_model()
        line_last = None
        n_children = model.iter_n_children(line_last)
        while 0 < n_children:
            line_last = model.iter_nth_child(line_last, n_children - 1)
            n_children = model.iter_n_children(line_last)
        if line_last is not None:
            path = model.get_path(line_last)
            self._ui_view_outline.expand_to_path(path)
            self._ui_view_outline.get_selection().select_iter(line_last)
            NO_COLUMN = None
            NO_ALIGN = False
            IGNORED = 0
            self._ui_view_outline.scroll_to_cell(
                path, NO_COLUMN, NO_ALIGN, IGNORED, IGNORED)


class SelectorItem:
    """Provides means to select an item in an outline.

    Visual element displays outline of items (such as specifications,
    topics, or facts).  The element identifies the element currently
    select and presents its summary.  A visual element may register a
    button with :class:`SelectorItem` to show and hide a field to search
    the outline.
    """

    _UI_TEXT = """
<?xml version="1.0" encoding="UTF-8"?>
<!-- Generated with glade 3.38.2 -->
<interface>
  <requires lib="gtk+" version="3.24"/>
  <object class="GtkImage" id="image_collapse">
    <property name="visible">True</property>
    <property name="can-focus">False</property>
    <property name="icon-name">format-indent-less-symbolic</property>
  </object>
  <object class="GtkImage" id="image_cycle">
    <property name="visible">True</property>
    <property name="can-focus">False</property>
    <property name="icon-name">emblem-synchronizing-symbolic</property>
  </object>
  <object class="GtkImage" id="image_expand">
    <property name="visible">True</property>
    <property name="can-focus">False</property>
    <property name="icon-name">format-indent-more-symbolic</property>
  </object>
  <object class="GtkImage" id="image_find">
    <property name="visible">True</property>
    <property name="can-focus">False</property>
    <property name="icon-name">edit-find-symbolic</property>
  </object>
  <object class="GtkImage" id="image_go_first">
    <property name="visible">True</property>
    <property name="can-focus">False</property>
    <property name="icon-name">go-top-symbolic</property>
  </object>
  <object class="GtkImage" id="image_go_last">
    <property name="visible">True</property>
    <property name="can-focus">False</property>
    <property name="icon-name">go-bottom-symbolic</property>
  </object>
  <object class="GtkImage" id="image_new_item">
    <property name="visible">True</property>
    <property name="can-focus">False</property>
    <property name="icon-name">document-new-symbolic</property>
  </object>
  <object class="GtkBox" id="ui_kit_selector_id">
    <property name="visible">True</property>
    <property name="can-focus">False</property>
    <child>
      <object class="GtkBox" id="tools">
        <property name="visible">True</property>
        <property name="can-focus">False</property>
        <property name="orientation">vertical</property>
        <child>
          <object class="GtkMenuButton" id="open_menu">
            <property name="visible">True</property>
            <property name="can-focus">True</property>
            <property name="receives-default">True</property>
            <property name="tooltip-text" translatable="yes">Menu of topic outline actions.</property>
            <property name="relief">none</property>
            <child>
              <object class="GtkImage" id="image_menu">
                <property name="visible">True</property>
                <property name="can-focus">False</property>
                <property name="icon-name">format-justify-fill-symbolic</property>
              </object>
            </child>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">0</property>
          </packing>
        </child>
        <child>
          <object class="GtkButton" id="new_item">
            <property name="visible">True</property>
            <property name="can-focus">True</property>
            <property name="receives-default">True</property>
            <property name="halign">center</property>
            <property name="action-name">outline.new-item</property>
            <property name="image">image_new_item</property>
            <property name="always-show-image">True</property>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">1</property>
          </packing>
        </child>
        <child>
          <object class="GtkToggleButton" id="ui_button_search">
            <property name="visible">True</property>
            <property name="can-focus">True</property>
            <property name="receives-default">True</property>
            <property name="halign">center</property>
            <property name="image">image_find</property>
            <property name="always-show-image">True</property>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">2</property>
          </packing>
        </child>
        <child>
          <object class="GtkButton" id="cycle_columns">
            <property name="visible">True</property>
            <property name="can-focus">True</property>
            <property name="receives-default">True</property>
            <property name="halign">center</property>
            <property name="action-name">outline.cycle-columns</property>
            <property name="image">image_cycle</property>
            <property name="always-show-image">True</property>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">3</property>
          </packing>
        </child>
        <child>
          <object class="GtkButton" id="go_first">
            <property name="visible">True</property>
            <property name="can-focus">True</property>
            <property name="receives-default">True</property>
            <property name="halign">center</property>
            <property name="action-name">outline.go-first</property>
            <property name="image">image_go_first</property>
            <property name="always-show-image">True</property>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">4</property>
          </packing>
        </child>
        <child>
          <object class="GtkButton" id="go_last">
            <property name="visible">True</property>
            <property name="can-focus">True</property>
            <property name="receives-default">True</property>
            <property name="halign">center</property>
            <property name="action-name">outline.go-last</property>
            <property name="image">image_go_last</property>
            <property name="always-show-image">True</property>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">5</property>
          </packing>
        </child>
        <child>
          <object class="GtkButton" id="expand">
            <property name="visible">True</property>
            <property name="can-focus">True</property>
            <property name="receives-default">True</property>
            <property name="halign">center</property>
            <property name="action-name">outline.expand</property>
            <property name="image">image_expand</property>
            <property name="always-show-image">True</property>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">6</property>
          </packing>
        </child>
        <child>
          <object class="GtkButton" id="collase">
            <property name="visible">True</property>
            <property name="can-focus">True</property>
            <property name="receives-default">True</property>
            <property name="action-name">outline.collapse</property>
            <property name="image">image_collapse</property>
            <property name="always-show-image">True</property>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">7</property>
          </packing>
        </child>
      </object>
      <packing>
        <property name="expand">False</property>
        <property name="fill">True</property>
        <property name="position">0</property>
      </packing>
    </child>
    <child>
      <object class="GtkBox">
        <property name="visible">True</property>
        <property name="can-focus">False</property>
        <property name="orientation">vertical</property>
        <child>
          <object class="GtkBox" id="ui_site_search">
            <property name="visible">True</property>
            <property name="can-focus">False</property>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">0</property>
          </packing>
        </child>
        <child>
          <object class="GtkPaned">
            <property name="visible">True</property>
            <property name="can-focus">True</property>
            <property name="orientation">vertical</property>
            <property name="wide-handle">True</property>
            <child>
              <object class="GtkExpander">
                <property name="visible">True</property>
                <property name="can-focus">True</property>
                <property name="expanded">True</property>
                <property name="label-fill">True</property>
                <property name="resize-toplevel">True</property>
                <child>
                  <object class="GtkScrolledWindow" id="ui_site_outline_id">
                    <property name="visible">True</property>
                    <property name="can-focus">True</property>
                    <property name="margin-start">6</property>
                    <property name="margin-end">6</property>
                    <property name="margin-bottom">6</property>
                    <property name="vexpand">True</property>
                    <property name="shadow-type">in</property>
                  </object>
                </child>
                <child type="label">
                  <object class="GtkLabel">
                    <property name="visible">True</property>
                    <property name="can-focus">False</property>
                    <property name="label" translatable="yes">&lt;i&gt; Options&lt;/i&gt;</property>
                    <property name="use-markup">True</property>
                  </object>
                </child>
              </object>
              <packing>
                <property name="resize">True</property>
                <property name="shrink">False</property>
              </packing>
            </child>
            <child>
              <object class="GtkExpander">
                <property name="visible">True</property>
                <property name="can-focus">True</property>
                <property name="expanded">True</property>
                <property name="label-fill">True</property>
                <property name="resize-toplevel">True</property>
                <child>
                  <object class="GtkScrolledWindow" id="ui_site_summary">
                    <property name="visible">True</property>
                    <property name="can-focus">True</property>
                    <property name="margin-start">6</property>
                    <property name="margin-end">6</property>
                    <property name="margin-bottom">6</property>
                    <property name="vexpand">True</property>
                    <property name="shadow-type">in</property>
                  </object>
                </child>
                <child type="label">
                  <object class="GtkLabel">
                    <property name="visible">True</property>
                    <property name="can-focus">False</property>
                    <property name="label" translatable="yes">&lt;i&gt; Summary&lt;/i&gt;</property>
                    <property name="use-markup">True</property>
                  </object>
                </child>
              </object>
              <packing>
                <property name="resize">True</property>
                <property name="shrink">False</property>
              </packing>
            </child>
          </object>
          <packing>
            <property name="expand">True</property>
            <property name="fill">True</property>
            <property name="position">1</property>
          </packing>
        </child>
      </object>
      <packing>
        <property name="expand">True</property>
        <property name="fill">True</property>
        <property name="position">1</property>
      </packing>
    </child>
  </object>
</interface>
    """

    def __init__(self, p_ui_outline: UiViewOutline) -> None:
        """Initialize outline view format, search, and summary.

        :param p_view_outline: visual element for view of outline.
        """
        get_ui_element = UI.GetUiElementByStr(p_string_ui=self._UI_TEXT)
        self._ui_selector = get_ui_element('ui_kit_selector_id')
        actions = UiActionsOutlineId()
        p_ui_outline.insert_action_group('outline', actions)
        site_outline = get_ui_element('ui_site_outline_id')
        site_outline.add(p_ui_outline)
        _ = InitColumnsOutlineId(p_ui_outline, actions)
        _ = InitMotionOutlineId(p_ui_outline, actions)
        ui_search = UiSearchOutlineId()
        _ = InitSearchOutlineId(p_ui_outline, ui_search)
        site_search = get_ui_element('ui_site_search')
        site_search.add(ui_search)
        model_summary = ModelSummary()
        _ = InitSummaryOutlineId(p_ui_outline, model_summary)
        factory_summary = FactoryDisplaySummary(model_summary)
        display_summary = factory_summary()
        site_summary = get_ui_element('ui_site_summary')
        site_summary.add(display_summary)

    # def _init_search(self, p_get_ui_element: UI.GetUiElement) -> None:
    #     """Initialize search bar and buttons.
    #
    #     :param p_get_ui_element: gets visual element from UI description.
    #     """
    #     self._scope_search = VID.FieldsId.NAME
    #     self._search_bar = p_get_ui_element('ui_search')
    #
    #     button_in_name = p_get_ui_element('ui_search_in_name')
    #     _ = button_in_name.connect(
    #         'toggled', self.on_changed_search_scope, VID.FieldsId.NAME)
    #     button_in_summary = p_get_ui_element('ui_search_in_summary')
    #     _ = button_in_summary.connect(
    #         'toggled', self.on_changed_search_scope, VID.FieldsId.SUMMARY)
    #     button_in_title = p_get_ui_element('ui_search_in_title')
    #     _ = button_in_title.connect(
    #         'toggled', self.on_changed_search_scope, VID.FieldsId.TITLE)
    #
    #     # self._ui_view_outline.set_enable_search(True)
    #     C_FIRST = 0
    #     self._ui_view_outline.set_search_column(C_FIRST)
    #     entry_search = p_get_ui_element('ui_search_entry')
    #     self._ui_view_outline.set_search_entry(entry_search)
    #     EXTRA = None
    #     self._ui_view_outline.set_search_equal_func(
    #         self._match_spec_ne, EXTRA)

    # def _init_summary(self, p_get_ui_element: UI.GetUiElement) -> None:
    #     """Initialize display for summary of chosen specification.
    #
    #     :param p_get_ui_element: gets visual element from UI description.
    #     """
    #     self._summary = ModelSummary(p_text=SelectorItem.NO_SUMMARY)
    #     factory_display = FactoryDisplaySummary(self._summary)
    #     display_summary = factory_display()
    #     site_summary = p_get_ui_element('ui_site_summary')
    #     site_summary.add(display_summary)
    #     display_summary.show()
    #     display_summary.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)

    # def _init_view_outline(self, p_get_ui_element: UI.GetUiElement) -> None:
    #     """Initialize specifications outline.
    #
    #     :param p_get_ui_element: gets visual element from UI description.
    #     """
    #     site_outline = p_get_ui_element('ui_site_outline')
    #     site_outline.add(self._ui_view_outline)
    #
    #     self._column_name = UI.new_column_stock('Name', self._markup_cell_name)
    #     self._ui_view_outline.append_column(self._column_name)
    #     self._column_title = (
    #         UI.new_column_stock('Title', self._markup_cell_title))
    #     self._ui_view_outline.append_column(self._column_title)
    #     self._ui_selection = self._ui_view_outline.get_selection()
    #     self._ui_selection.connect('changed', self.on_changed_selection)
    #     # self._ui_view_outline.show()

    # def _markup_cell_name(
    #         self, _column: Gtk.TreeViewColumn, p_render: Gtk.CellRenderer,
    #         p_ui_model: Gtk.TreeModel, p_line: BUI.LineOutline, _data) -> None:
    #     """Set markup for name cell in the items outline view.
    #
    #     :param _column: column of cell to format (unused).
    #     :param p_render: renders formatted cell contents.
    #     :param p_ui_model: contains cell content.
    #     :param p_line: line of cell to format.
    #     :param _data: user data (unused).
    #     """
    #     print('Enter: _markup_cell_name')
    #     item = ModelOutline.get_item_direct(p_ui_model, p_line)
    #     name = 'Missing'
    #     if item is not None:
    #         name = item.name.text
    #     p_render.set_property('markup', name)

    # def _markup_cell_title(
    #         self, _column: Gtk.TreeViewColumn, p_render: Gtk.CellRenderer,
    #         p_ui_model: Gtk.TreeModel, p_line: BUI.LineOutline, _data) -> None:
    #     """Set markup for title cell in the items outline view.
    #
    #     :param _column: column of cell to format (unused).
    #     :param p_render: renders formatted cell contents.
    #     :param _model: contains cell content.
    #     :param p_line: line of cell to format.
    #     :param _data: user data (unused).
    #     """
    #     item = ModelOutline.get_item_direct(p_ui_model, p_line)
    #     title = 'Missing'
    #     if item is not None:
    #         title = item.title.text
    #     p_render.set_property('markup', title)

    # def _match_spec_ne(
    #         self, p_ui_model: Gtk.TreeModel, _n_column: int, p_match_key: str,
    #         p_line: BUI.LineOutline, _extra: None):
    #     """Return False when given key is found with scope of search.
    #
    #     Implements `Gtk.TreeViewSearchEqualFunc`_. Search scope can
    #     include any combination of spec name, summary, or title.
    #
    #     :param p_ui_model: storage for spec outline visual element.
    #     :param _n_column: model column to match (unused).
    #     :param p_match_key: key to match within search field(s).
    #     :param p_line: line to check for key.
    #     :param _extra: optional extra parameter (unused)
    #
    #     .. _`Gtk.TreeViewSearchEqualFunc`::
    #         https://lazka.github.io/pgi-docs/Gtk-3.0/callbacks.html#
    #         Gtk.TreeViewSearchEqualFunc
    #     """
    #     if not self._scope_search:
    #         return True
    #
    #     item = ModelOutline.get_item_direct(p_ui_model, p_line)
    #     if item is None:
    #         line_str = p_ui_model.get_string_from_iter(p_line)
    #         logger.warning('Outline contains None at line "{}" ({}.{})'
    #                        ''.format(line_str, self.__class__.__name__,
    #                                  self._match_spec_ne.__name__))
    #         return True
    #
    #     if (self._scope_search & VID.FieldsId.NAME):
    #         if p_match_key in item.name.text:
    #             return False
    #
    #     if (self._scope_search & VID.FieldsId.SUMMARY):
    #         if p_match_key in item.summary.text:
    #             return False
    #
    #     if (self._scope_search & VID.FieldsId.TITLE):
    #         if p_match_key in item.title.text:
    #             return False
    #
    #     path = p_ui_model.get_path(p_line)
    #     _ = self._ui_view_outline.expand_row(path, False)
    #     return True

    # def on_changed_selection(self, _selection: Gtk.TreeSelection) -> None:
    #     """Changes summary text to match chosen item.
    #
    #     :param _selection: identifies chosen item (unused).
    #     """
    #     model, line = self._ui_selection.get_selected()
    #     if line is None:
    #         self._summary.text = self.NO_SUMMARY
    #         return
    #
    #     item = ModelOutline.get_item_direct(model, line)
    #     if item is None:
    #         self._summary.text = self.NO_SUMMARY
    #         return
    #
    #     self._summary.text = item.summary.text

    # def on_changed_search_scope(
    #         self, p_button: UiButtonSearchScope, p_field: VID.FieldsId
    #         ) -> None:
    #     """Sets search scope to match requested change.
    #
    #     :param p_button: search scope button changed by user.
    #     :param p_field: search field corresponding to changed button.
    #     """
    #     if p_button.get_active():
    #         self._scope_search |= p_field
    #     else:
    #         self._scope_search &= ~p_field

    # def sync_to_search(self, p_button_find: UiButtonFind) -> None:
    #     """Sync button to show and hide search of item outline.
    #
    #     :param p_button: button to sync with search.
    #     """
    #     _binding = p_button_find.bind_property(
    #         'active', self._search_bar, 'search-mode-enabled',
    #         GO.BindingFlags.BIDIRECTIONAL)

    @property
    def ui_selector(self) -> UiSelectorItem:
        """Return visual element for selecting an item.
        """
        return self._ui_selector


class InitSearchOutlineId:
    """Search bar for the visual element of an outline of identity items."""

    _UI_TEXT = """
        <?xml version="1.0" encoding="UTF-8"?>
        <!-- Generated with glade 3.38.2 -->
        <interface>
          <requires lib="gtk+" version="3.24"/>
          <object class="GtkBox" id="ui_kit_search_id">
            <property name="visible">True</property>
            <property name="can-focus">False</property>
            <property name="orientation">vertical</property>
            <child>
              <object class="GtkSearchEntry" id="ui_search_entry">
                <property name="visible">True</property>
                <property name="can-focus">True</property>
                <property name="primary-icon-name">edit-find-symbolic</property>
                <property name="primary-icon-activatable">False</property>
                <property name="primary-icon-sensitive">False</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">True</property>
                <property name="position">0</property>
              </packing>
            </child>
            <child>
              <object class="GtkBox">
                <property name="visible">True</property>
                <property name="can-focus">False</property>
                <child>
                  <object class="GtkLabel">
                    <property name="visible">True</property>
                    <property name="can-focus">False</property>
                    <property name="label" translatable="yes">Search in: </property>
                  </object>
                  <packing>
                    <property name="expand">False</property>
                    <property name="fill">True</property>
                    <property name="position">0</property>
                  </packing>
                </child>
                <child>
                  <object class="GtkCheckButton" id="ui_search_name">
                    <property name="label" translatable="yes">Name</property>
                    <property name="visible">True</property>
                    <property name="can-focus">True</property>
                    <property name="receives-default">False</property>
                    <property name="draw-indicator">True</property>
                  </object>
                  <packing>
                    <property name="expand">False</property>
                    <property name="fill">True</property>
                    <property name="position">1</property>
                  </packing>
                </child>
                <child>
                  <object class="GtkCheckButton" id="ui_search_title">
                    <property name="label" translatable="yes">Title</property>
                    <property name="visible">True</property>
                    <property name="can-focus">True</property>
                    <property name="receives-default">False</property>
                    <property name="draw-indicator">True</property>
                  </object>
                  <packing>
                    <property name="expand">False</property>
                    <property name="fill">True</property>
                    <property name="position">2</property>
                  </packing>
                </child>
                <child>
                  <object class="GtkCheckButton" id="ui_search_summary">
                    <property name="label" translatable="yes">Summary</property>
                    <property name="visible">True</property>
                    <property name="can-focus">True</property>
                    <property name="receives-default">False</property>
                    <property name="draw-indicator">True</property>
                  </object>
                  <packing>
                    <property name="expand">False</property>
                    <property name="fill">True</property>
                    <property name="position">3</property>
                  </packing>
                </child>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">True</property>
                <property name="position">1</property>
              </packing>
            </child>
          </object>
        </interface>
    """

    def __init__(self, p_ui_view_outline: UiDisplayOutlineId,
                 p_ui_view_search: UiSearchOutlineId) -> None:
        """Initialize search bar of outline of identity items.

        :param p_ui_view_outline: visual element of outline.
        :param p_ui_view_search: visual element for search.
        """
        get_ui_element = UI.GetUiElementByStr(p_string_ui=self._UI_TEXT)
        kit_search = get_ui_element('ui_kit_search_id')
        p_ui_view_search.add(kit_search)
        C_FIRST = 0
        p_ui_view_outline.set_search_column(C_FIRST)
        entry_search = get_ui_element('ui_search_entry')
        p_ui_view_outline.set_search_entry(entry_search)
        p_ui_view_outline.set_search_equal_func(
            self._match_spec_ne, p_ui_view_outline)

        button_name = get_ui_element('ui_search_name')
        _ = button_name.connect(
            'toggled', self.on_changed_search_scope, VID.FieldsId.NAME)
        self._scope_search = VID.FieldsId.VOID
        button_name.set_active(True)
        button_summary = get_ui_element('ui_search_summary')
        _ = button_summary.connect(
            'toggled', self.on_changed_search_scope, VID.FieldsId.SUMMARY)
        button_title = get_ui_element('ui_search_title')
        _ = button_title.connect(
            'toggled', self.on_changed_search_scope, VID.FieldsId.TITLE)

    def _match_spec_ne(self, p_ui_model: Gtk.TreeModel, _n_column: int,
                       p_match_key: str, p_line: BUI.LineOutline,
                       p_ui_view_outline: UiDisplayOutlineId) -> bool:
        """Return False when given key is found with scope of search.

        Implements `Gtk.TreeViewSearchEqualFunc`_. Search scope can
        include any combination of spec name, summary, or title.

        :param p_ui_model: storage for outline visual element.
        :param _n_column: model column to match (unused).
        :param p_match_key: key to match within search field(s).
        :param p_line: line to check for key.
        :param p_ui_view_outline: outline visual element.

        .. _`Gtk.TreeViewSearchEqualFunc`::
            https://lazka.github.io/pgi-docs/Gtk-3.0/callbacks.html#
            Gtk.TreeViewSearchEqualFunc
        """
        if not self._scope_search:
            return True

        item = ModelOutline.get_item_direct(p_ui_model, p_line)
        if item is None:
            line_str = p_ui_model.get_string_from_iter(p_line)
            logger.warning('Outline contains None at line "{}" ({}.{})'
                           ''.format(line_str, self.__class__.__name__,
                                     self._match_spec_ne.__name__))
            return True

        if (self._scope_search & VID.FieldsId.NAME):
            if p_match_key in item.name.text:
                return False

        if (self._scope_search & VID.FieldsId.SUMMARY):
            if p_match_key in item.summary.text:
                return False

        if (self._scope_search & VID.FieldsId.TITLE):
            if p_match_key in item.title.text:
                return False

        path = p_ui_model.get_path(p_line)
        _ = p_ui_view_outline.expand_row(path, False)
        return True

    def on_changed_search_scope(
            self, p_button: UiButtonSearchScope, p_field: VID.FieldsId
            ) -> None:
        """Sets search scope to match requested change.

        :param p_button: search scope button changed by user.
        :param p_field: search field corresponding to changed button.
        """
        if p_button.get_active():
            self._scope_search |= p_field
        else:
            self._scope_search &= ~p_field


class InitSummaryOutlineId:
    """Summary of item selected in outline of identity items.

    # .. attribute:: NO_SUMMARY
    #
    #    Summary text displayed when no item is selected.
    """

    NO_SUMMARY = 'Please select an item in the outline.'

    def __init__(self, p_ui_view_outline: UiDisplayOutlineId,
                 p_model_summary: ModelSummary) -> None:
        """Initialize updating of item summary when selection changes.

        :param p_ui_view_outline: visual element of outline
        :param p_model_summary: storage for summary of selected item.
        """
        self._model_summary = p_model_summary
        selection = p_ui_view_outline.get_selection()
        selection.connect('changed', self.on_changed_selection)
        # self._summary = ModelSummary(p_text=SelectorItem.NO_SUMMARY)
        # factory_display = FactoryDisplaySummary(self._summary)
        # display_summary = factory_display()
        # site_summary = p_get_ui_element('ui_site_summary')
        # site_summary.add(display_summary)
        # display_summary.show()
        # display_summary.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)

    def on_changed_selection(self, p_ui_selection: Gtk.TreeSelection) -> None:
        """Changes summary text to match selected item.

        :param p_ui_selection: identifies item selected by user.
        """
        model, line = p_ui_selection.get_selected()
        if line is None:
            self._model_summary.text = self.NO_SUMMARY
            return

        item = ModelOutline.get_item_direct(model, line)
        if item is None:
            self._model_summary.text = self.NO_SUMMARY
            return

        self._model_summary.text = item.summary.text


# class SetupUiDisplayOutlineId:
#     """Set up columns and, optionally, actions, search, and summary."""
#
#     def __init__(self, p_ui_view: UiDisplayOutlineId,
#                  p_action_group: UiActionsOutlineId = None,
#                  p_ui_search: UiSearchOutlineId = None,
#                  p_ui_model_summary: BUI.ModelTextStyled = None) -> None:
#         """Initialize columns in outline and given additional elements.
#
#         :param p_ui_view: visual element of outline.
#         :param p_action_group: container for outline actions (optional).
#         :param p_ui_search: visual element for search (optional).
#         :param p_ui_model_summary: model for summary visual element
#             (optional).
#         """
#         self._ui_view = p_ui_view
#         _ = InitColumnsOutlineId(p_ui_view)
#         # self._init_columns()
#         if p_action_group is not None:
#             self._init_actions(p_action_group)
#         if p_ui_search is not None:
#             raise NotImplementedError
#         if p_ui_model_summary is not None:
#             raise NotImplementedError
#
#     def _init_actions(self, p_action_group: Gio.SimpleActionGroup
#                       ) -> None:
#         """Add display actions to the given group.
#
#         :param p_action_group: group of outline's visual element actions.
#         """
#         handlers = {'collapse': self.on_change_depth,
#                     'expand': self.on_change_depth,
#                     'go-first': self.on_go_first_item,
#                     'go-last': self.on_go_last_item,
#                     'cycle-columns': self.on_switch_columns,
#                     }
#         for name, handler in handlers.items():
#             UI.new_action_active(
#                 p_group=p_action_group, p_name=name, p_handler=handler)
#         return
#
#     def _init_columns(self) -> None:
#         """Initialize columns in visual element of outline."""
#         self._column_name = UI.new_column_stock('Name', self._markup_cell_name)
#         self._ui_view.append_column(self._column_name)
#         self._column_title = UI.new_column_stock(
#             'Title', self._markup_cell_title)
#         self._ui_view.append_column(self._column_title)
#
#     def _init_search(self, p_ui_search: UiSearchOutlineId) -> None:
#         """Initialize components in visual element of search.
#
#         :param p_ui_search: visual element for search.
#         """
#         pass
#         # self._scope_search = VID.FieldsId.NAME
#         # self._search_bar = p_get_ui_element('ui_search')
#         #
#         # button_in_name = p_get_ui_element('ui_search_in_name')
#         # _ = button_in_name.connect(
#         #     'toggled', self.on_changed_search_scope, VID.FieldsId.NAME)
#         # button_in_summary = p_get_ui_element('ui_search_in_summary')
#         # _ = button_in_summary.connect(
#         #     'toggled', self.on_changed_search_scope, VID.FieldsId.SUMMARY)
#         # button_in_title = p_get_ui_element('ui_search_in_title')
#         # _ = button_in_title.connect(
#         #     'toggled', self.on_changed_search_scope, VID.FieldsId.TITLE)
#         #
#         # # self._ui_view_outline.set_enable_search(True)
#         # C_FIRST = 0
#         # self._ui_view_outline.set_search_column(C_FIRST)
#         # entry_search = p_get_ui_element('ui_search_entry')
#         # self._ui_view_outline.set_search_entry(entry_search)
#         # EXTRA = None
#         # self._ui_view_outline.set_search_equal_func(
#         #     self._match_spec_ne, EXTRA)
#
#     def _markup_cell_name(
#             self, _column: Gtk.TreeViewColumn, p_render: Gtk.CellRenderer,
#             p_ui_model: Gtk.TreeModel, p_line: BUI.LineOutline, _data) -> None:
#         """Set markup for name cell in the outline's visual element.
#
#         :param _column: column of cell to format (unused).
#         :param p_render: renders formatted cell contents.
#         :param p_ui_model: contains cell content.
#         :param p_line: line of cell to format.
#         :param _data: user data (unused).
#         """
#         item_id = BUI.ModelOutline.get_item_direct(p_ui_model, p_line)
#         name = 'Missing'
#         if item_id is not None:
#             name = item_id.name.text
#         p_render.set_property('markup', name)
#
#     def _markup_cell_title(
#             self, _column: Gtk.TreeViewColumn, p_render: Gtk.CellRenderer,
#             p_ui_model: Gtk.TreeModel, p_line: BUI.LineOutline, _data) -> None:
#         """Set markup for title cell in the outline visual element.
#
#         :param _column: column of cell to format (unused).
#         :param p_render: renders formatted cell contents.
#         :param p_ui_model: contains cell content.
#         :param p_line: line of cell to format.
#         :param _data: user data (unused).
#         """
#         item_id = BUI.ModelOutline.get_item_direct(p_ui_model, p_line)
#         title = 'Missing'
#         if item_id is not None:
#             title = item_id.title.text
#         p_render.set_property('markup', title)
#
#     def on_change_depth(
#             self, p_action: Gio.SimpleAction, _target: GLib.Variant) -> None:
#         """Expand or collapse outline.
#
#         :param p_action: user activated this action.
#         :param _target: target of action (unused).
#         """
#         name = p_action.get_name()
#         if 'collapse' == name:
#             self._ui_view.collapse_all()
#         elif 'expand' == name:
#             self._ui_view.expand_all()
#         else:
#             self._ui_view.expand_all()
#
#     def on_go_first_item(
#             self, _action: Gio.SimpleAction, _target: GLib.Variant) -> None:
#         """Make the first item in the outline the selected item.
#
#         :param _action: user activated this action (unused).
#         :param _target: parameter GTK provides with activation (unused).
#         """
#         # model, _ = self._ui_selection.get_selected()
#         model = self._ui_view.get_model()
#         line_first = model.get_iter_first()
#         if line_first is not None:
#             self._ui_view.get_selection().select_iter(line_first)
#
#     def on_go_last_item(
#             self, _action: Gio.SimpleAction, _target: GLib.Variant) -> None:
#         """Make the last item in the outline the selected item.
#
#         :param _action: user activated this action (unused).
#         :param _target: parameter GTK provides with activation (unused).
#         """
#
#         model = self._ui_view.get_model()
#         line_last = None
#         n_children = model.iter_n_children(line_last)
#         while 0 < n_children:
#             line_last = model.iter_nth_child(line_last, n_children - 1)
#             n_children = model.iter_n_children(line_last)
#         if line_last is not None:
#             path = model.get_path(line_last)
#             self._ui_view.expand_to_path(path)
#             self._ui_view.get_selection().select_iter(line_last)
#             NO_COLUMN = None
#             NO_ALIGN = False
#             IGNORED = 0
#             self._ui_view.scroll_to_cell(
#                 path, NO_COLUMN, NO_ALIGN, IGNORED, IGNORED)
#
#     def on_switch_columns(
#             self, _action: Gio.SimpleAction, _target: GLib.Variant) -> None:
#         """Switch between showing name column, title column, and both.
#
#         :param _action: user activated this action (unused).
#         :param _target: parameter GTK provides with activation (unused).
#         """
#         if not self._column_name.get_visible():
#             self._column_name.set_visible(True)
#         elif self._column_title.get_visible():
#             self._column_title.set_visible(False)
#         else:
#             self._column_name.set_visible(False)
#             self._column_title.set_visible(True)
#
#     # @property
#     # def ui_selection(self) -> UiSelectionOutlineId:
#     #     """Return visual element of outline display."""
#     #     return self._ui_selectionC
#
#     @property
#     def ui_view(self) -> UiDisplayOutlineId:
#         """Return visual element of outline display."""
#         return self._ui_view
