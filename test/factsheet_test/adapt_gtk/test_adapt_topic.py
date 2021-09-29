"""
Unit tests for GTK-based classes implementing abstract outline classes.
See :mod:`.adapt_topic`.
"""
import gi   # type: ignore[import]
import pytest   # type: ignore[import]

import factsheet.adapt_gtk.adapt_outline as AOUTLINE
import factsheet.adapt_gtk.adapt_topic as ATOPIC
import factsheet.model.fact as MFACT

gi.require_version('Gtk', '3.0')
from gi.repository import GObject as GO  # type: ignore[import] # noqa: E402
from gi.repository import Gtk   # type: ignore[import]    # noqa: E402


class PatchOutlineModel():
    """Outline model containing stock content.

    Attribute ``model`` contains a facts outline model with the
    following structure.::

        name_0xx | title_0xx | DEFINED
            name_00x | title_00x | UNDEFINED
                name_000 | title_000 | BLOCKED
            name_01x | title_01x | UNCHECKED
        name_1xx | title_1xx | UNDEFINED
            name_10x | title_10x | DEFINED
            name_11x | title_11x | BLOCKED
                name_110 | title_110 | DEFINED
                name_111 | title_111 | UNCHECKED
                name_112 | title_112 | UNDEFINED

    :param p_tag: label for each fact in summary.
    """

    def __init__(self, p_tag='Target'):
        self.model = Gtk.TreeStore(GO.TYPE_PYOBJECT)
        TOPIC = None

        item = MFACT.Fact(p_topic=TOPIC)
        item.init_identity(
            p_name='name_0xx', p_title='title_0xx', p_summary=p_tag)
        item._status = MFACT.StatusOfFact.DEFINED
        i_0xx = self.model.append(None, [item])
        item = MFACT.Fact(p_topic=TOPIC)
        item.init_identity(
            p_name='name_00x', p_title='title_00x', p_summary=p_tag)
        item._status = MFACT.StatusOfFact.UNDEFINED
        i_00x = self.model.append(i_0xx, [item])
        item = MFACT.Fact(p_topic=TOPIC)
        item.init_identity(
            p_name='name_000', p_title='title_000', p_summary=p_tag)
        item._status = MFACT.StatusOfFact.BLOCKED
        _i_000 = self.model.append(i_00x, [item])
        item = MFACT.Fact(p_topic=TOPIC)
        item.init_identity(
            p_name='name_01x', p_title='title_01x', p_summary=p_tag)
        _i_01x = self.model.append(i_0xx, [item])
        item._status = MFACT.StatusOfFact.UNCHECKED
        item = MFACT.Fact(p_topic=TOPIC)
        item.init_identity(
            p_name='name_1xx', p_title='title_1xx', p_summary=p_tag)
        i_1xx = self.model.append(None, [item])
        item._status = MFACT.StatusOfFact.UNDEFINED
        item = MFACT.Fact(p_topic=TOPIC)
        item.init_identity(
            p_name='name_10x', p_title='title_10x', p_summary=p_tag)
        _i_10x = self.model.append(i_1xx, [item])
        item._status = MFACT.StatusOfFact.DEFINED
        item = MFACT.Fact(p_topic=TOPIC)
        item.init_identity(
            p_name='name_11x', p_title='title_11x', p_summary=p_tag)
        i_11x = self.model.append(i_1xx, [item])
        item._status = MFACT.StatusOfFact.BLOCKED
        item = MFACT.Fact(p_topic=TOPIC)
        item.init_identity(
            p_name='name_110', p_title='title_110', p_summary=p_tag)
        _i_110 = self.model.append(i_11x, [item])
        item._status = MFACT.StatusOfFact.DEFINED
        item = MFACT.Fact(p_topic=TOPIC)
        item.init_identity(
            p_name='name_111', p_title='title_111', p_summary=p_tag)
        _i_111 = self.model.append(i_11x, [item])
        item._status = MFACT.StatusOfFact.UNCHECKED
        item = MFACT.Fact(p_topic=TOPIC)
        item.init_identity(
            p_name='name_112', p_title='title_112', p_summary=p_tag)
        _i_112 = self.model.append(i_11x, [item])
        item._status = MFACT.StatusOfFact.UNDEFINED


@pytest.fixture
def patch_outline():
    """Pytext fixture returns stub facts outline."""
    def factory_outline(p_tag='Facts outline stub.'):
        outline = ATOPIC.AdaptTreeStoreFact()
        outline._ui_model = PatchOutlineModel(p_tag=p_tag).model
        return outline

    return factory_outline


class TestAdaptTreeStoreFact:
    """Unit tests for :class:`.AdaptTreeStoreFact`."""

    def test_init(self):
        """Confirm initialization."""
        # Setup
        INDEX = None
        TOPIC = None
        fact = MFACT.Fact(p_topic=TOPIC)
        fact.init_identity(p_name='Parrot', p_title='The Parrot Sketch')
        # Test
        target = ATOPIC.AdaptTreeStoreFact()
        assert target is not None
        index_new = target.insert_before(fact, INDEX)
        assert index_new is not None
        assert isinstance(index_new, AOUTLINE.IndexGtk)

    def test_find_name(self):
        """| Confirm search by fact name.
        | Case: matching fact in outline.
        """
        # Setup
        target = ATOPIC.AdaptTreeStoreFact()
        target._ui_model = PatchOutlineModel(p_tag='Target').model
        PATH_VALUE = '1:1:1'
        i_value = target._ui_model.get_iter_from_string(PATH_VALUE)
        value = target.get_item(i_value).name
        PATH_AFTER = '1:1:1'
        i_after = target._ui_model.get_iter_from_string(PATH_AFTER)
        # Test
        i_match = target.find_name(value, i_after)
        assert PATH_VALUE == target._ui_model.get_string_from_iter(i_match)

    def test_find_name_absent(self):
        """| Confirm search by fact name.
        | Case: no matching fact in outline.
        """
        # Setup
        VALUE = 'Something completely different'
        target = ATOPIC.AdaptTreeStoreFact()
        target._ui_model = PatchOutlineModel(p_tag='Target').model
        # Test
        i_match = target.find_name(VALUE)
        assert i_match is None

    def test_find_title(self):
        """| Confirm search by fact title.
        | Case: matching fact in outline.
        """
        # Setup
        target = ATOPIC.AdaptTreeStoreFact()
        target._ui_model = PatchOutlineModel(p_tag='Target').model
        PATH_VALUE = '0:1'
        i_value = target._ui_model.get_iter_from_string(PATH_VALUE)
        value = target.get_item(i_value).title
        PATH_AFTER = '0:1'
        i_after = target._ui_model.get_iter_from_string(PATH_AFTER)
        # Test
        i_match = target.find_title(value, i_after)
        assert PATH_VALUE == target._ui_model.get_string_from_iter(i_match)

    def test_find_title_absent(self):
        """| Confirm search by fact title.
        | Case: no matching fact in outline.
        """
        # Setup
        VALUE = 'Something completely different'
        target = ATOPIC.AdaptTreeStoreFact()
        target._ui_model = PatchOutlineModel(p_tag='Target').model
        # Test
        i_match = target.find_title(VALUE)
        assert i_match is None


class TestAdaptTreeViewFact:
    """Unit tests for :class:`.AdaptTreeViewFact`."""

    def test_init(self, monkeypatch):
        """Confirm initialization."""
        # Setup
        class PatchSetFunc:
            def __init__(self): self.called = False

            def set_search_equal_func(self, *_a): self.called = True

        patch_func = PatchSetFunc()
        monkeypatch.setattr(Gtk.TreeView, 'set_search_equal_func',
                            patch_func.set_search_equal_func)
        COLUMN_NAME = 0
        COLUMN_STATUS = 1
        COLUMN_TITLE = 2
        COLUMN_PAD = 3
        N_CELLS = 1
        # Test
        target = ATOPIC.AdaptTreeViewFact()
        assert isinstance(target._gtk_view, Gtk.TreeView)
        assert target._gtk_view.get_model() is None
        assert patch_func.called
        assert isinstance(target._scope_search, ATOPIC.FieldsFact)
        assert target._scope_search is ATOPIC.FieldsFact.VOID

        assert AOUTLINE.AdaptTreeStore.N_COLUMN_ITEM == (
            target._gtk_view.get_search_column())
        assert target._gtk_view.get_enable_search()

        name_column = target._gtk_view.get_column(COLUMN_NAME)
        assert 'Name' == name_column.get_title()
        assert name_column.get_clickable()
        assert name_column.get_resizable()
        assert N_CELLS == len(name_column.get_cells())

        title_column = target._gtk_view.get_column(COLUMN_TITLE)
        assert 'Title' == title_column.get_title()
        assert title_column.get_clickable()
        assert title_column.get_resizable()
        assert N_CELLS == len(title_column.get_cells())

        status_column = target._gtk_view.get_column(COLUMN_STATUS)
        assert 'Status' == status_column.get_title()
        assert status_column.get_clickable()
        assert status_column.get_resizable()
        assert N_CELLS == len(status_column.get_cells())

        pad_column = target._gtk_view.get_column(COLUMN_PAD)
        assert pad_column is not None
        assert pad_column.get_expand()

    def test_fill_name(self, patch_outline):
        """Confirm name renderer property is set."""
        # Setup
        OUTLINE = patch_outline(p_tag='Fact')
        PATH_ITEM = '0'
        i_target = OUTLINE._ui_model.get_iter_from_string(PATH_ITEM)
        fact = OUTLINE.get_item(i_target)
        renderer = Gtk.CellRendererText()
        target = ATOPIC.AdaptTreeViewFact()
        OUTLINE.attach_view(target)
        # Test
        target._fill_name(None, renderer, OUTLINE._ui_model, i_target)
        assert fact.name == renderer.get_property('text')
        with pytest.raises(TypeError,
                           match='property markup is not readable'):
            assert fact.name == renderer.get_property('markup')

    @pytest.mark.parametrize(
        'SEARCH, PATH_ITEM, VALUE, EXPECT, EXPANDED', [
            (ATOPIC.FieldsFact.VOID, '1:0', 'title_10x', True, False),
            (ATOPIC.FieldsFact.NAME, '0:1', 'name_01x', False, False),
            (ATOPIC.FieldsFact.NAME, '0:1', 'title_01x', True, True),
            (ATOPIC.FieldsFact.TITLE, '0:0:0', 'name_000', True, True),
            (ATOPIC.FieldsFact.TITLE, '1:1', 'title_11x', False, False),
            (ATOPIC.FieldsFact.TITLE, '1:1', 't', False, False),
            (ATOPIC.FieldsFact.TITLE, '1:1', 'ti', False, False),
            (ATOPIC.FieldsFact.TITLE, '1:1', 'tiX', True, True),
            (ATOPIC.FieldsFact.STATUS, '1:1:1', 'BLOCKED', True, True),
            (ATOPIC.FieldsFact.STATUS, '1:1:1', 'UN', False, False),
            (ATOPIC.FieldsFact.STATUS, '1:1:1', 'UNC', False, False),
            (ATOPIC.FieldsFact.STATUS, '1:1:1', 'UND', True, True),
            (ATOPIC.FieldsFact.STATUS, '1:1:1', 'UNCHECKED', False, False),
            ])
    def test_test_field_eq(self, monkeypatch, SEARCH, PATH_ITEM, VALUE,
                           EXPECT, EXPANDED, patch_outline):
        """Confirm results of Gtk.TreeView search equal function."""
        # Setup
        class PatchExpand:
            def __init__(self):
                self.called = False
                self.path = None

            def expand_row(self, p, _a):
                self.called = True
                self.path = p

        patch_expand = PatchExpand()
        monkeypatch.setattr(
            Gtk.TreeView, 'expand_row', patch_expand.expand_row)

        OUTLINE = patch_outline(p_tag='Fact')
        i_item = OUTLINE._ui_model.get_iter_from_string(PATH_ITEM)
        target = ATOPIC.AdaptTreeViewFact()
        OUTLINE.attach_view(target)
        target._scope_search = SEARCH
        # Test
        actual = target._test_field_ne(
            OUTLINE._ui_model, AOUTLINE.AdaptTreeStore.N_COLUMN_ITEM,
            VALUE, i_item, None)
        assert actual is EXPECT
        assert patch_expand.called is EXPANDED
        if EXPANDED:
            assert PATH_ITEM == patch_expand.path.to_string()

    def test_fill_status(self, patch_outline):
        """Confirm status renderer property is set."""
        # Setup
        OUTLINE = patch_outline(p_tag='Fact')
        PATH_ITEM = '0:0'
        i_target = OUTLINE._ui_model.get_iter_from_string(PATH_ITEM)
        fact = OUTLINE.get_item(i_target)
        render = Gtk.CellRendererText()
        target = ATOPIC.AdaptTreeViewFact()
        OUTLINE.attach_view(target)
        status_text = fact.status.name
        # Test
        target._fill_status(None, render, OUTLINE._ui_model, i_target)
        assert status_text == render.get_property('text')
        with pytest.raises(TypeError,
                           match='property markup is not readable'):
            assert fact.title == render.get_property('markup')

    def test_fill_title(self, patch_outline):
        """Confirm title renderer property is set."""
        # Setup
        OUTLINE = patch_outline(p_tag='Fact')
        PATH_ITEM = '0:0:0'
        i_target = OUTLINE._ui_model.get_iter_from_string(PATH_ITEM)
        fact = OUTLINE.get_item(i_target)
        render = Gtk.CellRendererText()
        target = ATOPIC.AdaptTreeViewFact()
        OUTLINE.attach_view(target)
        # Test
        target._fill_title(None, render, OUTLINE._ui_model, i_target)
        assert fact.title == render.get_property('text')
        with pytest.raises(TypeError,
                           match='property markup is not readable'):
            assert fact.title == render.get_property('markup')

    @pytest.mark.parametrize('NAME_ATTR, NAME_PROP', [
        ['_scope_search', 'scope_search'],
        ])
    def test_property(self, NAME_ATTR, NAME_PROP):
        """Confirm properties are provide get and set but not delete..

        #. Case: get
        #. Case: set
        #. Case: no delete
        """
        # Setup
        target = ATOPIC.AdaptTreeViewFact()
        value_attr = getattr(target, NAME_ATTR)
        target_prop = getattr(ATOPIC.AdaptTreeViewFact, NAME_PROP)
        value_prop = getattr(target, NAME_PROP)
        # Test: read
        assert target_prop.fget is not None
        assert str(value_attr) == str(value_prop)
        # Test: no replace
        assert target_prop.fset is not None
        target.scope_search = ATOPIC.FieldsFact.NAME
        assert target._scope_search is ATOPIC.FieldsFact.NAME
        # Test: no delete
        assert target_prop.fdel is None


class TestFieldsFact:
    """Unit tests for :class:`.FieldsFact`."""

    def test_members(self):
        """Confirm member definitions."""
        # Setup
        # Test
        assert not bool(ATOPIC.FieldsFact.VOID)
        assert ATOPIC.FieldsFact.NAME
        assert ATOPIC.FieldsFact.STATUS
        assert ATOPIC.FieldsFact.TITLE


class TestTypes:
    """Unit tests for type definitions in :mod:`.adapt_topic`."""

    def test_types(self):
        """Confirm types defined."""
        # Setup
        # Test
        assert ATOPIC.IndexFact is AOUTLINE.IndexGtk
